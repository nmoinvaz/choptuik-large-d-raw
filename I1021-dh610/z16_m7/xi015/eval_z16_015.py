#!/usr/bin/env python3
"""eval_z16_015.py [--dir walks] [--mutate=shift5|shift7] [--selftest [--break]]: box 16 at xi1 0.15 with #1026's M = 5 control (eval1026.judge_control, the stored zero within
1e-5) and #1027's M = 7 control (eval1027.judge_control) as gates, then eval_z16.z16_verdict (#1027's rule). The result counts only if both gates pass in this run, else
NO VERDICT with the controls' residuals. --mutate=shift5 / shift7 moves that control's expected zero (the gate must fail, exit 1). --selftest: synthetic gate cases;
--break ignores the gates inside it (the self-test must then fail, exit 1)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import eval1026 as E5  # noqa: E402
import eval1027 as E7  # noqa: E402
import eval_z16 as Z  # noqa: E402


def gates(c5, c7, m5mut="", m7mut=""):
    """(ok5, text5, ok7, text7) from the two control walks (dicts or None)"""
    ok5, t5 = E5.judge_control(c5["verdict"], m5mut) if c5 else (False, "no walk")
    ok7, t7 = E7.judge_control(c7, m7mut) if c7 else (False, "no walk")
    return ok5, t5, ok7, t7


def final(m5, w7, w7in, c5, c7, brk=False, m5mut="", m7mut=""):
    ok5, t5, ok7, t7 = gates(c5, c7, m5mut, m7mut)
    lab, txt = Z.z16_verdict(m5, w7, w7in)
    counts = (ok5 and ok7) or brk
    out = "%s: %s" % (lab, txt) if counts else "NO VERDICT (control residuals: M = 5 control %s; M = 7 control %s)" % (t5, t7)
    return counts, out, ok5, t5, ok7, t7


def selftest(brk):
    mk7 = lambda ok: dict(points=[dict(F3=[0.05, 0], F5=[0.003, 0], F7=[0.003 * E7.CTRL_RATIO, 0])], verdict=dict(converged=True, A=E7.CTRL[0] + (1e-5 if ok else 1e-3), w=E7.CTRL[1]))
    mk5 = lambda ok: dict(verdict=dict(converged=True, A=E5.STORED[0] + (1e-6 if ok else 1e-3), w=E5.STORED[1]))
    m5 = dict(verdict=dict(converged=True, A=3.5533 + 0.05, w=0.4132))

    def w7(r):
        F5, F3 = [0.1, 0.0], [0.3, 0.0]
        p = dict(F3=F3, F5=F5, F7=[0.1 * r, 0.0])
        return dict(points=[p], verdict=dict(converged=True, A=3.5533 + 0.05 + 0.02, w=0.4132, F3=F3, F5=F5, F7=p["F7"]))
    got = [final(m5, w7(0.1), None, mk5(True), mk7(True), brk)[0], final(m5, w7(0.1), None, mk5(False), mk7(True), brk)[0],
           final(m5, w7(0.1), None, mk5(True), mk7(False), brk)[0], final(m5, w7(0.1), None, None, mk7(True), brk)[0]]
    want = [True, False, False, False]
    ok = got == want
    print(f"selftest{' --break (gates ignored)' if brk else ''}: result counts {got} (expect {want}; both controls pass, M = 5 control off, M = 7 control off, M = 5 control missing): {'PASS' if ok else 'FAIL'}")
    return ok


def main(argv):
    if "--selftest" in argv:
        return 0 if selftest("--break" in argv) else 1
    d = argv[argv.index("--dir") + 1] if "--dir" in argv else os.path.join(HERE, "walks")
    mut = next((a.split("=")[1] for a in argv if a.startswith("--mutate=")), "")
    ld = lambda n: json.load(open(os.path.join(d, f"walk_{n}_xi0.15.json"))) if os.path.exists(os.path.join(d, f"walk_{n}_xi0.15.json")) else None
    c5, c7 = ld("control5"), ld("control7")
    counts, out, ok5, t5, ok7, t7 = final(ld("z16m5"), ld("z16"), ld("z16in"), c5, c7, False, "shift" if mut == "shift5" else "", "shift" if mut == "shift7" else "")
    print(f"gate M = 5 (#1026's control at xi1 0.15): {'PASS' if ok5 else 'FAIL'}: {t5}")
    print(f"gate M = 7 (#1027's control at xi1 0.15): {'PASS' if ok7 else 'FAIL'}: {t7}")
    m5 = ld("z16m5")
    print(f"box 16 M = 5 walk: " + ("no walk" if not m5 else (f"converged, zero ({m5['verdict']['A']:.6f}, {m5['verdict']['w']:.6f})" if m5["verdict"].get("converged") else "no M = 5 zero: " + str(m5["verdict"].get("why")))))
    print(f"box 16 from the input's point (information): {Z.info_in(ld('z16in'))}")
    print(f"FINAL at xi1 0.15 ({'counts' if counts else 'does not count'}): {out}")
    return 0 if (ok5 and ok7) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
