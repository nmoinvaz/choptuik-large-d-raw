#!/usr/bin/env python3
"""rule_gate.py LOG [OUTDIR]: the verdict of #1064 part 7 (the chain's acceptance rules, not the 1e-60 gate). PASS = (1) the polish reports converged: the first 'octo-double Newton: N steps, max|F| X, converged' line of the log
(the base polish, as gate903d reads it); the line 'converged by the floor rule' before it, if any, is named; AND (2) the chain step is accepted: an 'a X -> D Y: predicted ... od N steps -> Z (tol T ...)' line with od steps > 0
and a finite result (an attempt line with 'od 0 steps -> nan' is a refused attempt and does not count; the first attempt that is not one is the accepted step), and, when OUTDIR is given, a saved anm_pin3_D*.npz and jet_pin3_D*.npz there. Prints 'PASS ...' or 'FAIL: reason'; exit 0 on PASS."""
import glob
import re
import sys

log = open(sys.argv[1], errors="replace").read()
outdir = sys.argv[2] if len(sys.argv) > 2 else None
m = re.search(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (not )?converged", log)
if not m:
    print("FAIL: no octo-double Newton line (the polish did not report)")
    sys.exit(1)
if m.group(3):
    print(f"FAIL: the polish reports NOT converged ({m.group(1)} steps, max|F| {m.group(2)})")
    sys.exit(1)
floor = re.search(r"on \d+: \|F\| [0-9.e+-]+ above tol at the floor.*converged by the floor rule", log[:m.start()])
pol = f"polish converged ({m.group(1)} od steps, max|F| {m.group(2)}{', by the floor rule' if floor else ''})"
pat = r"a ([0-9.]+) -> D ([0-9.]+): predicted \|F\| ([0-9.e+-]+), od (\d+) steps? -> ([0-9.e+-]+|nan) \(tol ([0-9.e+-]+)"
alls = list(re.finditer(pat, log))
if not alls:
    print(f"FAIL: {pol}, but no step attempt line")
    sys.exit(1)
good = [x for x in alls if x.group(5) != "nan" and int(x.group(4)) > 0]
if not good:
    print(f"FAIL: {pol}, but no attempt was an accepted corrector result ({len(alls)} attempt line(s), the last: a {alls[-1].group(1)} -> D {alls[-1].group(2)}, od {alls[-1].group(4)} steps -> {alls[-1].group(5)})")
    sys.exit(1)
acc = good[0]
files = ""
if outdir:
    b, j = glob.glob(f"{outdir}/anm_pin3_D*.npz"), glob.glob(f"{outdir}/jet_pin3_D*.npz")
    if not b or not j:
        print(f"FAIL: {pol}, step line a {acc.group(1)} -> D {acc.group(2)} present, but files missing (anm_pin3 {len(b)}, jet_pin3 {len(j)})")
        sys.exit(1)
    files = f"; saved {len(b)} anm_pin3 and {len(j)} jet_pin3 file(s)"
print(f"PASS: {pol}; step accepted: a {acc.group(1)} -> D {acc.group(2)}, od {acc.group(4)} steps -> {acc.group(5)} (tol {acc.group(6)}){files}")
