# Raw report inventory — as of 2026-10-31

48 PDFs downloaded to `raw-reports/{NSW,QLD,SA,WA}/`, ~92MB total.

## NSW — 8 files, `raw-reports/NSW/`
Dedicated DVDRT reports, 2010 to 2023. Source: coroners.nsw.gov.au/dvdrt-reports.html
- 2010-2011, 2011-2012, 2012-2013, 2013-2015, 2015-2017, 2017-2019, 2019-2021, 2021-2023

## QLD — 19 files, `raw-reports/QLD/`
Dedicated DFVDRAB annual reports + matching Queensland Government responses, 2016-17 to 2025-26 (2025-26 government response not yet published). Source: coronerscourt.qld.gov.au/dfvdrab/annual-reports-and-government-responses
- 2016-17 through 2025-26, report + response pairs (government response for 2025-26 pending)

The government response files are the most direct source for the `status` field in the extraction schema — QLD is the only jurisdiction where the government explicitly states, in writing, which recommendations it accepted, partially accepted, or rejected.

## SA — 17 files, `raw-reports/SA/`
**Correction to the original scope doc**: SA has no DV-dedicated death review report. DV content is a section embedded inside the general State Coroner's Annual Report (courts.sa.gov.au/publications/annual-reports/), required under the Coroners Act 2003. This means extraction has to locate the DV-specific subsection within a general-purpose coronial report, not parse a document that's already scoped to DV.
- Downloaded: 2005-2006, 2006-2007, 2007-2008, 2008-2009, 2009-2010, 2011-2012, 2012-2013, 2013-2014, 2014-2015, 2015-2016, 2017-2018, 2018-2019, 2020-2021, 2021-2022, 2022-2023, 2023-2024, 2024-2025
- **Missing — not fixable by retrying**: 2010-2011, 2016-2017, 2019-2020. Confirmed via raw HTTP response (not just a client-side retry) that courts.sa.gov.au returns `200 OK` with the correct declared `Content-Length` (e.g. 830083 bytes) but the body is entirely null bytes — a corrupted/zero-filled file on their own server, not a stale token or request issue. Checked for an alternate copy via Wayback Machine and the SA Parliament tabled-papers index; none found. The only remaining path is asking Courts SA directly (email/FOI) to re-upload the three files — not something scraping can fix.

**Decision (2026-10-31):** not chasing this further. The site will state these three years as a known data gap rather than block on them.

## WA — 4 files, `raw-reports/WA/`
Not a single-format series — three separate investigations plus one implementation check, 2015 to 2026. Source: ombudsman.wa.gov.au/Publications/Reports.htm
- `2015_VRO_investigation.pdf` — 54 recommendations to 4 agencies (VRO-focused)
- `2022_FDV_suicide_investigation.pdf` — 9 recommendations, 4-volume investigation
- `2023_implementation_report.pdf` — explicit follow-up on whether the 2022 recommendations were given effect (same value as QLD's government responses — a direct status source)
- `2026_FDV_review.pdf` — 9 recommendations, reviewing 237 fatalities since 2012

## Aggregate scorecard availability, by jurisdiction (checked 2026-11-01)

**NSW** — one-off aggregate table exists: Table 7.2 in the 2019-2021 report ("DVDRT recommendations by implementation status", n=122). Saved to `extracted/scorecards/NSW_2019-2021_scorecard.json`.

**QLD — confirmed, and better than NSW's.** Table 2.1 in the 2025-26 report ("Implementation status of Board recommendations, by financial year, 2016-2025") is a *running cumulative table the Board republishes and updates every year*, broken down per report-year with both government-response status (accepted/accepted in principle/accepted in part/noted) and implementation status (completed/in progress/not commenced), total n=84. Cross-checked against Figure 2.2 in the 2023-24 report, which shows the same per-year splits as they stood two years earlier — confirms it's a maintained series, not a one-off. No per-recommendation extraction needed for QLD jurisdiction-level findings. Saved to `extracted/scorecards/QLD_cumulative_scorecard.json`.

**SA — no aggregate scorecard, per-recommendation extraction required.** Checked the most recent available year (2024-2025): DV recommendations are scattered as individual inquest-level "Response to Recommendations" sections inside a general coronial annual report covering all death types (snorkelling accidents, etc., not just DV), each with its own numbered recommendations and agency responses. There is no table that rolls these up by DV-specific implementation status. Confirms the inventory note above — extraction will need to locate and hand-extract the DV subsection(s) per year, no shortcut available.

**WA — no table, but low-effort regardless.** The 2023 implementation report (direct follow-up to the 2022 FDV-and-suicide investigation) is structured as per-recommendation narrative, not a summary table — but it only covers 9 recommendations total, so manual/row-level extraction here is trivial and was always going to be needed at this volume.

**Net effect on the two-week plan:** NSW and QLD both have usable aggregates (QLD's is actually the strongest in the whole set). SA and WA's per-recommendation extraction is now done (see below) — all four Tier 1 jurisdictions have structured data ready for site-building.

## SA/WA per-recommendation extraction — complete (2026-11-01)

**WA — done. 72 recommendation rows across 3 files.** `extracted/recommendations/WA_2015_VRO_investigation.json` (54, agency-tagged, status not yet classified — pre-dates any WA follow-up report so no status source exists), `WA_2022_FDV_suicide_investigation.json` (9, each with a status verdict pulled from the 2023 implementation report — none are "implemented": all 9 are "in progress" at varying strength, from "steps have been taken and are proposed to be taken" down to the weaker "steps are proposed to be taken" for recs 5/6/8), `WA_2026_FDV_review.json` (9, all "not started" — report is brand new, government response due 1 Oct 2026). The 2023 implementation report contributed zero new recommendations of its own — it's pure status narrative on the 2022 set, so its content is folded into that file rather than kept separate.

**SA — done. 38 recommendation rows across 5 files**, matching scope.md's original ~35 estimate closely. DV-specific coronial recommendations are **not evenly spread across the 2005-2025 series** — they cluster almost entirely in 2011-2018:
- `SA_2011-2012.json` (14) — Hayward/Durance inquest, 13 numbered recs + 1 preliminary-finding rec, directed to the Attorney-General, Minister for Communities & Social Inclusion, Minister for Status of Women, and Commissioner of Police.
- `SA_2012-2013.json` (6) — Shane Andrew Robinson inquest, directed to Commissioner of Police and Minister for Correctional Services. Status verdicts for both this case and Hayward/Durance's recs 1-3 and 10-13 came from the following year's follow-up narrative (2013-2014 report) — SA's annual reports carry government-response updates the same way QLD's do, just as embedded case narrative rather than a table. One Hayward/Durance rec (3) was effectively superseded by different legislation (Statutes Amendment (Serious Firearm Offences) Act 2012) rather than the literal Bail Act amendment requested; one Robinson rec (5, random saliva testing) was explicitly rejected by Correctional Services as impractical.
- `SA_2014-2015.json` (9) — Zahra Abrahimzadeh inquest (SA's highest-profile DV homicide case; recommendations directed unusually to the Premier rather than the Police Commissioner "given that this Inquest is about domestic violence... a key priority of the Government"). **No formal government response to these 9 was found anywhere in the corpus** — unlike every other case here, Premier-directed recommendations don't appear to get the same follow-up reporting as Minister/Commissioner-directed ones. All 9 remain status "unclear" for that reason, not because extraction missed something.
- `SA_2015-2016.json` (4) — Jeremy Godfrey Harding-Roots inquest. Rec 1 explicitly repeats Abrahimzadeh's rec 1 verbatim ("as the State Coroner has recommended in the matter of the death of Mrs Zahra Abrahimzadeh") — a coroner-acknowledged repeat, linked via `repeat_of`. All 4 have same-report status verdicts (3 implemented, 1 superseded by a pre-existing legislative change).
- `SA_2017-2018.json` (5) — Deborah Francis McKenzie inquest. Of 12 total recommendations in this case, only 8-12 are DV-specific (complainant-as-informant-against-her-domestic-partner protocol, prosecutor bail training, witness protection); 1-7 are generic hospital/suicide-risk practice and are out of scope for this tracker.

**Scope boundary applied, worth recording:** a 2014-2015 Chloe Lee Valentine recommendation ("domestic violence counselling be implemented... where Families SA identifies it as a risk factor") was deliberately **excluded**. That case is a child-abuse death (leading to SA's Child Protection Systems Royal Commission), not a DV fatality — DV is named only as one contributing risk factor for the parent, not the cause of death. Including it would blur this tracker's scope into child-abuse case reviews generally, which is a different (if related) problem. Apply the same test to any future SA case: is the *death itself* DV-related, not merely does DV appear somewhere in the narrative.

**Confirmed empty, not an extraction gap:** 2005-06 through 2009-10 (zero "domestic violence"/"family violence" mentions — predates DV as a distinct coronial reporting category), 2013-14 (status-update-only, no new recs — folded into 2012-13 above), 2020-21 through 2023-24 (zero mentions of "domestic violence", "family violence", "intimate partner", "coercive control", or "former/ex-partner" — checked all four terms directly against text, not just the first two).

**2018-2019 and the missing 2019-2020 report — a real, not generic, consequence of the data gap.** The 2018-2019 report mentions a specific DV double-death inquest — Graziella Dailler and Wayne Dion Muir, same death date (15 May 2014), inquest 4/2018, opened April 2018 — receiving dedicated funding as one of four "complex inquests," findings not yet delivered as of that report. This case never appears again in any SA report we hold. Its outcome and any recommendations almost certainly landed in the one SA year we're missing and can't recover from the server (2019-2020, confirmed corrupted at courts.sa.gov.au — see above). This turns the known data gap from an abstract completeness caveat into a specific missing case worth naming on the site itself.

## Not yet pulled
- VIC FVRIM reports (Tier 2 — concluded 2022, different register format, deferred per scope)
- NT individual coronial inquest recommendations (Tier 2 — no standing register)
- QLD government response 2025-26 (not yet published by Queensland Government)
