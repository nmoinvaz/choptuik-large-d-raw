#!/usr/bin/env python3
"""eval_z7.py [--dir walks] [--mutate=shift|ratio] [--selftest [--break] [--mutate=nogate]]: the readings of box 7's zero at M = 7 (#1021; eval_z16.py of
I1021-dh610/z16_m7 at raw 5b72af8c with box 7's M = 3 zero, the control file's path, xi1 0.2 only and the M = 5 control added), #1027's rule
through eval1027.py (copy of I1027-dh610's, unchanged). At xi1 0.2: the M = 5 control walk (#1026's, judged by eval1026.py, unchanged), the control walk (the known zero, #1027's; validated
there only at 0.15, so here a control failure is reported as a result), the M = 5 walk of box 7 (Z5, the M 3 -> 5 shift s35 = |Z5 - Z3|, Z3 the M = 3
zero's located place), the M = 7 walk from Z5 (|F7/F5| and |F5/F3| at its first solve, the M = 7 zero Z7, the M 5 -> 7 shift s57). Verdict by eval1027.judge_zero: CONVERGES: |F7/F5| <= 0.2 at Z5 and a converged M = 7 walk with s57 < s35; DOES NOT:
|F7/F5| >= 0.3 or no M = 7 zero near it; UNDECIDED otherwise. With no M = 5 zero the verdict is UNDECIDED (box 7 has no input point to walk from). The evaluator is checked on #1027's validated control walk (xi1 0.15): it must pass, and with
--mutate=shift it must fail. --selftest: synthetic walks (and --break, which applies --mutate=ratio inside the self-test: it must then FAIL, exit 1)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval1027 as E  # noqa: E402
import eval1026 as E6  # noqa: E402

Z3 = (3.2454793232694903, 0.34585226845559425)     # box 7's M = 3 zero located at xi1 0.17 (I1021-mac/loc/z7_6da7da7b/count_M3_loc_z7_6da7da7b.json)
CTRL_FILE = os.path.join(HERE, "inputs", "walk_control_xi0.15.json")      # I1027-dh610/walks/ at raw 245cdef1


def load(d, name, xi):
    p = os.path.join(d, f"walk_{name}_xi{xi}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def z16_verdict(m5, w7, w7in, mut=""):
    """(label, text) for one radius from the M = 5 walk, the M = 7 walk from Z5 and the M = 7 walk from the input's point (dicts or None)"""
    if m5 and m5["verdict"].get("converged") and w7:
        z5 = (m5["verdict"]["A"], m5["verdict"]["w"])
        s35 = math.hypot(z5[0] - Z3[0], z5[1] - Z3[1])
        E.Z["z7"] = dict(M5=z5, s35=s35)
        lab, txt = E.judge_zero("z7", w7, mut)
        return lab, f"M = 5 zero ({z5[0]:.6f}, {z5[1]:.6f}), M 3 -> 5 shift {s35:.4f}; " + txt
    if m5 and m5["verdict"].get("converged"):
        return "UNDECIDED", "the M = 5 zero was found but the M = 7 walk from it did not run"
    why = "no M = 5 walk" if not m5 else "no M = 5 zero: " + str(m5["verdict"].get("why"))
    if not w7in:
        return "UNDECIDED", why + "; and no M = 7 walk from the input's point"
    E.Z["z7"] = dict(M5=Z3, s35=0.0)
    lab, txt = E.judge_zero("z7", w7in, mut)
    return lab, why + " (s35 undefined, taken as 0, so CONVERGES is not reachable); from the input's point: " + txt


def gated(lab, okc, mut=""):
    """the coordinator's rule (20 Nov, about 06:56 UTC): an M = 7 result at xi1 0.2 counts only if #1027's M = 7 control
    passes at 0.2 in the same run; --mutate=nogate drops the gate (the selftest must then fail)"""
    return lab if (okc or mut == "nogate") else "NO VERDICT"


def ctrl_res(c):
    p = c["points"][-1] if c and c.get("points") else None
    if not p or not p.get("r1"):
        return "no solve of the control has residuals"
    return (f"the control's last solve: |r_1| {math.hypot(*p['r1']):.3g}, |r_3| {p['r3']:.1e}, |r_5| {p['r5']:.1e}, "
            f"|r_7| {p['r7']:.1e}")


def info_in(w):
    if not w:
        return "no walk from the input's point"
    r75, r53 = E.start_of(w)
    v = w["verdict"]
    s = "start solve not converged" if r75 is None else f"|F7/F5| {r75:.4f} and |F5/F3| {r53:.4f} at the input's point"
    if v.get("converged"):
        sh = math.hypot(v["A"] - Z3[0], v["w"] - Z3[1])
        a, _ = E.ratios(v["F3"], v["F5"], v["F7"])
        s += f"; M = 7 zero ({v['A']:.6f}, {v['w']:.6f}), |F7/F5| {a:.4f} there, shift from the M = 3 zero {sh:.4f}"
    else:
        s += "; no M = 7 zero: " + str(v.get("why"))
    return s


def selftest(brk, nogate=False):
    mut = "ratio" if brk else ""

    def mk(r75, conv=True, A=Z3[0], w=Z3[1], why="x"):
        F5, F3 = [0.1, 0.0], [0.3, 0.0]
        p = dict(F3=F3, F5=F5, F7=[0.1 * r75, 0.0])
        return dict(points=[p], verdict=dict(converged=True, A=A, w=w, F3=F3, F5=F5, F7=p["F7"]) if conv else dict(converged=False, why=why))
    m5 = dict(verdict=dict(converged=True, A=Z3[0] + 0.05, w=Z3[1]))          # s35 about 0.05
    got = [z16_verdict(m5, mk(0.1, A=Z3[0] + 0.05 + 0.02), None, mut)[0],      # shift 0.02 < 0.05, ratio 0.1
           z16_verdict(m5, mk(0.35, A=Z3[0] + 0.05 + 0.02), None, mut)[0],
           z16_verdict(m5, mk(0.25, A=Z3[0] + 0.05 + 0.02), None, mut)[0],
           z16_verdict(m5, mk(0.1, A=Z3[0] + 0.05 + 0.2), None, mut)[0],      # shift 0.2 > 0.05
           z16_verdict(m5, mk(0.1, conv=False, why="no step reduced |r_1|"), None, mut)[0],
           z16_verdict(dict(verdict=dict(converged=False, why="x")), None, mk(0.35), mut)[0],
           z16_verdict(dict(verdict=dict(converged=False, why="x")), None, mk(0.1), mut)[0]]
    want = ["CONVERGES", "DOES NOT", "UNDECIDED", "UNDECIDED", "DOES NOT", "DOES NOT", "UNDECIDED"]
    g = [gated("CONVERGES", True), gated("CONVERGES", False, "nogate" if nogate else ""), gated("DOES NOT", False)]
    gw = ["CONVERGES", "NO VERDICT", "NO VERDICT"]
    print(f"selftest gate{' --mutate=nogate' if nogate else ''}: {g} (expect {gw}): {'PASS' if g == gw else 'FAIL'}")
    ok = got == want and g == gw
    print(f"selftest{' --break (--mutate=ratio inside)' if brk else ''}: z7 verdicts {got} (expect {want}): {'PASS' if ok else 'FAIL'}")
    return ok and (brk or E.selftest())


def main(argv):
    if "--selftest" in argv:
        return 0 if selftest("--break" in argv, "--mutate=nogate" in argv) else 1
    d = argv[argv.index("--dir") + 1] if "--dir" in argv else os.path.join(HERE, "walks")
    mut = next((a.split("=")[1] for a in argv if a.startswith("--mutate=")), "")
    out = []
    ok0, t0 = E.judge_control(json.load(open(CTRL_FILE)), mut)
    out.append(f"evaluator on #1027's validated control walk (xi1 0.15), mutate '{mut}': {'PASS' if ok0 else 'FAIL'}: {t0}")
    ok = ok0                                            # --mutate=shift moves the stored zero: the check must fail, exit 1
    for xi in ("0.2",):
        c5 = load(d, "control5", xi)
        if c5:
            ok5, t5 = E6.judge_control(c5["verdict"])
            out.append(f"xi1 {xi} M = 5 control (#1026's, the known zero from its M = 3 place): {'PASS' if ok5 else 'FAIL'}: {t5}")
        else:
            out.append(f"xi1 {xi} M = 5 control: no walk")
        c = load(d, "control", xi)
        okc = False
        if c:
            okc, tc = E.judge_control(c)
            out.append(f"xi1 {xi} control (the known zero at M = 7; validated only at 0.15 in #1027): {'PASS' if okc else 'FAIL'}: {tc}")
        else:
            out.append(f"xi1 {xi} control: no walk")
        lab, txt = z16_verdict(load(d, "z7m5", xi), load(d, "z7", xi), None, mut)
        g = gated(lab, okc, mut)
        out.append(f"xi1 {xi} z7: {g}: {txt}" + ("" if g == lab else f" (by the ratios and shifts alone: {lab}; not counted, since the M = 7 control at {xi} did not pass: {ctrl_res(c)})"))
    print("\n".join(out))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
