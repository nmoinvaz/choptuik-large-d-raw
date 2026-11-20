#!/usr/bin/env python3
"""eval1027.py [--dir walks] [--mutate=shift|ratio] [--selftest]: #1027's readings, fixed before the runs.
Control (the known zero, started at its M = 5 zero with F_7 = 0): the M = 7 walk must converge to (2.71924, 1.000025) (proof/B_tail_M7.md: the zero at rtol 1e-13 to 1e-14, +- 1e-5 over several solves) within 3e-4 in
A and in w/w_inf (one walk's noise, see walk1027.py), with |F_7/F_5| at its first solve (the M = 5 zero) within 5% of 0.0574 (the stored 0.0573). Per low-omega M = 5 zero (z2275 = (2.227529, 0.092574),
z2584 = (2.583888, 0.141358)): |F_7/F_5| and |F_5/F_3| from the first solve (a fixed-(A, w) M = 7 solve at the M = 5 zero, the harmonic measurement) and, when the walk converges, at the M = 7 zero, and
the M 5 -> 7 shift (Euclidean norm in (A, w/w_inf)). CONVERGES: |F_7/F_5| <= 0.2 at the first solve and the walk converges to a zero whose M 5 -> 7 shift is smaller than the M 3 -> 5 one (the smaller of the two
pairings, nearest M = 3 zero and the walk's origin). DOES NOT: |F_7/F_5| >= 0.3 at the first solve, or no M = 7 zero near it (the start or a Jacobian solve fails, no step lowers |r_1|). UNDECIDED otherwise. Exit 0 when the
control passes. Controls: --selftest (synthetic walks), --mutate=shift moves the control's expected zero by 1e-3 (it must fail), --mutate=ratio sets the ratios of every zero to 0.25 (must give UNDECIDED)."""
import json
import math
import os
import sys

CTRL = (2.71924, 1.000025)
CTRL_RATIO = 0.0574
Z = {"z2275": dict(M5=(2.227529227, 0.092573703), s35=min(0.1113, 0.3929)), "z2584": dict(M5=(2.583887556, 0.141357652), s35=min(0.0817, 0.2719))}


def ratios(F3, F5, F7):
    n = lambda F: math.hypot(*F)
    return n(F7) / n(F5), n(F5) / n(F3)


def start_of(w):
    p = w["points"][0]
    return ratios(p["F3"], p["F5"], p["F7"]) if p.get("F7") else (None, None)


def judge_control(w, mut=""):
    v = w["verdict"]
    exp = (CTRL[0] + (1e-3 if mut == "shift" else 0), CTRL[1])
    if not v.get("converged"):
        return False, "did not converge: " + str(v.get("why"))
    r75, _ = start_of(w)
    dA, dw = v["A"] - exp[0], v["w"] - exp[1]
    ok = abs(dA) <= 3e-4 and abs(dw) <= 3e-4 and r75 is not None and abs(r75 - CTRL_RATIO) <= 0.05 * CTRL_RATIO
    return ok, f"zero ({v['A']:.6f}, {v['w']:.6f}), stored ({exp[0]:.6f}, {exp[1]:.6f}), difference ({dA:+.2e}, {dw:+.2e}); |F7/F5| at the M = 5 zero {r75:.4f} (stored {CTRL_RATIO})"


def judge_zero(name, w, mut=""):
    z = Z[name]
    v = w["verdict"]
    r75, r53 = start_of(w)
    if mut == "ratio":
        r75 = 0.25
    if r75 is None:
        return "DOES NOT", "the start solve did not converge: " + str(v.get("why"))
    txt = f"|F7/F5| {r75:.4f} and |F5/F3| {r53:.4f} at the M = 5 zero"
    if v.get("converged"):
        a, b = ratios(v["F3"], v["F5"], v["F7"])
        sh = math.hypot(v["A"] - z["M5"][0], v["w"] - z["M5"][1])
        txt += f"; M = 7 zero ({v['A']:.6f}, {v['w']:.6f}), |F7/F5| {a:.4f}, shift ({v['A'] - z['M5'][0]:+.4f}, {v['w'] - z['M5'][1]:+.4f}) norm {sh:.4f} against the M 3 -> 5 shift {z['s35']:.4f}"
    else:
        sh = None
        txt += "; no M = 7 zero: " + str(v.get("why"))
    if r75 >= 0.3:
        return "DOES NOT", txt
    if not v.get("converged"):
        return ("UNDECIDED" if "iterations" in str(v.get("why")) else "DOES NOT"), txt
    if r75 <= 0.2:
        return ("CONVERGES" if sh < z["s35"] else "UNDECIDED"), txt
    return "UNDECIDED", txt


def selftest():
    def mk(r75, conv=True, A=2.2275, w=0.0926, why="x"):
        F5, F3 = [0.1, 0.0], [0.3, 0.0]
        p = dict(F3=F3, F5=F5, F7=[0.1 * r75, 0.0])
        return dict(points=[p], verdict=dict(converged=True, A=A, w=w, F3=F3, F5=F5, F7=p["F7"]) if conv else dict(converged=False, why=why))
    cs = [judge_zero("z2275", mk(0.1, A=2.2275 + 0.005))[0], judge_zero("z2275", mk(0.35, A=2.2275 + 0.005))[0], judge_zero("z2275", mk(0.25, A=2.2275 + 0.005))[0],
          judge_zero("z2275", mk(0.1, conv=False, why="no step reduced |r_1|"))[0], judge_zero("z2275", mk(0.1, A=2.2275 + 0.5))[0], judge_zero("z2275", mk(0.1, conv=False, why="25 iterations"))[0]]
    want = ["CONVERGES", "DOES NOT", "UNDECIDED", "DOES NOT", "UNDECIDED", "UNDECIDED"]
    good = dict(points=[dict(F3=[0.05, 0], F5=[0.003, 0], F7=[0.003 * CTRL_RATIO, 0])], verdict=dict(converged=True, A=CTRL[0] + 1e-5, w=CTRL[1]))
    bad = dict(points=good["points"], verdict=dict(converged=True, A=CTRL[0] + 1e-3, w=CTRL[1]))
    ct = [judge_control(good)[0], judge_control(bad)[0], judge_control(good, "shift")[0]]
    ok = cs == want and ct == [True, False, False]
    print(f"selftest: zero verdicts {cs} (expect {want}), control {ct} (expect [True, False, False]): {'PASS' if ok else 'FAIL'}")
    return ok


def main(argv):
    if "--selftest" in argv:
        return 0 if selftest() else 1
    d = argv[argv.index("--dir") + 1] if "--dir" in argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), "walks")
    mut = next((a.split("=")[1] for a in argv if a.startswith("--mutate=")), "")
    res = {}
    for name in ("control", "z2275", "z2584"):
        for xi in ("0.15", "0.2", "0.25"):
            p = os.path.join(d, f"walk_{name}_xi{xi}.json")
            if not os.path.exists(p):
                continue
            w = json.load(open(p))
            if name == "control":
                ok, txt = judge_control(w, mut)
                res[(name, xi)] = "PASS" if ok else "FAIL"
            else:
                res[(name, xi)], txt = judge_zero(name, w, mut)
            print(f"{name} xi1 {xi}: {res[(name, xi)]}: {txt}")
    return 0 if res.get(("control", "0.15")) == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
