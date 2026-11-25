#!/bin/bash
# the root's own check at M' 160: exactly one sign change in the first bracket, and the smallest pivot ratio (pivot_min / pivot_max over
# every determinant line) above 1e-20. usage: root_check.sh ROOT.log ; exit 0 passes, 1 fails; prints the numbers.
/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python -I - "$1" <<'PY'
import re, sys
t = open(sys.argv[1]).read()
m = re.search(r"root of D_m: lam ([0-9.eE+-]+) \((\d+) sign changes in the first bracket, (\d+) dets\)", t)
piv = [(float(a), float(b)) for a, b in re.findall(r"pivots ([0-9.e+-]+)\.\.([0-9.e+-]+)", t)]
if not m or not piv:
    print("no root line or no pivots in the log"); sys.exit(1)
lam, nch, nev = float(m.group(1)), int(m.group(2)), int(m.group(3))
ratio = min(a / b for a, b in piv)
ok = nch == 1 and ratio > 1e-20
print(f"root check: lam {lam!r}, gamma {1/lam!r}, sign changes {nch} (1 wanted), {nev} dets, {len(piv)} pivot lines, smallest pivot ratio {ratio:.2e} (> 1e-20 wanted): {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
PY
