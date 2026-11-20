#!/usr/bin/env python3
"""cmp_planted.py A.log B.log [--mutate]: two octo_corrector.py planted logs, compared line by line with the trailing wall seconds
(", 56.74 s") and the '#' header and 'exit' lines left out. Equal in every printed digit (every per-step max|F|, |dz|, dDelta,
the pivots, the final Delta) -> exit 0, else exit 1. --mutate changes one digit of the first max|F| value of B before comparing:
the control, which must exit 1."""
import re
import sys


def norm(path):
    out = []
    for ln in open(path).read().splitlines():
        if ln.startswith("#") or ln.startswith("exit "):
            continue
        out.append(re.sub(r", [0-9.]+ s$", "", ln.rstrip()))
    return out


def main():
    a, b = norm(sys.argv[1]), norm(sys.argv[2])
    if "--mutate" in sys.argv:
        for i, ln in enumerate(b):
            m = re.search(r"max\|F\| (\d)\.(\d)", ln)
            if m:
                d = str((int(m.group(2)) + 1) % 10)
                b[i] = ln[:m.start(2)] + d + ln[m.end(2):]
                break
    nF = sum("|F|" in ln for ln in a)
    fin = [ln for ln in a if "converged, Delta" in ln or ln.strip().startswith("od:")]
    bad = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    n_diff = len(bad) + abs(len(a) - len(b))
    for i, x, y in bad[:12]:
        print(f"line {i}: A {x[:160]}\n         B {y[:160]}")
    if len(a) != len(b):
        print(f"line counts differ: {len(a)} against {len(b)}")
    print(f"{len(a)} lines of A, {len(b)} of B, {nF} lines with |F|, final lines: {len(fin)}; {n_diff} differ: {'IDENTICAL' if n_diff == 0 else 'DIFFER'}")
    sys.exit(0 if n_diff == 0 else 1)


main()
