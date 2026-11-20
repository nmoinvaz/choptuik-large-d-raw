#!/usr/bin/env python3
"""eval1026.py [--dir walks] [--mutate=shift|known|noconv] [--selftest]: #1026's readings, fixed before the runs.
Control (the known zero, started at its M = 3 zero): the M = 5 walk must converge to the stored zero of logs/hier_M5_full_schur.log (A 2.718579189, w/w_inf 0.999228404) within 1e-5 in A and in w.
Candidate (started at its M = 3 zero with its M = 3 harmonics): PERSISTS when the walk converges (Newton step < 3e-6, |r_3| and |r_5| < 1e-6) to a zero not within 5e-3 (A and w) of the known zero's M = 5 zero,
with the M = 3 -> 5 shift, taken as the Euclidean norm in (A, w/w_inf), smaller than its M = 1 -> 3 shift; FAILS when no converged solve is reached from it (the start solve, a Jacobian solve or every
trial step does not converge), when it converges to the known zero, or when the shift is larger; UNDECIDED otherwise (the iteration cap, or xi1 0.2 and 0.25 disagreeing). The primary radius is xi1 0.2
(the control's), 0.25 is read alongside. Exit 0 when the control passes. Controls: --selftest (synthetic walks: a smaller shift persists, a larger fails, the known zero fails, a non-converged walk fails, the
control's shifted expected value fails); --mutate=shift moves the control's expected zero by 1e-4 (the control must then FAIL), --mutate=known gives every candidate the known zero's M = 5 place."""
import json
import math
import os
import sys

STORED = (2.718579189, 0.999228404)
M1 = dict(control=(2.542148, 0.776994), minus=(2.642772, 0.280029), plus=(2.877304, 0.300451), newzero=(2.139401, 0.278745))
M3 = dict(control=(2.726476, 1.015603), minus=(2.598600, 0.221757), plus=(2.844769, 0.217964), newzero=(2.338793, 0.096238))


def judge_control(v, mut=""):
    exp = (STORED[0] + (1e-4 if mut == "shift" else 0), STORED[1])
    if not v.get("converged"):
        return False, "did not converge: " + str(v.get("why"))
    dA, dw = v["A"] - exp[0], v["w"] - exp[1]
    return abs(dA) <= 1e-5 and abs(dw) <= 1e-5, f"zero ({v['A']:.9f}, {v['w']:.9f}), stored ({exp[0]:.9f}, {exp[1]:.9f}), difference ({dA:+.2e}, {dw:+.2e})"


def judge_candidate(name, v, mut=""):
    if not v.get("converged"):
        why = str(v.get("why"))
        return ("UNDECIDED" if "iterations" in why else "FAILS"), "no converged zero: " + why
    A, w = (STORED if mut == "known" else (v["A"], v["w"]))
    if abs(A - STORED[0]) < 5e-3 and abs(w - STORED[1]) < 5e-3:
        return "FAILS", f"converged to the known zero's place ({A:.6f}, {w:.6f})"
    s53 = math.hypot(A - M3[name][0], w - M3[name][1])
    s31 = math.hypot(M3[name][0] - M1[name][0], M3[name][1] - M1[name][1])
    txt = f"zero ({A:.6f}, {w:.6f}), M3 -> 5 shift ({A - M3[name][0]:+.4f}, {w - M3[name][1]:+.4f}) norm {s53:.4f} against M1 -> 3 shift ({M3[name][0] - M1[name][0]:+.4f}, {M3[name][1] - M1[name][1]:+.4f}) norm {s31:.4f}"
    return ("PERSISTS" if s53 < s31 else "FAILS"), txt


def selftest():
    good = dict(converged=True, A=2.5986 + 0.01, w=0.2218 + 0.01)
    big = dict(converged=True, A=2.5986 + 0.2, w=0.2218 + 0.2)
    known = dict(converged=True, A=2.7185792, w=0.9992284)
    nc = dict(converged=False, why="the start solve did not converge")
    r = [judge_candidate("minus", good)[0], judge_candidate("minus", big)[0], judge_candidate("minus", known)[0], judge_candidate("minus", nc)[0], judge_candidate("minus", dict(converged=False, why="25 iterations"))[0]]
    c = [judge_control(dict(converged=True, A=STORED[0] + 1e-7, w=STORED[1]))[0], judge_control(dict(converged=True, A=STORED[0] + 1e-4, w=STORED[1]))[0], judge_control(nc)[0]]
    ok = r == ["PERSISTS", "FAILS", "FAILS", "FAILS", "UNDECIDED"] and c == [True, False, False]
    print(f"selftest: candidate verdicts {r} (expect PERSISTS FAILS FAILS FAILS UNDECIDED), control {c} (expect True False False): {'PASS' if ok else 'FAIL'}")
    return ok


def main(argv):
    if "--selftest" in argv:
        return 0 if selftest() else 1
    d = argv[argv.index("--dir") + 1] if "--dir" in argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), "walks")
    mut = next((a.split("=")[1] for a in argv if a.startswith("--mutate=")), "")
    res = {}
    for name in ("control", "minus", "plus", "newzero"):
        for xi in ("0.2", "0.25"):
            p = os.path.join(d, f"walk_{name}_xi{xi}.json")
            if not os.path.exists(p):
                continue
            w = json.load(open(p))
            v = w["verdict"]
            if name == "control":
                ok, txt = judge_control(v, mut)
                res[(name, xi)] = "PASS" if ok else "FAIL"
            else:
                res[(name, xi)], txt = judge_candidate(name, v, mut)
            extra = f"  [r_1 {v['r1'][0]:+.2e}{v['r1'][1]:+.2e}i, |r_3| {v['r3']:.1e}, |r_5| {v['r5']:.1e}, {v['points']} solves]" if v.get("converged") else ""
            print(f"{name} xi1 {xi}: {res[(name, xi)]}: {txt}{extra}")
    for name in ("minus", "plus", "newzero"):
        a, b = res.get((name, "0.2")), res.get((name, "0.25"))
        if a is not None:
            fin = a if b in (None, a) else "UNDECIDED"
            print(f"{name}: verdict {fin}" + ("" if b is None else f" (xi1 0.2 {a}, 0.25 {b})"))
    return 0 if res.get(("control", "0.2")) == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
