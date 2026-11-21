#!/usr/bin/env python3
"""map_read2.py [DIR]: #1025 d185map on win2, after the split of window B (the final reading; map_read_v1.py was the first run's, with one B): the reading of D 18.5 (k_c 63) over lambda 1.00 to 2.60. Inputs: xfkappa's three D 18.5 scans (I1025-mac/d18: d185_scan_1025.jsonl 1.55 to 1.90, d185_scanhi_1025.jsonl 1.90 to 2.10,
d185_scanup_1025.jsonl 2.10 to 2.40) and this folder's scan_A.jsonl (2.40 repeat, then 2.41 to 2.60) and b_split/scan_B1.jsonl (1.55 repeat, then 1.28 to 1.54) and b_split/scan_B2.jsonl (1.55 repeat, then 1.00 to 1.27); the first run's stopped B (scan_B_stopped.jsonl) is used only to compare duplicate points.
1. The repeats (lambda 2.40 and 1.55) are checked by repeat_check.py's rule (same sign, ln|det| within 1e-2, noise-robust): across machines the ln|det| differs by about 1e-3 (the control: 8.9e-4), so the reader's same-machine
   repeat bar 1e-6 would flag them; they are therefore taken out of the files given to the reader (map_A_new.jsonl: lambda above 2.40; map_B_new.jsonl: lambda below 1.55), and checked here.
2. xfkappa's reader (d18d_read.py, the pinned copy in ../d18mid/pinned, blob 6b608903) reads the five files together: every robust sign change with its bracket, orientation and estimator range, every ln|det| local minimum
   without a sign change (the coordinator's reading), and the float64 sign beside. xfkappa's own repeated points (1.90, 2.10) are in the reader's repeat list.
3. Information: the reference points of xfkappa's sign-convention check at lambda 1.20 and 2.60 (d18_refsign_1025.jsonl, D 18.5: -1 and -1) against this folder's points at those lambdas (same sign, ln within 1e-2), and the sign
   parity: the signs at the window ends (1.00, 1.55, 2.40, 2.60) and the count of robust changes in each of the two new windows."""
import json
import os
import subprocess
import sys

H = (sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))).replace("\\", "/").rstrip("/") + "/"
RAWQ = "D:/choptuik-i935-raw/I1025-win2/d185map/inputs/"   # copies of xfkappa's files (I1025-mac/d18), blobs in inputs/BLOBS.txt
READER = "D:/choptuik-i935-raw/I1025-win2/d18mid/pinned/d18d_read.py"
WTM = "D:/choptuik-i1025d/solver/matter"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repeat_check as rc  # noqa: E402


def rows(path):
    return [json.loads(x) for x in open(path) if x.strip()] if os.path.exists(path) else []


A = rows(H + "scan_A.jsonl")
B1, B2 = rows(H + "b_split/scan_B1.jsonl"), rows(H + "b_split/scan_B2.jsonl")
B = B1 + B2
BS = rows(H + "scan_B_stopped.jsonl")
print("scan_A: %d rows, scan_B1: %d rows, scan_B2: %d rows, the first run's stopped B: %d rows" % (len(A), len(B1), len(B2), len(BS)))
bad = False
for name, R, lam, ref in (("A", A, 2.4, "d185_scanup_1025.jsonl"), ("B1", B1, 1.55, "d185_scan_1025.jsonl"), ("B2", B2, 1.55, "d185_scan_1025.jsonl")):
    r = next((x for x in R if abs(x["lam"] - lam) < 1e-9), None)
    if r is None:
        print("repeat %.2f (window %s): missing" % (lam, name))
        bad = True
        continue
    x = rc.ref_row(RAWQ, ref, lam)
    ok, same, d = rc.verdict(r, x)
    print("repeat %.2f (window %s): win2 %+d %.10f, xfkappa %+d %.10f, ln difference %+.3e (bar 1e-2): %s" % (lam, name, r["sign"], r["ln"], x["sign"], x["ln"], d, "agree" if ok else "DISAGREE"))
    bad = bad or not ok
if bad:
    print("STOP-level: a repeated point does not agree: no reading")
    sys.exit(2)
newA = [x for x in A if x["lam"] > 2.4 + 1e-9]
newB = sorted([x for x in B if x["lam"] < 1.55 - 1e-9], key=lambda q: q["lam"])
dup = sorted(set(round(x["lam"], 2) for x in newB if sum(1 for y in newB if abs(y["lam"] - x["lam"]) < 1e-9) > 1))
if dup:
    print("duplicate points between B1 and B2: %s (the first is kept by the reader's merge)" % dup)
for fn, R in (("map_A_new.jsonl", newA), ("map_B_new.jsonl", newB)):
    open(H + fn, "w").write("".join(json.dumps(x) + "\n" for x in R))
print("the first run's stopped B against B2/B1 (same machine, same code: sign equal and ln|det| within 1e-6):")
for x in BS:
    if abs(x["lam"] - 1.55) < 1e-9:
        continue
    m = next((q for q in newB if abs(q["lam"] - x["lam"]) < 1e-9), None)
    if m is not None:
        print("  lambda %.2f: stopped B %+d %.10f, split %+d %.10f, difference %+.2e: %s" % (x["lam"], x["sign"], x["ln"], m["sign"], m["ln"], m["ln"] - x["ln"], "agree" if (m["sign"] == x["sign"] and abs(m["ln"] - x["ln"]) <= 1e-6) else "DISAGREE"))
files = [RAWQ + "d185_scan_1025.jsonl", RAWQ + "d185_scanhi_1025.jsonl", RAWQ + "d185_scanup_1025.jsonl", H + "map_A_new.jsonl", H + "map_B_new.jsonl"]
files = [f for f, n in zip(files, (1, 1, 1, len(newA), len(newB))) if n]
print("reader on: " + ", ".join(os.path.basename(f) for f in files))
print()
r = subprocess.run([sys.executable, READER, "18.5", WTM, ",".join(files)], capture_output=True, text=True)
print(r.stdout.rstrip())
if r.returncode:
    print("reader exit %d: %s" % (r.returncode, r.stderr[-300:]))
print()
print("information:")
ref = rows(RAWQ + "d18_refsign_1025.jsonl")
for lam in (1.2, 2.6):
    x = next((q for q in ref if q["D"] == 18.5 and abs(q["lam"] - lam) < 1e-9), None)
    m = next((q for q in A + B if abs(q["lam"] - lam) < 1e-9), None)
    if x and m:
        print("  lambda %.2f: xfkappa's sign-convention reference %+d (ln %.8f); win2 %+d (ln %.8f); same sign %s, ln difference %+.2e" % (
            lam, x["sign"], x["ln"], m["sign"], m["ln"], m["sign"] == x["sign"], m["ln"] - x["ln"]))
    else:
        print("  lambda %.2f: not available" % lam)
sg = {round(q["lam"], 2): q["sign"] for q in A + B}
print("  signs at the window ends: " + ", ".join("%.2f %s" % (l, "%+d" % sg[l] if l in sg else "-") for l in (1.0, 1.55, 2.4, 2.6)))
for name, R in (("B (1.00 to 1.55)", sorted({round(q["lam"], 2): q for q in B}.values(), key=lambda q: q["lam"])), ("A (2.40 to 2.60)", sorted(A, key=lambda q: q["lam"]))):
    ch = [(a["lam"], b["lam"]) for a, b in zip(R, R[1:]) if a["sign"] != b["sign"]]
    print("  window %s: %d points, sign changes between neighbours (any, robust or not): %s" % (name, len(R), [(round(a, 2), round(b, 2)) for a, b in ch] or "none"))
