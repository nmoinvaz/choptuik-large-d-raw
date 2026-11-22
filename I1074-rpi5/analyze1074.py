#!/usr/bin/env python3
"""I1074: where is the +2.5e-6 step between Ecker et al.'s 512-mode Delta and ours at D 3.2?

    python3 -I analyze1074.py ECC CODE [--mutate=shift|trend]

ECC   clone of github.com/EckerChristian/CriticalSpacetimeCrystal (data only, none of its code runs)
CODE  checkout of main (hp/data)

Exit 0: acceptance passes. Exit 1: it fails, or a mutation fired as it must (shift: ours + 1e-6 at D 3.7 fails acceptance 1;
trend: d(3.2) x 3 makes the verdict not "theirs"). Exit 2: a mutation did not fire. Exit 3: an error.
"""
import csv
import glob
import json
import math
import os
import sys

ECC, CODE = sys.argv[1:3]
MUT = next((a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")), None)
FD = os.path.join(ECC, "complete_data", "FortranData")
KEYS17 = ["ny", "dim", "xleft", "xmid", "xright", "eps", "errmax", "verbose", "slowerr", "outevery", "useloggrid", "nleft", "nright", "tol", "tstep", "crit", "debug"]
KEYS16 = [k for k in KEYS17 if k != "useloggrid"]


def num(t):
    try:
        return float(t.lower().replace("d", "e"))
    except ValueError:
        return t


def par(path):
    vals = [l.split()[0] for l in open(path) if l.strip()]
    keys = KEYS17 if len(vals) == 17 else KEYS16
    assert len(vals) == len(keys), (path, len(vals))
    return dict(zip(keys, [num(v) for v in vals]))


def first(path):
    return float(open(path).read().split()[0])


def lagr(xs, ys, x):
    s = 0.0
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        t = yi
        for j, xj in enumerate(xs):
            if j != i:
                t *= (x - xj) / (xi - xj)
        s += t
    return s


def loo(xs, ys, i):
    """leave-one-out cubic residual at point i: y_i - cubic through the 2+2 nearest bracketing others ('x' if one-sided)"""
    lo = [j for j in range(len(xs)) if j < i][-2:]
    hi = [j for j in range(len(xs)) if j > i][:2]
    side = "b"
    if len(lo) < 2 or len(hi) < 2:
        side = "x"
        others = sorted((j for j in range(len(xs)) if j != i), key=lambda j: abs(xs[j] - xs[i]))[:4]
    else:
        others = lo + hi
    return ys[i] - lagr([xs[j] for j in others], [ys[j] for j in others], xs[i]), side


def their_runs():
    runs = {}
    for d in glob.glob(os.path.join(FD, "dim*")):
        D = round(float(os.path.basename(d)[3:]), 6)
        r = {}
        for res in ("128", "256", "512"):
            p = os.path.join(d, res, "Delta.out")
            if os.path.exists(p):
                r[res] = (first(p), par(os.path.join(d, res, "shoot_inner.par")), os.path.relpath(p, ECC))
        runs[D] = r
    return runs


def our_points():
    dd = {}
    for r in csv.DictReader(open(os.path.join(CODE, "hp", "data", "delta_dd.csv"))):
        dd[round(float(r["D"]), 6)] = r
    return dd


def our_records():
    recs = {}
    for fn in sorted(glob.glob(os.path.join(CODE, "hp", "data", "**", "*.jsonl"), recursive=True)):
        for l in open(fn):
            l = l.strip()
            if not l.startswith("{"):
                continue
            try:
                r = json.loads(l)
            except ValueError:
                continue
            D = r.get("D")
            if isinstance(D, (int, float)) and "Delta" in r and r.get("M") is not None and r.get("converged", True):
                recs.setdefault(round(D, 6), set()).add((r["M"], r["Delta"] + r.get("Delta_lo", 0.0), r.get("F"), os.path.relpath(fn, CODE)))
    return recs


def main():
    runs = their_runs()
    dd = our_points()
    ours = {D: float(r["Delta_hi"]) + float(r["Delta_lo"]) for D, r in dd.items()}
    DL = {round(float(a), 6): float(b) for a, b in (l.split() for l in open(os.path.join(ECC, "complete_data", "DeltaList.dat")) if l.strip())}
    for D, r in runs.items():
        if "512" in r and D in DL:
            assert abs(r["512"][0] - DL[D]) < 2e-12, D

    # ---- acceptance
    rows37 = [r for r in csv.DictReader(open(os.path.join(CODE, "hp", "data", "delta_dd_lowD.csv"))) if round(float(r["D"]), 6) == 3.7]
    m80 = [r for r in rows37 if int(r["M"]) == 80][0]
    o37 = float(m80["Delta_hi"]) + float(m80["Delta_lo"])
    if MUT == "shift":
        o37 += 1e-6
    t37 = runs[3.7]["512"][0]
    d37 = t37 - o37
    ok1 = abs(d37) <= 1e-7
    d32 = runs[3.2]["512"][0] - ours[3.2]
    ok2 = 2.45e-6 <= d32 < 2.55e-6
    print(f"ACCEPTANCE 1, D 3.7: theirs 512 {t37:.12f} ({runs[3.7]['512'][2]}), ours M 80 {o37:.12f}, diff {d37:+.2e}  {'ok' if ok1 else 'FAIL'} (bar 1e-7)")
    print(f"ACCEPTANCE 2, D 3.2: theirs 512 {runs[3.2]['512'][0]:.12f}, ours {ours[3.2]:.12f} (M 192), theirs - ours {d32:+.3e}  {'ok' if ok2 else 'FAIL'} (in [2.45e-6, 2.55e-6))")
    print(f"  mutation: {MUT or 'off'}\n")

    # ---- 1. their side
    Ds = sorted(D for D in runs if 3.1 - 1e-9 <= D <= 3.3 + 1e-9)
    print("1. THEIR RUNS, D 3.1 to 3.3 (Delta.out of FortranData/dim<D>/<res>/; 512-mode neighbours differences and divided second differences)")
    print("      D       Delta(128)      Delta(256)      Delta(512)     512 - prev D  slope(512)  2nd diff(512)")
    prev = prev2 = None
    sec = {}
    for D in Ds:
        r = runs[D]
        v = [r[x][0] if x in r else None for x in ("128", "256", "512")]
        f = lambda x: f"{x:.12f}" if x is not None else " " * 14
        dif = slp = s2 = ""
        if prev is not None and v[2] is not None and prev[1] is not None:
            dif = f"{v[2] - prev[1]:+.6e}"
            slp = f"{(v[2] - prev[1]) / (D - prev[0]):+.5f}"
            if prev2 is not None:
                # divided second difference f[x0,x1,x2]
                x0, y0 = prev2
                x1, y1 = prev[0], prev[1]
                s2v = ((v[2] - y1) / (D - x1) - (y1 - y0) / (x1 - x0)) / (D - x0)
                s2 = f"{s2v:+.4f}"
                sec[D] = s2v
        print(f"{D:8.4f}  {f(v[0])}  {f(v[1])}  {f(v[2])}  {dif:>13} {slp:>11} {s2:>11}")
        if v[2] is not None:
            prev2 = (prev[0], prev[1]) if prev is not None else None
            prev = (D, v[2])
    print()
    print("   settings of their 512-mode runs (shoot_inner.par); a row is printed where a field changes from the previous D")
    pv = None
    for D in Ds:
        if "512" not in runs[D]:
            continue
        p = runs[D]["512"][1]
        cur = {k: v for k, v in p.items() if k != "dim"}
        if pv is None:
            print(f"   {D:7.4f}  " + " ".join(f"{k}={v:g}" if isinstance(v, float) else f"{k}={v}" for k, v in cur.items() if k in ("ny", "xleft", "xmid", "nleft", "nright", "eps", "errmax", "tstep", "useloggrid", "debug")))
        else:
            ch = [f"{k} {pv[k]:g} -> {cur[k]:g}" if isinstance(cur[k], float) else f"{k} {pv[k]} -> {cur[k]}" for k in cur if k in pv and cur[k] != pv[k]]
            if ch:
                print(f"   {D:7.4f}  " + "; ".join(ch))
        pv = cur
    cls = {D: tuple(runs[D]["512"][1][k] for k in ("xleft", "nleft", "nright")) for D in Ds if "512" in runs[D]}
    bounds = [(a, b) for a, b in zip(sorted(cls), sorted(cls)[1:]) if cls[a] != cls[b]]
    print(f"   class (xleft, nleft, nright) changes between D {bounds}")
    c128 = {D: tuple(runs[D][x][1][k] for k in ("xleft", "xmid", "nleft", "nright", "eps", "tstep") for x in ("128", "256") if x in runs[D]) for D in Ds if "128" in runs[D]}
    print(f"   128 and 256 runs, D {min(c128)} to {max(c128)}: {len(set(c128.values()))} distinct setting(s) of (xleft, xmid, nleft, nright, eps, tstep)\n")

    # ---- 2. our side
    print("2. OUR VALUES, D 3.1 to 3.3 (hp/data/delta_dd.csv; the M sequence from every hp/data/**/*.jsonl record of Delta at that D)")
    recs = our_records()
    for D in sorted(d for d in dd if 3.1 - 1e-9 <= d <= 3.3 + 1e-9):
        r = dd[D]
        print(f"  D {D:<8} Delta {ours[D]:.12f}  run {r['run']}  M-difference err {r['Delta_err']} ({r['err_kind']})  F {r['F']}  max dDelta/dF {r['max_dDelta_dF']}")
        seq = {}
        for M, v, F, fn in sorted(recs.get(D, [])):
            seq.setdefault(M, v)
        ms = sorted(seq)
        if ms:
            st = "; ".join(f"M {a}->{b}: {seq[b] - seq[a]:+.2e}" for a, b in zip(ms, ms[1:]))
            print(f"           M sequence (distinct M): " + ", ".join(f"M {m} {seq[m]:.12f}" for m in ms) + (f"\n           steps: {st}" if st else ""))
    print()

    # ---- 3. d(D)
    common = sorted(D for D in ours if D in DL and D <= 3.6 + 1e-9)
    d = {D: DL[D] - ours[D] for D in common}
    if MUT == "trend":
        d[3.2] *= 3
    print("3. d(D) = theirs 512 (DeltaList) - ours, all common D to 3.6")
    last = None
    for D in common:
        ratio = f"  x{abs(d[D] / d[last]):.3g} vs D {last}" if last is not None and d[last] != 0 else ""
        print(f"  D {D:<8} d {d[D]:+.3e}  (our M-difference err {dd[D]['Delta_err']}){ratio}")
        last = D
    jumps = sorted(((abs(d[b] / d[a]), a, b) for a, b in zip(common, common[1:]) if d[a] != 0), reverse=True)
    print(f"  largest jump in |d|: x{jumps[0][0]:.3g} between D {jumps[0][1]} and {jumps[0][2]}; next x{jumps[1][0]:.3g} between {jumps[1][1]} and {jumps[1][2]}")
    a_ok = bool(bounds) and len(bounds) == 1 and bounds[0][0] < jumps[0][2] and bounds[0][1] >= jumps[0][2] and bounds[0][0] >= jumps[0][1]
    print(f"  (a) their 512 settings change between D {bounds[0] if bounds else None}; d jumps between D {jumps[0][1]} and {jumps[0][2]}: {'same interval' if a_ok else 'NOT the same interval'}")
    xs = [3.25, 3.3, 3.35, 3.4, 3.45]
    ys = [math.log(d[x]) for x in xs]
    # quadratic least squares in D - 3.35
    n = len(xs)
    t = [x - 3.35 for x in xs]
    S = [[sum(a ** (i + j) for a in t) for j in range(3)] for i in range(3)]
    bv = [sum(y * a ** i for a, y in zip(t, ys)) for i in range(3)]
    for i in range(3):
        for j in range(i + 1, 3):
            f = S[j][i] / S[i][i]
            S[j] = [sj - f * si for sj, si in zip(S[j], S[i])]
            bv[j] -= f * bv[i]
    c = [0.0] * 3
    for i in reversed(range(3)):
        c[i] = (bv[i] - sum(S[i][j] * c[j] for j in range(i + 1, 3))) / S[i][i]
    pred = math.exp(c[0] + c[1] * (3.2 - 3.35) + c[2] * (3.2 - 3.35) ** 2)
    res = max(abs(y - (c[0] + c[1] * a + c[2] * a * a)) for a, y in zip(t, ys))
    ratio = d[3.2] / pred
    b_ok = 1 / 1.5 <= ratio <= 1.5
    print(f"  (b) ln d quadratic through D {xs} (max fit residual in ln d {res:.2f}) extrapolated to 3.2: {pred:.3e}; d(3.2) {d[3.2]:+.3e}; ratio {ratio:.2f}  {'on trend' if b_ok else 'OFF trend'} (factor 1.5)")
    print(f"      d at 3.175 {d[3.175]:+.2e}: the trend continued to 3.175 would give {math.exp(c[0] + c[1] * (3.175 - 3.35) + c[2] * (3.175 - 3.35) ** 2):.2e}\n")

    # ---- (c) second differences inside each series
    print("(c) LEAVE-ONE-OUT CUBIC RESIDUALS inside each series (bracketing 2+2 nearest others; 'x' = one-sided at an end), D 3.1 to 3.35")
    th = sorted(D for D in runs if "512" in runs[D] and 3.1 - 1e-9 <= D <= 3.35 + 1e-9)
    ox = sorted(D for D in ours if 3.1 - 1e-9 <= D <= 3.35 + 1e-9)
    for name, xs_, ys_ in (("theirs 512", th, [runs[D]["512"][0] for D in th]), ("ours", ox, [ours[D] for D in ox])):
        out = []
        for i, D in enumerate(xs_):
            if 3.14 - 1e-9 <= D <= 3.3 + 1e-9:
                r, side = loo(xs_, ys_, i)
                out.append((D, r, side))
        print(f"  {name} ({len(xs_)} points): " + "  ".join(f"{D:g}:{r:+.1e}{s}" for D, r, s in out))
    print("  A step of 2.5e-6 at a point shows in its residual only if the smooth residual there is well below 2.5e-6: at D 3.2 the sparse neighbours")
    print("  (3.18, 3.25, 3.3 in theirs; 3.175, 3.25, 3.3 in ours) give residuals of order 1e-4 to 1e-2: this test cannot see the step at 3.2.\n")

    # ---- (d) our M sequence
    print("(d) OUR M SEQUENCES: last M step at each D (the M-difference stored with the value)")
    for D in sorted(d_ for d_ in dd if 3.1 - 1e-9 <= d_ <= 3.3 + 1e-9):
        seq = {}
        for M, v, F, fn in sorted(recs.get(D, [])):
            seq.setdefault(M, v)
        ms = sorted(seq)
        if len(ms) >= 2:
            print(f"  D {D:<8} M {ms[-2]}->{ms[-1]}: {seq[ms[-1]] - seq[ms[-2]]:+.2e}  stored err {dd[D]['Delta_err']}")
    d_ok = abs(float(dd[3.2]["Delta_err"])) <= 10 * max(float(dd[x]["Delta_err"]) for x in (3.175, 3.25, 3.3))
    print(f"  D 3.2's stored M difference {dd[3.2]['Delta_err']} is {'within' if d_ok else 'ABOVE'} 10x the largest of its neighbours' (3.175, 3.25, 3.3)\n")

    verdict = "theirs" if (a_ok and b_ok and d_ok) else ("ours" if (not b_ok and not bounds) else "undecided")
    print(f"VERDICT (rule in README): {verdict}  [(a) {a_ok}, (b) {b_ok}, (d) {d_ok}]")
    if MUT == "shift":
        sys.exit(1 if not ok1 else 2)
    if MUT == "trend":
        sys.exit(1 if verdict != "theirs" else 2)
    sys.exit(0 if (ok1 and ok2) else 1)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(3)
