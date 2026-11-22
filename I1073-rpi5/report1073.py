#!/usr/bin/env python3
"""I1073: Ecker et al.'s Delta and gamma below D 3.6 beside ours.

    python3 -I report1073.py ECC TABLES CODE RAW [--mutate=shift]

ECC    clone of github.com/EckerChristian/CriticalSpacetimeCrystal (data only, none of its code runs)
TABLES ecker_tables.txt (output of hp/lowD_ecker.py ecc --dmax=4.0)
CODE   checkout of main (hp/data/delta_all.csv, hp/data/delta_dd_lowD.csv)
RAW    raw-data clone (I1070-* gamma records)

Exit 0: the D 3.7 acceptance passes. Exit 1: it fails, or (with --mutate=shift) the mutation fires as it must.
Exit 2: --mutate=shift did not fire. Exit 3: an error. The tables are printed in every case.
"""
import csv
import glob
import json
import math
import os
import sys

ECC, TABLES, CODE, RAW = sys.argv[1:5]
MUT = "--mutate=shift" in sys.argv
TOL = 1e-7
SEL_G = [3.0444, 3.0475, 3.15, 3.425, 3.475, 3.5]


def parse_tables():
    """fixed columns of lowD_ecker.py's two tables (Delta: 14-wide, gamma: 11-wide), checked against the list column"""
    dl, gm = {}, {}
    sect = None
    for line in open(TABLES):
        if line.startswith("     D     Delta(128)"):
            sect = "d"
            continue
        if line.startswith("gamma by number"):
            sect = "g"
            continue
        if line.startswith("ours against"):
            break
        if sect is None or not line.strip():
            continue
        D = float(line[:8])
        if sect == "d":
            cols = [line[a:b].strip() for a, b in ((10, 24), (26, 40), (42, 56), (58, 72))]
            lst = float(line.split()[-1])
            dl[round(D, 6)] = ([float(c) if c else None for c in cols], lst)
        else:
            cols = [line[a:b].strip() for a, b in ((10, 21), (23, 34), (36, 47), (49, 60))]
            lst = float(line.split()[-1])
            gm[round(D, 6)] = ([float(c) if c else None for c in cols], lst)
    return dl, gm


def lagr(xs, ys, x):
    s = 0.0
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        t = yi
        for j, xj in enumerate(xs):
            if j != i:
                t *= (x - xj) / (xi - xj)
        s += t
    return s


def interp_spread(tab, D, xf=lambda k: k):
    """estimates at off-grid D: cubic through the 2+2 bracketing points, cubic through the 4 nearest, and quartics
    through 2+3 and 3+2 bracketing points, as a function of x = xf(D); (min, max, list). Interpolation spread, not a bound."""
    ks = sorted(tab)
    lo = [k for k in ks if k <= D]
    hi = [k for k in ks if k >= D]
    if not lo or not hi:
        return None
    if lo[-1] == D:
        return tab[D], tab[D], [tab[D]]
    sets = [lo[-2:] + hi[:2], sorted(sorted(ks, key=lambda k: abs(k - D))[:4]), lo[-2:] + hi[:3], lo[-3:] + hi[:2]]
    est = [lagr([xf(k) for k in s], [tab[k] for k in s], xf(D)) for s in sets if len(s) >= 4 and s[0] <= D <= s[-1]]  # extrapolating sets dropped
    return min(est), max(est), est


def ours_tables():
    dd, gg = {}, {}
    for r in csv.DictReader(open(os.path.join(CODE, "hp", "data", "delta_all.csv"))):
        if r["kind"] == "dd":
            dd[round(float(r["D"]), 6)] = (float(r["Delta_q0"]) + float(r["Delta_q1"]), r["err"], r["source"])
    best = {}
    for r in csv.DictReader(open(os.path.join(CODE, "hp", "data", "delta_dd_lowD.csv"))):
        if r["gamma"] and r["status"] == "clean":
            D, M = round(float(r["D"]), 6), int(r["M"])
            best.setdefault(D, {})[M] = (float(r["gamma"]), "hp/data/delta_dd_lowD.csv")
    for fn in glob.glob(os.path.join(RAW, "I1070-*", "lowD_gamma_D*_M*.jsonl")):
        for l in open(fn):
            if l.strip():
                r = json.loads(l)
                if r.get("gamma") and r.get("n_signchanges") == 1:
                    best.setdefault(round(r["D"], 6), {})[r["M"]] = (r["gamma"], os.path.relpath(fn, RAW))
    for D, m in best.items():
        gg[D] = m
    return dd, gg


def fmt(x, n=10):
    return "-" if x is None else f"{x:.{n}f}"


def main():
    dl, gm = parse_tables()
    DL = {round(float(a), 6): float(b) for a, b in (l.split() for l in open(os.path.join(ECC, "complete_data", "DeltaList.dat")) if l.strip())}
    GL = {round(float(a), 6): float(b) for a, b in (l.split() for l in open(os.path.join(ECC, "complete_data", "GammaList.dat")) if l.strip())}
    for D, (v, lst) in dl.items():
        if v[2] is not None:
            assert abs(v[2] - lst) < 2e-12, (D, v, lst)
    for D, (v, lst) in gm.items():
        if v[2] is not None and lst == lst:
            assert abs(v[2] - lst) < 2e-9, (D, v, lst)
    dd, gg = ours_tables()
    print(f"parsed: {len(dl)} Delta rows ({sum(1 for v in dl.values() if v[0][0] is not None)} with 128, "
          f"{sum(1 for v in dl.values() if v[0][1] is not None)} with 256, {sum(1 for v in dl.values() if v[0][2] is not None)} with 512, "
          f"{sum(1 for v in dl.values() if v[0][3] is not None)} with 1024); {len(gm)} gamma rows "
          f"({sum(1 for v in gm.values() if v[0][2] is not None)} with 512, {sum(1 for v in gm.values() if v[0][0] is not None or v[0][1] is not None or v[0][3] is not None)} with another resolution)")
    print(f"their lists: DeltaList {len(DL)} entries, D {min(DL)} to {max(DL)}; GammaList {len(GL)} entries, D {min(GL)} to {max(GL)}\n")

    # ---- acceptance at D 3.7
    rows37 = [r for r in csv.DictReader(open(os.path.join(CODE, "hp", "data", "delta_dd_lowD.csv")))
              if round(float(r["D"]), 6) == 3.7 and r["gamma"] and r["status"] == "clean"]
    bestM = max(int(r["M"]) for r in rows37)
    row = [r for r in rows37 if int(r["M"]) == bestM][0]
    d_ours = float(row["Delta_hi"]) + float(row["Delta_lo"])
    g_ours = float(row["gamma"])
    assert abs(d_ours - 3.4652004835) < 1e-9 and abs(g_ours - 0.3486501896) < 1e-9, "ours differs from LOW_D.md 5"
    if MUT:
        d_ours += 1e-6
        g_ours += 1e-6
    d_th, g_th = dl[3.7][0][2], gm[3.7][0][2]
    res_note = "512 modes (FortranData has no 1024 directory)"
    dd37, gg37 = d_th - d_ours, g_th - g_ours
    ok = abs(dd37) <= TOL and abs(gg37) <= TOL
    print("ACCEPTANCE at D 3.7 (|theirs - ours| <= 1e-7, theirs = highest resolution = " + res_note + f", ours = M {bestM}, dd)")
    print(f"  Delta  theirs {d_th:.12f}  ours {d_ours:.12f}  diff {dd37:+.2e}  {'ok' if abs(dd37) <= TOL else 'FAIL'}")
    print(f"  gamma  theirs {g_th:.9f}  ours {g_ours:.10f}  diff {gg37:+.2e}  {'ok' if abs(gg37) <= TOL else 'FAIL'}")
    print(f"  mutation shift: {'on (ours + 1e-6)' if MUT else 'off'}\n")

    # ---- per-resolution table, D <= 3.6
    print("THEIR Delta PER RESOLUTION, D <= 3.6 (FortranData; 1024 does not exist there), and the change between resolutions")
    print("      D   Delta(128)    Delta(256)    Delta(512)     256-128    512-256   ratio  | gamma(512)  [no gamma at 128/256]")
    for D in sorted(dl):
        if D > 3.6 + 1e-9:
            continue
        v = dl[D][0]
        c1 = v[1] - v[0] if v[0] is not None and v[1] is not None else None
        c2 = v[2] - v[1] if v[1] is not None and v[2] is not None else None
        rr = c2 / c1 if c1 and c2 else None
        g = gm.get(D, ([None] * 4, float("nan")))[0][2]
        print(f"{D:8.4f} {fmt(v[0], 9):>13} {fmt(v[1], 9):>13} {fmt(v[2], 9):>13} "
              f"{('%+.1e' % c1) if c1 is not None else '-':>10} {('%+.1e' % c2) if c2 is not None else '-':>10} "
              f"{('%+.1f' % rr) if rr is not None else '-':>7}  | {fmt(g, 9)}")
    n128 = sum(1 for D, v in dl.items() if D <= 3.6 + 1e-9 and v[0][0] is not None)
    n512 = sum(1 for D, v in dl.items() if D <= 3.6 + 1e-9 and v[0][2] is not None)
    print(f"rows D <= 3.6: {sum(1 for D in dl if D <= 3.6 + 1e-9)}; with 128: {n128}; with 512: {n512}; any gamma at 128/256/1024: "
          f"{sum(1 for D, v in gm.items() if v[0][0] is not None or v[0][1] is not None or v[0][3] is not None)}\n")

    # ---- C++ data (CppData, JSON): 512 -> 1024 modes below D 3.1, and Fortran against C++ at 512
    cpp = {}
    for fn in sorted(glob.glob(os.path.join(ECC, "complete_data", "CppData", "*.json"))):
        d = json.load(open(fn))
        for k, v in d.items():
            cpp.setdefault(os.path.basename(fn), {})[round(float(k), 6)] = (v["Ntau"], v["Initial_Conditions"]["Delta"], v["Converged"], v["mismatchNorm"])
    crit = {round(float(k), 6): (v["Ntau"], v["Initial_Conditions"]["Delta"], v["Converged"]) for k, v in json.load(open(os.path.join(ECC, "complete_data", "critcoll_data.json"))).items()}
    n2 = sorted(D for D, v in crit.items() if v[0] == 2048)
    print("THEIR C++ DATA (CppData, critcoll_data.json: Delta in Initial_Conditions; no gamma; Ntau = 2 x Fourier modes)")
    print(f"  critcoll_data.json: {len(crit)} D, Ntau 2048 (1024 modes) at {len(n2)} D from {n2[0]} to {n2[-1]}, Ntau 1024 (512 modes) above; all converged: {all(v[2] for v in crit.values())}")
    a, b = cpp["simulation_data_512.json"], cpp["data_lowD_1024_1.json"]
    print("  512 -> 1024 modes (simulation_data_512.json against data_lowD_1024_1.json), common D:")
    for D in sorted(set(a) & set(b)):
        print(f"    D {D:.4f}: Delta(512) {a[D][1]:.12f}  Delta(1024) {b[D][1]:.12f}  1024-512 {b[D][1] - a[D][1]:+.2e}")
    meta = {round(float(k), 6): v for k, v in json.load(open(os.path.join(ECC, "complete_data", "critcoll_data.json"))).items()}
    nocopy = sorted(D for D, v in meta.items() if v["mismatchNorm"] < 1.0)
    copies = sorted(D for D, v in meta.items() if v["mismatchNorm"] == 1.0)
    print(f"  critcoll_data.json entries with mismatchNorm 1.0, IterNewton 0, PrecisionNewton 0.1 (no C++ solve): {len(copies)} of {len(meta)}, "
          f"D {copies[0]} to {copies[-1]}; entries with a solve: {len(nocopy)}, D {nocopy[0]} to {nocopy[-1]}")
    cp = [D for D in copies if D in dl and dl[D][0][2] is not None]
    dcp = [meta[D]["Initial_Conditions"]["Delta"] - dl[D][0][2] for D in cp]
    print(f"  the no-solve entries against the Fortran 512 value: {len(cp)} common D, max |diff| {max(abs(x) for x in dcp):.1e} "
          f"(equal to 12 digits: they are not an independent check)")
    for D in sorted(set(nocopy) & set(dl)):
        if dl[D][0][2] is not None:
            print(f"  solved C++ entry against Fortran 512 at D {D}: Delta C++ {meta[D]['Initial_Conditions']['Delta']:.12f} (Ntau {meta[D]['Ntau']}, mismatch {meta[D]['mismatchNorm']:.1e}) "
                  f"Fortran {dl[D][0][2]:.12f} diff {meta[D]['Initial_Conditions']['Delta'] - dl[D][0][2]:+.2e}")
    print()

    # ---- gamma beside ours
    print("THEIR GAMMA BESIDE OURS (their gamma: 512 modes, GammaList; off-grid: interpolation spread of up to 4 Lagrange choices that bracket D, not a bound)")
    gk = sorted(GL)
    for D in SEL_G:
        lo = [k for k in gk if k <= D]
        hi = [k for k in gk if k >= D]
        s = f"D {D}: "
        lo_hi = lo_hi_l = lo_hi_d = None
        if lo and abs(lo[-1] - D) < 1e-9:
            s += f"on their grid: {GL[lo[-1]]:.9f}"
            lo_hi = lo_hi_l = lo_hi_d = (GL[lo[-1]], GL[lo[-1]])
        elif lo and hi:
            sp = interp_spread(GL, D)
            s += f"between their {lo[-1]} ({GL[lo[-1]]:.9f}) and {hi[0]} ({GL[hi[0]]:.9f}); interpolated in D {sp[0]:.7f} to {sp[1]:.7f} (spread {sp[1] - sp[0]:.1e})"
            lo_hi = (sp[0], sp[1])
            sl = interp_spread(GL, D, lambda k: math.log(k - 3))
            s += f"\n      in ln(D-3): {sl[0]:.7f} to {sl[1]:.7f} (spread {sl[1] - sl[0]:.1e})"
            s += "\n      the bracketing choices (cubic 2+2, cubic 4 nearest if it brackets, quartic 2+3, quartic 3+2), in D: " + ", ".join(f"{e:.7f}" for e in sp[2]) + "; in ln(D-3): " + ", ".join(f"{e:.7f}" for e in sl[2])
            DLx = DL if D not in DL else DL
            dD = dl[round(D, 6)][0][2] if round(D, 6) in dl and dl[round(D, 6)][0][2] is not None else None
            if dD is not None:
                DLm = dict(DL)
                DLm[round(D, 6)] = dD
                sd = interp_spread(GL, D, lambda k: DLm[round(k, 6)] if round(k, 6) in DLm else float("nan"))
                s += f"\n      in their Delta (Delta(D) {dD:.9f}, on their grid): {sd[0]:.7f} to {sd[1]:.7f} (spread {sd[1] - sd[0]:.1e})"
                lo_hi_d = (sd[0], sd[1])
            else:
                lo_hi_d = None
            lo_hi_l = (sl[0], sl[1])
        else:
            s += f"no data below D {hi[0]}: nearest {hi[0]} gamma {GL[hi[0]]:.9f}, {hi[0] - D:.4f} away"
            lo_hi = None
        near = [(k, m) for k, m in gg.items() if abs(k - D) < 1e-9]
        if near:
            m = max(near[0][1])
            gv = near[0][1][m][0]
            s += f"\n      ours M {m}: {gv:.10f}"
            if len(near[0][1]) > 1:
                m2 = sorted(near[0][1])[-2]
                s += f" (M {m2}: {near[0][1][m2][0]:.10f}, step {gv - near[0][1][m2][0]:+.1e})"
            if lo_hi:
                s += f"; theirs - ours: in D {lo_hi[0] - gv:+.2e} to {lo_hi[1] - gv:+.2e}"
                s += f", in ln(D-3) {lo_hi_l[0] - gv:+.2e} to {lo_hi_l[1] - gv:+.2e}"
                if lo_hi_d:
                    s += f", in Delta {lo_hi_d[0] - gv:+.2e} to {lo_hi_d[1] - gv:+.2e}"
        print("  " + s)
    print("  their gamma against ours at every common D <= 3.7 (theirs 512 modes; ours the highest M; M step = highest minus next lower M)")
    for D in sorted(gg):
        if D in GL and D <= 3.7 + 1e-9:
            Ms = sorted(gg[D])
            gv = gg[D][Ms[-1]][0]
            step = f"{gv - gg[D][Ms[-2]][0]:+.1e}" if len(Ms) > 1 else "no lower M"
            print(f"    D {D:<6} theirs {GL[D]:.9f}  ours M {Ms[-1]} {gv:.10f}  theirs - ours {GL[D] - gv:+.2e}  (M step {step})")
    print("  power-law extrapolation of their gamma to D 3.0444 and 3.0475 (ln gamma against ln(D - 3), their D in [3.1, 3.2]; extrapolation, NOT data):")
    pts = [(k, GL[k]) for k in gk if 3.1 - 1e-9 <= k <= 3.2 + 1e-9]
    xs = [math.log(k - 3) for k, _ in pts]
    ys = [math.log(g) for _, g in pts]
    n = len(xs)
    for deg in (1, 2):
        # least squares by normal equations
        A = [[sum(x ** (i + j) for x in xs) for j in range(deg + 1)] for i in range(deg + 1)]
        bb = [sum(y * x ** i for x, y in zip(xs, ys)) for i in range(deg + 1)]
        for i in range(deg + 1):
            piv = A[i][i]
            for j in range(i + 1, deg + 1):
                f = A[j][i] / piv
                A[j] = [aj - f * ai for aj, ai in zip(A[j], A[i])]
                bb[j] -= f * bb[i]
        c = [0.0] * (deg + 1)
        for i in reversed(range(deg + 1)):
            c[i] = (bb[i] - sum(A[i][j] * c[j] for j in range(i + 1, deg + 1))) / A[i][i]
        ev = lambda D: math.exp(sum(ci * math.log(D - 3) ** i for i, ci in enumerate(c)))
        print(f"    degree {deg} ({n} points): gamma(3.0444) {ev(3.0444):.5f}, gamma(3.0475) {ev(3.0475):.5f}, local exponent at D 3.1 "
              f"{c[1] + (2 * c[2] * math.log(0.1) if deg == 2 else 0):.3f}")
    print()

    # ---- Delta near 3.04375 and 3.0475
    print("THEIR DELTA (DeltaList: C++, 1024 modes below D 3.097) BESIDE OURS (hp/data/delta_all.csv, dd)")
    dk = sorted(DL)
    print(f"  their lowest D {dk[0]}; ours at 3.04375 {dd[3.04375][0]:.12f} (err {dd[3.04375][1]}), at 3.0475 {dd[3.0475][0]:.12f} (err {dd[3.0475][1]})")
    print(f"  D 3.0475: theirs {DL[3.0475]:.12f}  ours {dd[3.0475][0]:.12f}  theirs - ours {DL[3.0475] - dd[3.0475][0]:+.2e}")
    near = [k for k in dk if k >= 3.04375][:4]
    ex = lagr(near, [DL[k] for k in near], 3.04375)
    print(f"  D 3.04375 is {dk[0] - 3.04375:.5f} below their lowest D: no data. Cubic extrapolation from their {near}: {ex:.9f}, ours {dd[3.04375][0]:.9f}, "
          f"extrapolation - ours {ex - dd[3.04375][0]:+.1e} (extrapolation, NOT data)")
    com = sorted(D for D in dd if D in DL and D <= 3.6 + 1e-9)
    print(f"  all common D <= 3.6 ({len(com)}): theirs - ours")
    for D in com:
        t = DL[D]
        print(f"    D {D:<9} theirs {t:.12f}  ours {dd[D][0]:.12f}  diff {t - dd[D][0]:+.2e}  (our err {dd[D][1]})")
    print()

    # ---- Delta/(2 gamma)
    print("Delta/(2 gamma) FROM THEIR DATA AGAINST D (Delta: DeltaList, gamma: GammaList, both 512 modes at D >= 3.097)")
    print("      D     Delta       gamma     Delta/(2 gamma)   dln(gamma)/dln(Delta) to the row above")
    rows = [(D, DL[D], GL[D]) for D in gk if D in DL and D <= 4.0 + 1e-9]
    prev = None
    keep = [D for D in gk if D in DL and (D <= 3.6 + 1e-9 or D in (3.7, 3.8, 3.9, 4.0))]
    last = None
    rs = []
    for D in keep:
        R = DL[D] / (2 * GL[D])
        rs.append((D, R))
        sl = ""
        if last is not None and abs(D - last) > 0.009:
            sl = f"{math.log(GL[D] / GL[last]) / math.log(DL[D] / DL[last]):.3f}"
        if last is None or abs(D - last) > 0.009:
            print(f"{D:8.4f} {DL[D]:11.6f} {GL[D]:11.7f} {R:12.6f}      {sl}")
            last = D
    nonmono = sum(1 for (d1, r1), (d2, r2) in zip(rs, rs[1:]) if r2 > r1)
    print(f"  grid points D <= 4: {len(rs)}; adjacent pairs where R rises with D: {nonmono}")
    print(f"  R(3.1) {DL[3.1] / (2 * GL[3.1]):.4f}, R(3.14) {DL[3.14] / (2 * GL[3.14]):.4f}, R(3.2) {DL[3.2] / (2 * GL[3.2]):.4f}, R(3.5) {DL[3.5] / (2 * GL[3.5]):.4f}, "
          f"R(4.0) {DL[4.0] / (2 * GL[4.0]):.4f}")

    if MUT:
        sys.exit(1 if not ok else 2)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(3)
