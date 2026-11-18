#!/usr/bin/env python3
"""#949: ks_chain2 (ks 291) against ks_chain leg 8 (ks 250) at equal D, two different quantities, never to be confused:
  Delta(D): the state's last unknown z[-1], summed exactly over its eight parts (Fraction), the quantity win2b's posts quote;
  sigma_Delta: the Delta mode's singular value of near_null.py (this folder's JSONs), the quantity of #949's ORDER EFFECT table.
    python compare_delta949.py [ROOT=~/scratch949]
For every ks_chain2 state whose D is the same (the stored D_str, exactly) as a leg 8 state's it prints both files, the exact D strings, the
exact Delta difference and the relative sigma_Delta and sigma_pair differences. --selftest plants a Delta difference and checks it is found."""
import glob
import json
import os
import re
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser("~/scratch949")


def load(path):
    d = np.load(path)
    parts = [d[k] for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7") if k in d]
    m = json.loads(str(d["meta"]))
    delta = sum((Fraction(float(p[-1])) for p in parts), Fraction(0))
    return delta, m


def sigma(name):
    p = os.path.join(HERE, name + ".json")
    if not os.path.exists(p):
        return None
    r = json.load(open(p))
    v = r["vectors"]
    d = max(range(len(v)), key=lambda i: v[i]["delta"])
    pair = [i for i in range(len(v)) if i != d and {("p1", 3), ("m_h", 3)} <= {(b, k) for b, k, _ in v[i]["top"]}]
    sp = float(np.sqrt(v[pair[0]]["sigma"] * v[pair[1]]["sigma"])) if len(pair) == 2 else float("nan")
    return v[d]["sigma"], sp


def fmt(x, n=22):
    return f"{float(x):.{n}f}"


def main():
    leg8 = {}
    for p in glob.glob(f"{ROOT}/I903-win2/ks_chain/leg08_*_ks250/anm_pin3_D*.npz"):
        delta, m = load(p)
        leg8[str(m.get("D_str", m["D"]))] = (p, delta, m)
    for p in sorted(glob.glob(f"{ROOT}/I903-win2/ks_chain2/leg*_ks*/anm_pin3_D*.npz")):
        delta, m = load(p)
        D = str(m.get("D_str", m["D"]))
        rel = os.path.relpath(p, ROOT)
        if D not in leg8:
            print(f"{rel}: D {D} (ks {m['ks']}): no leg 8 state with this D string")
            continue
        q, d250, m250 = leg8[D]
        s1 = sigma(f"ks{m['ks']}_D{float(D):.4f}")
        s0 = sigma(f"ks{m250['ks']}_D{float(D):.4f}")
        print(f"D {D}: ks {m['ks']} {rel}\n   against ks {m250['ks']} {os.path.relpath(q, ROOT)} (D_str {m250.get('D_str')})")
        print(f"   Delta(D) {fmt(delta)} (ks {m['ks']}) minus {fmt(d250)} (ks {m250['ks']}) = {float(delta - d250):+.4e}")
        if s0 and s1:
            print(f"   sigma_Delta {s1[0]:.10e} against {s0[0]:.10e}: {s1[0] / s0[0] - 1:+.3e} relative ({s1[0] - s0[0]:+.3e} absolute); "
                  f"sigma_pair {s1[1]:.6e} against {s0[1]:.6e}: {s1[1] / s0[1] - 1:+.3e} relative")


def selftest():
    a, b = Fraction(3, 2), Fraction(3, 2) + Fraction(1, 10 ** 18)
    ok = float(b - a) == 1e-18 and float(Fraction(1.0) + Fraction(2.0 ** -60) - Fraction(1.0)) == 2.0 ** -60
    print("selftest:", "pass" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        ROOT = sys.argv[1]
    main()
