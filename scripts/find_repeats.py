#!/usr/bin/env python3
"""
Candidate generator for `repeat_of` -- the field that shows the same thing being
recommended over and over.

Two independent signals, because neither is sufficient alone:

1. THE TEAM'S OWN CROSS-CITATIONS. The 2019-21 NSW report footnotes group
   recommendations across reports ("DVDRT Report 2012-13, Recommendation 1;
   DVDRT Report 2015-17, Recommendation 2; DVDRT Report 2017-19,
   Recommendation 9"). That is the review body itself saying these belong
   together, which beats any similarity score. But it is NOT proof of
   repetition: some of those footnotes group by theme, and at least one groups
   by *status* ("The recommendations that were not supported are as follows"),
   which would produce entirely spurious repeat links. So the lead-in text is
   captured with every group and status-list footnotes are flagged for
   exclusion rather than silently trusted.

2. TEXT SIMILARITY. IDF-weighted cosine over the recommendation text, computed
   only across different rounds (a recommendation cannot repeat itself). Domain
   terms that appear everywhere -- "domestic", "violence", "nsw", "recommend" --
   are stripped, because leaving them in makes every pair look alike and buries
   the real matches.

This script PROPOSES. It does not write `repeat_of`. Every pair it emits has to
be read against the two source texts before it is accepted, because a false
repeat claim is the kind of thing that discredits the whole tracker.
"""
import json, re, math, sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
RECS = ROOT / "extracted" / "recommendations"
TEXT = ROOT / "text" / "nsw"

# ---------------------------------------------------------------- load rows
def load():
    """rows keyed by (round, printed label) plus an index from (round, top-level
    number) to every row under it. The footnotes cite top-level numbers, but a
    recommendation split into sub-parts is stored under "27.1"/"27.2", so a bare
    "#27" has to fan out to both rather than silently failing to resolve."""
    rows, by_num = {}, defaultdict(list)
    for f in sorted(RECS.glob("NSW_*.json")):
        for r in json.load(open(f)):
            label = r.get("recommendation_part") or str(r["recommendation_number"])
            key = (r["report_period"], label)
            rows[key] = r
            by_num[(r["report_period"], str(r["recommendation_number"]))].append(key)
    return rows, by_num


def resolve(cited, rows, by_num):
    """A cited (round, number) -> the row keys it refers to."""
    if cited in rows:
        return [cited]
    return by_num.get((cited[0], cited[1].split(".")[0]), [])

# --------------------------------------------- the Team's own cross-citations
CITE = re.compile(r'(?:DVDRT )?Report ?(\d{4})[-/](\d{2,4}), Recommendations? ([0-9][0-9.,\sand-]*)')
# A footnote that enumerates by status, not by subject -- these must not become
# repeat links.
STATUS_LIST = re.compile(r'not supported|were (?:not )?implemented|are as follows', re.I)

def norm_round(a, b):
    b = b if len(b) == 4 else a[:2] + b
    return f"{a}-{b}"

def parse_nums(blob):
    """'8, 12, 15 and 25' -> ['8','12','15','25']; '1-3' -> ['1','2','3']"""
    out = []
    blob = blob.replace(" and ", ",").replace("and ", ",")
    for part in blob.split(","):
        part = part.strip(" .;")
        if not part:
            continue
        m = re.fullmatch(r'(\d+)\s*-\s*(\d+)', part)
        if m:
            out += [str(n) for n in range(int(m.group(1)), int(m.group(2)) + 1)]
        elif re.fullmatch(r'\d+(?:\.\d+)?', part):
            out.append(part)
    return out

def citation_groups():
    groups = []
    for rep in ["2017-2019", "2019-2021"]:
        path = TEXT / f"{rep}.txt"
        if not path.exists():
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").split("\n")):
            hits = CITE.findall(line)
            if len(hits) < 2:
                continue
            members = []
            for a, b, nums in hits:
                rd = norm_round(a, b)
                members += [(rd, n) for n in parse_nums(nums)]
            if len({m[0] for m in members}) < 2:
                continue                      # all one round: not a cross-report group
            groups.append({
                "source_report": rep,
                "line": i + 1,
                "text": line.strip()[:400],
                "members": sorted(set(members)),
                "looks_like_status_list": bool(STATUS_LIST.search(line)),
            })
    return groups

# ------------------------------------------------------------- similarity
STOP = set("""a an the and or of to in for that this these those with on by at as is are was were be been
being from into their there it its his her they them which who whom whose where when what how all any
both each more most other some such no nor not only own same so than too very can will just should now
if then but because while during above below between under over again further once here why about
against through before after up down out off then""".split())
# Terms that appear in nearly every recommendation in this corpus and therefore
# carry no signal about whether two recommendations are the same.
DOMAIN = set("""domestic violence nsw recommendation recommendations recommend team dvdrt report government
family deaths death victim victims should consider considered consideration review reviewed give ensure
ensuring work working develop development including include includes relation relevant person people
process processes service services agency agencies department departments""".split())

def tokens(text):
    ws = re.findall(r"[a-z]{3,}", text.lower())
    return [w for w in ws if w not in STOP and w not in DOMAIN]

def vectors(rows):
    docs = {k: Counter(tokens(r["recommendation_text"])) for k, r in rows.items()}
    N = len(docs)
    df = Counter()
    for c in docs.values():
        df.update(c.keys())
    idf = {t: math.log(N / (1 + n)) + 1 for t, n in df.items()}
    vecs = {}
    for k, c in docs.items():
        v = {t: (1 + math.log(n)) * idf[t] for t, n in c.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs[k] = {t: x / norm for t, x in v.items()}
    return vecs

def cosine(a, b):
    short, long_ = (a, b) if len(a) < len(b) else (b, a)
    return sum(x * long_.get(t, 0.0) for t, x in short.items())

def shared(rows, ka, kb, n=8):
    ta, tb = Counter(tokens(rows[ka]["recommendation_text"])), Counter(tokens(rows[kb]["recommendation_text"]))
    return sorted(set(ta) & set(tb), key=lambda t: -(ta[t] + tb[t]))[:n]

# ------------------------------------------------------------------- main
def main():
    rows, by_num = load()
    print(f"loaded {len(rows)} NSW rows across {len({k[0] for k in rows})} rounds\n")

    groups = citation_groups()
    usable = [g for g in groups if not g["looks_like_status_list"]]
    excluded = [g for g in groups if g["looks_like_status_list"]]
    print(f"{'='*78}\nSIGNAL 1 - the Team's own cross-report citation groups")
    print(f"  {len(groups)} cross-report groups found; {len(excluded)} excluded as status lists\n")

    for g in excluded:
        print(f"  EXCLUDED (status list) {g['source_report']}:{g['line']}")
        print(f"     {g['text'][:150]}")
    print()

    resolved = unresolved = 0
    for g in usable:
        g["resolved"] = []
        miss = []
        for m in g["members"]:
            keys = resolve(m, rows, by_num)
            if keys: g["resolved"] += keys
            else: miss.append(m)
        g["resolved"] = sorted(set(g["resolved"]))
        g["unresolved"] = miss
        resolved += len(g["resolved"]); unresolved += len(miss)
        print(f"  {g['source_report']}:{g['line']}  {len(g['resolved'])} rows"
              + (f", {len(miss)} UNRESOLVED" if miss else ""))
        print(f"     cite: {g['text'][:135]}")
        for k in g["resolved"]:
            print(f"       {k[0]} #{k[1]}")
        for m in miss:
            print(f"       {m[0]} #{m[1]}   <- no extracted row")
    print(f"\n  rows reached by citation: {resolved}; citations not resolving: {unresolved}")

    # ---- signal 2
    vecs = vectors(rows)
    keys = sorted(rows)
    pairs = []
    for i, ka in enumerate(keys):
        for kb in keys[i+1:]:
            if ka[0] == kb[0]:
                continue                      # same round cannot be a repeat
            s = cosine(vecs[ka], vecs[kb])
            if s >= 0.22:
                pairs.append((s, ka, kb))
    pairs.sort(reverse=True)

    cited = set()
    for g in usable:
        for a in g["resolved"]:
            for b in g["resolved"]:
                if a < b: cited.add((a, b))

    print(f"\n{'='*78}\nSIGNAL 2 - text similarity, cross-round only, threshold 0.22")
    print(f"  {len(pairs)} candidate pairs\n")
    for s, ka, kb in pairs[:40]:
        mark = "CITED" if (min(ka,kb), max(ka,kb)) in cited else "     "
        print(f"  {s:.3f} {mark}  {ka[0]} #{ka[1]:<5s} <-> {kb[0]} #{kb[1]:<5s}  {', '.join(shared(rows, ka, kb))}")

    out = ROOT / "extracted" / "repeat_candidates.json"
    out.write_text(json.dumps({
        "citation_groups": [
            {**g, "members": [list(m) for m in g["members"]],
             "resolved": [list(k) for k in g.get("resolved", [])],
             "unresolved": [list(m) for m in g.get("unresolved", [])]}
            for g in groups
        ],
        "similarity_pairs": [
            {"score": round(s, 4), "a": list(ka), "b": list(kb),
             "shared_terms": shared(rows, ka, kb),
             "also_cited_together": (min(ka,kb), max(ka,kb)) in cited,
             "a_text": rows[ka]["recommendation_text"],
             "b_text": rows[kb]["recommendation_text"]}
            for s, ka, kb in pairs
        ],
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\ncandidates -> {out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
