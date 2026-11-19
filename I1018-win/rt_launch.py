#!/usr/bin/env python3
"""Run one of solver/rt's scripts with the two names this interpreter lacks supplied: multidouble._dd_dot and math.fma.
usage: python rt_launch.py SCRIPT.py [args...]      (SCRIPT.py is rt_run.py, rt_roots.py or rt_grids.py of the worktree)
1. solver/rt/rt_mpsolve.py checks for multidouble.dd_dot and then calls multidouble._dd_dot (line 187), a name this venv's multidouble 0.1.0 does not have. It has
   dd_dot(xh, xl, yh, yl), the same arguments, a wrapper that converts its arguments to float64 and calls the Rust function; the alias makes the call the wrapper.
2. rt_mpsolve._dd_div calls math.fma (Python 3.13 and later; this venv is Python 3.10). math.fma(x, y, z) is x*y + z with one rounding. The replacement computes it exactly
   with fractions.Fraction and rounds once to the nearest double (Fraction.__float__ is correctly rounded), so it returns what math.fma returns. Selftest: `python rt_launch.py --selftest`.
No file of the repository is changed."""
import math
import os
import random
import runpy
import sys
from fractions import Fraction

import multidouble as md

if not hasattr(md, "_dd_dot"):
    md._dd_dot = md.dd_dot


def _fma(x, y, z):
    x, y, z = float(x), float(y), float(z)
    if not (math.isfinite(x) and math.isfinite(y) and math.isfinite(z)):
        return x * y + z
    r = Fraction(x) * Fraction(y) + Fraction(z)
    return float(r)


if not hasattr(math, "fma"):
    math.fma = _fma


def selftest():
    import flint
    flint.ctx.prec = 600
    rng = random.Random(1)
    bad, naive_differs = 0, 0
    for _ in range(20000):
        x = rng.uniform(-1, 1) * 2.0 ** rng.randint(-30, 30)
        y = rng.uniform(-1, 1) * 2.0 ** rng.randint(-30, 30)
        z = -x * y * (1 + rng.uniform(-1, 1) * 2.0 ** -rng.randint(40, 60)) if rng.random() < 0.5 else rng.uniform(-1, 1) * 2.0 ** rng.randint(-60, 60)
        want = float(flint.arb(x) * flint.arb(y) + flint.arb(z))
        got = _fma(x, y, z)
        bad += got != want
        naive_differs += (x * y + z) != want
    print(f"fma shim against arb at 600 bits: {bad} differ of 20000; the naive x*y + z differs from the exact value in {naive_differs} (the control: the test can see a missing single rounding)")
    return 0 if bad == 0 and naive_differs > 0 else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest())
    script = sys.argv[1]
    sys.argv = [script] + sys.argv[2:]
    sys.path.insert(0, os.path.dirname(script))
    runpy.run_path(script, run_name="__main__")
