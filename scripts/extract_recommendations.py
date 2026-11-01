#!/usr/bin/env python3
"""
Pulls candidate recommendation blocks out of pdftotext -layout output.
Pure pattern-matching pass: finds "Recommendation N" markers and captures
the text up to the next marker or a clear section break. This is a first
pass to cut 70k+ lines down to the ~200 lines that actually matter per
report, not a finished extraction. Output still needs a human/LLM read
to classify theme/target_agency/status and to merge split paragraphs.
"""
import re
import sys
import json
import os

REC_MARKER = re.compile(r'^\s*Recommendation\s+(\d+[a-z]?)\s*:?\s*(.*)$', re.IGNORECASE)

def extract(path):
    with open(path, encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    blocks = []
    current = None
    for i, line in enumerate(lines):
        m = REC_MARKER.match(line.strip())
        if m:
            if current:
                blocks.append(current)
            current = {
                "rec_number": m.group(1),
                "start_line": i + 1,
                "text_lines": [m.group(2)] if m.group(2) else [],
            }
        elif current is not None:
            stripped = line.strip()
            # stop a block on an obvious heading/page-break marker
            if re.match(r'^(CHAPTER|Chapter)\s+\d+', stripped) or stripped.isdigit():
                blocks.append(current)
                current = None
                continue
            if stripped:
                current["text_lines"].append(stripped)
            if len(current["text_lines"]) > 25:  # safety cap per block
                blocks.append(current)
                current = None
    if current:
        blocks.append(current)

    for b in blocks:
        b["text"] = " ".join(b.pop("text_lines")).strip()
    return blocks

def main():
    text_dir = sys.argv[1]
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    for fn in sorted(os.listdir(text_dir)):
        if not fn.endswith(".txt"):
            continue
        path = os.path.join(text_dir, fn)
        blocks = extract(path)
        out_path = os.path.join(out_dir, fn.replace(".txt", "_raw.json"))
        with open(out_path, "w") as f:
            json.dump(blocks, f, indent=2)
        print(f"{fn}: {len(blocks)} candidate recommendation blocks -> {out_path}")

if __name__ == "__main__":
    main()
