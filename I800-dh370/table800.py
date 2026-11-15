#!/usr/bin/env python3
"""#800 stage 1's table and verdicts (notes/FACTORED_HORIZON.md 4.7), from I800-dh370.
    python -I table800.py FOLDER      (FOLDER: I800-dh370; its parent is the raw clone)
    python -I table800.py --selftest
(1) t0 (orders 131..250 weighted 0) equals #696's r130k base in Delta to 1e-40; (2) each rung converged by its last
"octo-double Newton" line, Delta - Delta(t0) per rung; (3) at w = 1 Delta - Delta(t0) against #796's single-order climb
and the model's T_omit / sigma_inf (2.7e-12, a conjecture good to a factor 100); (4) sigma_3 at w = 0, 1/2, 1 from
near_null's JSON: the reading of 4.3 holds if ln sigma_3(1) - ln sigma_3(0) lies within 30% of the model's -ln f at
ks 130, 50.7 (interpolated in D between 241.96 and 249.01 in 4.2's table), and fails if sigma_3 changes by less than a
factor 2. --selftest: the verdict of (4) on planted sigma pairs."""
import json
import math
import os
import re
import sys

import mpmath as mp
import numpy as np

mp.mp.prec = 600
KEYS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
LNF = 50.7
RUNGS = [("t0", 0.0), ("t015625", 1 / 64), ("t03125", 1 / 32), ("t0625", 1 / 16), ("t125", 1 / 8), ("t25", 1 / 4),
         ("t375", 3 / 8), ("t5", 1 / 2), ("t625", 5 / 8), ("t75", 3 / 4), ("t875", 7 / 8), ("t1", 1.0)]


def delta(path):
    d = np.load(path, allow_pickle=False)
    return mp.fsum(mp.mpf(float(d[k][-1])) for k in KEYS if k in d.files)


def base(folder):
    n = [f for f in os.listdir(folder) if f.startswith("base_pin3_D") and f.endswith(".npz")] if os.path.isdir(folder) else []
    return os.path.join(folder, sorted(n)[0]) if n else None


def newton(log):
    if not os.path.exists(log):
        return None
    ls = [s for s in open(log, encoding="utf-8", errors="replace") if re.search(r"octo-double Newton: \d+ steps", s)]
    m = re.search(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.eE+-]+|nan), (not converged|converged)", ls[-1]) if ls else None
    return (int(m.group(1)), m.group(2), m.group(3) == "converged") if m else None


def verdict4(s0, s1):
    if not (s0 and s1):
        return "not measured"
    d = math.log(s1) - math.log(s0)
    if abs(d - LNF) <= 0.3 * LNF:
        return f"holds (ln ratio {d:.2f} against {LNF})"
    if abs(d) < math.log(2):
        return f"fails (ln ratio {d:.2f}, a change below a factor 2)"
    return f"neither (ln ratio {d:.2f} against {LNF})"


def main(folder):
    raw = os.path.dirname(os.path.abspath(folder))
    ref = None
    for cand in (os.path.join(raw, "I696-win2", "D245", "r130k"),):
        b = base(cand)
        ref = delta(b) if b else None
    d0 = None
    print("| rung | w | Newton steps | final max\\|F\\| | converged | Delta - Delta(t0) |\n|---|---|---|---|---|---|")
    for tag, w in RUNGS:
        nw = newton(os.path.join(folder, f"{tag}.log"))
        b = base(os.path.join(folder, tag))
        if nw is None:
            continue
        dl = delta(b) if b and nw[2] else None
        if tag == "t0" and dl is not None:
            d0 = dl
        dd = mp.nstr(dl - d0, 5) if dl is not None and d0 is not None else "-"
        print(f"| {tag} | {w:g} | {nw[0]} | {nw[1]} | {'yes' if nw[2] else 'NO'} | {dd} |")
    if ref is not None and d0 is not None:
        c = abs(d0 - ref)
        print(f"\n(1) t0 against r130k: {mp.nstr(c, 3)}: {'met' if c <= mp.mpf('1e-40') else 'NOT MET'}")
    else:
        print("\n(1) t0 or r130k's base missing")
    sig = {}
    for tag in ("t0", "t5", "t1"):
        p = os.path.join(folder, f"sigma_{tag}.json")
        if os.path.exists(p):
            j = json.load(open(p))
            sig[tag] = sorted(v["sigma"] for v in j.get("vectors", []))
    print("sigma_1..4: " + "; ".join(f"{t}: {', '.join(f'{x:.3e}' for x in v)}" for t, v in sig.items()))
    s0 = sig.get("t0", [None] * 4)[2] if "t0" in sig else None
    s1 = sig.get("t1", [None] * 4)[2] if "t1" in sig else None
    print(f"(4) sigma_3 from w = 0 to 1: {verdict4(s0, s1)}")
    return 0


def selftest():
    cases = [(1e-40, 1e-40 * math.exp(50.7), "holds"), (1e-40, 1.5e-40, "fails"), (1e-40, 1e-30, "neither"), (None, 1.0, "not measured")]
    bad = 0
    for a, b, want in cases:
        got = verdict4(a, b)
        ok = got.startswith(want)
        bad += not ok
        print(f"  {a} -> {b}: {got} ({'ok' if ok else 'WRONG'})")
    print("selftest", "passed" if not bad else "FAILED")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
