#!/usr/bin/env python3
"""eval_m7b.py --box z7|z16|b1115p [--dir walks] [--xi 0.15] [--mutate=shift|ratio|pos7|nogate] [--selftest [--mutate=...]]: the readings
of #1021's rerun of box 7, box 16 or b11-15's +1 at M = 7 under the criteria the coordinator fixed on #1048 (closing comment 7034798454),
before the rerun, with its amendment (at M = 7 the step and last-two-points bars stay walk1027's 3e-4, since its step
noise is 1.7e-5). xi1 0.15. Walk bars, at one iteration: |r_1| of the best point <= 3.8e-2 (M = 5) or 0.24 (M = 7), the Newton
step under 1e-5 (M = 5) or 3e-4 (M = 7) in A and in w/w_inf, and for the box walks the last two accepted walk points within
1e-5 (M = 5) or 3e-4 (M = 7) (walk1026b.py,
walk1027b.py; each walk's verdict records its bars, and a walk run with other bars does not count). Controls, both gates in the
same run: #1026's M = 5 walk from the known zero's M = 3 place converges within 1e-5 of the stored M = 5 zero (2.718579189,
0.999228404) (eval1026.judge_control); #1027's M = 7 walk from the M = 5 zero converges within 1e-5 of (2.71924, 1.000025) with
|F7/F5| at its first solve within 5% of 0.0574. The box: #1027's rule through eval1027.judge_zero, unchanged (CONVERGES: |F7/F5|
<= 0.2 at Z5 and a converged M = 7 walk with s57 < s35; DOES NOT: |F7/F5| >= 0.3 or no M = 7 zero near it; UNDECIDED
otherwise or without an M = 5 zero), counted only when both controls pass (else NO VERDICT). Controls of this evaluator:
--mutate=shift moves the M = 7 control's stored zero by 1e-3 (a passing control must then fail), --mutate=pos7 restores
eval1027's 3e-4 position bar and --mutate=nogate drops the gate (the selftest must fail under each), --mutate=ratio sets
|F7/F5| to 0.25. Exit 0 when the evaluator passes #1027's stored control walk under its own bars (xi1 0.15)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval1027 as E   # noqa: E402
import eval1026 as E6  # noqa: E402

Z3 = {"z7": (3.2454793232694903, 0.34585226845559425),     # box 7's M = 3 zero at xi1 0.17 (loc/z7_6da7da7b)
      "z16": (3.553346604669114, 0.41317228451624904),     # box 16's at xi1 0.18 (loc/z16_6da7da7b, located_r1b)
      "b1115p": (3.52647082272762, 0.21149502797254496)}  # b11-15's +1 at xi1 0.18 (loc/b1115p_r0.18_6da7da7b, located)
CTRL7, POS, RTOL = (2.71924, 1.000025), 1e-5, 0.05
BARS = {("control5", 5): [3.8e-2, 1e-5, None], ("control", 7): [0.24, 3e-4, None], ("box", 5): [3.8e-2, 1e-5, 1e-5], ("box", 7): [0.24, 3e-4, 3e-4]}
CTRL_FILE = os.path.join(HERE, "inputs", "walk_control_xi0.15.json")


def bars_ok(w, key):
    b = w["verdict"].get("bars")
    return b is not None and all((x is None and y is None) or (x is not None and y is not None and abs(x - y) <= 1e-15 * abs(y))
                                 for x, y in zip(b, BARS[key]))


def judge7(w, mut="", own_bars=True):
    v = w["verdict"]
    if not v.get("converged"):
        return False, "did not converge: " + str(v.get("why"))
    if own_bars and not bars_ok(w, ("control", 7)):
        return False, f"run with bars {v.get('bars')}, not {BARS[('control', 7)]}"
    exp = (CTRL7[0] + (1e-3 if mut == "shift" else 0.0), CTRL7[1])
    bar = 3e-4 if mut == "pos7" else POS
    r75, _ = E.start_of(w)
    dA, dw = v["A"] - exp[0], v["w"] - exp[1]
    ok = abs(dA) <= bar and abs(dw) <= bar and r75 is not None and abs(r75 - E.CTRL_RATIO) <= RTOL * E.CTRL_RATIO
    return ok, (f"zero ({v['A']:.6f}, {v['w']:.6f}), stored ({exp[0]:.6f}, {exp[1]:.6f}), difference ({dA:+.2e}, {dw:+.2e}) "
                f"against {bar:g}; |F7/F5| at the M = 5 zero " + (f"{r75:.4f}" if r75 is not None else "none") + f" (stored {E.CTRL_RATIO})")


def judge5(w):
    v = w["verdict"]
    if not v.get("converged"):
        return False, "did not converge: " + str(v.get("why"))
    if not bars_ok(w, ("control5", 5)):
        return False, f"run with bars {v.get('bars')}, not {BARS[('control5', 5)]}"
    return E6.judge_control(v)


def box_verdict(box, m5, w7, mut=""):
    if not m5:
        return "UNDECIDED", "no M = 5 walk"
    if not m5["verdict"].get("converged"):
        return "UNDECIDED", "no M = 5 zero: " + str(m5["verdict"].get("why"))
    if not bars_ok(m5, ("box", 5)):
        return "UNDECIDED", f"the M = 5 walk ran with bars {m5['verdict'].get('bars')}"
    if not w7:
        return "UNDECIDED", "the M = 5 zero was found but no M = 7 walk ran from it"
    v = w7["verdict"]
    if v.get("converged") and not bars_ok(w7, ("box", 7)):
        return "UNDECIDED", f"the M = 7 walk ran with bars {v.get('bars')}"
    z5 = (m5["verdict"]["A"], m5["verdict"]["w"])
    s35 = math.hypot(z5[0] - Z3[box][0], z5[1] - Z3[box][1])
    E.Z[box] = dict(M5=z5, s35=s35)
    lab, txt = E.judge_zero(box, w7, mut)
    return lab, f"M = 5 zero ({z5[0]:.6f}, {z5[1]:.6f}), M 3 -> 5 shift {s35:.4f}; " + txt


def gated(lab, ok5, ok7, mut=""):
    return lab if (ok5 and ok7) or mut == "nogate" else "NO VERDICT"


def selftest(mut):
    bx5, bx7, c7 = BARS[("box", 5)], BARS[("box", 7)], BARS[("control", 7)]
    F = lambda r: dict(F3=[0.3, 0.0], F5=[0.1, 0.0], F7=[0.1 * r, 0.0])
    m5 = dict(verdict=dict(converged=True, A=Z3["z7"][0] + 0.05, w=Z3["z7"][1], bars=bx5))
    w7 = lambda r, dA, bars=bx7: dict(points=[F(r)], verdict=dict(converged=True, A=Z3["z7"][0] + 0.05 + dA, w=Z3["z7"][1], bars=bars, **F(r)))
    got = [box_verdict("z7", m5, w7(0.1, 0.02), mut)[0], box_verdict("z7", m5, w7(0.35, 0.02), mut)[0],
           box_verdict("z7", m5, w7(0.25, 0.02), mut)[0], box_verdict("z7", m5, w7(0.1, 0.2), mut)[0],
           box_verdict("z7", m5, w7(0.1, 0.02, [0.24, 1e-5, 1e-5]), mut)[0],
           box_verdict("z7", dict(verdict=dict(converged=False, why="start")), None, mut)[0]]
    want = ["CONVERGES", "DOES NOT", "UNDECIDED", "UNDECIDED", "UNDECIDED", "UNDECIDED"]
    ctl = lambda dA: dict(points=[dict(F3=[0.05, 0], F5=[0.003, 0], F7=[0.003 * E.CTRL_RATIO, 0])], verdict=dict(converged=True, A=CTRL7[0] + dA, w=CTRL7[1], bars=c7))
    cg = [judge7(ctl(5e-6), mut)[0], judge7(ctl(2e-5), mut)[0], judge7(dict(ctl(5e-6), verdict=dict(ctl(5e-6)["verdict"], bars=[0.24, 1e-5, None])), mut)[0]]
    cw = [True, False, False]
    gg = [gated("CONVERGES", True, True, mut), gated("CONVERGES", True, False, mut), gated("DOES NOT", False, True, mut)]
    gw = ["CONVERGES", "NO VERDICT", "NO VERDICT"]
    ok = got == want and cg == cw and gg == gw
    print(f"selftest{' --mutate=' + mut if mut else ''}: box {got} (expect {want}); M = 7 control {cg} (expect {cw}); gate {gg} (expect {gw}): {'PASS' if ok else 'FAIL'}")
    return ok


def main(argv):
    mut = next((a.split("=")[1] for a in argv if a.startswith("--mutate=")), "")
    if "--selftest" in argv:
        return 0 if selftest(mut) else 1
    box = argv[argv.index("--box") + 1]
    d = argv[argv.index("--dir") + 1] if "--dir" in argv else os.path.join(HERE, "walks")
    xi = argv[argv.index("--xi") + 1] if "--xi" in argv else "0.15"
    load = lambda n: json.load(open(p)) if os.path.exists(p := os.path.join(d, f"walk_{n}_xi{xi}.json")) else None
    ok0, t0 = judge7(json.load(open(CTRL_FILE)), mut, own_bars=False)
    out = [f"evaluator on #1027's stored control walk (xi1 0.15, its own bars), mutate '{mut}': {'PASS' if ok0 else 'FAIL'}: {t0}"]
    c5, c7 = load("control5"), load("control")
    ok5, t5 = judge5(c5) if c5 else (False, "no walk")
    ok7, t7 = judge7(c7, mut) if c7 else (False, "no walk")
    out.append(f"xi1 {xi} M = 5 control (#1026's): {'PASS' if ok5 else 'FAIL'}: {t5}")
    out.append(f"xi1 {xi} M = 7 control (#1027's): {'PASS' if ok7 else 'FAIL'}: {t7}")
    lab, txt = box_verdict(box, load(f"{box}m5"), load(box), mut)
    g = gated(lab, ok5, ok7, mut)
    out.append(f"xi1 {xi} {box}: {g}: {txt}" + ("" if g == lab else f" (by the ratios and shifts alone: {lab}; not counted: a control did not pass)"))
    print("\n".join(out))
    return 0 if ok0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
