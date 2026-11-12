# Google Local Services Ads (LSA) eligibility — AE-035

**Status:** assessment only. LSA requires a Google Ads account, a verified
business, and Google's own screening. Nothing has been submitted.

## Why LSA matters here

LSA places the business above regular search ads with a "Google Guaranteed"
badge and charges per *lead* (not per click). For an LA electrical contractor
it is usually the highest-intent paid channel, and it competes directly with
the GBP map pack.

## Eligibility check

| Requirement | AMY Electric status | Action |
|---|---|---|
| Licensed contractor | C-10 #981578, active (CSLB verified 2026-11-12) | Ready |
| Business insurance | CSLB bond verified; certificate of insurance on request | Upload COI when applying |
| Background check | Owner + any technician who may be dispatched | Google runs this per person |
| Business verification | GBP must exist and be verified | Confirm GBP is verified |
| Service area | Greater Los Angeles | Define the same radius as the site |
| Google Ads account | Not yet created | Create, then apply at `ads.google.com/local-services-ads` |
| Response time | Must answer leads fast (LSA ranks responsiveness) | Route to a phone that is answered 07:00–19:00 |

## Category selection

Apply under **Electrician** (primary). Secondary categories may include
`EV Charger Installation` if offered in the LSA vertical list — check the
current category picker; do not select categories you cannot service.

## Screened / Guaranteed

"Google Guaranteed" requires the background check and insurance. Once approved:

- Badge appears on the LSA unit and in GBP-adjacent placements.
- Google may reimburse up to a cap for claims on screened work.
- Keep the COI current — lapse suspends the badge.

## Budget and lead economics

- Start with a monthly cap, not a daily bid: $1,500–$2,500/mo is a common
  starting range for a single-market electrical contractor.
- LSA leads are charged per lead, and *disputes* are allowed for spam/wrong
  service area. Dispute every junk lead within the window.
- Track LSA leads in the CRM with `source=lsa` and `utm_source=lsa` so
  `/api/admin/report` can compute cost per qualified lead.

## Integration work (already supported)

- Every lead stores `utm_source`, `gclid`, `source_page` and segment/urgency.
- `POST /api/admin/spend` accepts `channel: "lsa"` rows so LSA spend is
  included in the weekly report and CPQL.
- Phone calls from LSA land on (818) 302-5614; the site's `phone_click` event
  covers on-site calls, but LSA calls are reported by Google, not the site.

## Decision

Apply. The licence, bond and service area already clear the hard requirements;
the only open items are the Google Ads account, the background check and the
certificate of insurance.
