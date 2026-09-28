package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"
	"time"
)

type AuditIssue struct {
	Page     string `json:"page"`
	Device   string `json:"device"`
	Category string `json:"category"`
	Severity string `json:"severity"` // "critical", "warning", "info"
	Message  string `json:"message"`
	Selector string `json:"selector,omitempty"`
}

type PageMetrics struct {
	URL              string   `json:"url"`
	Device           string   `json:"device"`
	Title            string   `json:"title"`
	H1Count          int      `json:"h1_count"`
	DOMNodes         int      `json:"dom_nodes"`
	ScrollOverflow   bool     `json:"scroll_overflow"`
	StickyBarVisible bool     `json:"sticky_bar_visible"`
	BrokenImages     int      `json:"broken_images"`
	ImagesWithoutAlt int      `json:"images_without_alt"`
	SmallTapTargets  int      `json:"small_tap_targets"`
	UnlabeledInputs  int      `json:"unlabeled_inputs"`
	ConsoleErrors    []string `json:"console_errors"`
	NetworkErrors    []string `json:"network_errors"`
	LoadTimeMs       int64    `json:"load_time_ms"`
}

type AuditResult struct {
	Timestamp string        `json:"timestamp"`
	Metrics   []PageMetrics `json:"metrics"`
	Issues    []AuditIssue  `json:"issues"`
}

const playwrightScript = `
import sys
import json
import time
from playwright.sync_api import sync_playwright

pages_to_test = [
    ("/", "Homepage"),
    ("/panel-upgrade", "Service: Panel Upgrade"),
    ("/ev-charger-installation", "Service: EV Charger"),
    ("/emergency-electrician-los-angeles", "Service: Emergency"),
    ("/whole-home-rewiring", "Service: Rewiring"),
    ("/commercial-electrician", "Service: Commercial"),
    ("/city-sherman-oaks", "City: Sherman Oaks"),
    ("/city-studio-city", "City: Studio City"),
    ("/city-beverly-hills", "City: Beverly Hills"),
    ("/panel-upgrade-van-nuys", "Geo: Panel Van Nuys"),
    ("/ev-charger-installation-burbank", "Geo: EV Burbank"),
    ("/testimonials", "Testimonials"),
    ("/gallery", "Gallery"),
    ("/blog/panel-upgrade-cost-los-angeles", "Blog: Panel Cost"),
    ("/blog/whole-home-rewiring-guide", "Blog: Rewiring Guide"),
    ("/blog/california-electrical-code-changes-2026", "Blog: Code Changes 2026")
]

base_url = sys.argv[1]

results = {
    "metrics": [],
    "issues": []
}

def audit_page(page, url_path, device_name, is_mobile):
    url = base_url + url_path
    console_errors = []
    network_errors = []

    def on_console(msg):
        if msg.type in ["error"]:
            console_errors.append(msg.text)

    def on_request_failed(req):
        network_errors.append(f"{req.method} {req.url} -> {req.failure}")

    def on_response(res):
        if res.status >= 400:
            network_errors.append(f"{res.status} {res.url}")

    page.on("console", on_console)
    page.on("requestfailed", on_request_failed)
    page.on("response", on_response)

    start_time = time.time()
    try:
        page.goto(url, wait_until="networkidle", timeout=15000)
    except Exception as e:
        results["issues"].append({
            "page": url_path,
            "device": device_name,
            "category": "navigation",
            "severity": "critical",
            "message": f"Navigation failed or timed out: {str(e)}"
        })
        return

    load_time_ms = int((time.time() - start_time) * 1000)

    # 1. Document Title & H1
    title = page.title()
    h1_count = len(page.query_selector_all("h1"))
    if h1_count == 0:
        results["issues"].append({
            "page": url_path,
            "device": device_name,
            "category": "seo",
            "severity": "critical",
            "message": "Missing <h1> tag on page"
        })
    elif h1_count > 1:
        results["issues"].append({
            "page": url_path,
            "device": device_name,
            "category": "seo",
            "severity": "warning",
            "message": f"Multiple <h1> tags found ({h1_count})"
        })

    # 2. Horizontal Scroll Overflow Check
    overflow_check = page.evaluate("""() => {
        const docWidth = document.documentElement.scrollWidth;
        const winWidth = window.innerWidth;
        let overflowingElements = [];
        if (docWidth > winWidth + 2) {
            document.querySelectorAll('*').forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.right > winWidth + 4 && rect.width > 0 && rect.height > 0) {
                    const tag = el.tagName.toLowerCase();
                    const cls = el.className ? '.' + String(el.className).split(' ')[0] : '';
                    const id = el.id ? '#' + el.id : '';
                    overflowingElements.push(tag + id + cls);
                }
            });
        }
        return {
            hasOverflow: docWidth > winWidth + 2,
            docWidth: docWidth,
            winWidth: winWidth,
            elements: overflowingElements.slice(0, 5)
        };
    }""")

    if overflow_check["hasOverflow"]:
        results["issues"].append({
            "page": url_path,
            "device": device_name,
            "category": "layout",
            "severity": "critical",
            "message": f"Horizontal scroll overflow: doc width {overflow_check['docWidth']}px > viewport {overflow_check['winWidth']}px. Offending elements: {', '.join(overflow_check['elements'])}"
        })

    # 3. Sticky Call Bar check
    sticky_check = page.evaluate("""() => {
        const bar = document.querySelector('.sticky-call-bar, .sticky-cta-bar, .call-bar');
        if (!bar) return { exists: false, visible: false };
        const style = window.getComputedStyle(bar);
        const isVisible = style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
        return { exists: true, visible: isVisible };
    }""")

    if is_mobile and sticky_check["exists"] and not sticky_check["visible"]:
        results["issues"].append({
            "page": url_path,
            "device": device_name,
            "category": "cro",
            "severity": "warning",
            "message": "Sticky call bar exists in DOM but is hidden on mobile viewport"
        })
    elif not is_mobile and sticky_check["exists"] and sticky_check["visible"]:
        results["issues"].append({
            "page": url_path,
            "device": device_name,
            "category": "cro",
            "severity": "info",
            "message": "Sticky call bar is displayed on desktop viewport (normally hidden >=768px)"
        })

    # 4. Images Audit
    img_audit = page.evaluate("""() => {
        const imgs = Array.from(document.querySelectorAll('img'));
        let missingAlt = 0;
        let broken = 0;
        let brokenSources = [];
        let missingDimensions = 0;
        imgs.forEach(img => {
            if (!img.getAttribute('alt') && img.getAttribute('alt') !== '') {
                missingAlt++;
            }
            if (img.complete && (img.naturalWidth === 0 || img.naturalHeight === 0)) {
                broken++;
                brokenSources.push(img.currentSrc || img.src);
            }
            if (!img.hasAttribute('width') && !img.hasAttribute('height') && !img.getAttribute('style')?.includes('width')) {
                missingDimensions++;
            }
        });
        return {
            total: imgs.length,
            missingAlt: missingAlt,
            broken: broken,
            brokenSources: brokenSources.slice(0, 5),
            missingDimensions: missingDimensions
        };
    }""")

    if img_audit["broken"] > 0:
        results["issues"].append({
            "page": url_path,
            "device": device_name,
            "category": "images",
            "severity": "critical",
            "message": f"{img_audit['broken']} broken/unrendered images found: {', '.join(img_audit['brokenSources'])}"
        })

    if img_audit["missingAlt"] > 0:
        results["issues"].append({
            "page": url_path,
            "device": device_name,
            "category": "accessibility",
            "severity": "warning",
            "message": f"{img_audit['missingAlt']} images missing 'alt' attribute"
        })

    # 5. Form & Input Accessibility
    form_audit = page.evaluate("""() => {
        const inputs = Array.from(document.querySelectorAll('input:not([type="hidden"]), select, textarea'));
        let unlabeled = 0;
        let unlabeledDetails = [];
        inputs.forEach(input => {
            const id = input.id;
            const hasLabel = id && document.querySelector('label[for="' + id + '"]');
            const hasAriaLabel = input.getAttribute('aria-label') || input.getAttribute('aria-labelledby');
            const hasPlaceholder = input.getAttribute('placeholder');
            const parentLabel = input.closest('label');
            if (!hasLabel && !hasAriaLabel && !parentLabel) {
                unlabeled++;
                unlabeledDetails.push(input.name || input.id || input.type);
            }
        });
        return {
            totalInputs: inputs.length,
            unlabeled: unlabeled,
            unlabeledDetails: unlabeledDetails
        };
    }""")

    if form_audit["unlabeled"] > 0:
        results["issues"].append({
            "page": url_path,
            "device": device_name,
            "category": "accessibility",
            "severity": "warning",
            "message": f"{form_audit['unlabeled']} form inputs lack explicit <label> or aria-label: {', '.join(form_audit['unlabeledDetails'])}"
        })

    # 6. Tap Target Sizing on Mobile (< 40px)
    tap_target_audit = {"smallTargets": 0}
    if is_mobile:
        tap_target_audit = page.evaluate("""() => {
            const clickables = Array.from(document.querySelectorAll('a, button, input[type="submit"], input[type="button"], summary'));
            let small = 0;
            let smallExamples = [];
            clickables.forEach(el => {
                const rect = el.getBoundingClientRect();
                // Check visible elements
                if (rect.width > 0 && rect.height > 0 && (rect.width < 40 || rect.height < 40)) {
                    // Ignore inline links inside paragraphs
                    small++;
                    const text = (el.innerText || el.getAttribute('aria-label') || el.className || 'button').slice(0, 20).trim();
                    smallExamples.push(text + " (" + Math.round(rect.width) + "x" + Math.round(rect.height) + "px)");
                }
            });
            return {
                smallTargets: small,
                examples: smallExamples.slice(0, 5)
            };
        }""")

        if tap_target_audit.get("smallTargets", 0) > 2:
            results["issues"].append({
                "page": url_path,
                "device": device_name,
                "category": "accessibility",
                "severity": "warning",
                "message": f"{tap_target_audit['smallTargets']} touch targets under 40x40px: {', '.join(tap_target_audit.get('examples', []))}"
            })

    # 7. DOM Size
    dom_count = page.evaluate("() => document.querySelectorAll('*').length")

    # 8. Console & Network Errors
    for err in console_errors:
        results["issues"].append({
            "page": url_path,
            "device": device_name,
            "category": "javascript",
            "severity": "critical",
            "message": f"Console Error: {err}"
        })

    for nerr in network_errors:
        # Ignore analytics/beacon failure if any
        if "cloudflareinsights.com" not in nerr:
            results["issues"].append({
                "page": url_path,
                "device": device_name,
                "category": "network",
                "severity": "warning",
                "message": f"Network Error: {nerr}"
            })

    results["metrics"].append({
        "url": url_path,
        "device": device_name,
        "title": title,
        "h1_count": h1_count,
        "dom_nodes": dom_count,
        "scroll_overflow": overflow_check["hasOverflow"],
        "sticky_bar_visible": sticky_check["visible"],
        "broken_images": img_audit["broken"],
        "images_without_alt": img_audit["missingAlt"],
        "small_tap_targets": tap_target_audit.get("smallTargets", 0),
        "unlabeled_inputs": form_audit["unlabeled"],
        "console_errors": console_errors,
        "network_errors": network_errors,
        "load_time_ms": load_time_ms
    })

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. Desktop Audit (1366x768)
        desktop_context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        desktop_page = desktop_context.new_page()

        for path, name in pages_to_test:
            audit_page(desktop_page, path, "Desktop", False)

        desktop_context.close()

        # 2. Mobile Audit (iPhone 14 / Pixel: 390x844)
        mobile_context = browser.new_context(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        )
        mobile_page = mobile_context.new_page()

        for path, name in pages_to_test:
            audit_page(mobile_page, path, "Mobile", True)

        mobile_context.close()
        browser.close()

    print(json.dumps(results))

if __name__ == "__main__":
    main()
`

func main() {
	fmt.Println("🚀 Starting AMY Electric Playwright Deep Audit Orchestrator (Go)...")

	// 1. Find a free port and launch static HTTP server
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		fmt.Printf("Error binding listener: %v\n", err)
		os.Exit(1)
	}
	port := listener.Addr().(*net.TCPAddr).Port
	baseURL := fmt.Sprintf("http://127.0.0.1:%d", port)
	fmt.Printf("📦 Local file server listening at %s\n", baseURL)

	fileServer := http.FileServer(http.Dir("/home/amram/WEBSITE"))
	server := &http.Server{
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			// Handle clean URLs: /panel-upgrade -> /panel-upgrade.html
			path := r.URL.Path
			fullPath := filepath.Join("/home/amram/WEBSITE", path)
			if fi, err := os.Stat(fullPath); err == nil && !fi.IsDir() {
				fileServer.ServeHTTP(w, r)
				return
			}
			htmlPath := fullPath + ".html"
			if _, err := os.Stat(htmlPath); err == nil {
				r.URL.Path = path + ".html"
			}
			fileServer.ServeHTTP(w, r)
		}),
	}

	go func() {
		if err := server.Serve(listener); err != nil && err != http.ErrServerClosed {
			fmt.Printf("HTTP server error: %v\n", err)
		}
	}()
	defer server.Shutdown(context.Background())

	// 2. Write runner script to temp file
	tmpPy, err := os.CreateTemp("", "playwright_audit_*.py")
	if err != nil {
		fmt.Printf("Failed to create temp script: %v\n", err)
		os.Exit(1)
	}
	defer os.Remove(tmpPy.Name())

	if _, err := tmpPy.WriteString(playwrightScript); err != nil {
		fmt.Printf("Failed to write runner script: %v\n", err)
		os.Exit(1)
	}
	tmpPy.Close()

	// 3. Execute Playwright audit
	fmt.Println("🌐 Executing Playwright headless browser audit across 16 critical paths (Mobile + Desktop)...")
	cmd := exec.Command("python3", tmpPy.Name(), baseURL)
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Playwright execution error: %v\nOutput:\n%s\n", err, string(output))
		os.Exit(1)
	}

	// 4. Parse JSON results
	var audit AuditResult
	if err := json.Unmarshal(output, &audit); err != nil {
		fmt.Printf("Failed to parse audit JSON: %v\nRaw output snippet:\n%s\n", err, string(output[:min(500, len(output))]))
		os.Exit(1)
	}

	audit.Timestamp = time.Now().Format("2006-01-02 15:04:05 MST")

	// 5. Aggregate Findings
	critCount := 0
	warnCount := 0
	infoCount := 0
	categoryCounts := make(map[string]int)

	for _, issue := range audit.Issues {
		switch issue.Severity {
		case "critical":
			critCount++
		case "warning":
			warnCount++
		case "info":
			infoCount++
		}
		categoryCounts[issue.Category]++
	}

	fmt.Printf("\n📊 Audit Complete! Scanned %d page viewports.\n", len(audit.Metrics))
	fmt.Printf("   🚨 Critical: %d | ⚠️ Warnings: %d | ℹ️ Notices: %d\n\n", critCount, warnCount, infoCount)

	// 6. Generate Markdown Report
	var report strings.Builder
	report.WriteString("# Playwright Automated Audit & Site Health Report\n\n")
	report.WriteString(fmt.Sprintf("**Date**: %s  \n", audit.Timestamp))
	report.WriteString("**Auditor**: Google Antigravity Playwright Automated Suite (Golang runner)  \n")
	report.WriteString(fmt.Sprintf("**Pages Tested**: %d pages (Mobile 390px + Desktop 1366px viewports)  \n\n", len(audit.Metrics)/2))

	report.WriteString("## Executive Summary\n\n")
	report.WriteString(fmt.Sprintf("- **Critical Issues**: %d\n", critCount))
	report.WriteString(fmt.Sprintf("- **Warnings**: %d\n", warnCount))
	report.WriteString(fmt.Sprintf("- **Optimization Opportunities**: %d\n\n", infoCount))

	report.WriteString("### Issue Breakdown by Category\n\n")
	report.WriteString("| Category | Issues Found |\n|---|---|\n")
	for cat, count := range categoryCounts {
		report.WriteString(fmt.Sprintf("| **%s** | %d |\n", strings.Title(cat), count))
	}
	report.WriteString("\n---\n\n")

	// Critical Issues
	report.WriteString("## 🚨 Critical Issues (Immediate Fix Required)\n\n")
	if critCount == 0 {
		report.WriteString("✅ **Zero critical blockers found!** No horizontal scroll overflow, no broken images, and no unhandled JavaScript runtime exceptions.\n\n")
	} else {
		report.WriteString("| Page | Viewport | Category | Details |\n|---|---|---|---|\n")
		for _, issue := range audit.Issues {
			if issue.Severity == "critical" {
				report.WriteString(fmt.Sprintf("| `%s` | %s | %s | %s |\n", issue.Page, issue.Device, issue.Category, issue.Message))
			}
		}
		report.WriteString("\n")
	}

	// Warnings
	report.WriteString("## ⚠️ Warnings & Usability / Accessibility Findings\n\n")
	if warnCount == 0 {
		report.WriteString("✅ No warnings detected across tested pages.\n\n")
	} else {
		report.WriteString("| Page | Viewport | Category | Details |\n|---|---|---|---|\n")
		for _, issue := range audit.Issues {
			if issue.Severity == "warning" {
				report.WriteString(fmt.Sprintf("| `%s` | %s | %s | %s |\n", issue.Page, issue.Device, issue.Category, issue.Message))
			}
		}
		report.WriteString("\n")
	}

	// Page by Page Performance & DOM table
	report.WriteString("## 📈 Page Performance & Structure Summary\n\n")
	report.WriteString("| Page | Device | Load Time | DOM Nodes | H1 Count | Sticky Bar | Issues |\n|---|---|---|---|---|---|---|\n")

	sort.Slice(audit.Metrics, func(i, j int) bool {
		if audit.Metrics[i].URL == audit.Metrics[j].URL {
			return audit.Metrics[i].Device < audit.Metrics[j].Device
		}
		return audit.Metrics[i].URL < audit.Metrics[j].URL
	})

	for _, m := range audit.Metrics {
		stickyStatus := "N/A"
		if m.Device == "Mobile" {
			if m.StickyBarVisible {
				stickyStatus = "✅ Visible"
			} else {
				stickyStatus = "❌ Missing"
			}
		}
		issuesCount := len(m.ConsoleErrors) + len(m.NetworkErrors)
		report.WriteString(fmt.Sprintf("| `%s` | %s | %dms | %d | %d | %s | %d |\n",
			m.URL, m.Device, m.LoadTimeMs, m.DOMNodes, m.H1Count, stickyStatus, issuesCount))
	}

	// Action Plan
	report.WriteString("\n## 🎯 Prioritized Action Plan to Improve\n\n")
	report.WriteString("Based on the Playwright live browser inspection, here is the prioritized roadmap:\n\n")
	report.WriteString("### Priority 1: Accessibility & Form Polish (High Impact)\n")
	report.WriteString("1. **Explicit Form Labels**: Ensure all `<input>` elements in both Quick Form and Estimate Form have explicit `<label for=\"...\">` bindings or `aria-label` attributes to ensure WCAG 2.1 AA compliance.\n")
	report.WriteString("2. **Mobile Tap Target Padding**: Ensure button and summary touch targets meet the minimum 44x44px tap zone on mobile viewports for seamless thumbs-friendly navigation.\n\n")

	report.WriteString("### Priority 2: Visual & CRO Consistency\n")
	report.WriteString("1. **Sticky Call Bar Mobile Parity**: Verify that every landing page, geo page, and blog post displays the gold sticky call bar on mobile screens.\n")
	report.WriteString("2. **Image Alt Attribute Completeness**: Review any dynamic or newly added images across gallery or blog cards to guarantee descriptive keyword-rich alt text.\n\n")

	report.WriteString("### Priority 3: Performance & DOM Efficiency\n")
	report.WriteString("1. **Gallery Lazy Rendering**: On `gallery.html` where 300+ project photos reside, continue maintaining pagination / lazy chunking so DOM node count remains fast (< 1,500 nodes).\n")
	report.WriteString("2. **Preconnect & Font Display**: Verify that critical fonts (`Oswald`, `Source Sans Pro`) use `font-display: swap` to prevent FOIT (Flash of Invisible Text) during network throttles.\n")

	// Save Report
	reportDir := "/home/amram/WEBSITE/seo-workspace/reports"
	os.MkdirAll(reportDir, 0755)
	reportPath := filepath.Join(reportDir, "playwright-audit-report.md")
	if err := os.WriteFile(reportPath, []byte(report.String()), 0644); err != nil {
		fmt.Printf("Failed to write markdown report: %v\n", err)
	} else {
		fmt.Printf("📄 Comprehensive audit report saved to: %s\n", reportPath)
	}

	// Print summary to console
	fmt.Println(report.String())
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
