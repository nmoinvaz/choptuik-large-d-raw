#!/usr/bin/env python3
"""#1025 eval_dh170_d1975 (dh610) eval_compare.py MINE_1.32.jsonl MINE_1.33.jsonl HIS.jsonl LINRE_1.32.jsonl LINRE_1.33.jsonl | selftest [--mutate]
dh170's start state (blob 352107a8) evaluated on this build at 1.32 and 1.33 (x), against dh170's own rows (h, I1025-dh170/kc87_d1975, his machine) and against linRe's rows (l, this build, 4.0e-10 from his state), in ln|det|.
The coordinator's readings, as numeric rules written before the run (both lambda must satisfy):
  (b) the evaluation is that steep along the 4e-10 move: |x - h| <= 1e-3.
  (a) the two Linux machines evaluate ln|det| differently: |x - l| <= 1e-4 and |x - h| >= 0.1 (the observed |l - h| is 0.416 and 0.378).
  (c) neither: anything else; the numbers are reported.
Exit 0 after printing (the reading is information); selftest exit 0 only if every planted case reads as written; --mutate widens (b)'s bar to 1.0, which the 0.2 case must then fail to catch (exit 1)."""
import sys, json

BAR_B, BAR_A_L, MIN_A_H = 1e-3, 1e-4, 0.1


def last(f, lam):
    return [r for r in map(json.loads, (l for l in open(f) if l.strip())) if abs(r["lam"] - lam) < 1e-9][-1]


def read(xs, hs, ls, bar_b=BAR_B):
    dh = [x - h for x, h in zip(xs, hs)]
    dl = [x - l for x, l in zip(xs, ls)]
    b = all(abs(d) <= bar_b for d in dh)
    a = all(abs(d) <= BAR_A_L for d in dl) and all(abs(d) >= MIN_A_H for d in dh)
    return ("a" if a else "b" if b else "c"), dh, dl


H = (-2806.4460599255, -2806.6102602939)
L = (-2806.0300899137, -2806.9886015473)


def selftest(mutate):
    bb = 1.0 if mutate else BAR_B
    cases = [("(a) planted: x = l + 5e-5", [l + 5e-5 for l in L], "a"), ("(b) planted: x = h + 5e-4", [h + 5e-4 for h in H], "b"),
             ("(b) planted: x = h exactly", list(H), "b"), ("(c) planted: x = h + 0.2", [h + 0.2 for h in H], "c"),
             ("(c) planted: x = h + 2e-3 (between the bars)", [h + 2e-3 for h in H], "c"), ("(c) planted: x = l + 3e-4 (outside (a)'s bar)", [l + 3e-4 for l in L], "c"),
             ("(c) planted: (b) at 1.32 only", [H[0] + 5e-4, H[1] + 0.2], "c")]
    bad = 0
    for name, xs, want in cases:
        got = read(xs, H, L, bb)[0]
        ok = got == want
        bad += not ok
        print(f"  {name}: read ({got}), wanted ({want}): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    m1, m2, hf, l1, l2 = sys.argv[1:6]
    mine = [last(m1, 1.32), last(m2, 1.33)]
    his = [last(hf, 1.32), last(hf, 1.33)]
    lin = [last(l1, 1.32), last(l2, 1.33)]
    xs, hs, ls = [r["ln"] for r in mine], [r["ln"] for r in his], [r["ln"] for r in lin]
    rd, dh, dl = read(xs, hs, ls)
    sg = lambda s: "+" if s > 0 else "-"
    print("| lambda | this build on dh170's state | hybrid sign | noise signs | float64 sign | dh170's rows (his machine) | linRe (this build) | mine minus his | mine minus linRe | his minus linRe |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for i, lam in enumerate((1.32, 1.33)):
        print(f"| {lam:.2f} | {xs[i]:.10f} | {sg(mine[i]['sign'])} | {''.join(sg(x) for x in mine[i]['noise'])} (robust {mine[i]['noise_robust']}) | {sg(mine[i]['f64_sign'])} | {hs[i]:.10f} ({sg(his[i]['sign'])}) | {ls[i]:.10f} ({sg(lin[i]['sign'])}) | {dh[i]:+.6f} | {dl[i]:+.6f} | {hs[i] - ls[i]:+.6f} |")
    root = lambda a, b: 1.32 + 0.01 * 1.0 / (1.0 + __import__("math").exp(b - a)) if mine[0]["sign"] != mine[1]["sign"] else None
    r = root(xs[0], xs[1])
    print(f"det-linear root in (1.32, 1.33) from the two points: this build on dh170's state {r:.6f}" if r else "no sign change between 1.32 and 1.33 on this build")
    print(f"reading by the rules written before the run: ({rd})  [(b) |mine - his| <= 1e-3 at both; (a) |mine - linRe| <= 1e-4 and |mine - his| >= 0.1 at both; (c) otherwise]")
