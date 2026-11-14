#!/usr/bin/env python3
"""#784: A (#608's flags) against B (--od_abort_theta 1e8), one step each from D 249.5375.
    python -I compare784.py FOLDER     (FOLDER: I784-dh370; exit 0 when every bar holds)
    python -I compare784.py --selftest
Bars, fixed before the run: (1) A reproduces #608's attempts, a 0.4883 not converged after 20 steps and a smaller a
accepted; (2) B refuses a 0.4883 at iteration 1 (its log's "attempt refused at iteration 1" line) and accepts the same
smaller a; (3) A's and B's accepted states agree in every unknown to 1e-55 (the exact sum of the eight parts, 600 bits)
at the same D_str; (4) B's wall time is below A's. --selftest: the state comparison on planted states (equal ones pass, a
state off by 1e-54 fails)."""
import glob
import json
import os
import re
import sys

import mpmath as mp
import numpy as np

mp.mp.prec = 600
KEYS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")


def exact(z):
    return [mp.fsum(mp.mpf(float(z[k][i])) for k in KEYS if k in z) for i in range(len(z[KEYS[0]]))]


def state(folder):
    s = sorted(glob.glob(os.path.join(folder, "anm_pin3_D*.npz")))
    if not s:
        return None, None
    d = np.load(s[-1], allow_pickle=False)
    m = json.loads(str(d["meta"])) if "meta" in d.files else {}
    return {k: np.array(d[k]) for k in KEYS if k in d.files}, m.get("D_str")


def diff_ok(za, zb):
    dmax = max(abs(x - y) for x, y in zip(exact(za), exact(zb)))
    return dmax <= mp.mpf("1e-55"), dmax


def main(folder):
    la = open(os.path.join(folder, "A.log"), encoding="utf-8", errors="replace").read()
    lb = open(os.path.join(folder, "B.log"), encoding="utf-8", errors="replace").read()
    a20 = bool(re.search(r"octo-double Newton: 20 steps, max\|F\| [0-9.e+-]+, not converged", la))
    babort = "attempt refused at iteration 1" in lb
    za, da = state(os.path.join(folder, "A"))
    zb, db = state(os.path.join(folder, "B"))
    ok3, dmax = (diff_ok(za, zb) if za is not None and zb is not None else (False, None))
    ex = open(os.path.join(folder, "exits_784.txt")).read()
    wa, wb = (int(re.search(rf"^{s} exit \d+ wall (\d+) s", ex, re.M).group(1)) for s in ("A", "B"))
    bars = [("(1) A: a 20-step attempt not converged, then a state saved", a20 and za is not None),
            ("(2) B: refused at iteration 1, then a state saved", babort and zb is not None),
            (f"(3) the states at the same D_str ({da} and {db}) agree to 1e-55 (max {mp.nstr(dmax, 3) if dmax is not None else '-'})",
             ok3 and da == db and da is not None),
            (f"(4) B's wall {wb} s below A's {wa} s", wb < wa)]
    for label, ok in bars:
        print(f"{label}: {'met' if ok else 'FAILED'}")
    good = all(ok for _, ok in bars)
    print("PASS" if good else "FAIL")
    return 0 if good else 1


def selftest():
    z = {k: (np.array([1.0, 2.0]) if k == "zh" else np.zeros(2)) for k in KEYS}
    off = {k: v.copy() for k, v in z.items()}
    off["z4"][1] = 1e-54
    ok1, ok2 = diff_ok(z, z)[0], diff_ok(z, off)[0]
    good = ok1 and not ok2
    print(f"  equal states {ok1} (expected True); off by 1e-54 {ok2} (expected False)")
    print("selftest", "passed" if good else "FAILED")
    return 0 if good else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
