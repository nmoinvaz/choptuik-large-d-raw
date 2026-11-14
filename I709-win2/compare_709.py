#!/usr/bin/env python3
"""#709: the A/B of newton_od's full step's drop on chain_nsr's attempts 4 and 5.
    python -I compare_709.py FOLDER          (FOLDER: I709-win2; exit 0 when both pairs pass)
    python -I compare_709.py --selftest
For each attempt (att4, att5), A ran without --od_full_drop and B with 1e-20, one step each from the same base. From each
run's anm_run.jsonl (its step's last attempt) and its saved state anm_pin3_D<D>.npz, a pair passes when (1) both are
accepted at the same D_str, (2) the two states agree in every unknown to 1e-55 (the exact sum of the eight parts,
mpmath at 600 bits), and (3) B's corrector time t_corr is below A's. The octo-double step counts are printed beside.
--selftest: the pair test on planted records and states (equal ones pass; a state off by 1e-54, a different D_str and a
slower B each fail), and must exit 0.
"""
import glob
import json
import os
import sys

import mpmath as mp
import numpy as np

mp.mp.prec = 600
KEYS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")


def exact(z):
    """the exact sum of the eight parts, per unknown"""
    n = len(z[KEYS[0]])
    return [mp.fsum(mp.mpf(float(z[k][i])) for k in KEYS if k in z) for i in range(n)]


def last_attempt(folder):
    p = os.path.join(folder, "anm_run.jsonl")
    if not os.path.exists(p):
        return None
    recs = [json.loads(x) for x in open(p) if x.strip()]
    return recs[-1]["attempts"][-1] if recs and recs[-1].get("attempts") else None


def state(folder):
    s = sorted(glob.glob(os.path.join(folder, "anm_pin3_D*.npz")))
    if not s:
        return None
    d = np.load(s[-1], allow_pickle=False)
    return {k: np.array(d[k]) for k in KEYS if k in d.files}


def pair(ra, rb, za, zb):
    """(passes, reasons, max state difference)"""
    why = []
    if not ra or not rb or not ra.get("accepted") or not rb.get("accepted"):
        why.append("not both accepted")
    elif ra.get("D_str") != rb.get("D_str"):
        why.append("different D_str")
    dmax = None
    if za is None or zb is None:
        why.append("a state is missing")
    else:
        dmax = max(abs(x - y) for x, y in zip(exact(za), exact(zb)))
        if dmax > mp.mpf("1e-55"):
            why.append(f"states differ by {mp.nstr(dmax, 3)}")
    if ra and rb and not rb.get("t_corr", 1e30) < ra.get("t_corr", 0):
        why.append("B is not faster")
    return not why, why, dmax


def main(folder):
    ok = True
    print("| attempt | steps A, B | t_corr A, B (s) | D_str equal | max state difference | verdict |\n|---|---|---|---|---|---|")
    for att in ("att4", "att5"):
        fa, fb = os.path.join(folder, f"{att}_A"), os.path.join(folder, f"{att}_B")
        ra, rb, za, zb = last_attempt(fa), last_attempt(fb), state(fa), state(fb)
        good, why, dmax = pair(ra, rb, za, zb)
        ok &= good
        st = f"{ra.get('steps') if ra else '-'}, {rb.get('steps') if rb else '-'}"
        tc = f"{ra.get('t_corr', float('nan')):.0f}, {rb.get('t_corr', float('nan')):.0f}" if ra and rb else "-"
        eq = bool(ra and rb and ra.get("D_str") == rb.get("D_str"))
        print(f"| {att} | {st} | {tc} | {eq} | {mp.nstr(dmax, 3) if dmax is not None else '-'} | "
              f"{'pass' if good else 'FAIL: ' + '; '.join(why)} |")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def selftest():
    z = {k: np.array([1.0, 2.0]) if k == "zh" else np.zeros(2) for k in KEYS}
    off = {k: v.copy() for k, v in z.items()}
    off["z3"][0] = 1e-54
    r = dict(accepted=True, D_str="254.1", steps=7, t_corr=360.0)
    rb = dict(r, steps=3, t_corr=150.0)
    cases = [("equal pair", pair(r, rb, z, z)[0], True), ("a state off by 1e-54", pair(r, rb, z, off)[0], False),
             ("a different D_str", pair(r, dict(rb, D_str="254.2"), z, z)[0], False),
             ("a slower B", pair(r, dict(rb, t_corr=400.0), z, z)[0], False)]
    bad = 0
    for label, got, want in cases:
        print(f"  {label}: {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    print("selftest", "FAILED" if bad else "passed")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
