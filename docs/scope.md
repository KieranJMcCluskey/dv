# DV Death Review Recommendation Tracker — scope

## Why this, not the judge-scorecard idea
Judge-level sentencing data is not published in Australia (confirmed against
BOCSAR, SACStat, ABS Criminal Courts methodology, and the NSW Judicial
Commission's own writing on the question). A league table of judges would
need data that doesn't exist publicly and would carry real defamation
exposure on top of that. Death review recommendations are the opposite shape:
written for publication, institution-named not person-named, and already
show a strong, citable finding — implementation running at roughly 15-32% a
year across the two jurisdictions already studied (Buxton-Namisnyk & Gibson,
2024).

## What the tracker actually shows
Every state DV/family-violence death review body publishes recommendations
in annual-report PDFs. Nobody aggregates them. The product is: pull every
recommendation out of every published report, tag it, track its status over
time, and surface the two things no single report shows on its own —
recommendations that keep reappearing year after year, and the jurisdictions
with no review mechanism at all.

## Jurisdictions, by maturity of what's publicly available

**Tier 1 — standing body, multiple report-points over time, explicit recommendations**
- NSW — Domestic Violence Death Review Team (NSW Coroners Court). Reports back to 2015.
- QLD — Domestic and Family Violence Death Review and Advisory Board (Coroners Court of Qld). Monitors ~75 recommendations.
- SA — DV recommendations required under the Coroners Act 2003, but **not published as a standalone report**: they're a section embedded inside the general State Coroner's Annual Report (courts.sa.gov.au). Extraction has to find the DV subsection inside a general coronial report rather than parse a document already scoped to DV. ~35 DV-specific recommendations across the series.
- WA — Ombudsman WA has reviewed every individual FDV fatality on a standing statutory basis since 1 July 2012 (not a single annual-report format like the others, but a continuing function with repeated recommendation sets): 2015 VRO investigation (54 recs to 4 agencies), 2022 "Family and Domestic Violence and Suicide" investigation (9 recs, 4 volumes), 2026 review of 237 fatalities since 2012 (9 recs), plus yearly annual-report activity (2024-25: 14 fatality reviews finalised, 1 recommendation to WA Police/Justice). Three recommendation sets across 11 years makes WA one of the best jurisdictions for testing the repeat-recommendation signal directly — worth checking whether anything from 2015 reappeared in 2022 or 2026.

**Tier 2 — concluded or ad hoc, not a continuing recommendation register**
- VIC — Family Violence Reform Implementation Monitor tracked all 227 Royal Commission recommendations annually, but the office closed 31 Dec 2022; monitoring moved to Dept of Premier & Cabinet and is no longer independent/annual in the same format.
- NT — no standing body. Recommendations come from individual coronial inquests (e.g. the Nov 2024 inquest into 4 Aboriginal women's deaths, 35 recommendations; NT govt claims 24/35 "already in place" as of its July 2025 response — a claim worth checking against the actual wording, not just repeating).

**Tier 3 — no mechanism**
- ACT, TAS — no domestic/family violence death review mechanism exists at all, per the Australian Human Rights Commission's own 2016 call to expand DV death review to these jurisdictions. Worth stating as a finding in its own right, not just an absence: nobody is systematically counting or reviewing these deaths in two Australian jurisdictions.

## Extraction schema (one row per recommendation)
- `id` — jurisdiction + report year + recommendation number
- `jurisdiction`
- `review_body`
- `report_title`, `report_url`, `page_ref`
- `report_period` — years covered by the report
- `recommendation_number`
- `recommendation_text` — verbatim
- `target_agency` — multi-select: police / health / courts-justice / corrections / child-protection / education / housing / state-govt / other
- `theme` — risk assessment, information sharing, perpetrator accountability, cultural safety/First Nations, training, legislative reform, data collection, housing, other
- `status` — not started / in progress / implemented / rejected / superseded / unclear
- `status_as_of` — most recent report that commented on this recommendation
- `first_appeared_year`
- `repeat_of` — id of an earlier, materially identical recommendation (this field is what exposes institutional inertia)
- `source_quote` — the sentence the status call is based on, so every status is checkable against the original PDF

## What's shippable in two weeks
1. **Days 1-3** — collect every available report PDF for NSW, QLD, SA, and WA (the four Tier 1 jurisdictions — maybe 20-25 PDFs total, most already linked above; WA's are the 2015 VRO report, the 2022 four-volume FDV-and-suicide report, and the 2026 review).
2. **Days 4-7** — AI-assisted extraction: chunk each PDF, prompt-extract rows against the schema above, spot-check a sample against the source by hand (NSW+QLD already have one academic cross-check to validate against — Buxton-Namisnyk & Gibson 2024 — use it to sanity-test the extraction, not to skip it).
3. **Days 8-10** — build the site: static table + filters (jurisdiction, theme, agency, status), a timeline view that visually flags repeat recommendations, and a headline stat bar (total recommendations, % implemented, count of repeats). Follow the vite + index.html + src pattern already used in echo-chamber / tax-the-gas / housing.
4. **Days 11-12** — write up the Tier 2/Tier 3 gap (VIC/WA/NT ad hoc, ACT/TAS nonexistent) as a short companion page — cheap to produce, no extraction needed, and it's a strong standalone finding.
5. **Days 13-14** — publish, source-link everything back to the original PDF + page, write the one-paragraph "here's what this shows" for sharing.

Not in v1: VIC historical FVRIM data (227 recommendations, different format, concluded body — bigger lift), NT inquest-by-inquest recommendations (no standing register to anchor against), any individual- or victim-level detail beyond what the source reports already published.

## Notes
- `~/kieran-os/projects/echo-chamber` (misinformation/echo chambers) and
  `~/kieran-os/projects/tax-the-gas` (tax/inequality) already exist for the
  other two causes on the list, both dormant since mid-2026. Worth deciding
  whether this tracker is the one to actually finish before touching those
  again.
