#!/usr/bin/env python3
"""#742: the full system D 113 to 120 in octo-double: control (a), per attempt the corrector's numbers, and Delta_full - Delta_held at each integer D with the ratio to delta_all.csv's err.
usage: python table_742.py [--selftest]       (venv-t151 python, from this folder; reads P/ and L/ (anm_run.jsonl, states), logs/P.log, logs/L.log, ../I739-win/B, the stage checkout's T138-win2/chain held states, the worktree's hp/data/delta_all.csv)
FIRST it reproduces #739's D 113 value (+4.3655e-13, Delta of I739-win/B/anm_pin13_D113.0000.npz minus the held D 113) and exits 1 if it does not.
Converged = the attempt's octo-double max|F| at most 1e-60 and the corrector's own "converged". Delta of a state = the exact sum of the last entry of every part present, arb at 600 bits (I739-win/cmp_739.py's reading).
--selftest: a planted attempt at 2e-60 that says converged must read NOT converged, one at 1e-62 converged; a planted displaced Delta must show in the difference."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I726-win"))
sys.path.insert(0, os.path.join(RAW, "I739-win"))
import table_726 as t26      # noqa: E402  (fits_err, STAGE)
import table_739 as t39      # noqa: E402  (log parsing)
import cmp_739 as c          # noqa: E402  (eight-part Delta, sets arb precision 600)

c.flint.ctx.prec = 600
BAR = 1e-60
HELD = lambda D: os.path.join(t26.STAGE, "T138-win2", "chain", f"anm_pin3_D{D}.0000.npz")
B113 = os.path.join(RAW, "I739-win", "B", "anm_pin13_D113.0000.npz")


def converged(says, F):
    return bool(says) and F is not None and F <= BAR


def shift(full_path, D):
    return float((c.delta(full_path) - c.delta(HELD(D))).mid())


def selftest():
    bad = 0
    for label, says, F, want in (("1e-62, says converged", True, 1e-62, True), ("2e-60, says converged", True, 2e-60, False), ("1e-70, says not converged", False, 1e-70, False)):
        got = converged(says, F)
        print(f"  planted attempt '{label}': converged {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    a = c.arb("1.733640141567942734406710993193602081591")
    shown = float(((a + c.arb("2.2e-13")) - a).mid())
    ok = abs(shown - 2.2e-13) < 1e-25
    print(f"  planted Delta displaced by 2.2e-13: difference {shown:.4e} {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def attempts(name):
    out = []
    p = os.path.join(HERE, name, "anm_run.jsonl")
    if os.path.exists(p):
        for ln in open(p):
            if ln.strip():
                r = json.loads(ln)
                for at in r["attempts"]:
                    out.append((name, r["step"], r["D0"], at))
    return out


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    s113 = shift(B113, 113)
    ok = abs(s113 - 4.3655e-13) < 5e-18
    print(f"reading check: Delta_full - Delta_held at D 113 from I739-win/B = {s113:+.4e} (#739: +4.3655e-13) {'ok' if ok else 'MISMATCH'}")
    if not ok:
        sys.exit(1)
    qa = c.delta(B113)
    ctl = os.path.join(HERE, "P", "base_pin13_D113.0000.npz")
    if os.path.exists(ctl):
        d = float((c.delta(ctl) - qa).mid())
        print(f"control (a): the D 113 start re-polished (P/base_pin13_D113.0000.npz), Delta - B's Delta = {d:+.4e}; Delta {c.delta(ctl).str(40, radius=False)}; bar 1e-30: {'met' if abs(d) <= 1e-30 else 'NOT MET'}")
    else:
        print("control (a): P/base_pin13_D113.0000.npz does not exist yet")
    print("\n### per attempt\n")
    print("| run | step | from D | a | to D | corrector steps | seconds | max abs F at the end | converged (at most 1e-60) | accepted |\n|---|---|---|---|---|---|---|---|---|---|")
    for name in ("P", "L", "M"):
        lp = os.path.join(HERE, "logs", f"{name}.log")
        ends = []
        if os.path.exists(lp):
            for label, seg in t39.segments(open(lp, encoding="utf-8", errors="replace").read().splitlines()):
                if label.startswith("attempt"):
                    ends.append(t39.parse(seg)[2])
        for k, (nm, step, D0, at) in enumerate(attempts(name)):
            e = ends[k] if k < len(ends) else None
            F = e["F"] if e else None
            print(f"| {nm} | {step} | {D0:g} | {at['a']:g} | {at['D']:g} | {at['steps']} | {at['t_corr']:.0f} | {'n/a' if F is None else format(F, '.2e')} | {'yes' if e and converged(e['converged'], F) else 'NO'} | {at['accepted']} |")
    print("\n### Delta_full - Delta_held\n")
    err = t26.fits_err()
    print("| D | Delta_full (octo-double, 40 digits) | Delta_full - Delta_held | delta_all.csv err (kind) | ratio to the err | ratio of the shift to the previous D's |\n|---|---|---|---|---|---|")
    prev = None
    for D in range(113, 121):
        p = B113 if D == 113 else None
        for run in ("P", "L", "M"):
            q = os.path.join(HERE, run, f"anm_pin13_D{D}.0000.npz")
            if os.path.exists(q):
                p = q
        if p is None:
            print(f"| {D} | not reached | | | | |")
            continue
        if not os.path.exists(HELD(D)):
            print(f"| {D} | {c.delta(p).str(40, radius=False)} | no held state | | | |")
            continue
        s = shift(p, D)
        e = err.get(round(float(D), 6))
        print(f"| {D} | {c.delta(p).str(40, radius=False)} | {s:+.4e} | {('%.1e (%s)' % (e[1], e[0])) if e else 'no row'} | {('%.3f' % (s / e[1])) if e else ''} | {('%.4f' % (s / prev)) if prev else ''} |")
        prev = s


if __name__ == "__main__":
    main()
