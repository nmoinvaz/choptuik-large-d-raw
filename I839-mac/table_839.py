#!/usr/bin/env python3
"""#839's per-step table and fits for one planted run (NAME.json and NAME.log of octo_corrector.py planted, with
--Delta_ref the truth's Delta).

Per step k: Delta_k - truth before the step (the offset leaves Delta at the truth's value, plant_start moves only
[0, 576), and step j moves it by lam_j dDelta_j, the projection only m_h and a_h), max|F|, |dz|, the smallest pivot,
pivot/|dz| and the accepted lam. Fits (least squares in log10): the lam-1 trials' point max|F| against the move
|dz| (exponent free, then fixed at 4), and the smallest pivot against |dz|.
Check: the summed Delta moves at the end against planted's own Delta - Delta_ref (relative 1e-6), must agree.
usage: python3 table_839.py NAME            (NAME.json and NAME.log; exit 0 when the check passes)
       python3 table_839.py --selftest      (a planted run and planted trials; exit 0 on pass)
       python3 table_839.py --selftest --mutate=lam     (the first step's lam taken as 1; must fail)
       python3 table_839.py --selftest --mutate=power   (the planted trials at exponent 3; must fail)"""
import json
import math
import re
import sys

TRIAL = re.compile(r"^    on (\d+) trial lam (\S+): max\|F\| (\S+); raw \|dz_t\| \S+ vs \|dz\| (\S+)")


def fit(xs, ys, p=None):
    """log10 y = a + p log10 x by least squares (p free when None): (p, 10**a, max |y/fit - 1|)"""
    lx, ly = [math.log10(x) for x in xs], [math.log10(y) for y in ys]
    n = len(lx)
    if p is None:
        mx, my = sum(lx) / n, sum(ly) / n
        p = sum((a - mx) * (b - my) for a, b in zip(lx, ly)) / sum((a - mx) ** 2 for a in lx)
    a = sum(b - p * c for b, c in zip(ly, lx)) / n
    return p, 10 ** a, max(abs(y / (10 ** a * x ** p) - 1) for x, y in zip(xs, ys))


def steps(hist, mutate=""):
    """rows per step: (it, Delta - truth before it, F, dz, piv_min, lam, F_new), and Delta - truth after the last"""
    rows, dD = [], 0.0
    for k, h in enumerate(hist):
        lam = 1.0 if (mutate == "lam" and k == 0) else h.get("lam", 0.0)
        rows.append((h["it"], dD, h["F"], h["dz"], h["piv"][0], lam, h.get("F_new")))
        dD += lam * h["dDelta"]
    return rows, dD


def trials(lines):
    """(step, lam, point max|F|, |dz|) per refused trial printed in the log"""
    return [(int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)))
            for m in map(TRIAL.match, lines) if m]


def report(rec, lines, mutate=""):
    import mpmath as mp
    hist = rec["od"]["hist"]
    rows, dD = steps(hist, mutate)
    print("| step | Delta - truth before | max\\|F\\| | \\|dz\\| | smallest pivot | pivot/\\|dz\\| | accepted lam |")
    print("|---|---|---|---|---|---|---|")
    for it, d, F, dz, pv, lam, Fn in rows:
        print(f"| {it} | {d:+.4e} | {F:.3e} | {dz:.3e} | {pv:.3e} | {pv / dz:.4f} | "
              f"{'none (stopped)' if not lam else ('1' if lam == 1 else f'1/{round(1 / lam)}')} |")
    with mp.workdps(60):
        own = float(mp.mpf(rec["od"]["Delta"]) - mp.mpf(rec["Delta_ref"])) if rec.get("Delta_ref") else None
    print(f"end: Delta - truth {dD:+.6e} summed from the steps; planted's Delta - Delta_ref "
          f"{'none' if own is None else f'{own:+.6e}'}; max|F| {rec['od']['F']:.3e}, converged {rec['od']['converged']}")
    ok = own is not None and abs(dD - own) <= 1e-6 * abs(own)
    print(f"check: the summed Delta moves against planted's own Delta - truth, relative "
          f"{'n/a' if own is None else f'{abs(dD - own) / abs(own):.2e}'} (bound 1e-6): {'pass' if ok else 'FAIL'}")
    tr = trials(lines)
    one = [(dz, F) for _, lam, F, dz in tr if lam == 1]
    if len(one) >= 2:
        p, C, dev = fit(*zip(*one))
        _, C4, dev4 = fit(*zip(*one), p=4)
        print(f"lam-1 trials ({len(one)}): point max|F| = {C:.3e} |dz|^{p:.4f} (max deviation {dev:.2%}); with the "
              f"exponent 4, C = {C4:.4e} (max deviation {dev4:.2%})")
        other = [(lam * dz, F, F / (C4 * (lam * dz) ** 4)) for _, lam, F, dz in tr if lam < 1]
        for m, F, r in other:
            print(f"  shorter trial: move {m:.3e}, point max|F| {F:.3e}, {r:.3f} of C4 move^4")
    acc = [(dz, pv) for _, _, _, dz, pv, lam, _ in rows]
    if len(acc) >= 2:
        q, B, devq = fit(*zip(*acc))
        print(f"smallest pivot = {B:.3e} |dz|^{q:.4f} over {len(acc)} steps (max deviation {devq:.2%})")
    return 0 if ok else 1


def selftest(mutate):
    lam = [1 / 8, 1 / 4, 1 / 4, 1 / 2, 1 / 2]
    dz, hist, D = 2.2e-12, [], 0.0
    for k, l in enumerate(lam):
        hist.append(dict(it=k, F=1.5 * dz, dz=dz, dDelta=-dz, piv=[0.009 * dz, 1.2e36], lam=l, F_new=1.5 * dz * (1 - l)))
        D -= l * dz
        dz *= 1 - l
    import mpmath as mp
    with mp.workdps(60):
        Ds = mp.nstr(mp.mpf("1.6845") + mp.mpf(D), 50)      # the planted end, at 60 digits
    rec = dict(od=dict(hist=hist, Delta=Ds, F=1.5 * dz, converged=False), Delta_ref="1.6845")
    p = 3 if mutate == "power" else 4
    lines = [f"    on {k} trial lam 1: max|F| {5.36e64 * h['dz'] ** p:.3e}; raw |dz_t| 1e12 vs |dz| {h['dz']:.3e} "
             f"(not <); refused, 1 s" for k, h in enumerate(hist)]
    ok = report(rec, lines, mutate) == 0
    pf = fit(*zip(*[(h["dz"], 5.36e64 * h["dz"] ** p) for h in hist]))[0]
    ok &= abs(pf - 4) <= 0.01
    print(f"  the planted exponent recovered: {pf:.4f} (want 4 within 0.01): {'pass' if abs(pf - 4) <= 0.01 else 'FAIL'}")
    print(f"table_839 selftest{' --mutate=' + mutate if mutate else ''}: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv):
    if argv and argv[0] == "--selftest":
        return selftest(next((a.split("=", 1)[1] for a in argv[1:] if a.startswith("--mutate=")), ""))
    with open(argv[0] + ".json") as f:
        rec = json.load(f)
    with open(argv[0] + ".log") as f:
        return report(rec, f.read().splitlines())


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
