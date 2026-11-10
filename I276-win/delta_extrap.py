"""#276 acceptance: a saved state's Delta against the degree-5 extrapolation of the chain's previous six Delta.

    python3 delta_extrap.py RAW CHAIN TARGET_D [--unit] [--mutate=shift=X] [--methodcheck]

CHAIN is d6 or d10. The saved states of I215-win/chain_CHAIN/ and I276-win/chain_CHAIN/ give (D, Delta), Delta the last
entry of the state's parts summed exactly (mpmath, 60 digits). The six saved states with the largest D below TARGET_D
(--unit: the six at integer spacing ending at 214.5, so the extrapolation distance is the 0.5 of #215's checks) give the
interpolating polynomial of degree 5, evaluated at TARGET_D. The check passes when |Delta - extrapolation| < 1e-12.
--mutate=shift=X adds X to the target's Delta first (the control: 1e-11 must fail). --methodcheck prints the same
difference for the saved states D 209 to 214.5, whose previous six are all in the chain (#215 reported 3.6e-13 to 4.9e-13).
Exits 1 when the check fails."""
import glob
import json
import os
import re
import sys

import mpmath as mp
import numpy as np

mp.mp.dps = 60
TOL = mp.mpf("1e-12")


def load(raw, chain):
    out = {}
    for sub in ("I215-win", "I276-win"):
        for p in glob.glob(os.path.join(raw, sub, f"chain_{chain}", "anm_pin3_D*.npz")):
            d = np.load(p, allow_pickle=True)
            m = json.loads(str(d["meta"]))
            parts = [k for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7") if k in d]
            delta = mp.fsum(mp.mpf(float(d[k][-1])) for k in parts)
            out[mp.mpf(m["D_str"])] = (delta, os.path.relpath(p, raw).replace("\\", "/"), len(parts))
    return out


def extrap(pts, x):
    """Lagrange interpolation through pts [(x_i, y_i)] evaluated at x"""
    s = mp.mpf(0)
    for i, (xi, yi) in enumerate(pts):
        t = yi
        for j, (xj, _) in enumerate(pts):
            if j != i:
                t *= (x - xj) / (xi - xj)
        s += t
    return s


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    raw, chain, target = args[0], args[1], mp.mpf(args[2])
    shift = mp.mpf(0)
    for a in argv:
        if a.startswith("--mutate=shift="):
            shift = mp.mpf(a.split("=", 2)[2])
    states = load(raw, chain)
    Ds = sorted(states)
    if "--methodcheck" in argv:
        for D in [d for d in Ds if 209 <= d <= mp.mpf("214.5")]:
            prev = [d for d in Ds if d < D][-6:]
            e = extrap([(d, states[d][0]) for d in prev], D)
            print(f"  {chain} D {mp.nstr(D, 8):>9}: previous six D {mp.nstr(prev[0], 6)}..{mp.nstr(prev[-1], 6)}, "
                  f"|Delta - extrapolation| {mp.nstr(abs(states[D][0] - e), 3)}")
        return 0
    if target not in states:
        raise SystemExit(f"no saved state at D {target} for {chain}")
    if "--unit" in argv:
        prev = [mp.mpf("214.5") - k for k in range(6)][::-1]
        prev = [d for d in prev if d in states]
    else:
        prev = [d for d in Ds if d < target][-6:]
    assert len(prev) == 6, prev
    e = extrap([(d, states[d][0]) for d in prev], target)
    dl = states[target][0] + shift
    diff = abs(dl - e)
    ok = diff < TOL
    print(f"{chain} D {mp.nstr(target, 8)}: Delta {mp.nstr(dl, 25)} ({states[target][1]}, {states[target][2]} parts)")
    print(f"  previous six D: {', '.join(mp.nstr(d, 7) for d in prev)}")
    print(f"  degree-5 extrapolation {mp.nstr(e, 25)}")
    print(f"  |Delta - extrapolation| {mp.nstr(diff, 3)} {'<' if ok else '>='} 1e-12: {'ok' if ok else 'FAIL'}"
          + (f"  (mutate shift {mp.nstr(shift, 3)})" if shift else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
