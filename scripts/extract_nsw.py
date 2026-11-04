#!/usr/bin/env python3
"""
NSW DVDRT: pull per-recommendation government status out of the "response and
update" chapters.

NSW works differently from SA and WA. Each biennial report restates the
PREVIOUS report's recommendations and prints, against each one, the Whole of
Government response and (in later reports) a follow-up update. That chapter is
the only place a status appears per recommendation -- Chapter 7 of the 2019-21
report publishes implementation counts only (Table 7.2, n=122), so the counts
and these rows are two different measurements and must not be mixed.

The chapter is structured text, so this is a real extraction rather than a
candidate-block pass. Three header styles appear across the years and all
three are matched. A block is kept only if it carries a "Lead agency:" field:
that field appears nowhere else in these reports, so it cleanly separates the
update chapter from the summary tables earlier in each report, which
pdftotext -layout interleaves into unusable multi-column soup.

Counts are checked against each chapter's own stated number of
recommendations. A mismatch is reported, not silently accepted.
"""
import re, json, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "text" / "nsw"
OUT  = ROOT / "extracted" / "recommendations"

# Which report carries the update chapter, and what it says about itself.
SOURCES = {
    "2015-2017": dict(url="coroners.nsw.gov.au/documents/reports/2013-2015_DVDRT_Report.pdf",
                      update_year=None, response_year=2016, covers=None),
    "2017-2019": dict(url="coroners.nsw.gov.au/documents/reports/2017-2019_DVDRT_Report.pdf",
                      update_year=2019, response_year=2018, covers="2015-2017"),
    "2019-2021": dict(url="coroners.nsw.gov.au/documents/reports/2019-2021_DVDRT_Report.pdf",
                      update_year=2021, response_year=2020, covers="2017-2019"),
}

# A recommendation header. The report label is optional -- when absent the
# originating round comes from the most recent "<period> DVDRT Report" heading.
HEADERS = [
    # (number, part, round-a, round-b) -- groups absent in a style are None
    re.compile(r'^\s*RECOMMENDATION\s+(\d+)(?:\.(\d+))?\s*$'),
    re.compile(r'^\s*Recommendation\s+(\d+)(?:\.(\d+))?\s*\((\d{4})[/-](\d{2,4})\s+report\)\s*$', re.I),
    re.compile(r'^\s*Recommendation\s+(\d+)(?:\.(\d+))?\s*$'),
]
# The report prints the recommendation's own number at the head of its text
# ("27.2 That the NSW Government..."). Where that disagrees with the heading it
# is authoritative: the 2019-21 report heads its 27.2 with "RECOMMENDATION 27.1".
BODY_NUM = re.compile(r'^\s*(\d+)\.(\d+)\s+That\b')
ROUND = re.compile(r'^\s*(\d{4})\s*[-/]\s*(\d{2,4})\s+DVDRT Report\s*$')

# Field markers inside a block. Everything before the first of these is the
# recommendation's own text.
F_RESP_INLINE = re.compile(r'^\s*Whole of government response\s*[-–]?\s*(\d{4})?\s*:\s*(.*)$', re.I)
F_RESP_HEAD   = re.compile(r'^\s*Whole of government response\s*[-–]?\s*(\d{4})?\s*$', re.I)
F_RESPONSE    = re.compile(r'^\s*Response:\s*(.*)$', re.I)
F_AGENCY      = re.compile(r'^\s*Lead agency:\s*(.*)$', re.I)
F_UPDATE      = re.compile(r'^\s*Update:\s*(.*)$', re.I)
F_UPD_HEAD    = re.compile(r'^\s*Whole of government (?:update|progress report)\s*[-–]?\s*(\d{4})?\s*$', re.I)
F_DETAILS     = re.compile(r'^\s*Details of implementation:\s*(.*)$', re.I)
F_COMMENT     = re.compile(r'^\s*Whole of government commentary:\s*(.*)$', re.I)
F_OPPS        = re.compile(r'^\s*Opportunities, challenges and/or consequences:\s*(.*)$', re.I)
# The 2015-17 report heads the update with a year and then just writes it out,
# with no "Update:" label to anchor on.
F_AGENCY_UPD  = re.compile(r'^\s*Agency update\s*[-–]?\s*(\d{4})?\s*$', re.I)
MARKERS = [F_RESP_INLINE, F_RESP_HEAD, F_RESPONSE, F_AGENCY, F_UPDATE,
           F_UPD_HEAD, F_DETAILS, F_COMMENT, F_OPPS, F_AGENCY_UPD]

# Page furniture. These sit mid-block and would otherwise land in the text.
FURNITURE = [
    re.compile(r'^\s*\d{1,3}\s*$'),
    re.compile(r'NSW DOMESTIC VIOLENCE DEATH REVIEW TEAM\s*$'),
    re.compile(r'^\s*REPORT\s+\d{4}\s+\d{4}\s'),
    re.compile(r'^\s*\d{1,3}\s+NSW DOMESTIC VIOLENCE'),
    re.compile(r'^\s*0\d\s*$'),
]

# A block normally ends at the next recommendation header. The LAST block in a
# chapter has no such header, so without an explicit terminator its unlabelled
# prose update ran to the end of the document -- 2011-12 Recommendation 14
# swallowed Appendix A, the homicide figures and the back cover, 69,000
# characters of it. These are the headings that start whatever follows the
# status chapter.
BLOCK_END = [
    re.compile(r'^\s*Appendix\s+[A-Z]\b'),
    # A "<period> DVDRT Report" heading starts the next round's section, so it
    # also ends the last block of the previous one -- 2012-13 Recommendation 23
    # had the 2011-12 section's introduction appended to its status update.
    re.compile(r'^\s*\d{4}\s*[-/]\s*\d{2,4}\s+DVDRT Report\s*$'),
    re.compile(r'^\s*(CHAPTER|Chapter)\s+\d+'),
    re.compile(r'^\s*(FIGURE|Figure|TABLE|Table)\s+\d+\s*:'),
]


def block_end(line):
    return any(p.match(line) for p in BLOCK_END)


def furniture(line):
    return any(p.search(line) for p in FURNITURE)

def is_marker(line):
    return any(p.match(line) for p in MARKERS)

def header(line):
    for pat in HEADERS:
        m = pat.match(line)
        if m:
            g = m.groups()
            num  = int(g[0])
            part = int(g[1]) if len(g) > 1 and g[1] else None
            label = None
            if len(g) > 3 and g[2]:
                a, b = g[2], g[3]
                b = b if len(b) == 4 else a[:2] + b
                label = f"{a}-{b}"
            return num, part, label
    return None

def join(lines):
    """Wrapped lines back into paragraphs; blank line separates."""
    paras, cur = [], []
    for l in lines:
        s = l.strip()
        if not s:
            if cur: paras.append(" ".join(cur)); cur = []
        else:
            cur.append(s)
    if cur: paras.append(" ".join(cur))
    txt = "\n".join(paras)
    # Superscript footnote markers glued to sentence ends ("below.761").
    # A letter or bracket must precede the punctuation: footnotes attach to
    # words, never to numbers. Without that guard this ate the sub-part digit
    # off every "27.1 That the..." and collapsed 27.1 and 27.2 into one row.
    txt = re.sub(r'([A-Za-z\)’”][.,;:\)])\d{1,3}(?=\s|$)', r'\1', txt)
    return re.sub(r'\s+\n', '\n', txt).strip()

AGENCY_TAGS = [
    ("police",          ["nsw police", "nswpf", "police"]),
    ("child-protection",["child and family", "family and community", "facs", "child protection",
                         "out-of-home", "children's guardian"]),
    ("corrections",     ["corrective services", "corrections", "parole"]),
    ("courts-justice",  ["judicial", "courts", "legal aid", "director of public prosecutions",
                         "odpp", "attorney general", "justice", "coroner"]),
    ("health",          ["health", "mental health"]),
    ("state-govt",      ["nsw government", "premier", "treasury", "women nsw", "dcj",
                         "communities and justice", "education", "department"]),
]
def tag_agency(text):
    if not text: return ["other"]
    low = text.lower()
    tags = [t for t, needles in AGENCY_TAGS if any(n in low for n in needles)]
    # DCJ absorbs several functions; keep the specific tag when one matched.
    if len(tags) > 1 and "state-govt" in tags:
        tags = [t for t in tags if t != "state-govt"]
    return tags or ["other"]

def norm_status(update, response, labelled):
    """Government's own words -> the project's status vocabulary.

    Two kinds of update appear and they are not equally trustworthy. The
    2017-19 and 2019-21 reports print a labelled "Update:" field whose value is
    a short controlled phrase ("Complete", "Underway - expected...", "Not
    commenced"); that maps cleanly. The 2015-17 report instead writes the
    update as free prose, and prose cannot be reduced to one status by keyword:
    searching it anywhere made 2013-15 Recommendation 4 come out "implemented"
    off the phrase "which was completed in 2017", when the same paragraph says
    "no formal response has been received" and "component c) is in progress".

    So prose updates are deliberately left "unclear" and carried in
    source_quote for a human or LLM coding pass. Refusing to assign a status is
    the honest result; guessing one pollutes every count built on top of it.
    Each row records which basis was used.
    """
    r = (response or "").lower()
    refused = bool(re.search(r'not supported|does not support|declin', r))

    # The labelled update outranks the response: it is later, and it is an
    # explicit implementation assessment where the response only says whether
    # the recommendation was accepted. Reading the refusal as final got two rows
    # wrong in opposite directions -- 2015-17 Recommendation 1.1 was refused in
    # 2018 ("does not intend to become a member of Our Watch") and the 2019
    # update reads "Complete - In July 2019, the NSW Government joined Our
    # Watch". A refusal is a position, not an outcome.
    if labelled and update:
        u = update.lower().strip()
        # Anchored at the start of the field: it is a controlled value, not prose.
        for pat, st in [
            (r'(complete|implemented|delivered|finalised)', "implemented"),
            (r'(not started|not commenc|no action|yet to commence|nil)', "not started"),
            (r'(underway|ongoing|in progress|continu|partial|progress|commenc)', "in progress"),
            (r'(supersed|no longer|overtaken)',               "superseded"),
            (r'(not supported|not proceed|declin)',           "rejected"),
        ]:
            if re.match(pat, u):
                return st, "labelled update"
        return ("rejected", "government response") if refused else \
               ("unclear", "labelled update, value not recognised")

    if refused:
        return "rejected", "government response"

    if update:
        return "unclear", "prose update, not coded"
    return "unclear", "response only"


def parse(report):
    path = TEXT / f"{report}.txt"
    lines = path.read_text(encoding="utf-8", errors="ignore").split("\n")
    meta = SOURCES[report]

    blocks, cur, round_label = [], None, None
    for i, line in enumerate(lines):
        rm = ROUND.match(line)
        if rm:
            a, b = rm.group(1), rm.group(2)
            b = b if len(b) == 4 else a[:2] + b
            round_label = f"{a}-{b}"
        h = header(line)
        if h:
            if cur: blocks.append(cur)
            num, part, label = h
            cur = dict(num=num, part=part, label=label or round_label or meta["covers"],
                       heading=line.strip(), line=i + 1, body=[])
            continue
        if cur is not None:
            cur["body"].append(line)
    if cur: blocks.append(cur)

    recs = []
    for b in blocks:
        body = [l for l in b["body"] if not furniture(l)]
        for i, l in enumerate(body):
            if block_end(l):
                body = body[:i]
                break
        if not any(F_AGENCY.match(l) or F_RESP_INLINE.match(l) or F_RESP_HEAD.match(l)
                   or F_UPDATE.match(l) for l in body):
            continue                      # not the update chapter

        text_lines, fields, current = [], {}, None
        for l in body:
            m = F_RESP_INLINE.match(l)
            if m:
                fields.setdefault("response", m.group(2).strip())
                fields.setdefault("response_year", m.group(1))
                current = "response"; continue
            m = F_RESP_HEAD.match(l)
            if m:
                fields.setdefault("response_year", m.group(1)); current = None; continue
            m = F_RESPONSE.match(l)
            if m: fields.setdefault("response", m.group(1).strip()); current = "response"; continue
            m = F_AGENCY.match(l)
            if m: fields.setdefault("agency", m.group(1).strip()); current = "agency"; continue
            m = F_UPD_HEAD.match(l)
            if m: fields.setdefault("update_year", m.group(1)); current = None; continue
            m = F_AGENCY_UPD.match(l)
            if m:
                fields.setdefault("update_year", m.group(1))
                fields.setdefault("update_free", []); current = "update_free"; continue
            m = F_UPDATE.match(l)
            if m: fields.setdefault("update", m.group(1).strip()); current = "update"; continue
            m = F_DETAILS.match(l)
            if m: fields.setdefault("details", [m.group(1)]); current = "details"; continue
            m = F_COMMENT.match(l)
            if m: fields.setdefault("details", [m.group(1)]); current = "details"; continue
            m = F_OPPS.match(l)
            if m: current = None; continue
            if not fields:
                text_lines.append(l)
            elif current == "details":
                fields["details"].append(l)
            elif current == "update_free":
                fields["update_free"].append(l)
            elif current in ("response", "agency", "update") and l.strip():
                # single-line fields; a continuation line is wrapped value
                if len(fields.get(current, "")) < 120 and not l.startswith("    "):
                    fields[current] = (fields[current] + " " + l.strip()).strip()
                current = None

        rec_text = join(text_lines)
        if not rec_text or len(rec_text) < 30:
            continue

        num, part, heading_wrong = b["num"], b["part"], None
        bm = BODY_NUM.match(rec_text)
        if bm:
            bn, bp = int(bm.group(1)), int(bm.group(2))
            # An unnumbered heading over numbered text is just a heading style
            # (the 2017-19 report does this throughout) -- adopt the part. A
            # heading that carries a different part is a contradiction, so
            # record it: the 2019-21 report heads its 27.2 "RECOMMENDATION 27.1".
            if part is not None and (bn, bp) != (num, part):
                heading_wrong = b["heading"]
            if (bn, bp) != (num, part):
                num, part = bn, bp

        origin = b["label"] or report
        first_year = int(origin.split("-")[1]) if "-" in origin else None
        details = join(fields.get("details", [])) if fields.get("details") else None
        labelled = bool(fields.get("update"))
        update = fields.get("update") or (join(fields["update_free"]) if fields.get("update_free") else None)
        if update: update = update.rstrip(" ,.;") + "."
        status, basis = norm_status(update, fields.get("response"), labelled)
        refused = bool(re.search(r'not supported|does not support|declin',
                                 (fields.get("response") or "").lower()))
        reversed_refusal = refused and status in ("implemented", "in progress")
        agency_src = fields.get("agency") or rec_text
        agency_basis = "lead agency" if fields.get("agency") else "recommendation text"
        as_of = fields.get("update_year") or fields.get("response_year") or report

        label = f"{num}.{part}" if part else str(num)
        recs.append({
            "id": f"NSW-{origin}-{label}",
            "jurisdiction": "NSW",
            "review_body": "NSW Domestic Violence Death Review Team",
            "report_title": f"NSW Domestic Violence Death Review Team Report {origin}",
            "report_url": meta["url"],
            "page_ref": None,
            "report_period": origin,
            "recommendation_number": num,
            "recommendation_part": label if part else None,
            "recommendation_text": rec_text,
            "target_agency": tag_agency(agency_src),
            "status": status,
            "status_as_of": f"NSW_{report} whole-of-government "
                            + ("update " + fields["update_year"] if fields.get("update_year")
                               else "response " + str(fields.get("response_year") or "")),
            "first_appeared_year": first_year,
            "repeat_of": None,
            "source_quote": details or update,
            # NSW-only provenance: the government's own words, kept verbatim so a
            # reader can see what the normalised status was derived from.
            "govt_response": fields.get("response"),
            "govt_update": update,
            "lead_agency_text": fields.get("agency"),
            "status_basis": basis,
            # government refused, then acted anyway
            "response_reversed": reversed_refusal,
            "agency_basis": agency_basis,
            "source_line": b["line"],
            # set where the printed heading contradicts the recommendation's own
            # number, so the correction is visible rather than assumed
            "heading_discrepancy": heading_wrong,
        })
    return recs

def main():
    allrecs = []
    for report in SOURCES:
        recs = parse(report)
        out = OUT / f"NSW_{report}.json"
        out.write_text(json.dumps(recs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rounds = {}
        for r in recs:
            rounds.setdefault(r["report_period"], []).append(
                r.get("recommendation_part") or str(r["recommendation_number"]))
        print(f"\n{report}: {len(recs)} recommendations -> {out.name}")
        for rd, labels in sorted(rounds.items()):
            tops = sorted({int(l.split(".")[0]) for l in labels})
            gaps = [n for n in range(1, max(tops) + 1) if n not in tops] if tops else []
            dupes = sorted({l for l in labels if labels.count(l) > 1})
            print(f"   {rd}: rows={len(labels)} top-level={len(tops)} max={max(tops)}"
                  + (f" MISSING={gaps}" if gaps else "")
                  + (f" DUPLICATE={dupes}" if dupes else ""))
        allrecs += recs
    print(f"\ntotal NSW rows: {len(allrecs)}")
    from collections import Counter
    print("status:", dict(Counter(r["status"] for r in allrecs)))
    print("status basis:", dict(Counter(r["status_basis"] for r in allrecs)))
    print("agency basis:", dict(Counter(r["agency_basis"] for r in allrecs)))
    rev = [r for r in allrecs if r["response_reversed"]]
    print(f"refused then acted on anyway: {len(rev)} -> {[r['id'] for r in rev]}")

    # The 122 check: the Team's own Table 7.2 (2019-21 report) puts every
    # recommendation it has ever made at n=122. Five reports made numbered
    # recommendations (2011-12 through 2017-19); 2010-11 is an establishment
    # report that makes none, and 2021-23 has no recommendations chapter. So the
    # top-level count across those five rounds should land exactly on 122.
    tops = {(r["report_period"], r["recommendation_number"]) for r in allrecs}
    # Length alone is a poor test: a five-part recommendation with a full
    # multi-part agency response legitimately runs to ~7,400 characters. What
    # actually marks a runaway is swallowed document structure, so look for that
    # as well as for absurd length.
    LEAK = re.compile(r'Appendix\s+[A-Z]\b|coroners\.justice\.nsw\.gov\.au|FIGURE\s+\d+:', re.I)
    longest = max(allrecs, key=lambda r: len(r["govt_update"] or ""))
    leaked = [r["id"] for r in allrecs if LEAK.search(r["govt_update"] or "")]
    oversize = [r["id"] for r in allrecs if len(r["govt_update"] or "") > 8000]
    print(f"\nlongest government update: {len(longest['govt_update'] or '')} chars ({longest['id']})")
    print(f"updates containing swallowed document structure: {leaked or 'none'}")
    print(f"updates over 8,000 chars: {oversize or 'none'}")

    print(f"top-level recommendations across all rounds: {len(tops)}"
          f"  (Table 7.2 states n=122 -> {'MATCH' if len(tops) == 122 else 'MISMATCH'})")

    # The site projection is written by scripts/apply_repeats.py, not here.
    # This script rebuilds the extraction from the PDFs and would overwrite the
    # hand-adjudicated repeat_of / related_to links, so it must always be
    # followed by apply_repeats.py before anything consumes data/.
    print("\nNOTE: repeat_of / related_to have just been cleared. "
          "Run scripts/apply_repeats.py to restore them and rebuild data/nsw-recommendations.json.")

def project(allrecs):
    """The shape the site consumes, matching data/wa-recommendations.json."""
    return [{
        "id": r["id"],
        "report": r["report_title"],
        "report_period": r["report_period"],
        "recommendation_number": r["recommendation_number"],
        "recommendation_part": r["recommendation_part"],
        "text": r["recommendation_text"],
        "target_agency": r["target_agency"],
        "status": r["status"],
        "status_as_of": r["status_as_of"],
        "status_basis": r["status_basis"],
        "response_reversed": r["response_reversed"],
        "govt_response": r["govt_response"],
        "govt_update": r["govt_update"],
        "page_ref": r["page_ref"],
        "report_url": r["report_url"],
    } for r in allrecs]


if __name__ == "__main__":
    main()
