#!/usr/bin/env python3
"""gate1064.py LOG OUTDIR | --selftest [--break]: the verdict of one base polish (#1064, the issue's reading, #973's gate). 'converged' when the LAST
octo-double Newton line of LOG ends 'converged' (not 'not converged', in either case) and OUTDIR holds a saved base (base_pin3_D*.npz); else 'failed'
with the reason. The line's max|F| is printed as information (leg 13's --tol_od is 2e-34; #973's gate also asked max|F| <= 1e-60, its --tol_od). Exit 0 converged,
1 failed. --selftest runs planted logs through the same function, each with its expected verdict, and exits 0 when every verdict is as expected; --break
flips one expectation and must exit 1."""
import glob
import os
import re
import sys
import tempfile

LINE = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.eE+-]+|nan|inf), (not converged|converged)", re.I)


def verdict(text, base_saved):
    lines = LINE.findall(text)
    if not lines:
        return False, "no octo-double Newton line"
    n, F, c = lines[-1]
    ok = c.lower() == "converged" and base_saved
    return ok, f"last octo-double Newton line {n} steps, max|F| {F}, {c}, base saved {base_saved}"


def gate(log, outdir):
    text = open(log, errors="replace").read()
    return verdict(text, bool(glob.glob(f"{outdir}/base_pin3_D*.npz")))


def selftest(brk):
    conv = "octo-double Newton: 3 steps, max|F| 7.4e-38, converged; double-double |F| of its first two parts 5.6e+31\n"
    notc = "octo-double Newton: 5 steps, max|F| 1.6e-24, not converged; double-double |F| of its first two parts 8.0e+05\n"
    NOTC = notc.replace("not converged", "NOT converged")
    cases = [  # name, text, base saved, expected
        ("converged and base saved", conv, True, True),
        ("converged, no base", conv, False, False),
        ("not converged (lower case), base saved", notc, True, False),
        ("NOT converged (upper case), base saved", NOTC, True, False),
        ("converged then not converged last", conv + notc, True, False),
        ("not converged then converged last", notc + conv, True, True),
        ("no Newton line", "horizon series to order 315\n", True, False),
    ]
    if brk:
        cases[2] = (cases[2][0], cases[2][1], cases[2][2], True)
    bad = 0
    for name, text, base, want in cases:
        with tempfile.TemporaryDirectory() as d:
            if base:
                open(f"{d}/base_pin3_D261.0721.npz", "w").close()
            open(f"{d}/l.log", "w").write(text)
            ok, msg = gate(f"{d}/l.log", d)
        print(f"  {name}: {'converged' if ok else 'failed'} (expected {'converged' if want else 'failed'}): {'ok' if ok == want else 'WRONG'}")
        bad += ok != want
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    ok, msg = gate(sys.argv[1], sys.argv[2])
    print(f"{'converged' if ok else 'failed'}: {msg}")
    sys.exit(0 if ok else 1)
