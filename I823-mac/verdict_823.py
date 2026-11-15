#!/usr/bin/env python3
"""#823's verdict on the reduced map g along +-e at s0_D252's planted truth (reduced_cubic.py curve --json).

A ray has a root within |c| <= T when, between two neighbouring converged grid points t_i < t_j <= T (t = 0 is g(0)),
every component of g changes sign. Judged at T = 1e-4 (the amended criterion); T = 1e-5 (the issue's literal one) is
reported. The root's Delta is read at t = |a| on the + ray (--curve_t=a): Delta_truth + dlast there, with |g| / |g(0)|.
Within a bracket, t* and Delta* interpolate s(t) = g.g(0) / |g(0)|^2 and dlast linearly (reported, not judged).
usage: python3 verdict_823.py CURVE.json DZ0.npz    (exit 0 when decided on every ray run, 1 when a ray stops
                                                     before 1e-4 without a root; a ray not yet run is reported)
       python3 verdict_823.py --selftest             (planted rays; exit 0 on pass)
       python3 verdict_823.py --selftest --mutate=any   (a root when any component changes sign; must fail)"""
import json
import sys

T_JUDGED, T_LITERAL = 1e-4, 1e-5


def bracket(pts, g0, dl0, mutate=""):
    """pts: [(t, g, dlast)] converged, increasing t. The first neighbouring pair (t = 0 first) across which every
    component of g changes sign: (t_i, t_j, t*, dlast*), or None"""
    seq = [(0.0, g0, dl0)] + list(pts)
    flip = any if mutate == "any" else all
    n0 = sum(x * x for x in g0)
    for (ti, gi, di), (tj, gj, dj) in zip(seq, seq[1:]):
        if flip(x * y < 0 for x, y in zip(gi, gj)):
            si = sum(x * y for x, y in zip(gi, g0)) / n0
            sj = sum(x * y for x, y in zip(gj, g0)) / n0
            f = si / (si - sj) if si != sj else 0.5
            return ti, tj, ti + f * (tj - ti), di + f * (dj - di)
    return None


def judge_ray(pts, g0, dl0, stop, mutate=""):
    """the ray's reading: root within T_JUDGED and T_LITERAL, its bracket, or no root, or undecided (stopped early)"""
    b = bracket(pts, g0, dl0, mutate)
    if b is not None and b[1] <= T_JUDGED:
        return dict(root=True, literal=b[1] <= T_LITERAL, bracket=b, decided=True)
    reached = max((p[0] for p in pts), default=0.0)
    decided = reached >= T_JUDGED * 0.999 or b is not None
    return dict(root=False, literal=False, bracket=b, decided=decided, stop=stop, reached=reached)


def selftest(mutate):
    ta = 1.1e-5
    tp = [1e-24, 1e-6, 1e-5, ta, 1e-4, 1e-3, 3.16e-3, 1e-2]
    tm = [1e-6, 1e-5, 1e-4, 1e-3, 3.16e-3, 1e-2]
    g0 = [1.0, -2.0, 0.5, 3.0]

    def lin(ts, r, sgn, bad=None):
        return [(t, [x * (1 - sgn * t / r) if m != bad else x * (1 + t) for m, x in enumerate(g0)], sgn * t) for t in ts]
    cases = [("root at 1.2e-5 on +", lin(tp, 1.2e-5, 1), (True, False)),
             ("root at 5e-6 on +", lin(tp, 5e-6, 1), (True, True)),
             ("one component never flips", lin(tp, 1.2e-5, 1, bad=2), (False, False)),
             ("root at 3e-4 on +", lin(tp, 3e-4, 1), (False, False)),
             ("root at 2e-5 on -", lin(tm, 2e-5, 1), (True, False)),
             ("no root on - (g grows)", lin(tm, 1.2e-5, -1), (False, False))]
    ok = True
    for name, pts, want in cases:
        r = judge_ray(pts, g0, 0.0, None, mutate)
        got = (r["root"], r["literal"])
        good = got == want
        if name == "root at 1.2e-5 on +" and good:     # t* and dlast* by s(t), linear here: both 1.2e-5
            good = abs(r["bracket"][2] - 1.2e-5) < 1e-12 and abs(r["bracket"][3] - 1.2e-5) < 1e-12
        ok &= good
        print(f"  {name}: root within 1e-4 {got[0]}, within 1e-5 {got[1]} (want {want}){'' if good else '  <- wrong'}")
    print(f"verdict_823 selftest{' --mutate=' + mutate if mutate else ''}: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv):
    if argv and argv[0] == "--selftest":
        mutate = next((a.split("=", 1)[1] for a in argv[1:] if a.startswith("--mutate=")), "")
        return selftest(mutate)
    import mpmath as mp
    import numpy as np
    mp.mp.dps = 60
    rec = json.load(open(argv[0]))
    f = np.load(argv[1])
    D_truth = mp.fsum(mp.mpf(float(f[f"z{q}"][-1])) for q in range(8))
    cv = rec.get("curve", {})
    g0, dl0, na = cv.get("g0"), cv.get("dlast0", 0.0), cv.get("na")
    if g0 is None:
        print("no g(0) in the JSON yet")
        return 1
    print(f"{argv[0]}: |a| {na:.6e}, |g(0)| {sum(x * x for x in g0) ** 0.5:.4e}, Delta_truth {mp.nstr(D_truth, 40)}")
    stop = cv.get("stop", {})
    decided = True
    for sgn, name in ((1, "+"), (-1, "-")):
        allp = [p for p in cv.get("points", []) if p["sgn"] == sgn]
        if not allp:
            print(f"  {name} ray: not yet run")
            continue
        pts = sorted((p["t"], p["g"], p["dlast"]) for p in allp if p["ok"])
        for p in sorted(allp, key=lambda q: q["t"]):
            if p["ok"]:
                s = sum(x * y for x, y in zip(p["g"], g0)) / sum(x * x for x in g0)
                print(f"    {name}t {p['t']:.4e}: g against g(0) {p['signs']}, s {s:+.6e}, dlast {p['dlast']:+.10e}")
            else:
                print(f"    {name}t {p['t']:.4e}: NOT converged")
        r = judge_ray(pts, g0, dl0, stop.get(str(sgn)))
        b = r["bracket"]
        if r["root"]:
            print(f"  {name} ray: ROOT within 1e-4 (within 1e-5: {r['literal']}), every component changes sign in "
                  f"({b[0]:.4e}, {b[1]:.4e}); t* {b[2]:.4e}, Delta* = Delta_truth {b[3]:+.6e}")
        elif r["decided"]:
            print(f"  {name} ray: no root within 1e-4" + ("" if b is None else
                  f" (every component changes sign first in ({b[0]:.4e}, {b[1]:.4e}))"))
        else:
            print(f"  {name} ray: undecided, it reaches t {r['reached']:.4e} and stops at {r['stop']}")
            decided = False
        if sgn == 1 and na:
            pa = next((p for p in allp if p["ok"] and abs(p["t"] / na - 1) < 1e-9), None)
            if pa is not None:
                ga = sum(x * x for x in pa["g"]) ** 0.5 / sum(x * x for x in g0) ** 0.5
                print(f"  at t = |a|: |g| / |g(0)| {ga:.4e}, Delta = Delta_truth {pa['dlast']:+.12e} = "
                      f"{mp.nstr(D_truth + mp.mpf(pa['dlast']), 25)}")
    return 0 if decided else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
