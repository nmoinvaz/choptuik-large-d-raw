#!/usr/bin/env python3
"""#816's verdict on the first Newton step from the planted truth at D 252.6 (truth_D252.json, octo_corrector.py
planted --rel 0). The step's Delta correction dD gives:
  "truth": |dD| < 1e-20, so the truth is the root along Delta;
  "corrector": |dD - (-2.018e-11)| <= 1e-12, so the root lies at the corrector's Delta (#713, #777);
  "neither": anything else, reported as such.
usage: python3 verdict_816.py RUN.json      (exit 0 when a verdict is reached, either one; 1 for "neither")
       python3 verdict_816.py --selftest    (planted dD values through the same rule; exit 0 on pass)
       python3 verdict_816.py --selftest --mutate=sign   (the rule with the reference's sign flipped; must fail)"""
import json
import sys

REF = -2.018e-11        # #777's rerun and #713's s0_D252: the corrector's Delta against the truth
TRUTH_BAR, REF_BAR = 1e-20, 1e-12


def verdict(dD, ref=REF):
    if abs(dD) < TRUTH_BAR:
        return "truth"
    if abs(dD - ref) <= REF_BAR:
        return "corrector"
    return "neither"


def selftest(mutate):
    ref = -REF if mutate == "sign" else REF
    planted = [(0.0, "truth"), (9.9e-21, "truth"), (-3e-20, "neither"), (-2.0184e-11, "corrector"),
               (-2.018e-11 + 9e-13, "corrector"), (-2.018e-11 - 1.1e-12, "neither"), (+2.018e-11, "neither"),
               (1.1e-5, "neither")]
    ok = True
    for dD, want in planted:
        got = verdict(dD, ref)
        ok &= got == want
        print(f"  dD {dD:+.4e}: {got} (want {want}){'' if got == want else '  <- wrong'}")
    print(f"verdict_816 selftest{' --mutate=' + mutate if mutate else ''}: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv):
    if argv and argv[0] == "--selftest":
        mutate = next((a.split("=", 1)[1] for a in argv[1:] if a.startswith("--mutate=")), "")
        return selftest(mutate)
    rec = json.load(open(argv[0]))
    hist = rec["od"]["hist"]
    h0 = hist[0]
    v = verdict(h0["dDelta"])
    print(f"{argv[0]}: start max|F| {h0['F']:.3e}, first step |dz| {h0['dz']:.4e}, dDelta {h0['dDelta']:+.6e}, lam "
          f"{h0.get('lam')}, smallest pivot {h0['piv'][0]:.2e}")
    for h in hist[1:]:
        print(f"  step {h['it']}: max|F| {h['F']:.3e}, |dz| {h['dz']:.4e}, dDelta {h['dDelta']:+.6e}, lam {h.get('lam')}")
    print(f"  od: steps {rec['od']['steps']}, converged {rec['od']['converged']}, final max|F| {rec['od']['F']:.3e}, "
          f"Delta {rec['od']['Delta']}")
    print(f"verdict: {v} (|dD| < {TRUTH_BAR:g}: truth; within {REF_BAR:g} of {REF:g}: corrector)")
    return 1 if v == "neither" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
