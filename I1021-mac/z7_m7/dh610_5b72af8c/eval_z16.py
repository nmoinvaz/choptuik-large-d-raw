#!/usr/bin/env python3
"""eval_z16.py [--dir walks] [--mutate=shift|ratio] [--selftest [--break]]: the readings of box 16's zero at M = 7 (#1021), #1027's rule
through eval1027.py (copy of I1027-dh610's, unchanged). Per radius xi1 in (0.25, 0.2): the control walk (the known zero, #1027's; validated
there only at 0.15, so here a control failure is reported as a result), the M = 5 walk of box 16 (Z5, the M 3 -> 5 shift s35 = |Z5 - Z3|, Z3 the M = 3
zero's located place), the M = 7 walk from Z5 (|F7/F5| and |F5/F3| at its first solve, the M = 7 zero Z7, the M 5 -> 7 shift s57) and the M = 7 walk from the
input's own point (information). Verdict by eval1027.judge_zero: CONVERGES: |F7/F5| <= 0.2 at Z5 and a converged M = 7 walk with s57 < s35; DOES NOT:
|F7/F5| >= 0.3 or no M = 7 zero near it; UNDECIDED otherwise. With no M = 5 zero the M = 7 walk from the input's point is judged with s35 = 0 (the ratio
alone can give DOES NOT; CONVERGES cannot be reached). The evaluator is checked on #1027's validated control walk (xi1 0.15): it must pass, and with
--mutate=shift it must fail. --selftest: synthetic walks (and --break, which applies --mutate=ratio inside the self-test: it must then FAIL, exit 1)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval1027 as E  # noqa: E402

Z3 = (3.553346604669114, 0.41317228451624904)      # the M = 3 zero's located place (inputs/z16_m7_inputs.json, m3_zero.located_r1b)
CTRL_FILE = "/home/nathan/Source/choptuik-large-d-raw/I1027-dh610/walks/walk_control_xi0.15.json"


def load(d, name, xi):
    p = os.path.join(d, f"walk_{name}_xi{xi}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def z16_verdict(m5, w7, w7in, mut=""):
    """(label, text) for one radius from the M = 5 walk, the M = 7 walk from Z5 and the M = 7 walk from the input's point (dicts or None)"""
    if m5 and m5["verdict"].get("converged") and w7:
        z5 = (m5["verdict"]["A"], m5["verdict"]["w"])
        s35 = math.hypot(z5[0] - Z3[0], z5[1] - Z3[1])
        E.Z["z16"] = dict(M5=z5, s35=s35)
        lab, txt = E.judge_zero("z16", w7, mut)
        return lab, f"M = 5 zero ({z5[0]:.6f}, {z5[1]:.6f}), M 3 -> 5 shift {s35:.4f}; " + txt
    if m5 and m5["verdict"].get("converged"):
        return "UNDECIDED", "the M = 5 zero was found but the M = 7 walk from it did not run"
    why = "no M = 5 walk" if not m5 else "no M = 5 zero: " + str(m5["verdict"].get("why"))
    if not w7in:
        return "UNDECIDED", why + "; and no M = 7 walk from the input's point"
    E.Z["z16"] = dict(M5=Z3, s35=0.0)
    lab, txt = E.judge_zero("z16", w7in, mut)
    return lab, why + " (s35 undefined, taken as 0, so CONVERGES is not reachable); from the input's point: " + txt


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


def selftest(brk):
    mut = "ratio" if brk else ""

    def mk(r75, conv=True, A=3.5533, w=0.4132, why="x"):
        F5, F3 = [0.1, 0.0], [0.3, 0.0]
        p = dict(F3=F3, F5=F5, F7=[0.1 * r75, 0.0])
        return dict(points=[p], verdict=dict(converged=True, A=A, w=w, F3=F3, F5=F5, F7=p["F7"]) if conv else dict(converged=False, why=why))
    m5 = dict(verdict=dict(converged=True, A=3.5533 + 0.05, w=0.4132))          # s35 about 0.05
    got = [z16_verdict(m5, mk(0.1, A=3.5533 + 0.05 + 0.02), None, mut)[0],      # shift 0.02 < 0.05, ratio 0.1
           z16_verdict(m5, mk(0.35, A=3.5533 + 0.05 + 0.02), None, mut)[0],
           z16_verdict(m5, mk(0.25, A=3.5533 + 0.05 + 0.02), None, mut)[0],
           z16_verdict(m5, mk(0.1, A=3.5533 + 0.05 + 0.2), None, mut)[0],      # shift 0.2 > 0.05
           z16_verdict(m5, mk(0.1, conv=False, why="no step reduced |r_1|"), None, mut)[0],
           z16_verdict(dict(verdict=dict(converged=False, why="x")), None, mk(0.35), mut)[0],
           z16_verdict(dict(verdict=dict(converged=False, why="x")), None, mk(0.1), mut)[0]]
    want = ["CONVERGES", "DOES NOT", "UNDECIDED", "UNDECIDED", "DOES NOT", "DOES NOT", "UNDECIDED"]
    ok = got == want
    print(f"selftest{' --break (--mutate=ratio inside)' if brk else ''}: z16 verdicts {got} (expect {want}): {'PASS' if ok else 'FAIL'}")
    return ok and (brk or E.selftest())


def main(argv):
    if "--selftest" in argv:
        return 0 if selftest("--break" in argv) else 1
    d = argv[argv.index("--dir") + 1] if "--dir" in argv else os.path.join(HERE, "walks")
    mut = next((a.split("=")[1] for a in argv if a.startswith("--mutate=")), "")
    out = []
    ok0, t0 = E.judge_control(json.load(open(CTRL_FILE)), mut)
    out.append(f"evaluator on #1027's validated control walk (xi1 0.15), mutate '{mut}': {'PASS' if ok0 else 'FAIL'}: {t0}")
    ok = ok0                                            # --mutate=shift moves the stored zero: the check must fail, exit 1
    for xi in ("0.25", "0.2"):
        c = load(d, "control", xi)
        if c:
            okc, tc = E.judge_control(c)
            out.append(f"xi1 {xi} control (the known zero at M = 7; validated only at 0.15 in #1027): {'PASS' if okc else 'FAIL'}: {tc}")
        else:
            out.append(f"xi1 {xi} control: no walk")
        lab, txt = z16_verdict(load(d, "z16m5", xi), load(d, "z16", xi), load(d, "z16in", xi), mut)
        out.append(f"xi1 {xi} z16: {lab}: {txt}")
        out.append(f"xi1 {xi} z16 from the input's point (information): {info_in(load(d, 'z16in', xi))}")
    print("\n".join(out))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
