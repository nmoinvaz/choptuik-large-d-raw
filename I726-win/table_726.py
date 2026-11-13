#!/usr/bin/env python3
"""#726: the full system with --elim_switch 0 from D 104.5078 to D 120: per attempt the numbers of the corrector, and at each integer D from 105 to 120 Delta_full - Delta_held beside delta_all.csv's err.
usage: python table_726.py [--selftest]          (venv-t151 python, from this folder; reads S1/ and L/ anm_run.jsonl, logs/S1.log, logs/L.log, the stage checkout's T138-win2/chain states and the worktree's hp/data/delta_all.csv)
Per attempt: a, D, the quad-double max|F| of the re-seeded prediction at the start of the corrector (first `qn 0 [full]` after the re-seed line), the |F| after the first full step, the corrector's steps, the converged
qd max|F| (converged means at most 1e-44, the issue's bar), the elimination counts, the outcome. Delta of a state = the sum of the last entry of each part, in arb at 400 bits. Ratio = (Delta_full - Delta_held) / err, the err
of the chain_fit row of delta_all.csv at that D (kind "fits d10"). --selftest: the convergence classifier on planted attempts (one at 2e-44 must read NOT converged) and a planted displaced Delta that must show in the difference."""
import csv
import json
import os
import re
import sys

import flint
import numpy as np

flint.ctx.prec = 400
arb = flint.arb
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = r"C:\Users\nathan\Source\choptuik-large-d-raw-stage"
DELTA_ALL = r"C:\Users\nathan\Source\choptuik-i710\hp\data\delta_all.csv"
BAR = 1e-44
RESEED = re.compile(r"^    a ([0-9.]+): re-seeded")
QN = re.compile(r"qn (\d+)(?: \[full\])?: \|F\| ([0-9.e+-]+)(?: -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+))?")
QD = re.compile(r"quad-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (converged|not converged)")
ELIM = re.compile(r"elim projections (\{.*\})")


def parse_log(path):
    out, cur = [], None
    for ln in open(path, encoding="utf-8", errors="replace"):
        m = RESEED.match(ln)
        if m:
            cur = dict(a=float(m.group(1)), f0=None, f1=None, steps=None, fin=None, says=None, elim=None)
            out.append(cur)
            continue
        if cur is None:
            continue
        m = QN.search(ln)
        if m and m.group(1) == "0" and cur["f0"] is None:
            cur["f0"] = float(m.group(2))
            cur["f1"] = float(m.group(3)) if m.group(3) else None
        m = ELIM.search(ln)
        if m:
            cur["elim"] = eval(m.group(1), {"__builtins__": {}})
        m = QD.search(ln)
        if m:
            cur["steps"], cur["fin"], cur["says"] = int(m.group(1)), float(m.group(2)), m.group(3) == "converged"
    return out


def converged(at):
    """the issue's criterion: qd max|F| at most 1e-44 (and the corrector's own verdict)."""
    return bool(at["says"]) and at["fin"] is not None and at["fin"] <= BAR


def delta(path):
    d = np.load(path, allow_pickle=True)
    s = arb(0)
    for k in ("zh", "zl", "z2", "z3"):
        if k in d.files:
            s += arb(float(d[k][-1]))
    return s


def fits_err():
    out = {}
    for r in csv.reader(open(DELTA_ALL)):
        try:
            out[round(float(r[0]), 6)] = (r[5], float(r[6]))
        except (ValueError, IndexError):
            pass
    return out


def selftest():
    bad = 0
    for name, at, want in (("1e-45 converged", dict(says=True, fin=1e-45), True), ("2e-44 says converged but above the bar", dict(says=True, fin=2e-44), False), ("5e-25 not converged", dict(says=False, fin=5e-25), False)):
        got = converged(at)
        print(f"  planted '{name}': converged {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    a, b = arb("1.7450264844326"), arb("1.7450264844326")
    plant = arb("2.2e-13")
    shown = float(((a + plant) - b).mid())
    ok = abs((float((a - b).mid()))) == 0.0 and abs(shown - 2.2e-13) < 1e-20
    print(f"  planted Delta displaced by 2.2e-13: difference {shown:.4e} {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    err = fits_err()
    attempts = []
    for name in ("S1", "L"):
        jp, lp = os.path.join(HERE, name, "anm_run.jsonl"), os.path.join(HERE, "logs", f"{name}.log")
        if not (os.path.exists(jp) and os.path.exists(lp)):
            continue
        recs = [json.loads(ln) for ln in open(jp) if ln.strip()]
        logs = parse_log(lp)
        k = 0
        for r in recs:
            for at in r["attempts"]:
                attempts.append((name, r, at, logs[k] if k < len(logs) else {}))
                k += 1
    print("| step | D from -> to | a | qd max abs F of the re-seeded prediction | after the first full step | corrector steps | converged qd max abs F | converged (at most 1e-44) | elim counts | outcome |\n|---|---|---|---|---|---|---|---|---|---|")
    f = lambda x: "n/a" if x is None else f"{x:.2e}"
    for name, r, at, lg in attempts:
        outc = "accepted" if at["accepted"] else "REFUSED"
        print(f"| {name} {r['step']} | {r['D0']:.4f} -> {at['D']:.4f} | {at['a']:g} | {f(lg.get('f0'))} | {f(lg.get('f1'))} | {lg.get('steps')} | {f(lg.get('fin'))} | {'yes' if lg and converged(lg) else 'NO'} | {lg.get('elim')} | {outc} |")
    print("\n| D | Delta_full (this task) | Delta_held (T138-win2 chain) | Delta_full - Delta_held | delta_all.csv err (kind) | ratio to the err |\n|---|---|---|---|---|---|")
    rows = []
    for D in range(105, 121):
        found = None
        for d in ("S1", "L"):
            p = os.path.join(HERE, d, f"anm_pin13_D{D}.0000.npz")
            if os.path.exists(p):
                found = p
        h = os.path.join(STAGE, "T138-win2", "chain", f"anm_pin3_D{D}.0000.npz")
        if not found:
            print(f"| {D} | not reached | | | | |")
            continue
        if not os.path.exists(h):
            print(f"| {D} | {delta(found).str(24, radius=False)} | no held state | | | |")
            continue
        a, b = delta(found), delta(h)
        diff = float((a - b).mid())
        e = err.get(round(float(D), 6))
        rows.append((D, diff))
        print(f"| {D} | {a.str(24, radius=False)} | {b.str(24, radius=False)} | {diff:+.4e} | {('%.1e (%s)' % (e[1], e[0])) if e else 'no row'} | {('%.3f' % (diff / e[1])) if e else ''} |")
    if len(rows) > 1:
        print("\nsuccessive ratios of the shift: " + ", ".join(f"{b[1] / a[1]:.3f}" for a, b in zip(rows, rows[1:])))


if __name__ == "__main__":
    main()
