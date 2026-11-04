#!/usr/bin/env python3
"""
Writes the hand-adjudicated recommendation links into the NSW extraction.

Every link below was read against both source texts before being accepted.
`scripts/find_repeats.py` proposed candidates from two signals (the Team's own
cross-report footnote citations, and IDF-weighted text similarity); this file
records the verdicts. Of 15 similarity candidates and 23 citation groups, 8
links survived reading and 7 similarity pairs were rejected as same-theme,
different-ask.

TWO FIELDS, NOT A "KIND" ENUM. The obvious move was one `repeat_of` plus a
three-value kind (restated / extended / successor). That was rejected on the
grounds that the three values make three different strength claims, and the
only claim the tracker actually rests on is the first: "this was recommended
again and still is not done". Mixing the weaker two into the same field would
inflate any count built on it. So:

  repeat_of   - ONLY a materially identical ask, restated in a later report.
                This is the inertia signal and it has to stay clean enough that
                counting it is defensible.
  related_to  - same measure asked of a new agency, or a later recommendation
                on the same harm. Real and worth showing, but it is NOT
                evidence of a recommendation being ignored.

The rejected candidates are recorded too, so the next person does not redo the
reading or assume an absent link means nobody looked.
"""
import json, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECS = ROOT / "extracted" / "recommendations"

# later id -> (earlier id, basis, note)
REPEAT_OF = {
    "NSW-2017-2019-19": (
        "NSW-2015-2017-17",
        "Team cross-citation (2019-21 report, footnote 649) and near-verbatim text",
        "Both ask for an interagency working group to rapidly share information between NSW "
        "Health and Justice about Community Treatment Orders. The 2017-19 version widens the "
        "addressee from NSW Health to the NSW Government and the cohort from CTO clients to "
        "mental health consumers presenting a serious risk, but the ask is the same mechanism.",
    ),
    # SA's cleanest case in the whole corpus: the Coroner re-made the
    # recommendation word for word and named the earlier inquest while doing it.
    "SA-2015-2016-HardingRoots-1": (
        "SA-2014-2015-Abrahimzadeh-1",
        "Verbatim restatement, attributed by the Coroner in the recommendation itself",
        "Word-for-word the same recommendation, re-made in a later inquest: 'I recommend, as the "
        "State Coroner has recommended in the matter of the death of Mrs Zahra Abrahimzadeh, that "
        "all aspects of domestic violence policing be characterised by a sense of curiosity, "
        "questioning and listening. Risk assessment must be actually applied, not merely recited "
        "as a mantra.' No inference required - the source states the repetition.",
    ),
    "SA-2014-2015-Abrahimzadeh-3": (
        "SA-2012-2013-Robinson-4",
        "Text comparison across inquests",
        "The same ask: domestic violence calls to the SAPOL call centre must be handled by trained "
        "sworn police officers rather than civilian call-centre staff. Robinson put it as a "
        "prohibition on administrative officers making cold calls to victims; Abrahimzadeh put it "
        "as a positive requirement that sworn officers with risk-assessment training take the "
        "calls.",
    ),
    "NSW-2015-2017-33": (
        "NSW-2012-2013-9",
        "Team statement in the 2015-17 report plus cross-citation (2019-21 report, footnote 467)",
        "Both address children who survive a domestic homicide and whose carers will not engage "
        "with services - the closing clause is near-verbatim across the two. The Team wrote in "
        "the 2015-17 report that 'despite its earlier recommendations, many of the same issues "
        "continue to arise in respect of the response to surviving children of homicide'.",
    ),
}

# id -> list of (other id, note). Deliberately not repeat_of.
RELATED_TO = {
    "NSW-2013-2015-14": [(
        "NSW-2012-2013-4",
        "Same measure, new target: a quick-close button and browser-history guidance on domestic "
        "violence web pages, asked of the NSW Police Force in 2012-13 and of the federal family "
        "courts in 2013-15.",
    )],
    "NSW-2012-2013-5": [(
        "NSW-2011-2012-4",
        "Same measure, new circumstance: amend NSW Police standard operating procedures to "
        "require a COPS event be created - for child-custody advice in 2011-12, for mental "
        "health detention assessments and directions in 2012-13.",
    )],
    "NSW-2015-2017-9": [(
        "NSW-2012-2013-16",
        "Same measure, new profession: equip health practitioners to recognise domestic violence "
        "and refer on - assisted reproductive services in 2012-13, primary care in 2015-17.",
    )],
    "NSW-2013-2015-10": [(
        "NSW-2012-2013-3",
        "Carried forward rather than restated. The 2013-15 report asks Justice to keep informing "
        "DVSAT evaluations, and in its commentary the Team 'reiterates the need to consider "
        "Recommendation 3 from the 2012/13 Report when evaluating the use of the DVSAT in NSW' - "
        "that earlier recommendation having asked for two specific questions to be added.",
    )],
    "NSW-2017-2019-33": [(
        "NSW-2011-2012-1",
        "The earlier recommendation was implemented and then found insufficient - not the same "
        "ask twice. In 2011-12 the Team asked that s101B(1) of the Coroners Act 2009 (NSW) be "
        "broadened so a 'domestic violence death' covered deaths caused by someone in a domestic "
        "relationship with the deceased and deaths of third parties to such a relationship; the "
        "government records that as 'completed and implemented by amendments to the Coroners Act "
        "2009 (NSW) in 2013'. In 2017-19 the Team went further and asked that the definition "
        "become simply 'a death which occurs in the context of domestic violence', with the "
        "reference to relationship omitted altogether. As of the last published update that "
        "second change had an expected completion date of end-2021 and no confirmation.",
    )],
    "SA-2014-2015-Abrahimzadeh-3": [(
        "SA-2012-2013-Robinson-3",
        "Adjacent ask in the same inquest set: Robinson-3 asks that call-centre staff and officers "
        "receive regular training on responding to domestic violence disclosures, where "
        "Abrahimzadeh-3 asks who should take the calls at all.",
    )],
    "SA-2017-2018-McKenzie-9": [(
        "SA-2011-2012-Hayward-Durance-1",
        "Same problem, different instrument: bail in alleged domestic violence matters. The 2011-12 "
        "recommendation sought an amendment to the Bail Act 1985 so only a Court could grant bail; "
        "the 2017-18 one seeks education of police prosecutors on their existing duties under "
        "s10A. Not the same ask.",
    )],
    "WA-2026-2": [(
        "WA-2015-54",
        "Same instrument, different subject: review the barriers then publish an action plan. In "
        "2015 the subject was implementation of family and domestic violence policy and practice "
        "guidance; in 2026 it was FDVRT compliance with record keeping, risk assessment and "
        "escalation to Multi-Agency Case Management.",
    )],
    "NSW-2017-2019-11": [(
        "NSW-2015-2017-5.1",
        "Successor on the same harm, not a restatement. The 2015-17 recommendation asked the "
        "Attorney General to review whether the s37 strangulation offence was working; the "
        "government records that the simplified offence in the Crimes Legislation Amendment Act "
        "2018 was made in response to it. The 2017-19 recommendation then asks for judicial "
        "education on non-fatal strangulation - a different ask on the same subject.",
    )],
}

# Read and rejected, so nobody repeats the work or reads the absence as an oversight.
REJECTED = [
    ("NSW-2013-2015-5",   "NSW-2015-2017-16.1", 0.332, "Both mental health/AOD. One asks for an information-sharing mechanism between the Team and NSW Health; the other for a literature review and model of practice. Different asks."),
    ("NSW-2012-2013-22",  "NSW-2015-2017-18",   0.322, "Both elder abuse. One asks for usage reporting on the Elder Abuse Helpline; the other for NSW Police to update its SOPs and training. Different asks."),
    ("NSW-2011-2012-9",   "NSW-2012-2013-22",   0.289, "Both concern the elder abuse helpline, but one is about using case reviews to build training resources and the other about reporting on helpline use."),
    ("NSW-2011-2012-14",  "NSW-2013-2015-12",   0.286, "Both Housing NSW. One reminds staff to refer tenants to DV services; the other asks for a z-card on head-tenant rights."),
    ("NSW-2012-2013-18",  "NSW-2015-2017-23.1", 0.280, "Both Aboriginal-focused and otherwise unrelated: a parenting program for Aboriginal fathers versus court-attendance support for Aboriginal women."),
    ("NSW-2015-2017-33",  "NSW-2017-2019-6",    0.272, "Both about people who do not engage with services, but different populations and mechanisms - homicide secondary victims versus repeat Central Referral Point referrals."),
    ("NSW-2013-2015-5",   "NSW-2017-2019-22",   0.255, "Both mental health/AOD. One is an information-sharing mechanism for the Team; the other strengthens GP referral pathways."),
    ("NSW-2011-2012-14",  "NSW-2013-2015-11",   0.232, "Both Housing NSW. One is a staff reminder; the other an information bulletin on tenant rights developed with police."),
    ("NSW-2015-2017-16.1","NSW-2017-2019-21",   0.226, "Both the AOD/DV workforce, but one asks for a model of practice and the other for evidence-based training. Same problem recurring; not the same ask."),
    ("NSW-2012-2013-16",  "NSW-2015-2017-9",    0.224, "Accepted as related_to rather than rejected - see RELATED_TO."),
    ("WA-2015-54",         "WA-2022-5",          0.300, "Both say 'conduct a review', of unrelated things: barriers to implementing FDV policy and practice guidance, versus data on FDV in duty interactions concerning older children and adolescents."),
    ("WA-2015-40",         "WA-2022-4",          0.222, "Share only the vocabulary of duty interactions and departmental business. Different asks."),
]

# WA produced no repeat_of at this threshold, which is worth recording because
# docs/scope.md predicted the opposite - three recommendation sets over 11 years
# looked like the best place in the country to find a recommendation re-made.
# The reason it does not is structural: WA's three documents are separate
# investigations (violence restraining orders in 2015, FDV and suicide in 2022,
# a review of 237 fatalities in 2026), not a standing annual recommendation
# cycle re-reporting on its own back catalogue the way NSW's is.
NOTES = {
    "WA": "No repeat_of links found at similarity >= 0.22 across the three report periods. One "
          "same-instrument link recorded as related_to. WA's reports are discrete investigations "
          "rather than a recurring cycle, so there is no mechanism by which a recommendation "
          "would be formally re-made.",
    "SA": "Two repeat_of links, one of them verbatim and attributed by the Coroner. SA's "
          "recommendations are per-inquest, so a repeat here means a different death produced the "
          "same finding - arguably the strongest form of this signal available.",
    "NSW": "Two repeat_of links from 15 similarity candidates and 23 Team cross-citation groups. "
           "Two further candidates were demoted to related_to only after reading the full texts.",
}

def main():
    files = sorted(RECS.glob("*.json"))
    index = {}
    for f in files:
        for r in json.load(open(f)):
            index[r["id"]] = True

    missing = [i for i in list(REPEAT_OF) + [v[0] for v in REPEAT_OF.values()] if i not in index]
    missing += [i for i in RELATED_TO for i in [i]] and [
        i for k, v in RELATED_TO.items() for i in [k] + [x[0] for x in v] if i not in index]
    if missing:
        raise SystemExit(f"refusing to write - ids not found: {sorted(set(missing))}")

    touched = 0
    for f in files:
        rows = json.load(open(f))
        for r in rows:
            rid = r["id"]
            if rid in REPEAT_OF:
                earlier, basis, note = REPEAT_OF[rid]
                r["repeat_of"] = earlier
                r["repeat_basis"] = basis
                r["repeat_note"] = note
                touched += 1
            else:
                # Cleared explicitly, not setdefault: this script must be a pure
                # function of the tables above, so that demoting a link here
                # actually removes it from the data. setdefault preserved a
                # repeat_of from an earlier run after it had been demoted to
                # related_to, leaving the same pair asserted in both fields.
                r["repeat_of"] = None
                r["repeat_basis"] = None
                r["repeat_note"] = None
            r["related_to"] = [{"id": i, "note": n} for i, n in RELATED_TO.get(rid, [])]
            if r["related_to"]:
                touched += 1
        f.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    (ROOT / "extracted" / "repeat_adjudication.json").write_text(json.dumps({
        "method": "candidates from scripts/find_repeats.py; every link read against both "
                  "source texts before acceptance",
        "repeat_of": {k: {"earlier": v[0], "basis": v[1], "note": v[2]} for k, v in REPEAT_OF.items()},
        "related_to": {k: [{"id": i, "note": n} for i, n in v] for k, v in RELATED_TO.items()},
        "rejected": [{"a": a, "b": b, "similarity": s, "reason": why} for a, b, s, why in REJECTED],
        "per_jurisdiction_notes": NOTES,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    rows = []
    for f in files:
        rows += json.load(open(f))

    # The NSW site projection. WA and SA already have their own data files in a
    # different shape (data/wa-recommendations.json is what wa-action.html
    # reads), so they are deliberately not regenerated here -- that would break
    # a working page to no benefit.
    proj = [{
        "id": r["id"],
        "report": r["report_title"],
        "report_period": r["report_period"],
        "recommendation_number": r["recommendation_number"],
        "recommendation_part": r.get("recommendation_part"),
        "text": r["recommendation_text"],
        "target_agency": r["target_agency"],
        "status": r["status"],
        "status_as_of": r["status_as_of"],
        "status_basis": r.get("status_basis"),
        "status_quote": r.get("status_quote"),
        "status_note": r.get("status_note"),
        "response_reversed": r.get("response_reversed", False),
        "govt_response": r.get("govt_response"),
        "govt_update": r.get("govt_update"),
        "repeat_of": r.get("repeat_of"),
        "repeat_note": r.get("repeat_note"),
        "related_to": r.get("related_to", []),
        "page_ref": r["page_ref"],
        "report_url": r["report_url"],
    } for r in rows if r["jurisdiction"] == "NSW"]
    data = ROOT / "data" / "nsw-recommendations.json"
    data.write_text(json.dumps(proj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"site data -> {data.relative_to(ROOT)} ({len(proj)} NSW rows)")

    # Jurisdiction-agnostic link file, so the site can show the repeat signal
    # without every jurisdiction's rows having to share one schema first.
    links = ROOT / "data" / "repeat-links.json"
    links.write_text(json.dumps({
        "repeat_of": [
            {"later": r["id"], "earlier": r["repeat_of"], "jurisdiction": r["jurisdiction"],
             "later_period": r["report_period"], "basis": r.get("repeat_basis"),
             "note": r.get("repeat_note")}
            for r in rows if r.get("repeat_of")
        ],
        "related_to": [
            {"from": r["id"], "to": l["id"], "jurisdiction": r["jurisdiction"], "note": l["note"]}
            for r in rows for l in r.get("related_to", [])
        ],
        "notes": NOTES,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"link file -> {links.relative_to(ROOT)}")

    print(f"repeat_of written: {len(REPEAT_OF)}")
    print(f"related_to written: {sum(len(v) for v in RELATED_TO.values())} links on {len(RELATED_TO)} rows")
    print(f"rejected candidates recorded: {len(REJECTED)}")
    print(f"rows updated: {touched}")

if __name__ == "__main__":
    main()
