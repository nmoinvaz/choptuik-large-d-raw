#!/usr/bin/env python3
"""#710: the five runs' attempts (a, D, every qn line, the elimination counts, the corrector's verdict), A0 and B0 against cont3's refused attempts, A1 and B1's criteria and Delta checks, C's steps.
usage: python table_710.py [--selftest]          (venv-t151 python, from this folder; reads logs/{A0,A1,B0,B1,C}.log, {run}/anm_run.jsonl, ../I682-win/logs/cont3.log, ../I682-win/cont3 states)
Rules (README, choices 2 to 4). Reproduces: the numbers of every `qn k [full]` line and the no-trial line of the attempt, as printed, equal those of the cont3 attempt (A0: cont3 step 1's first attempt,
a 0.125 from D 99.75; B0: step 4's first attempt, a 0.0977 from D 99.953125). Converges: the attempt's corrector says converged in at most 8 steps with max|F| <= 1e-44, `u0q` > 0 and `skipped` 0.
Delta of a state = the sum of the last entry of each part, in arb at 400 bits; bar 1e-30. --selftest: the parser and the comparison on cont3's own log, and a planted change of one digit that must DIFFER."""
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
CONT3_LOG = os.path.join(RAW, "I682-win", "logs", "cont3.log")
CONT3 = os.path.join(RAW, "I682-win", "cont3")
RESEED = re.compile(r"^    a ([0-9.]+): re-seeded")
QN = re.compile(r"^  qn (\d+) \[full\]: \|F\| ([0-9.e+-]+) -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+), lam ([0-9.]+)")
NOTRIAL = re.compile(r"^  qn (\d+): \|F\| ([0-9.e+-]+), \|dz\| ([0-9.e+-]+): no trial step accepted")
CONV = re.compile(r"^  qn (\d+): \|F\| ([0-9.e+-]+) converged, Delta ([0-9.]+)")
ELIM = re.compile(r"elim projections (\{.*\})")
QD = re.compile(r"quad-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (converged|not converged)")
ATT = re.compile(r"^    a ([0-9.]+) -> D ([0-9.]+): predicted")


def parse(path):
    """list of attempts in log order: dict(a, qn=[(k,F0,F1,dz0,dz1,lam)], tail=('notrial', k, F, dz) | ('conv', k, F), elim=dict, steps, fin, ok, D)."""
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
            cur["tail"] = ("notrial",) + m.groups()
        m = CONV.match(ln)
        if m:
            cur["tail"] = ("conv", m.group(1), m.group(2))
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


def same(a, b):
    """equal as printed: the qn lines and the tail."""
    return a["qn"] == b["qn"] and a["tail"] == b["tail"]


def delta(path):
    d = np.load(path, allow_pickle=True)
    s = arb(0)
    for k in ("zh", "zl", "z2", "z3"):
        if k in d.files:
            s += arb(float(d[k][-1]))
    return s


def selftest():
    c3 = parse(CONT3_LOG)
    a_ref, b_ref = c3[1], c3[5]
    print(f"  cont3 attempt 1: a {a_ref['a']}, {len(a_ref['qn'])} qn lines, tail {a_ref['tail']}, elim skipped {a_ref['elim']['skipped']}")
    print(f"  cont3 attempt 5: a {b_ref['a']}, {len(b_ref['qn'])} qn lines, tail {b_ref['tail']}, elim skipped {b_ref['elim']['skipped']}")
    bad = 0
    ok1 = same(a_ref, parse(CONT3_LOG)[1])
    mut = parse(CONT3_LOG)[1]
    q = list(mut["qn"][0])
    q[2] = q[2][:-1] + ("0" if q[2][-1] != "0" else "1")
    mut["qn"][0] = tuple(q)
    ok2 = not same(a_ref, mut)
    mut2 = parse(CONT3_LOG)[1]
    mut2["tail"] = ("notrial", "2", "5.29e-25", "7.7e-25")
    ok3 = not same(a_ref, mut2)
    ok4 = not same(a_ref, c3[2])
    for name, ok in (("an attempt equals itself", ok1), ("a changed digit in a qn line differs", ok2), ("a changed digit in the tail differs", ok3), ("a different attempt differs", ok4)):
        print(f"  planted '{name}': {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def records(run):
    p = os.path.join(HERE, run, "anm_run.jsonl")
    return [json.loads(ln) for ln in open(p) if ln.strip()] if os.path.exists(p) else []


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    c3 = parse(CONT3_LOG)
    ref = {"A0": c3[1], "B0": c3[5]}
    for run in ("A0", "A1", "B0", "B1", "C"):
        p = os.path.join(HERE, "logs", f"{run}.log")
        if not os.path.exists(p):
            continue
        att = parse(p)
        recs = records(run)
        flat = [(r["step"], r["D0"], a) for r in recs for a in r["attempts"]]
        print(f"\n### {run}: {len(att)} attempts")
        print("| attempt | a | D | qn lines (|F| before -> after, lam) | tail | elim projections | corrector | accepted |\n|---|---|---|---|---|---|---|---|")
        for i, at in enumerate(att):
            qn = "; ".join(f"{k}: {f0} -> {f1}, |dz| {d1}, lam {lam}" for k, f0, f1, d0, d1, lam in at["qn"])
            tail = ("no trial step accepted at qn %s (|F| %s, |dz| %s)" % at["tail"][1:]) if at["tail"] and at["tail"][0] == "notrial" else (("converged at qn %s (|F| %s)" % at["tail"][1:]) if at["tail"] else "n/a")
            acc = "n/a"
            if i < len(flat):
                acc = "accepted" if flat[i][2]["accepted"] else "REFUSED"
            print(f"| {i} | {at['a']} | {at['D']} | {qn} | {tail} | {at['elim']} | {at['steps']} steps, max|F| {at['fin']:.1e}, {'converged' if at['ok'] else 'not converged'} | {acc} |")
        if run in ref and att:
            print(f"  reproduces cont3's refused attempt to the printed digits: {'YES' if same(att[0], ref[run]) else 'NO'} (cont3: {len(ref[run]['qn'])} qn lines, tail {ref[run]['tail']}; here {len(att[0]['qn'])} qn lines, tail {att[0]['tail']})")
        if run in ("A1", "B1") and att:
            a0 = att[0]
            el = a0["elim"] or {}
            conv = a0["ok"] and a0["steps"] <= 8 and a0["fin"] <= 1e-44
            print(f"  first attempt converges within 8 steps to 1e-44: {'YES' if conv else 'NO'} ({a0['steps']} steps, max|F| {a0['fin']:.1e}); u0q {el.get('u0q')} (needs > 0), skipped {el.get('skipped')} (needs 0): {'YES' if el.get('u0q', 0) > 0 and el.get('skipped', 1) == 0 else 'NO'}")
            name = "anm_pin13_D99.8750.npz" if run == "A1" else "anm_pin13_D100.0508.npz"
            mine, theirs = os.path.join(HERE, run, name), os.path.join(CONT3, name)
            if os.path.exists(mine) and os.path.exists(theirs):
                dm, dt = delta(mine), delta(theirs)
                diff = abs(float((dm - dt).mid()))
                print(f"  Delta {name}: {dm.str(30, radius=False)} against cont3's {dt.str(30, radius=False)}: |diff| {diff:.3e} (bar 1e-30): {'MATCHES' if diff <= 1e-30 else 'DIFFERS'}")
            else:
                print(f"  Delta check not made: {name} missing in {run} ({os.path.exists(mine)}) or in cont3 ({os.path.exists(theirs)})")
        if run == "C":
            print("  C's steps (record order): " + "; ".join(f"step {s} from D {d0:.4f}: a {a['a']:g} -> D {a['D']:.4f} {'accepted' if a['accepted'] else 'REFUSED'}" for s, d0, a in flat))


if __name__ == "__main__":
    main()
