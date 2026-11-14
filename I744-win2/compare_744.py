#!/usr/bin/env python3
"""#744: the checks and the table of the homotopy in the horizon order at D 245.1366.
    python -I compare_744.py control FOLDER     exit 0 when c131's and w0's Delta agree to 1e-40 (w = 0 is order 131)
    python -I compare_744.py table FOLDER       the ladder's table, and the mutation: jump's step-0 lines against s132's
    python -I compare_744.py selftest           the checks on planted inputs; exit 0 when each fires as it must
FOLDER is I744-win2/ (its parent is the raw clone). Delta is the exact sum of a saved base's eight parts (mpmath, 600
bits). The mutation passes when jump.log's step-0 lines, timings cut, equal I696-win2/D245/s132.log's: the jump from
w = 0 to w = 1 in one step is s132's first step, the 1.18e20 one.
"""
import os
import re
import sys

import mpmath as mp
import numpy as np

mp.mp.prec = 600
KEYS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
RUNGS = [("w0", 0.0), ("w0625", 0.0625), ("w125", 0.125), ("w25", 0.25), ("w5", 0.5), ("w1", 1.0)]
TIMING = re.compile(r", [0-9.]+ s$")


def delta(path):
    d = np.load(path, allow_pickle=False)
    return mp.fsum(mp.mpf(float(d[k][-1])) for k in KEYS if k in d.files)


def base(folder, tag):
    p = os.path.join(folder, tag)
    names = [f for f in os.listdir(p) if f.startswith("base_pin3_D") and f.endswith(".npz")] if os.path.isdir(p) else []
    return os.path.join(p, sorted(names)[0]) if names else None


def newton(log):
    """(steps, final max|F|, converged) from a log's last octo-double Newton line"""
    if not os.path.exists(log):
        return None
    lines = [s for s in open(log, encoding="utf-8", errors="replace") if re.search(r"octo-double Newton: \d+ steps", s)]
    if not lines:
        return None
    return newton_line(lines[-1])


def step0(lines):
    return [TIMING.sub("", s.strip()) for s in lines if re.match(r"\s*on 0[ :]", s)]


def control_ok(a, b):
    return abs(a - b) <= mp.mpf("1e-40")


def control(folder):
    pa, pb = base(folder, "c131"), base(folder, "w0")
    if not pa or not pb:
        print(f"control: a base is missing (c131 {pa}, w0 {pb})")
        return 1
    d = delta(pb) - delta(pa)
    ok = control_ok(delta(pa), delta(pb))
    print(f"control: Delta(w0) - Delta(c131) = {mp.nstr(d, 5)}; bar 1e-40: {'met' if ok else 'NOT MET'}")
    return 0 if ok else 1


def table(folder):
    raw = os.path.dirname(os.path.abspath(folder))
    rows, d0, prev = [], None, None
    print("| rung | w | Newton steps | final max\\|F\\| | converged | Delta - Delta(w0) | change from the rung before |")
    print("|---|---|---|---|---|---|---|")
    for tag, w in RUNGS:
        b, nw = base(folder, tag), newton(os.path.join(folder, f"{tag}.log"))
        if not b or not nw:
            print(f"| {tag} | {w} | not run or no base | | | | |")
            continue
        dl = delta(b)
        d0 = dl if d0 is None else d0
        ch = "" if prev is None else mp.nstr(dl - prev, 4)
        print(f"| {tag} | {w} | {nw[0]} | {nw[1]} | {'yes' if nw[2] else 'NO'} | {mp.nstr(dl - d0, 4)} | {ch} |")
        prev = dl
    j, s = os.path.join(folder, "jump.log"), os.path.join(raw, "I696-win2", "D245", "s132.log")
    if os.path.exists(j) and os.path.exists(s):
        a = step0(open(s, encoding="utf-8", errors="replace").read().splitlines())
        b = step0(open(j, encoding="utf-8", errors="replace").read().splitlines())
        ok = len(a) > 0 and a == b[:len(a)]
        print(f"\nmutation: jump's step-0 lines against s132's: {len(b)} against {len(a)}, "
              f"{'equal (the 1.18e20 step reproduced)' if ok else 'DIFFER'}")
        if not ok:
            for k in range(min(len(a), len(b))):
                if a[k] != b[k]:
                    print(f"   first difference at line {k}:\n     s132: {a[k]}\n     jump: {b[k]}")
                    break
    return 0


def selftest():
    bad = 0
    for x, y, want in ((mp.mpf(1), mp.mpf(1) + mp.mpf("2e-40"), False), (mp.mpf(1), mp.mpf(1) + mp.mpf("5e-41"), True)):
        got = control_ok(x, y)
        print(f"  control at {mp.nstr(y - x, 2)}: {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    ln = "  octo-double Newton: 7 steps, max|F| 3.2e-62, converged; double-double |F| of its first two parts 1.0e+06"
    got = newton_line(ln)
    ok = got == (7, "3.2e-62", True)
    print(f"  a converged Newton line: {got} {'ok' if ok else 'WRONG'}")
    bad += not ok
    got = newton_line(ln.replace(", converged", ", not converged"))
    ok = got is not None and got[2] is False
    print(f"  a not-converged Newton line: {got} {'ok' if ok else 'WRONG'}")
    bad += not ok
    a = ["  on 0 chord 0: max|F| 1.18e+20, |dw| 4.995e+30", "    on 0 trial lam 1: max|F| 1.18e+20; refused, 60.34 s"]
    b = [a[0], a[1].replace("60.34", "71.02")]
    ok = step0(a) == step0(b) and step0(a) != step0([a[0], a[1].replace("1.18e+20; refused", "1.17e+20; refused")])
    print(f"  step-0 lines equal across timings and differ on a value: {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return 1 if bad else 0


def newton_line(line):
    m = re.search(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.eE+-]+|nan), (not converged|converged)", line)
    return (int(m.group(1)), m.group(2), m.group(3) == "converged") if m else None


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "selftest":
        sys.exit(selftest())
    if cmd in ("control", "table") and len(sys.argv) == 3:
        sys.exit(control(sys.argv[2]) if cmd == "control" else table(sys.argv[2]))
    sys.exit(__doc__)
