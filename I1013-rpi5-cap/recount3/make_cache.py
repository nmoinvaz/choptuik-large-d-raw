"""#1013 recount3: step 2's 0.18 points file without its off-sheet records.
    python3 make_cache.py STEP2_POINTS_0.18 SHEETFIX_POINTS_0.17 OUT_POINTS_0.18 OUT_REMOVED
OUT_POINTS keeps the other lines of step 2's file byte for byte and in order; OUT_REMOVED holds the removed lines byte for byte.
A line is removed when sheet_precheck.off_sheet flags it (a valued point more than 0.1 in F3 from the sheetfix's 0.17 sheet)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sheet_precheck import off_sheet

src, p17, out, rem = sys.argv[1:5]
lines = open(src).read().splitlines(True)
bad, _ = off_sheet([json.loads(l) for l in open(p17)], [json.loads(l) for l in lines], quiet=True)
open(out, "w").write("".join(l for i, l in enumerate(lines) if i not in bad))
open(rem, "w").write("".join(lines[i] for i in bad))
print(f"{len(lines)} lines in, {len(lines) - len(bad)} kept, {len(bad)} removed (lines {[i + 1 for i in bad]})")
