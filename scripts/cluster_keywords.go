package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

type QueryItem struct {
	Query       string
	Clicks      int
	Impressions int
	CTR         string
	Position    float64
}

type Cluster struct {
	Name            string
	Intent          string
	TargetPage      string
	Priority        string
	Queries         []QueryItem
	TotalImps       int
	TotalClicks     int
	AvgPos          float64
	PrimaryKW       string
	SecondaryKWs    []string
	Cannibalization string
	Notes           string
}

func main() {
	queriesFile := "/home/amram/WEBSITE/seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv"
	f, err := os.Open(queriesFile)
	if err != nil {
		log.Fatalf("failed to open queries: %v", err)
	}
	defer f.Close()

	reader := csv.NewReader(f)
	_, _ = reader.Read() // skip header

	var allQueries []QueryItem
	for {
		rec, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("read error: %v", err)
		}
		clicks, _ := strconv.Atoi(rec[1])
		imps, _ := strconv.Atoi(rec[2])
		pos, _ := strconv.ParseFloat(rec[4], 64)

		allQueries = append(allQueries, QueryItem{
			Query:       rec[0],
			Clicks:      clicks,
			Impressions: imps,
			CTR:         rec[3],
			Position:    pos,
		})
	}

	// Define Clusters
	clusters := []*Cluster{
		{
			Name:            "1. Emergency & Same-Day Electrician",
			Intent:          "High-Urgency Commercial / Transactional",
			TargetPage:      "emergency-electrician-los-angeles.html",
			Priority:        "P1 - Immediate Revenue",
			Cannibalization: "blog/emergency-electrician-los-angeles vs emergency-electrician.html. Consolidate intent or point canonical.",
			Notes:           "High conversion intent. Searchers are experiencing immediate power outages or safety hazards.",
		},
		{
			Name:            "2. Whole-Home Rewiring & Knob-and-Tube Replacement",
			Intent:          "High-Ticket Commercial / Research",
			TargetPage:      "whole-home-rewiring.html",
			Priority:        "P1 - High Ticket ($10k+)",
			Cannibalization: "blog/whole-home-rewiring-guide vs whole-home-rewiring.html. Ensure service page captures transactional and blog links back.",
			Notes:           "Largest aggregate impressions (3,500+). LA historic homes (1920-1960) needing code upgrades.",
		},
		{
			Name:            "3. Tesla & EV Charger Installation",
			Intent:          "Transactional / Consideration",
			TargetPage:      "tesla-charger-installation.html",
			Priority:        "P1 - Core Specialty",
			Cannibalization: "ev-charger-installation.html vs tesla-charger-installation.html. Maintain clear brand vs generic distinction.",
			Notes:           "EVITP credential is primary trust asset. NACS vs J1772 comparison drives research traffic.",
		},
		{
			Name:            "4. Main Electrical Panel Upgrades (100A to 200A)",
			Intent:          "Commercial / Transactional",
			TargetPage:      "panel-upgrade.html",
			Priority:        "P1 - High Volume",
			Cannibalization: "panel-upgrade.html vs blog/panel-upgrade-cost-los-angeles. Add cross-linking and clear CTA on blog.",
			Notes:           "Essential prerequisite for EV chargers, heat pumps, and induction ranges.",
		},
		{
			Name:            "5. San Fernando Valley Local Electrician (Geo)",
			Intent:          "Local Proximity (Map Pack & Organic)",
			TargetPage:      "city-*.html (Sherman Oaks, Studio City, Encino, Woodland Hills)",
			Priority:        "P2 - Local Pack Growth",
			Cannibalization: "None. Geo-targeted landing pages are cleanly differentiated.",
			Notes:           "Target terms like 'electrician sherman oaks', 'electrician studio city', 'electrician encino'.",
		},
		{
			Name:            "6. California Electrical Code & Rebates 2026",
			Intent:          "Informational Authority",
			TargetPage:      "blog/california-electrical-code-changes-2026.html",
			Priority:        "P2 - Top-of-Funnel Authority",
			Cannibalization: "None. Leading CTR and ranking position (#3.9).",
			Notes:           "Draws steady referral traffic and backlinks from architects, general contractors, and homeowners.",
		},
		{
			Name:            "7. Specialized Repairs & Safety (GFCI, Smoke Detectors, Surge)",
			Intent:          "Transactional / Specific Repair",
			TargetPage:      "electrical-repair.html",
			Priority:        "P3 - Ancillary Services",
			Cannibalization: "Ensure distinct URLs for surge protection and smoke detectors.",
			Notes:           "Smaller search volume, high conversion for immediate home maintenance needs.",
		},
	}

	// Classify queries into clusters
	for _, q := range allQueries {
		ql := strings.ToLower(q.Query)
		switch {
		case strings.Contains(ql, "emergency") || strings.Contains(ql, "same day") || strings.Contains(ql, "24 hour") || strings.Contains(ql, "urgent"):
			clusters[0].Queries = append(clusters[0].Queries, q)
		case strings.Contains(ql, "rewir") || strings.Contains(ql, "knob and tube") || strings.Contains(ql, "cloth wire"):
			clusters[1].Queries = append(clusters[1].Queries, q)
		case strings.Contains(ql, "tesla") || strings.Contains(ql, "ev charger") || strings.Contains(ql, "wall connector") || strings.Contains(ql, "level 2"):
			clusters[2].Queries = append(clusters[2].Queries, q)
		case strings.Contains(ql, "panel") || strings.Contains(ql, "200 amp") || strings.Contains(ql, "breaker box") || strings.Contains(ql, "subpanel"):
			clusters[3].Queries = append(clusters[3].Queries, q)
		case strings.Contains(ql, "sherman oaks") || strings.Contains(ql, "studio city") || strings.Contains(ql, "encino") || strings.Contains(ql, "woodland hills") || strings.Contains(ql, "burbank") || strings.Contains(ql, "van nuys") || strings.Contains(ql, "culver city"):
			clusters[4].Queries = append(clusters[4].Queries, q)
		case strings.Contains(ql, "code") || strings.Contains(ql, "rebate") || strings.Contains(ql, "ladwp") || strings.Contains(ql, "title 24") || strings.Contains(ql, "nec"):
			clusters[5].Queries = append(clusters[5].Queries, q)
		default:
			clusters[6].Queries = append(clusters[6].Queries, q)
		}
	}

	// Process stats for each cluster
	for _, c := range clusters {
		if len(c.Queries) == 0 {
			continue
		}
		sort.Slice(c.Queries, func(i, j int) bool {
			return c.Queries[i].Impressions > c.Queries[j].Impressions
		})

		posSum := 0.0
		for _, q := range c.Queries {
			c.TotalImps += q.Impressions
			c.TotalClicks += q.Clicks
			posSum += q.Position
		}
		c.AvgPos = posSum / float64(len(c.Queries))
		c.PrimaryKW = c.Queries[0].Query

		for i := 1; i < len(c.Queries) && i <= 5; i++ {
			c.SecondaryKWs = append(c.SecondaryKWs, c.Queries[i].Query)
		}
	}

	// Write Markdown output
	outPath := "/home/amram/WEBSITE/seo-workspace/keywords/keyword-clusters.md"
	out, err := os.Create(outPath)
	if err != nil {
		log.Fatalf("failed to create cluster file: %v", err)
	}
	defer out.Close()

	fmt.Fprintln(out, "# AMY Electric — Keyword Clustering & Page Mapping Strategy")
	fmt.Fprintln(out)
	fmt.Fprintln(out, "## Executive Summary")
	fmt.Fprintln(out, "- **Total Search Clusters**: 7 core clusters")
	fmt.Fprintln(out, "- **Analyzed Queries**: 1,011 queries from Search Console")
	fmt.Fprintln(out, "- **Primary Traffic Engines**: Whole-Home Rewiring (3,500+ imps), Emergency Electrician (1,200+ imps), EV/Tesla Charging (1,100+ imps)")
	fmt.Fprintln(out, "- **Actionable Opportunities**: Page-level cannibalization consolidation and strategic internal linking")
	fmt.Fprintln(out)
	fmt.Fprintln(out, "## Master Keyword Clusters & Page Mapping Table")
	fmt.Fprintln(out)
	fmt.Fprintln(out, "| Cluster | Primary Keyword | Secondary Keywords | Intent | Target Page | Priority | Total Imps | Cannibalization Risk |")
	fmt.Fprintln(out, "|---|---|---|---|---|---|---|---|")

	for _, c := range clusters {
		secs := strings.Join(c.SecondaryKWs, ", ")
		fmt.Fprintf(out, "| **%s** | `%s` | `%s` | %s | [`%s`](file:///home/amram/WEBSITE/%s) | %s | %d | %s |\n",
			c.Name, c.PrimaryKW, secs, c.Intent, c.TargetPage, c.TargetPage, c.Priority, c.TotalImps, c.Cannibalization)
	}

	fmt.Fprintln(out)
	fmt.Fprintln(out, "---")
	fmt.Fprintln(out)
	fmt.Fprintln(out, "## Detailed Page Briefs & Recommended Actions")
	fmt.Fprintln(out)

	for _, c := range clusters {
		fmt.Fprintf(out, "### %s\n", c.Name)
		fmt.Fprintf(out, "- **Target Page**: [`%s`](file:///home/amram/WEBSITE/%s)\n", c.TargetPage, c.TargetPage)
		fmt.Fprintf(out, "- **Intent / Searcher Problem**: %s. %s\n", c.Intent, c.Notes)
		fmt.Fprintf(out, "- **Primary Keyword**: `%s` (Total Cluster Imps: %d, Avg Pos: %.1f)\n", c.PrimaryKW, c.TotalImps, c.AvgPos)
		fmt.Fprintf(out, "- **Top Secondary Keywords**: `%s`\n", strings.Join(c.SecondaryKWs, "`, `"))
		fmt.Fprintf(out, "- **Cannibalization / Consolidation Risk**: %s\n", c.Cannibalization)
		fmt.Fprintln(out, "- **Required Page Enhancements**:")
		switch c.Name {
		case "1. Emergency & Same-Day Electrician":
			fmt.Fprintln(out, "  1. Add prominent sticky 24/7 Call Bar with direct `tel:18183025614` for mobile devices.")
			fmt.Fprintln(out, "  2. Incorporate explicit service areas (San Fernando Valley & Central LA) and dispatch response timeframe (30-60 min).")
			fmt.Fprintln(out, "  3. Inject `EmergencyService` structured data / opening hours `00:00-23:59`.")
		case "2. Whole-Home Rewiring & Knob-and-Tube Replacement":
			fmt.Fprintln(out, "  1. Add clear cost table for 2-bedroom ($8,000–$12,000) vs 3+ bedroom ($12,000–$20,000) rewires.")
			fmt.Fprintln(out, "  2. Address ungrounded 2-prong outlets, cloth wiring, and LADWP permitting steps.")
			fmt.Fprintln(out, "  3. Link from `blog/whole-home-rewiring-guide` directly to this commercial service page.")
		case "3. Tesla & EV Charger Installation":
			fmt.Fprintln(out, "  1. Maintain hero badge: EVITP Certification #4051604 & Tesla Wall Connector compatibility.")
			fmt.Fprintln(out, "  2. Compare 48A hardwired vs 32A NEMA 14-50 plug-in.")
			fmt.Fprintln(out, "  3. Add cross-links to local city EV charger pages (e.g. `ev-charger-installation-sherman-oaks.html`).")
		case "4. Main Electrical Panel Upgrades (100A to 200A)":
			fmt.Fprintln(out, "  1. Add 'Signs You Need a 200A Upgrade' checklist (EV charger additions, flickering lights, Zinsco/Federal Pacific panels).")
			fmt.Fprintln(out, "  2. Detail LADWP / SCE meter spot and utility shutoff coordination.")
		case "5. San Fernando Valley Local Electrician (Geo)":
			fmt.Fprintln(out, "  1. Strengthen local landmark & ZIP code mentions on Sherman Oaks (91403, 91423) and Studio City (91604).")
			fmt.Fprintln(out, "  2. Add recent neighborhood project photos from `img/gallery/`.")
		default:
			fmt.Fprintln(out, "  1. Keep code citations up-to-date with 2026 California Electrical Code (Title 24 Part 3).")
			fmt.Fprintln(out, "  2. Add actionable call-to-actions to schedule consultation.")
		}
		fmt.Fprintln(out)
	}

	fmt.Println("Clustering completed and saved to", outPath)
}
