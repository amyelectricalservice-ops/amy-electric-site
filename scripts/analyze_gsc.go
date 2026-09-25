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

type QueryRow struct {
	Query       string
	Clicks      int
	Impressions int
	CTR         string
	Position    float64
}

func main() {
	queriesPath := "/home/amram/WEBSITE/seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv"
	f, err := os.Open(queriesPath)
	if err != nil {
		log.Fatalf("failed to open queries: %v", err)
	}
	defer f.Close()

	reader := csv.NewReader(f)
	// Read header
	header, err := reader.Read()
	if err != nil {
		log.Fatalf("failed to read header: %v", err)
	}
	_ = header

	var rows []QueryRow
	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("csv read error: %v", err)
		}
		if len(record) < 5 {
			continue
		}
		clicks, _ := strconv.Atoi(record[1])
		imps, _ := strconv.Atoi(record[2])
		pos, _ := strconv.ParseFloat(record[4], 64)

		rows = append(rows, QueryRow{
			Query:       record[0],
			Clicks:      clicks,
			Impressions: imps,
			CTR:         record[3],
			Position:    pos,
		})
	}

	// 1. Striking Distance: Position 4.0 - 25.0, sorted by Impressions desc
	var strikingDistance []QueryRow
	for _, r := range rows {
		if r.Position >= 4.0 && r.Position <= 25.0 && r.Impressions >= 10 {
			strikingDistance = append(strikingDistance, r)
		}
	}
	sort.Slice(strikingDistance, func(i, j int) bool {
		return strikingDistance[i].Impressions > strikingDistance[j].Impressions
	})

	// 2. High Impression Terms: Impressions >= 100
	var highImps []QueryRow
	for _, r := range rows {
		if r.Impressions >= 100 {
			highImps = append(highImps, r)
		}
	}
	sort.Slice(highImps, func(i, j int) bool {
		return highImps[i].Impressions > highImps[j].Impressions
	})

	// 3. Cluster by topic
	clusters := map[string][]QueryRow{
		"Emergency & 24/7":      {},
		"EV & Tesla":            {},
		"Panel & Rewiring":      {},
		"Local City / Geo":      {},
		"Codes, Rebates, Admin": {},
	}

	for _, r := range rows {
		q := strings.ToLower(r.Query)
		if strings.Contains(q, "emergency") || strings.Contains(q, "24") || strings.Contains(q, "troubleshoot") {
			clusters["Emergency & 24/7"] = append(clusters["Emergency & 24/7"], r)
		} else if strings.Contains(q, "ev") || strings.Contains(q, "tesla") || strings.Contains(q, "charger") {
			clusters["EV & Tesla"] = append(clusters["EV & Tesla"], r)
		} else if strings.Contains(q, "panel") || strings.Contains(q, "rewir") || strings.Contains(q, "wire") {
			clusters["Panel & Rewiring"] = append(clusters["Panel & Rewiring"], r)
		} else if strings.Contains(q, "sherman oaks") || strings.Contains(q, "studio city") || strings.Contains(q, "burbank") || strings.Contains(q, "encino") || strings.Contains(q, "woodland hills") || strings.Contains(q, "van nuys") || strings.Contains(q, "los angeles") {
			clusters["Local City / Geo"] = append(clusters["Local City / Geo"], r)
		} else {
			clusters["Codes, Rebates, Admin"] = append(clusters["Codes, Rebates, Admin"], r)
		}
	}

	reportPath := "/home/amram/WEBSITE/seo-workspace/reports/gsc-opportunity-report.md"
	out, err := os.Create(reportPath)
	if err != nil {
		log.Fatalf("failed to create report: %v", err)
	}
	defer out.Close()

	fmt.Fprintln(out, "# Google Search Console Opportunity Audit Report")
	fmt.Fprintln(out, "Site: https://amyelectric.com")
	fmt.Fprintln(out, "Source Data: amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv")
	fmt.Fprintln(out)
	fmt.Fprintln(out, "## 1. Top Striking Distance Keywords (Positions 4.0 – 25.0)")
	fmt.Fprintln(out, "These queries have real Google search impressions and are on the verge of first-page visibility. Small content enhancements, internal linking, and click-through optimizations can push them into high-traffic positions.")
	fmt.Fprintln(out)
	fmt.Fprintln(out, "| Query | Impressions | Clicks | CTR | Current Avg Position | Recommended Target Page |")
	fmt.Fprintln(out, "|---|---|---|---|---|---|")

	for i, r := range strikingDistance {
		if i >= 20 {
			break
		}
		target := guessTarget(r.Query)
		fmt.Fprintf(out, "| `%s` | %d | %d | %s | %.2f | %s |\n", r.Query, r.Impressions, r.Clicks, r.CTR, r.Position, target)
	}

	fmt.Fprintln(out)
	fmt.Fprintln(out, "## 2. High Impression Search Demands (Top Overall Queries)")
	fmt.Fprintln(out, "| Query | Impressions | Clicks | CTR | Current Position | Focus Area |")
	fmt.Fprintln(out, "|---|---|---|---|---|---|")
	for i, r := range highImps {
		if i >= 15 {
			break
		}
		fmt.Fprintf(out, "| `%s` | %d | %d | %s | %.2f | %s |\n", r.Query, r.Impressions, r.Clicks, r.CTR, r.Position, guessCategory(r.Query))
	}

	fmt.Fprintln(out)
	fmt.Fprintln(out, "## 3. High-Value Action Items")
	fmt.Fprintln(out, "1. **Emergency & 24/7 Electrician**: `emergency electrician los angeles` has 404 impressions at position 17.07. Boost `emergency-electrician-los-angeles.html` title tag, add emergency call-out schema, and ensure direct tap-to-call is above the fold.")
	fmt.Fprintln(out, "2. **Home Rewiring**: `home rewiring` has 499 impressions at position 23.24. Enhance `whole-home-rewiring.html` with explicit pricing ranges, permitting timelines, and internal links from city pages.")
	fmt.Fprintln(out, "3. **City Pages (Studio City, Sherman Oaks, Encino)**: `electrician studio city` (192 imps, pos 25.91) and `electrician sherman oaks` (296 imps, pos 37.04). Strengthen local knowledge sections and link directly from homepage.")
	fmt.Fprintln(out, "4. **Tesla & EV Charging**: `tesla charger installation` has 338 impressions. Cross-link between `tesla-charger-installation.html` and city EV charger pages.")

	fmt.Println("Report written successfully to", reportPath)
}

func guessCategory(q string) string {
	q = strings.ToLower(q)
	if strings.Contains(q, "emergency") || strings.Contains(q, "24") {
		return "Emergency"
	}
	if strings.Contains(q, "rewir") || strings.Contains(q, "panel") {
		return "Panel & Rewiring"
	}
	if strings.Contains(q, "tesla") || strings.Contains(q, "ev") {
		return "EV & Tesla"
	}
	if strings.Contains(q, "electrician") {
		return "Local Electrician"
	}
	return "General / Code"
}

func guessTarget(q string) string {
	q = strings.ToLower(q)
	if strings.Contains(q, "emergency") {
		return "[emergency-electrician-los-angeles.html](file:///home/amram/WEBSITE/emergency-electrician-los-angeles.html)"
	}
	if strings.Contains(q, "rewir") {
		return "[whole-home-rewiring.html](file:///home/amram/WEBSITE/whole-home-rewiring.html)"
	}
	if strings.Contains(q, "tesla") {
		return "[tesla-charger-installation.html](file:///home/amram/WEBSITE/tesla-charger-installation.html)"
	}
	if strings.Contains(q, "studio city") {
		return "[electrician-studio-city.html](file:///home/amram/WEBSITE/electrician-studio-city.html)"
	}
	if strings.Contains(q, "sherman oaks") {
		return "[electrician-sherman-oaks.html](file:///home/amram/WEBSITE/electrician-sherman-oaks.html)"
	}
	if strings.Contains(q, "california electrical code") {
		return "[blog/california-electrical-code-changes-2026.html](file:///home/amram/WEBSITE/blog/california-electrical-code-changes-2026.html)"
	}
	return "[index.html](file:///home/amram/WEBSITE/index.html)"
}
