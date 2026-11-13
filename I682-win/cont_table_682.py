#!/usr/bin/env python3
"""#682's continuation toward D 100: per step the attempts' numbers, and at each integer D Delta_full - Delta_held beside delta_all.csv's err and #641's kfreeze 7 shift.
usage: python cont_table_682.py          (venv-t151 python, from this folder; reads cont/, cont2/, cont3/, cont4/ anm_run.jsonl when present, logs/cont.log, logs/cont2.log, logs/cont3.log, logs/cont4.log, the stage checkout's T138-win2/chain states
and the worktree's hp/data/delta_all.csv)
Per attempt: a, D, the quad-double max|F| of the re-seeded prediction at the start of the corrector (first `qn 0` after the re-seed line), the corrector's first step |dz| (the prediction's distance to the
converged state, the record's `moved` is the dd-parts' distance), its steps and the converged qd max|F| (or the failure), the smallest pivot of the step's Newton matrix.
Delta of a state = the sum of the last entry of each part, in arb at 400 bits."""
import csv
import json
import os
import re

import flint
import numpy as np

flint.ctx.prec = 400
arb = flint.arb
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = r"C:\Users\nathan\Source\choptuik-large-d-raw-stage"
DELTA_ALL = r"C:\Users\nathan\Source\choptuik-i682\hp\data\delta_all.csv"
KF7 = {80: 3.665e-14, 100: 9.694e-13}
RESEED = re.compile(r"^    a ([0-9.]+): re-seeded")
QN = re.compile(r"qn (\d+)(?: \[full\])?: \|F\| ([0-9.e+-]+)(?: -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+))?")
QD = re.compile(r"quad-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (converged|not converged)")
PIV = re.compile(r"piv ([0-9.e+-]+)\.\.")


def delta(path):
    d = np.load(path, allow_pickle=True)
    s = arb(0)
    for k in ("zh", "zl", "z2", "z3"):
        if k in d.files:
            s += arb(float(d[k][-1]))
    return s


def parse_log(path):
    """list of attempts: dict(a, f0, dz0, steps, fin, ok, minpiv) in log order."""
    out, cur = [], None
    for ln in open(path, encoding="utf-8", errors="replace"):
        m = RESEED.match(ln)
        if m:
            cur = dict(a=float(m.group(1)), f0=None, dz0=None, steps=None, fin=None, ok=None, minpiv=None)
            out.append(cur)
            continue
        if cur is None:
            continue
        m = QN.search(ln)
        if m and m.group(1) == "0" and cur["f0"] is None:
            cur["f0"] = float(m.group(2))
            cur["dz0"] = float(m.group(4)) if m.group(4) else None
        p = PIV.search(ln)
        if p:
            v = float(p.group(1))
            cur["minpiv"] = v if cur["minpiv"] is None else min(cur["minpiv"], v)
        m = QD.search(ln)
        if m:
            cur["steps"], cur["fin"], cur["ok"] = int(m.group(1)), float(m.group(2)), m.group(3) == "converged"
    return out


def fits_err():
    out = {}
    for r in csv.reader(open(DELTA_ALL)):
        try:
            out[round(float(r[0]), 6)] = (r[5], float(r[6]))
        except (ValueError, IndexError):
            pass
    return out


def main():
    err = fits_err()
    attempts = []
    for name in ("cont", "cont2", "cont3", "cont4"):
        jp, lp = os.path.join(HERE, name, "anm_run.jsonl"), os.path.join(HERE, "logs", f"{name}.log")
        if not (os.path.exists(jp) and os.path.exists(lp)):
            continue
        recs = [json.loads(ln) for ln in open(jp) if ln.strip()]
        logs = parse_log(lp)
        k = 0
        for r in recs:
            for at in r["attempts"]:
                lg = logs[k] if k < len(logs) else {}
                k += 1
                attempts.append((name, r, at, lg))
    print("| step | D from -> to | a | quad-double max abs F of the prediction | first Newton step max abs dz | corrector steps | converged max abs F | outcome | smallest pivot | moved (dd parts) |\n|---|---|---|---|---|---|---|---|---|---|")
    for name, r, at, lg in attempts:
        outc = "accepted" if at["accepted"] else "REFUSED"
        f = lambda x: "n/a" if x is None else f"{x:.2e}"
        print(f"| {name} {r['step']} | {r['D0']:.4f} -> {at['D']:.4f} | {at['a']:g} | {f(lg.get('f0'))} | {f(lg.get('dz0'))} | {lg.get('steps')} | {f(lg.get('fin'))}{'' if lg.get('ok') in (True, None) else ' (not converged)'} | {outc} | {f(lg.get('minpiv'))} | {at['moved']:.1e} |")
    print("\n| D | Delta_full (this task) | Delta_held (T138-win2 chain) | Delta_full - Delta_held | delta_all.csv err (kind) | ratio to the err | #641's kfreeze 7 shift |\n|---|---|---|---|---|---|---|")
    rows = []
    for D in range(78, 101):
        found = None
        for d in ("chain", "cont", "cont2", "cont3", "cont4"):
            p = os.path.join(HERE, d, f"anm_pin13_D{D}.0000.npz")
            if os.path.exists(p):
                found = p
        h = os.path.join(STAGE, "T138-win2", "chain", f"anm_pin3_D{D}.0000.npz")
        if not found or not os.path.exists(h):
            continue
        a, b = delta(found), delta(h)
        diff = float((a - b).mid())
        e = err.get(round(float(D), 6))
        rows.append((D, diff))
        print(f"| {D} | {a.str(24, radius=False)} | {b.str(24, radius=False)} | {diff:+.4e} | {('%.1e (%s)' % (e[1], e[0])) if e else 'no row'} | {('%.2f' % (diff / e[1])) if e else ''} | {('%+.3e' % KF7[D]) if D in KF7 else ''} |")
    if rows:
        print("\nsuccessive ratios of the shift: " + ", ".join(f"{b[1] / a[1]:.2f}" for a, b in zip(rows, rows[1:])))


if __name__ == "__main__":
    main()
