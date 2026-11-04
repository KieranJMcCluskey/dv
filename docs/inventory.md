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

**NSW — aggregate AND per-recommendation, both published.** Corrected 2026-11-04; the earlier version of this line said NSW had the aggregate only, and the two-week plan was scoped around that. It was wrong, and wrong in the direction that made the project look unviable outside WA.

- *Aggregate:* Table 7.2 in the 2019-2021 report ("DVDRT recommendations by implementation status", n=122). Saved to `extracted/scorecards/NSW_2019-2021_scorecard.json`. This is the **Team's own** assessment, in its own five-value vocabulary (implemented / alternative practice adopted / partially implemented in progress / partially implemented not in progress / not implemented).
- *Per-recommendation:* every NSW report restates the **previous** report's recommendations in a "response and update" chapter and prints, against each one, the Whole of Government response and (from the 2017-19 report on) a follow-up update with a lead agency. That chapter is structured text, so it extracts cleanly. This is the **government's** self-assessment and is a different measurement from Table 7.2 — do not mix the two or add them together.

Why the mistake happened: the first look used `pdftotext -layout` output and found only 32 lines matching `^Recommendation \d+` against 148 mentions, because each report *also* carries a multi-column summary table that `-layout` interleaves into unusable soup. The interleaved table was read as the only presentation of the recommendations. The structured chapter was further down the same file.

**QLD — confirmed, and better than NSW's.** Table 2.1 in the 2025-26 report ("Implementation status of Board recommendations, by financial year, 2016-2025") is a *running cumulative table the Board republishes and updates every year*, broken down per report-year with both government-response status (accepted/accepted in principle/accepted in part/noted) and implementation status (completed/in progress/not commenced), total n=84. Cross-checked against Figure 2.2 in the 2023-24 report, which shows the same per-year splits as they stood two years earlier — confirms it's a maintained series, not a one-off. No per-recommendation extraction needed for QLD jurisdiction-level findings. Saved to `extracted/scorecards/QLD_cumulative_scorecard.json`.

**SA — no aggregate scorecard, per-recommendation extraction required.** Checked the most recent available year (2024-2025): DV recommendations are scattered as individual inquest-level "Response to Recommendations" sections inside a general coronial annual report covering all death types (snorkelling accidents, etc., not just DV), each with its own numbered recommendations and agency responses. There is no table that rolls these up by DV-specific implementation status. Confirms the inventory note above — extraction will need to locate and hand-extract the DV subsection(s) per year, no shortcut available.

**WA — no table, but low-effort regardless.** The 2023 implementation report (direct follow-up to the 2022 FDV-and-suicide investigation) is structured as per-recommendation narrative, not a summary table — but it only covers 9 recommendations total, so manual/row-level extraction here is trivial and was always going to be needed at this volume.

**Net effect on the two-week plan:** all four Tier 1 jurisdictions now have structured data ready for site-building. QLD's maintained cumulative table is still the strongest aggregate in the set; NSW is the largest per-recommendation dataset (122 recommendations, 2011-2019) and the only one where the reviewing body publishes its own implementation verdict *alongside* the government's, which makes NSW the one jurisdiction where the two can be shown against each other.

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

## NSW per-recommendation extraction — complete (2026-11-04)

`scripts/extract_nsw.py` → `extracted/recommendations/NSW_{2015-2017,2017-2019,2019-2021}.json`
and the site projection `data/nsw-recommendations.json`. **125 rows / 122 top-level
recommendations** (three of the 2017-19 recommendations are split into lettered sub-parts).

Each file is named for the report that *carries* the status chapter; `report_period` on each
row is the round the recommendation was *made* in:

| Status chapter in | Covers round | Top-level recs | Status fields published |
|---|---|---|---|
| 2015-2017 report | 2011-2012 | 14 | response + prose update (2017) |
| 2015-2017 report | 2012-2013 | 23 | response + prose update (2017) |
| 2015-2017 report | 2013-2015 | 15 | response + prose update (2017) |
| 2017-2019 report | 2015-2017 | 36 | response (2018) + labelled update (2019) |
| 2019-2021 report | 2017-2019 | 34 | response (2020) + labelled update (2021) |

**Checks that passed.** Every chapter's row count matches the number of recommendations that
chapter states it is reporting on (14/23/15/36/34), with no gaps or duplicates in the
numbering. The five rounds sum to exactly **122 top-level recommendations, matching Table 7.2's
own n=122** — an independent check, since that total comes from the Team's aggregate and the
rows come from five separate chapters. All 125 rows' recorded source line points at a real
`Recommendation …` header. No row's text is truncated (min 83, median 356, max 2223 chars).

**What those checks could not have caught.** The 122 match verifies *count and numbering*, not
that each recommendation's text is correctly segmented — a block that swallowed a neighbour's
trailing sentence would still count as one. The line-alignment check confirms the header, not
the body. Both were spot-checked by hand against the PDF for one row per status value, which is
5 of 125.

**Status is deliberately incomplete.** 69 of 125 rows get their status from a labelled
`Update:` field whose value is a short controlled phrase — those are reliable. 50 rows (every
row sourced from the 2015-2017 report) have the update written as free prose instead, and those
are left `unclear` with the prose carried in `source_quote` for a later coding pass. They are
not guessed: keyword-matching the prose had 2013-15 Recommendation 4 coming out "implemented"
off the phrase "which was completed in 2017", in a paragraph that also says "no formal response
has been received from NSW Health" and "component c) is in progress". Every row carries
`status_basis` naming which of these it came from, so the uncoded 50 can be found and the
reliable 69 can be counted on their own.

**Gaps in NSW itself, not in the extraction.**
- The **2021-2023 report publishes no recommendations and no status chapter** — confirmed
  against its contents page, it is a data-only report (166pp vs 298pp). So the most recent
  government position on any NSW recommendation dates from **2021**, and the 2019-21 and
  2021-23 rounds have no published status at all.
- The **2010-2011 report makes no numbered recommendations** — it is a 44-page establishment
  report describing the Team's future recommendation function. This is why the 122 sums.
- The 2019-21 report heads its recommendation 27.2 **"RECOMMENDATION 27.1"**, duplicating the
  previous heading. The recommendation's own number in its body text is treated as
  authoritative and the clash is recorded in `heading_discrepancy` on that row.
- Recommendation 7 of the 2015-17 round has sub-parts 7.2 and 7.3 that are referred to in the
  implementation detail but never restated as headed recommendations, so no text exists to
  extract for them.

**Which field decides the status.** Where a labelled `Update:` exists it outranks the
Whole of Government response, because it is later and is an explicit implementation
assessment where the response only records whether the recommendation was accepted. Reading
the refusal as final was wrong in both directions: 2015-17 Recommendation 1.1 was refused in
2018 — *"the NSW Government … does not intend to become a member of Our Watch"* — and the 2019
update against it reads *"Complete. In July 2019, the NSW Government joined Our Watch."*

Those cases are flagged `response_reversed` (2 rows: `NSW-2015-2017-1.1`, `NSW-2015-2017-32.1`),
because a refusal later overtaken by action is the single most useful fact in this dataset for
the purpose the tracker exists for: it is the published evidence that "not supported" is a
position rather than an outcome.

## `repeat_of` populated — NSW, SA, WA (2026-11-04)

`scripts/find_repeats.py` proposes, `scripts/apply_repeats.py` records the verdicts, and every
link was read against both source texts before acceptance. Outputs:
`data/repeat-links.json` (jurisdiction-agnostic) plus the fields on each extracted row.

**Two fields, not one, and deliberately not a three-value "kind" enum.**

- `repeat_of` — a materially identical ask, restated in a later report. **4 links.** This is
  the inertia signal and it has to stay clean enough that counting it is defensible.
- `related_to` — the same measure asked of a new agency, or a later recommendation on the same
  harm. **9 links.** Real, worth showing, and *not* evidence of a recommendation being ignored.

A single `repeat_of` plus a kind of restated/extended/successor was the obvious design and was
rejected: those three values make three different strength claims, and folding the weaker two
into the field anyone will count would inflate the headline number.

### The four repeats

| Later | Repeats | Gap | Basis |
|---|---|---|---|
| `SA-2015-2016-HardingRoots-1` | `SA-2014-2015-Abrahimzadeh-1` | 1 yr | **Verbatim, attributed in the recommendation itself** |
| `SA-2014-2015-Abrahimzadeh-3` | `SA-2012-2013-Robinson-4` | 2 yrs | Text comparison across inquests |
| `NSW-2015-2017-33` | `NSW-2012-2013-9` | 4 yrs | Team statement + cross-citation (footnote 467) |
| `NSW-2017-2019-19` | `NSW-2015-2017-17` | 2 yrs | Team cross-citation (footnote 649) + near-verbatim |

The SA Harding/Roots recommendation is the strongest instance in the corpus: *"I recommend, as
the State Coroner has recommended in the matter of the death of Mrs Zahra Abrahimzadeh, that
all aspects of domestic violence policing be characterised by a sense of curiosity, questioning
and listening. Risk assessment must be actually applied, not merely recited as a mantra."*
Word for word, a different death, and the source states the repetition — no inference needed.

The NSW 2015-17 #17 → 2017-19 #19 chain is the cleanest inertia example: the same interagency
working group on rapid NSW Health/Justice information sharing, status *"Underway"* in 2019 and
*"Underway – expected completion date to be confirmed (estimated early 2022)"* in 2021. As of
the last published word it was never completed.

### Two candidates were demoted after reading, which is why nothing is accepted on a score

- `NSW-2017-2019-11` ↔ `NSW-2015-2017-5.1` looked like a repeat and is not. The earlier asked
  the Attorney General to review whether the s37 strangulation offence worked; the government
  records the simplified offence in the Crimes Legislation Amendment Act 2018 as made in
  response to it. The later asks for *judicial education* on non-fatal strangulation — a
  different ask on the same subject.
- `NSW-2017-2019-33` ↔ `NSW-2011-2012-1` likewise. The 2011-12 recommendation asked that the
  s101B definition of a 'domestic violence death' be **broadened** to cover third parties, and
  the government records it *"completed and implemented by amendments to the Coroners Act 2009
  (NSW) in 2013"*. The 2017-19 recommendation asks that the relationship reference be
  **omitted entirely** — it goes further than the first rather than repeating it. Still a good
  finding (a fix made, then found insufficient), but not inertia.

12 further similarity candidates were read and rejected as same-theme/different-ask; all are
recorded with reasons in `extracted/repeat_adjudication.json` so the reading is not redone and
an absent link is not mistaken for nobody having looked.

### WA produced no repeats, against expectation

`docs/scope.md` predicted WA would be the best place in the country to find a recommendation
re-made — three recommendation sets over eleven years. It found none, and the reason is
structural rather than a limit of the method: WA's three documents are discrete investigations
(violence restraining orders 2015, FDV and suicide 2022, a review of 237 fatalities 2026), not
a standing annual cycle that re-reports on its own back catalogue the way NSW's does. There is
no mechanism by which a WA recommendation would be formally restated. One same-instrument link
is recorded as `related_to`.

**What this pass could not have caught.** Candidates come from IDF-weighted cosine similarity
at a 0.22 threshold, cross-period only, plus the reports' own cross-references. A
recommendation re-made in substantially different language, with no citation linking it, would
be missed — and NSW is the only jurisdiction with a second signal (the Team's footnotes) to
catch that. So WA's nil result and SA's two are weaker evidence than NSW's. The threshold is
also unvalidated: nothing below 0.22 was read, so the false-negative rate is unknown.

## The 50 prose statuses, coded by hand (2026-11-04)

`scripts/code_prose_statuses.py`. Every NSW row now carries a status; nothing is left
uncoded. The 50 are the 2011-12, 2012-13 and 2013-15 rounds as reported on in the 2015-17
report, which wrote its updates as narrative rather than the labelled `Update:` field the
later reports use.

**Pipeline order now matters in three steps**, because each rebuild clears what the next
step adds:

```
python3 scripts/extract_nsw.py          # rebuilds from the PDFs; clears statuses and links
python3 scripts/code_prose_statuses.py  # the 50 hand verdicts
python3 scripts/apply_repeats.py        # repeat_of / related_to, then writes data/
```

`code_prose_statuses.py` refuses to run if a row's basis is not `prose update, not coded` —
so if the extraction changes under it, it stops rather than overwriting a status that was
derived some other way.

**The rule applied, uniformly.** `implemented` where the words state an action was taken or
completed; `in progress` where action is underway or committed with no completion stated;
`not started` where nothing was done or the approached body never engaged; `rejected` where
it was considered and declined; `superseded` where the government says it was reframed as
another recommendation; `unclear` where the words describe adjacent or pre-existing activity
without establishing that *this* ask was acted on.

That last category is doing real work and is not a shrug. Four of the five remaining
`unclear` rows are the agency offering something that already existed in place of what was
asked — long-standing optional interpreter courses instead of a mandatory induction unit; a
link to the Elder Abuse Helpline instead of the Seniors Card module; existing police course
sessions instead of the review and revision of training materials. Coding those `implemented`
would credit the government for work it never claimed to do.

| Verdict | Rows |
|---|---:|
| implemented | 26 |
| in progress | 15 |
| unclear | 5 |
| not started | 2 |
| rejected | 1 |
| superseded | 1 |

Two rows have no update of their own and take their status from another row because the
report says to ("See above"; "See update above from FACS in relation to Recommendation 8 of
the 2013/15 Report"). Both are marked in their note.

### NSW complete, and it validates against the Team's own verdict

| | Government's own account (125 rows) | The Team (Table 7.2, 122 recs) |
|---|---:|---:|
| Implemented | 45 | 49 |
| In progress / partially implemented | 61 | 48 |
| Not started, rejected / not implemented | 12 | 10 |
| Unclear | 6 | — |
| Superseded | 1 | — |
| Alternative practice approach adopted | — | 15 |

**The two ends agree closely** — implemented 45 against 49, and refused-or-never-started 12
against 10 — which is a real check, because the Team's figures come from its own aggregate
table and these come from reading five chapters of government responses.

**The middle diverges for a known reason.** The Team has a category this project's vocabulary
does not: *alternative practice approach adopted* (15 recommendations). Several rows coded
here as `implemented` with a note, or as `unclear`, are exactly that case. Adding a sixth
status value was considered and rejected — it would have to propagate to the SA and WA
datasets and to every consumer, for a distinction the `status_note` already carries. The
consequence is that `in progress` here is broader than the Team's "partially implemented".

**What this pass cannot do.** These are the *government's* accounts of its own compliance,
nearly all dated mid-2017, and several are an agency asserting that pre-existing activity
satisfies the ask. `implemented` means the agency said it did the thing — not that anyone
verified it. Where the Team disagreed, Table 7.2 is the place that records it. The two are
different measurements of the same 122 recommendations and must not be summed.

Also note the unit difference in the comparison above: 125 rows against 122 recommendations,
because three 2017-19 recommendations are split into lettered sub-parts.

### Two more extraction bugs found while reading

Both were silent, and both passed the 122 checksum, because a count check cannot see what is
*inside* a field:

- The last block in a chapter has no following header to terminate it, so its unlabelled
  prose update ran to the end of the document. 2011-12 Recommendation 14 had swallowed
  Appendix A, the homicide figures and the back cover — 69,003 characters. Fixed with explicit
  block terminators (`Appendix X`, `CHAPTER n`, `FIGURE/TABLE n:`).
- The same for a `<period> DVDRT Report` heading, which starts the next round's section:
  2012-13 Recommendation 23 had the 2011-12 section's introduction appended to its status.

The length check added afterwards tests for swallowed document structure rather than length
alone, because a five-part recommendation with a full multi-part agency response legitimately
runs to about 7,400 characters.
