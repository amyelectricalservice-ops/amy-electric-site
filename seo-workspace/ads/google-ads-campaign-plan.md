# Google Ads campaign plan — AE-031 → AE-034

**Status:** spec only. Nothing here has been created in a Google Ads account — no
account access is configured in this repo. An owner or ads manager imports it.
**Do not claim these campaigns are live.**

- Account: AMY Electric (to be created / linked to the GBP)
- Conversion actions: `lead_accepted` (website form), `phone_click` (click-to-call), `booking_request`
- Tracking template: `{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_term={keyword}&gclid={gclid}`
- Final URL suffix: none (the site reads `gclid` and UTM params from the query string)
- Geo: Los Angeles metro; exclude outside service radius
- Networks: Search only (no Display / Partners at launch)
- Ad schedule: Mon–Sat 07:00–19:00; emergency campaign 24/7
- Location option: "Presence or interest" → **Presence only**
- Language: English

Budgets are starting recommendations, not approved spend.

---

## AE-031 — EV Charger Installation

| Setting | Value |
|---|---|
| Campaign | `Search — EV Charger — LA` |
| Daily budget | $35 |
| Bid strategy | Maximize conversions (start), then tCPA $120 after 30 conversions |
| Landing page | `/ev-charger-installation` (variant: `/tesla-charger-installation`) |
| Match types | Phrase + exact only |

**Ad group 1 — Tesla Wall Connector**
Keywords: `[tesla wall connector installation los angeles]`, `"tesla charger installer near me"`, `"tesla wall charger installation cost"`, `"tesla charger installation"`

**Ad group 2 — Level 2 / NEMA**
Keywords: `"level 2 ev charger installation"`, `"nema 14-50 installation los angeles"`, `"ev charger installation cost"`, `"home ev charging installation"`

**Ad group 3 — Rebates**
Keywords: `"ladwp ev charger rebate"`, `"ev charger rebate los angeles"`, `"ev charger installation rebate"`

RSA headlines (≤30 chars):
`Tesla Charger Install`, `EVITP Certified Installer`, `LADWP Rebate Paperwork`, `Permit Included`, `From $350 — Free Quote`, `C-10 #981578 Licensed`, `Same-Week Installation`, `Charge At Home Tonight`

Descriptions (≤90):
`Tesla Wall Connector, NEMA 14-50 and hardwired Level 2 chargers. Permit, load calc and inspection included.`
`EVITP-certified C-10 electricians. Upfront written pricing from $350. We handle the LADWP rebate paperwork.`

Sitelinks: `EV Charger Pricing`, `Tesla Wall Connector`, `LADWP Rebates`, `Book Online`

---

## AE-032 — Panel Upgrade

| Setting | Value |
|---|---|
| Campaign | `Search — Panel Upgrade — LA` |
| Daily budget | $30 |
| Bid strategy | Maximize conversions → tCPA $150 |
| Landing page | `/panel-upgrade` (variant: `/200-amp-panel-upgrade`) |

**Ad group 1 — 200A upgrade**
Keywords: `[200 amp panel upgrade los angeles]`, `"electrical panel upgrade cost"`, `"100 to 200 amp service upgrade"`, `"panel upgrade electrician"`

**Ad group 2 — Hazard panels**
Keywords: `"federal pacific panel replacement"`, `"zinsco panel replacement"`, `"replace fpe panel"`, `"old electrical panel replacement"`

**Ad group 3 — Capacity**
Keywords: `"do i need a panel upgrade"`, `"electrical load calculation los angeles"`, `"panel upgrade for ev charger"`

Headlines: `200A Panel Upgrade`, `From $2,500 — Permitted`, `LADWP Coordination`, `Federal Pacific Hazard?`, `C-10 #981578 Licensed`, `Free Written Estimate`, `Done In One Day`, `Panel + Permit Included`

Descriptions:
`100A to 200A service upgrades with LADWP coordination, LADBS permit and inspection. Written price before we start.`
`Federal Pacific and Zinsco replacement, subpanels, EV-ready capacity. Licensed C-10 #981578. Free estimate.`

Sitelinks: `Panel Upgrade Cost`, `200A Upgrade`, `FPE & Zinsco`, `Book Online`

---

## AE-033 — Residential Electrician

| Setting | Value |
|---|---|
| Campaign | `Search — Residential — LA` |
| Daily budget | $40 |
| Bid strategy | Maximize conversions → tCPA $130 |
| Landing page | `/residential-electrician` |

**Ad group 1 — Repairs**
Keywords: `"electrician near me"`, `[electrician los angeles]`, `"emergency electrician los angeles"`, `"outlet repair los angeles"`, `"breaker keeps tripping"`

**Ad group 2 — Rewiring**
Keywords: `"whole home rewiring cost"`, `"knob and tube wiring replacement"`, `"aluminum wiring repair"`, `"house rewiring los angeles"`

**Ad group 3 — Lighting / fans**
Keywords: `"recessed lighting installation los angeles"`, `"ceiling fan installation"`, `"outdoor lighting installer"`

Headlines: `Licensed LA Electrician`, `Same-Day Dispatch`, `Upfront Written Price`, `C-10 #981578 · Bonded`, `Repairs, Panels, Rewiring`, `4.9★ · 87 Reviews`, `Permits Handled`, `Call (818) 302-5614`

Descriptions:
`Repairs, panel upgrades, rewiring and lighting for LA homes. Written price before work starts. Permits handled.`
`Licensed C-10 #981578 and EVITP #4051604. Same-day dispatch when available. Call or book online.`

Sitelinks: `Same-Day Repair`, `Panel Upgrades`, `Rewiring Guide`, `Reviews`

---

## AE-034 — Commercial Electrician

| Setting | Value |
|---|---|
| Campaign | `Search — Commercial — LA` |
| Daily budget | $30 |
| Bid strategy | Maximize conversions → tCPA $300 (longer cycle) |
| Landing page | `/commercial-electrical` |
| Schedule | Mon–Fri 07:00–18:00 |

**Ad group 1 — Tenant improvement**
Keywords: `"commercial electrician los angeles"`, `"tenant improvement electrician"`, `"commercial electrical contractor"`, `"restaurant electrical contractor"`

**Ad group 2 — Fleet charging**
Keywords: `"commercial ev charger installation"`, `"fleet charging installation"`, `"workplace ev charging installer"`

**Ad group 3 — 3-phase / service**
Keywords: `"3 phase electrical service installation"`, `"400 amp commercial service"`, `"commercial panel upgrade los angeles"`

Headlines: `Commercial Electrician`, `Tenant Improvements`, `EV Fleet Charging`, `3-Phase & 400A Service`, `After-Hours Available`, `C-10 #981578 · Bonded`, `Free Site Walkthrough`, `Permits & Inspections`

Descriptions:
`Tenant improvements, LED retrofits, 3-phase service and EV fleet charging. Permitted, inspected, on schedule.`
`One licensed C-10 contractor from rough-in to final. After-hours work to avoid downtime. Free walkthrough.`

Sitelinks: `Commercial Services`, `EV Fleet Charging`, `Panel Upgrades`, `Request Walkthrough`

---

## Shared negative keywords (apply to all four campaigns)

```
free electrician
diy
how to
youtube
apprentice
jobs
hiring
salary
license lookup
renew license
school
course
training
wholesale
supply house
home depot
lowes
amazon
generator repair
solar panel installation
solar company
roofing
plumbing
handyman
cheap
$50
coupon
```

## Conversion setup (AE-023 / AE-024)

| Action | Type | Source | Value |
|---|---|---|---|
| `lead_accepted` | Website | gtag event fired only after `/api/contact` returns success | $120 residential / $300 commercial |
| `phone_click` | Website | `tel:` click event | $60 |
| `booking-request` | Website | `/book` form success (request_type=`booking-request`) | $80 |
| Calls from ads | Call reporting | Google forwarding number on mobile | count >60s as conversion |

Primary conversion for bidding: `lead_accepted`. Secondary (observe only): `phone_click`.

## Launch checklist

- [ ] Google Ads account created and billing verified
- [ ] GA4 property created; `GA4_ID` set as a Worker secret
- [ ] Conversion actions created and linked to the account
- [ ] `GADS_ID` and `GADS_CONVERSION_LABEL` set as Worker secrets
- [ ] Search Console linked to Ads
- [ ] Landing pages return 200 on production and pass mobile Lighthouse
- [ ] Call extension added with (818) 302-5614
- [ ] Budget approved by owner
- [ ] Negative keyword list applied
- [ ] After 14 days: review search terms, add negatives, pause zero-conversion keywords
