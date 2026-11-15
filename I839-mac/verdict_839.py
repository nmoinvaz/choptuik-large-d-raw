#!/usr/bin/env python3
"""#839's verdict on planted's runs at s0_D252 in the chain's own system (A_s1, B_s1, A_s2, B_s2 .json, --out of
octo_corrector.py planted with --Delta_ref the truth's Delta).

Per run: pass when the corrector converged with pinned max|F| below 1e-40 within 12 steps and |Delta - Delta_truth|
<= 1e-30 (planted's own dDelta against --Delta_ref); otherwise the step where it stopped, with its trials' count. Per
arm: the two seeds agree in Delta to 1e-30 where both converged.
usage: python3 verdict_839.py DIR             (exit 0 when every run present passes and the seeds agree)
       python3 verdict_839.py --selftest      (planted records; exit 0 on pass)
       python3 verdict_839.py --selftest --mutate=bar   (the Delta bar at 1e-20 instead of 1e-30; must fail)"""
import json
import os
import sys

F_BAR, D_BAR, STEPS = 1e-40, 1e-30, 12


def judge(rec, d_bar=D_BAR):
    """(passed, line) for one planted record"""
    od = rec.get("od", {})
    conv, F, steps, dD = bool(od.get("converged")), od.get("F", float("inf")), od.get("steps", 0), rec.get("dDelta")
    ok = conv and F < F_BAR and steps <= STEPS + 1 and dD is not None and dD <= d_bar
    hist = od.get("hist", [])
    last = hist[-1] if hist else {}
    where = "" if ok else (f"; stopped at step {last.get('it')} (max|F| {last.get('F', float('nan')):.2e}, "
                           f"lam {last.get('lam')}, |dz| {last.get('dz', float('nan')):.2e})" if last else "")
    return ok, (f"converged {conv}, {steps} records, max|F| {F:.3e} (< {F_BAR:g}), |Delta - truth| "
                f"{'none' if dD is None else f'{dD:.3e}'} (<= {d_bar:g}){where}: {'pass' if ok else 'FAIL'}")


def agree(r1, r2, d_bar=D_BAR):
    """the seeds' Deltas against each other, when both converged (None when not both)"""
    import mpmath as mp
    if not (r1.get("od", {}).get("converged") and r2.get("od", {}).get("converged")):
        return None
    with mp.workdps(60):
        return float(abs(mp.mpf(r1["od"]["Delta"]) - mp.mpf(r2["od"]["Delta"])))


def selftest(mutate):
    bar = 1e-20 if mutate == "bar" else D_BAR
    good = dict(od=dict(converged=True, F=3e-45, steps=5, Delta="1.6845344501189222944531290453175690889942", hist=[]),
                dDelta=4e-41)
    cases = [(good, True), (dict(good, dDelta=2e-25), False),
             (dict(good, od=dict(good["od"], F=2e-39)), False),
             (dict(good, od=dict(good["od"], converged=False, steps=13, hist=[dict(it=12, F=1e-35, lam=0.5, dz=1e-30)])),
              False)]
    ok = True
    for rec, want in cases:
        got, line = judge(rec, bar)
        ok &= got == want
        print(f"  {line} (want {'pass' if want else 'FAIL'}){'' if got == want else '  <- wrong'}")
    print(f"verdict_839 selftest{' --mutate=' + mutate if mutate else ''}: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv):
    if argv and argv[0] == "--selftest":
        return selftest(next((a.split("=", 1)[1] for a in argv[1:] if a.startswith("--mutate=")), ""))
    d = argv[0]
    recs, ok = {}, True
    for name in ("A_s1", "B_s1", "A_s2", "B_s2"):
        p = os.path.join(d, name + ".json")
        if not os.path.exists(p):
            print(f"  {name}: not run yet")
            continue
        recs[name] = json.load(open(p))
        good, line = judge(recs[name])
        ok &= good
        print(f"  {name}: {line}")
    for arm in "AB":
        a, b = recs.get(f"{arm}_s1"), recs.get(f"{arm}_s2")
        if a and b:
            x = agree(a, b)
            if x is None:
                print(f"  arm {arm}: the seeds' Deltas not compared (not both converged)")
            else:
                ok &= x <= D_BAR
                print(f"  arm {arm}: seeds 1 and 2 agree in Delta to {x:.3e} (<= {D_BAR:g}): "
                      f"{'pass' if x <= D_BAR else 'FAIL'}")
    print(f"verdict_839: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
