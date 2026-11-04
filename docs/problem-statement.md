# Problem statement — DV Death Review Recommendation Tracker

Drafted 4 Nov 2026. Every figure here is sourced, and the limits of each source are
stated with it. Where something could not be verified it says so rather than rounding
to a confident number.

## The short version

**The deaths are counted. Nothing counts whether anything was done about why.**

Australia has a national, per-state, consistently defined, annually published count of
domestic homicide. It is the Australian Institute of Criminology's National Homicide
Monitoring Program, it covers all eight jurisdictions including the two with no death
review body at all, and it is good. **We should use it, not rebuild it.**

What does not exist anywhere is a register of what the death review bodies *recommended*
after those deaths, and whether governments did it. Those recommendations are written for
publication, name institutions rather than people, and sit in PDFs nobody aggregates. For
NSW alone there are **122 recommendations made between 2011 and 2019**, and the most recent
published government position on any of them is from **2021**.

That gap is the product.

## 1. How many people die

### National, and by state — this already exists

AIC National Homicide Monitoring Program, *Homicide in Australia 2024–25* (Statistical
Report 58), covering 1 July 2024 – 30 June 2025:

- **279 homicide victims** nationally.
- **90 domestic homicide incidents — 34% of all homicide incidents.** A third of the people
  killed in Australia are killed by family.
- **46 intimate partner homicide deaths**, down 16 on the previous year, the third-lowest
  rate recorded.
- Domestic homicide rate **0.33 per 100,000**.

Domestic homicide incidents by jurisdiction:

| Jurisdiction | 2024–25 | 2023–24 |
|---|---:|---:|
| NSW | 23 | 26 |
| VIC | 15 | 13 |
| QLD | 22 | 15 |
| WA  | 14 | 16 |
| SA  |  4 |  8 |
| TAS |  1 |  3 |
| ACT |  0 |  3 |
| NT  | 11 |  4 |
| **Australia** | **90** | **88** |

Both columns sum to their stated totals, which is the one internal check available on a
figure read from a summary rather than the row data.

2023–24 also breaks domestic homicide down by type: intimate partner 55, parricide 18,
filicide 6, other family 6, siblicide 3. And the rate spread is the finding the national
average hides — **0.19 per 100,000 in Victoria to 1.58 in the Northern Territory, an
eight-fold difference.**

### "Running total" — the honest answer

There is no official running count, and this is the one real gap in the death data.

*Homicide in Australia 2024–25* was published in **February 2026** and its data stops at
**30 June 2025**. So today, in November 2026, the most recent official national count
covers a year that ended **16 months ago**, and the next release is not due until around
February 2027. Nobody official can tell you how many women were killed last month.

Live tallies do exist outside government — volunteer-maintained counts such as Counting
Dead Women. **I have not verified any of them and this document states no figure from
them.** They count a different thing (all violent deaths of women, not domestic homicide
specifically) and they are not official. Using one is a decision with a trade-off, and
it is listed as an open question below rather than assumed.

### What the state review bodies publish, and why it cannot be a national total

Each body publishes its own count, on its own definition, over its own period:

| Jurisdiction | Period | Published count | Unit |
|---|---|---|---|
| NSW (DVDRT) | Jul 2000 – Jun 2022, 22 yrs | **550 DV-context homicide deaths** of 1,832 homicides (30%) — 331 female, 219 male | deceased persons |
| QLD (DFVDRAB) | Jul 2019 – Jun 2025, 6 yrs | **114 DFV-related homicide events**, 134 deaths (124 victims + 10 offenders) | events *and* persons |
| WA (Ombudsman) | Jul 2012 – Jun 2025, 13 yrs | **237 FDV fatalities** notified, 217 offenders | fatalities notified |
| SA (State Coroner) | — | **nothing since 2017–18** | — |

These cannot be added together or compared. The periods differ (6 vs 13 vs 22 years), the
units differ (events vs deceased persons vs fatalities notified), the definitions differ
(DV-context vs DFV-related vs FDV), and half the country is missing. Anyone presenting a
national figure built by summing these is presenting an artefact.

NSW's internal breakdown of its 550: intimate partner 308, filicide 96, relative/kin 91,
other DV 55. The report's own chapters quote slightly different denominators for the same
groups (IPV as 308, 300 and 286; relative/kin as 91 and 94) because each table uses the
subset for which that variable was known. Not an error, but it means a number must be
quoted with its table, never on its own.

**They do cross-check against AIC, though, and that matters.** NSW's 550 over 22 years is
~25 deaths a year against AIC's 23 and 26 incidents for NSW; QLD's 134 over 6 years is ~22
against AIC's 22 and 15; WA's 237 over 13 years is ~18 against AIC's 14 and 16. Units are
not identical — incidents are not deceased persons — so this is not a reconciliation. But
two independent data systems landing in the same place in three jurisdictions is good
evidence that the AIC series is sound enough to build a public-facing counter on.

### SA has stopped reporting, and that is a finding

South Australia has no standalone DV death review report; recommendations sit inside the
general State Coroner's annual report. Across the 17 SA reports in this corpus, the word
"homicide" appears **zero times in every report from 2018–19 onward** — while "coroner"
appears 76–129 times in those same files, so this is the reports' content, not a failed
text extraction. The last SA report with substantial DV content was **2017–18**.

Limit of that check: it covers the State Coroner's *annual reports*, the only SA series
collected here. SA publishes individual inquest findings separately and those are not in
this corpus, so the claim is "SA's annual reporting carries no DV death count", not "SA
reviews nothing".

### Two jurisdictions review nothing, and still bury people

- **Tasmania** — the only state or territory with no domestic violence death review team.
  Family-violence deaths are examined only by a coroner, and those investigations are often
  not publicly released. A Coroners Act review was underway as of July 2026.
- **ACT** — has no standing death review team. The Domestic Violence Prevention Council
  has done review work and the government has been urged to establish a mechanism.
  **Current status not verified** — `docs/scope.md` rests this on a 2016 AHRC call, which
  is ten years old and should not be cited as current. Needs checking before publication.
- **VIC** — the Family Violence Reform Implementation Monitor tracked all 227 Royal
  Commission recommendations annually, then closed 31 December 2022. Monitoring moved to
  the Department of Premier and Cabinet and is no longer independent or annual.

AIC still counts these deaths: Tasmania 1 and 3, the ACT 0 and 3 across the two most recent
years. Small numbers, and nobody is asking why any of them happened.

## 2. What happened to the recommendations — the actual gap

NSW is now fully extracted and it is the proof of concept.

**122 recommendations, 2011 to 2019.** Reconciled against the Team's own Table 7.2 total of
122, arrived at independently from five separate report chapters. Of those:

- **19 implemented, 46 in progress, 6 not started** — the 71 whose status comes from a
  labelled government field and can be relied on.
- **50 have no usable status.** Their updates are written as free prose and are deliberately
  left uncoded rather than guessed; keyword-matching that prose produced a false
  "implemented" on a recommendation whose update says *"no formal response has been
  received"*. Every row records which basis it came from.
- **3 refused outright.**
- **9 refused or never started**, seven of them sitting with courts and justice — three
  *"pending identification of resources"*, and start dates that have since passed.
- **The most recent government word on any of it is 2021.** The 2021–23 NSW report publishes
  no recommendations and no status chapter at all, so the 2019–21 and 2021–23 rounds have
  never been reported on.

**And two were refused and then quietly done anyway.** Recommendation 1.1 was refused in
2018 — *"the NSW Government … does not intend to become a member of Our Watch"* — and the
2019 update against it reads *"Complete. In July 2019, the NSW Government joined Our
Watch."*

That is the single most useful fact in the dataset. It is published, government-sourced
proof that **"not supported" is a position, not an outcome.** It is the answer to anyone who
says writing to a minister changes nothing.

## 3. The path to action

Three steps, in the order a stranger meets them:

1. **The number, for their state.** 90 domestic homicides last year; 23 in NSW. One third of
   everyone killed in Australia, killed by family. Sourced to the AIC, per state, with the
   eight-fold rate spread visible.
2. **These deaths were reviewed, and recommendations were written.** Here are the
   recommendations for your state, what the government said, and what it then did — or
   didn't. Refused and stalled items surfaced first, each linked to the page of the PDF it
   came from so the claim is checkable.
3. **One click to act.** A prefabricated email to the named minister about a specific
   stalled recommendation, quoting the recommendation and the government's own words about
   it. Already built for WA (`wa-action.html`, `data/wa-ministers.json`); NSW now has the
   recommendation data and needs the minister mapping.

The design claim is that specificity is what converts. Not "domestic violence is terrible"
but "Recommendation 18 of the 2017–19 report, directed at your Attorney General, has been
'not started — pending identification of resources' since 2021."

## 4. What this is not

- Not a death counter. The AIC already does that better than this project could, and the
  site should link to it and cite it, not reproduce it.
- Not victim-level detail. Nothing beyond what the source reports already published.
- Not a judge scorecard. That was the original idea; judge-level sentencing data is not
  published in Australia and the idea carried real defamation exposure. See `scope.md`.

## 5. Open questions — these need a decision, not an assumption

1. **Live counter, or official only?** An official-only counter is accurate and 16 months
   stale. A volunteer tally is current, unofficial, and counts a different population.
   Possible answer: lead with the AIC figure and show "and X since the last official count"
   from a clearly attributed secondary source. Needs the source verified first.
2. **Does the site cover all eight jurisdictions, or only the four with recommendations?**
   Covering all eight makes "two jurisdictions review nothing" a visible finding rather than
   a footnote, at the cost of several states having a death count and an empty
   recommendations table.
3. **The 50 uncoded NSW statuses** need a reading pass to become usable. They are the
   2011–2015 rounds, so the oldest and the most likely to show inertia — which is exactly
   the signal the tracker exists to expose.
4. **ACT's current review status** must be checked before anything is published.
5. **`repeat_of` is unpopulated across every jurisdiction.** It is the field that exposes the
   same recommendation being made three times in a decade, and it is the strongest argument
   available. It needs a matching pass.

## Sources

- AIC, *Homicide in Australia 2024–25*, Statistical Report 58, published Feb 2026 —
  https://www.aic.gov.au/publications/sr/sr58
- AIC, *Homicide in Australia 2023–24*, Statistical Report 52 —
  https://www.aic.gov.au/sites/default/files/2025-03/sr52_homicide_in_australia_2023-24.pdf
- NSW DVDRT Report 2021–2023, ch. 2 (figures 2.1–2.3) — `raw-reports/NSW/2021-2023.pdf`
- NSW DVDRT Reports 2015–2017, 2017–2019, 2019–2021 — recommendation status chapters;
  extraction and its limits in `docs/inventory.md`
- QLD DFVDRAB Annual Report 2025–26, Table 3.5 — `raw-reports/QLD/`
- Ombudsman WA, *A Review of Family and Domestic Violence in Western Australia* (2026), §5.4
- SA State Coroner annual reports 2005–06 to 2024–25 — `text/SA_*.txt`
