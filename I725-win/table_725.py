#!/usr/bin/env python3
"""#725: Delta of the two switch-0 a = 1/16 states against cont3's default-switch states at the same D, the reading of README choice 3, and the state differences.
usage: python table_725.py [--selftest]          (venv-t151 python, from this folder; reads logs/{X1,X2}.log, {X1,X2}/anm_run.jsonl, ../I682-win/logs/cont3.log and ../I682-win/cont3/anm_pin13_D99.8125.npz, D99.8750.npz)
Delta of a state = the sum of the last entry of each of the four parts, in arb at 400 bits. Reading of the two absolute differences d1 (X1 against cont3's D 99.8125) and d2 (X2 against cont3's D 99.875):
both < 1e-30 -> LARGE STEP (the bar of #710 is met at a = 1/16); both in [1e-28, 1e-24] -> 1e-26 SCALE (floor = max(d1, d2)); anything else -> NEITHER (reported as it is).
--selftest: planted pairs that must read LARGE STEP, 1e-26 SCALE and NEITHER, and a planted state whose last entry is displaced by 1e-27 that must move d from below 1e-30 into the 1e-26 scale class."""
import json
import os
import re
import sys

import flint
import numpy as np

flint.ctx.prec = 400
arb = flint.arb
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
CONT3 = os.path.join(RAW, "I682-win", "cont3")
CONT3_LOG = os.path.join(RAW, "I682-win", "logs", "cont3.log")
RESEED = re.compile(r"^    a ([0-9.]+): re-seeded")
QN = re.compile(r"^  qn (\d+) \[full\]: \|F\| ([0-9.e+-]+) -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+), lam ([0-9.]+)")
CONV = re.compile(r"^  qn (\d+): \|F\| ([0-9.e+-]+) converged")
NOTRIAL = re.compile(r"^  qn (\d+): \|F\| ([0-9.e+-]+), \|dz\| ([0-9.e+-]+): no trial step accepted")
ELIM = re.compile(r"elim projections (\{.*\})")
QD = re.compile(r"quad-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (converged|not converged)")
ATT = re.compile(r"^    a ([0-9.]+) -> D ([0-9.]+): predicted")


def parse(path):
    out, cur = [], None
    for ln in open(path, encoding="utf-8", errors="replace"):
        m = RESEED.match(ln)
        if m:
            cur = dict(a=m.group(1), qn=[], tail=None, elim=None, steps=None, fin=None, ok=None, D=None)
            out.append(cur)
            continue
        if cur is None:
            continue
        m = QN.match(ln)
        if m:
            cur["qn"].append(m.groups())
        m = NOTRIAL.match(ln)
        if m:
            cur["tail"] = "no trial step accepted at qn %s (|F| %s)" % (m.group(1), m.group(2))
        m = CONV.match(ln)
        if m:
            cur["tail"] = "converged at qn %s (|F| %s)" % (m.group(1), m.group(2))
        m = ELIM.search(ln)
        if m:
            cur["elim"] = eval(m.group(1), {"__builtins__": {}})
        m = QD.search(ln)
        if m:
            cur["steps"], cur["fin"], cur["ok"] = int(m.group(1)), float(m.group(2)), m.group(3) == "converged"
        m = ATT.match(ln)
        if m:
            cur["D"] = float(m.group(2))
    return out


def parts_of(path):
    d = np.load(path, allow_pickle=True)
    return [np.asarray(d[k], dtype=float) for k in ("zh", "zl", "z2", "z3") if k in d.files]


def total(parts, i):
    s = arb(0)
    for p in parts:
        s += arb(float(p[i]))
    return s


def delta(path):
    ps = parts_of(path)
    return total(ps, len(ps[0]) - 1)


def read(d1, d2):
    if d1 < 1e-30 and d2 < 1e-30:
        return "LARGE STEP"
    if 1e-28 <= d1 <= 1e-24 and 1e-28 <= d2 <= 1e-24:
        return "1e-26 SCALE"
    return "NEITHER"


def selftest():
    bad = 0
    for name, d1, d2, want in (("both 1e-33", 1e-33, 4e-32, "LARGE STEP"), ("both near 3e-26", 3e-26, 1e-25, "1e-26 SCALE"), ("one below, one above", 1e-31, 3e-26, "NEITHER"), ("both 1e-20", 1e-20, 2e-20, "NEITHER")):
        got = read(d1, d2)
        print(f"  planted '{name}': {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    ps = parts_of(os.path.join(CONT3, "anm_pin13_D99.8125.npz"))
    base = total(ps, len(ps[0]) - 1)
    shifted = base + arb(1e-27)
    d_same, d_shift = abs(float((base - base).mid())), abs(float((shifted - base).mid()))
    ok = d_same < 1e-30 and 1e-28 <= d_shift <= 1e-24 and read(d_same, d_same) == "LARGE STEP" and read(d_shift, d_shift) == "1e-26 SCALE"
    print(f"  planted last entry displaced by 1e-27: d {d_same:.1e} -> {d_shift:.1e}, reads {read(d_same, d_same)} -> {read(d_shift, d_shift)} {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    c3 = parse(CONT3_LOG)
    ref = {"X1": ("anm_pin13_D99.8125.npz", 99.8125), "X2": ("anm_pin13_D99.8750.npz", 99.875)}
    d = {}
    for run in ("X1", "X2"):
        p = os.path.join(HERE, "logs", f"{run}.log")
        if not os.path.exists(p):
            continue
        att = parse(p)
        recs = [json.loads(ln) for ln in open(os.path.join(HERE, run, "anm_run.jsonl")) if ln.strip()]
        flat = [a for r in recs for a in r["attempts"]]
        print(f"\n### {run}: {len(att)} attempts")
        print("| attempt | a | D | qn lines | tail | elim projections | corrector | accepted |\n|---|---|---|---|---|---|---|---|")
        for i, at in enumerate(att):
            qn = "; ".join(f"{k}: {f0} -> {f1}, lam {lam}" for k, f0, f1, d0, d1, lam in at["qn"])
            acc = ("accepted" if flat[i]["accepted"] else "REFUSED") if i < len(flat) else "n/a"
            print(f"| {i} | {at['a']} | {at['D']} | {qn} | {at['tail']} | {at['elim']} | {at['steps']} steps, max|F| {at['fin']:.1e}, {'converged' if at['ok'] else 'not converged'} | {acc} |")
        name, Dref = ref[run]
        mine = os.path.join(HERE, run, name)
        theirs = os.path.join(CONT3, name)
        if not (os.path.exists(mine) and os.path.exists(theirs)):
            print(f"  Delta check not made: {name} missing (mine {os.path.exists(mine)}, cont3 {os.path.exists(theirs)})")
            continue
        pm, pt = parts_of(mine), parts_of(theirs)
        dm, dt = total(pm, len(pm[0]) - 1), total(pt, len(pt[0]) - 1)
        diff = abs(float((dm - dt).mid()))
        d[run] = diff
        n = len(pm[0])
        el = np.array([abs(float((total(pm, i) - total(pt, i)).mid())) for i in range(n)])
        same_lead = int((parts_of(mine)[0] == parts_of(theirs)[0]).sum())
        c3att = [a for a in c3 if a["D"] is not None and abs(a["D"] - Dref) < 1e-9 and a["ok"]]
        c3f = f"{c3att[0]['fin']:.1e}" if c3att else "n/a"
        print(f"  Delta {name}: {dm.str(30, radius=False)} against cont3's {dt.str(30, radius=False)}: |diff| {diff:.3e}")
        print(f"  state difference (769 entries): max {el.max():.3e}, median {np.median(el):.3e}; same leading double in {same_lead} of {n}; qd max|F| here {att[0]['fin']:.1e}, cont3's state {c3f}")
    if len(d) == 2:
        print(f"\nREADING (README choice 3): d1 = {d['X1']:.3e}, d2 = {d['X2']:.3e} -> {read(d['X1'], d['X2'])}" + (f"; floor = {max(d['X1'], d['X2']):.3e}" if read(d['X1'], d['X2']) == "1e-26 SCALE" else ""))


if __name__ == "__main__":
    main()
