#!/usr/bin/env python3
"""The step line's pivots are those of the accepted point (octo_corrector.newton_od prints st after z, st = zk, stt),
so they pair with that point's own step |dz_new|, not with the |dz| the step started from (table_839.py's pairing).
Prints both ratios per accepted step and the fit of the pivot against |dz_new|. Check: the fit's exponent recovers 1
within 0.05 on a planted series piv = 0.0105 |dz|; control --mutate=pair uses the start |dz| on the planted series
shifted by one step, which must not recover the planted constant within 3%.
usage: python3 pivot_pair.py LOG... | --selftest [--mutate=pair]"""
import math
import re
import sys

STEP = re.compile(r"^  on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+), dDelta (\S+), piv (\S+)\.\.")


def fit(xs, ys):
    lx, ly = [math.log10(x) for x in xs], [math.log10(y) for y in ys]
    mx, my = sum(lx) / len(lx), sum(ly) / len(ly)
    p = sum((a - mx) * (b - my) for a, b in zip(lx, ly)) / sum((a - mx) ** 2 for a in lx)
    return p, 10 ** (my - p * mx)


def rows(path):
    return [(int(m.group(1)), float(m.group(4)), float(m.group(5)), float(m.group(8)))
            for m in map(STEP.match, open(path).read().splitlines()) if m]


def selftest(mutate):
    dz = [2.2e-12 * 0.7 ** k for k in range(8)]
    r = [(k, dz[k], dz[k + 1], 0.0105 * dz[k + 1]) for k in range(7)]
    xs = [a for _, a, _, _ in r] if mutate == "pair" else [b for _, _, b, _ in r]
    p, c = fit(xs, [v for *_, v in r])
    ok = abs(p - 1) <= 0.05 and abs(c / 0.0105 - 1) <= 0.03
    print(f"pivot_pair selftest{' --mutate=' + mutate if mutate else ''}: exponent {p:.4f}, constant {c:.4e} "
          f"(planted 1, 0.0105): {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv):
    if argv and argv[0] == "--selftest":
        return selftest(next((a.split("=", 1)[1] for a in argv[1:] if a.startswith("--mutate=")), ""))
    for path in argv:
        r = rows(path)
        print(f"{path}: | step | \\|dz\\| start | \\|dz\\| at the accepted point | pivot there | pivot/start | pivot/own |")
        for k, a, b, v in r:
            print(f"  | {k} | {a:.2e} | {b:.2e} | {v:.1e} | {v / a:.4f} | {v / b:.4f} |")
        own = [v / b for _, _, b, v in r]
        p, c = fit([b for _, _, b, _ in r], [v for *_, v in r])
        print(f"  pivot/own from {min(own):.4f} to {max(own):.4f}; fit pivot = {c:.3e} |dz|^{p:.4f} over {len(r)} points")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
