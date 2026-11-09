#!/usr/bin/env python3
"""#266's tables from the records of I266-mac (run from that folder): python3 scripts/tabulate.py > table.txt"""
import json

import mpmath as mp

mp.mp.dps = 40


def rows(path):
    return [json.loads(line) for line in open(path)]


solve = {(r["state"], r["path"]): r for r in rows("states/solve.jsonl")}
qd_all = rows("states/qd.jsonl")
qd = {r["state"]: r for r in qd_all if not r["mutate"]}      # the unmutated polishes
lam = {r["state"]: r for r in rows("lam.jsonl")}
an = rows("analyze.jsonl")
res = rows("lamres.jsonl")


def L(name):
    f = lam[name]["lam_fine"]
    return mp.mpf(f["base"]) + mp.mpf(f["t"])


def s(x, n=3):
    return mp.nstr(x, n, min_fixed=0, max_fixed=0)


print("1. The M 48 solves from the M 32 state (gamma_m48_gap.py solve)")
for (st, p), r in sorted(solve.items()):
    print(f"   D {r['D']:.4f} {p:6s}: |F| start {r['F_start']:.1e}, end {r['F']:.1e}; Delta(48) - Delta(32) "
          f"{r['Delta_diff']:+.3e}")

print("\n2. Both M 48 states on one solver (analyze; A = gamma path, B = R2 path)")
for r in an:
    a, b = r["A_rec"], r["B_rec"]
    print(f"   A {r['A']}: |F| dd {a['F']:.2e} qd {a['F_qd']:.2e}, linearised dDelta {a['est']:+.3e}; "
          f"B: |F| dd {b['F']:.2e} qd {b['F_qd']:.2e}, linearised dDelta {b['est']:+.3e}")
    print(f"     |A - B| {r['d_norm']:.2e}, Delta part {r['d_Delta']:+.3e}; Newton step at A vs -(A - B): cosine "
          f"{r['newtonA_cos_minus_d']:.13f}, length ratio {r['newtonA_ratio']:.8f}; outside the {r['w']} weakest "
          f"directions {r['outside_weak'] / r['d_norm']:.1e} of |A - B|")
    kk = r.get("p1_harmonics_k")      # the first analysis ran before the harmonics were recorded
    for i in range(6 if kk else 0):
        h = r["p1_harmonics_dirs"][i]
        k = kk[max(range(len(h)), key=lambda j: h[j])]
        print(f"     direction {i}: sigma {r['sigma'][i]:.3e}, p1 harmonic {k}, Delta component "
              f"{r['dir_Delta'][i]:+.2e}, coefficient of A - B {r['coef'][i]:+.3e}, its Delta "
              f"{r['coef'][i] * r['dir_Delta'][i]:+.2e}")
    if r.get("lam_A"):
        print(f"     lam(A) {r['lam_A']!r}, lam(B) {r['lam_B']!r}, difference {r['lam_A'] - r['lam_B']:+.3e}")

print("\n3. Quad-double polish (qd); Delta(start) - Delta(qd)")
for r in qd_all:
    st = r["state"]
    print(f"   {st:32s} M {r['M']} mutate {r['mutate']}: converged {r['converged']}, |F| qd {r['F_qd']:.1e}, "
          f"Newton steps {r['steps'] - (1 if r['converged'] else 0)}; {s(mp.mpf(r['Delta_start']) - mp.mpf(r['Delta_qd']))}")
pairs = [("D 50", "up8_D50.0075_M48_r2.npz", "up8_D50.0075.npz"),
         ("D 58", "up12_D58.0060_M48_r2.npz", "up12_D58.0060.npz")]
for lab, a48, a32 in pairs:
    if a48 in qd and a32 in qd:
        print(f"   {lab}: Delta(48) - Delta(32), both quad-double: {s(mp.mpf(qd[a48]['Delta_qd']) - mp.mpf(qd[a32]['Delta_qd']))}")
g, r_ = "up8_D50.0075_M48_kf13.npz", "up8_D50.0075_M48_r2.npz"
if g in qd and r_ in qd:
    print(f"   D 50: gamma path's polish minus R2 path's, Delta: {s(mp.mpf(qd[g]['Delta_qd']) - mp.mpf(qd[r_]['Delta_qd']))}")

print("\n4. lam (lam: find_lam, then refined in double-double lam)")
for st, r in lam.items():
    print(f"   {st:32s} M {r['M']}: |F| {r['F']:.1e}, linearised dDelta {r['est']:+.1e}, lam {r['lam_fine']['str']}")
for lab, a48, a32 in pairs:
    q48, q32 = a48[:-4] + "_qd.npz", a32[:-4] + "_qd.npz"
    if q48 in lam and q32 in lam:
        print(f"   {lab}: lam(48) - lam(32), quad-double solutions: {s(L(q48) - L(q32))}")
    if a48 in lam and q48 in lam:
        print(f"   {lab}: lam on the dd M 48 state minus on its qd polish: {s(L(a48) - L(q48))}")
    if a32 in lam and q32 in lam:
        print(f"   {lab}: lam on the saved dd M 32 state minus on its qd polish: {s(L(a32) - L(q32))}")

print("\n5. The root's resolution (lamres: root inside base +- h on the state and on copies with relative noise eps)")
for r in res:
    print(f"   {r['state']:32s} M {r['M']} base {r['base']!r}, h {r['h']:.0e}: " + "; ".join(
        f"eps {x['eps']:.0e} {'%+.1e' % x['t'] if x['t'] is not None else '-'}"
        + ("" if x["signs"][0] != x["signs"][1] else " (outside +-h)") for x in r["roots"]))
