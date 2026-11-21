#!/usr/bin/env python3
"""gate1064f.py LOG OUTDIR [MAXF] | --selftest [--break]: the verdict of one base polish for run1064f.sh (#1064, D 237.7132; the coordinator's gate of 21 Nov: the octo-double Newton converged with max|F| <= 1e-60,
--tol_od 1e-60 as in #973). 'converged' when the LAST octo-double Newton line of LOG ends 'converged' (not 'not converged', in either case), its max|F| is a number at most MAXF (default 1e-60) and OUTDIR holds a saved base
(base_pin3_D*.npz); else 'failed' with the reason (a converged line above MAXF, as ends by the floor rule, is a failure of this gate and says so). Exit 0 converged, 1 failed. --selftest runs planted logs through the same
function, each with its expected verdict, and exits 0 when every verdict is as expected; --break flips one expectation and must exit 1."""
import glob
import re
import sys
import tempfile

LINE = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.eE+-]+|nan|inf), (not converged|converged)", re.I)


def verdict(text, base_saved, maxf=1e-60):
    lines = LINE.findall(text)
    if not lines:
        return False, "no octo-double Newton line"
    n, F, c = lines[-1]
    try:
        f = float(F)
    except ValueError:
        f = float("nan")
    conv = c.lower() == "converged"
    small = f <= maxf          # false for nan
    ok = conv and small and base_saved
    why = f"last octo-double Newton line {n} steps, max|F| {F}, {c}, base saved {base_saved}"
    if conv and not small:
        why += f"; max|F| above {maxf:g}"
    return ok, why


def gate(log, outdir, maxf=1e-60):
    text = open(log, errors="replace").read()
    return verdict(text, bool(glob.glob(f"{outdir}/base_pin3_D*.npz")), maxf)


def selftest(brk):
    conv = "octo-double Newton: 3 steps, max|F| 7.4e-86, converged; double-double |F| of its first two parts 5.6e+31\n"
    floor = "octo-double Newton: 5 steps, max|F| 2.5e-34, converged; double-double |F| of its first two parts 1.6e+31\n"
    edge = "octo-double Newton: 4 steps, max|F| 1e-60, converged; double-double |F| of its first two parts 1.6e+31\n"
    over = "octo-double Newton: 4 steps, max|F| 1.1e-60, converged; double-double |F| of its first two parts 1.6e+31\n"
    notc = "octo-double Newton: 5 steps, max|F| 1.6e-90, not converged; double-double |F| of its first two parts 8.0e+05\n"
    NOTC = notc.replace("not converged", "NOT converged")
    nan = "octo-double Newton: 5 steps, max|F| nan, converged; double-double |F| of its first two parts 8.0e+05\n"
    cases = [  # name, text, base saved, expected
        ("converged at 7.4e-86 and base saved", conv, True, True),
        ("converged at 7.4e-86, no base", conv, False, False),
        ("converged at 2.5e-34 (floor rule), base saved", floor, True, False),
        ("converged at exactly 1e-60, base saved", edge, True, True),
        ("converged at 1.1e-60, base saved", over, True, False),
        ("not converged (lower case) at 1.6e-90, base saved", notc, True, False),
        ("NOT converged (upper case), base saved", NOTC, True, False),
        ("converged then not converged last", conv + notc, True, False),
        ("not converged then converged last", notc + conv, True, True),
        ("converged at nan", nan, True, False),
        ("no Newton line", "horizon series to order 331\n", True, False),
    ]
    if brk:
        cases[2] = (cases[2][0], cases[2][1], cases[2][2], True)
    bad = 0
    for name, text, base, want in cases:
        with tempfile.TemporaryDirectory() as d:
            if base:
                open(f"{d}/base_pin3_D237.7132.npz", "w").close()
            open(f"{d}/l.log", "w").write(text)
            ok, msg = gate(f"{d}/l.log", d)
        print(f"  {name}: {'converged' if ok else 'failed'} (expected {'converged' if want else 'failed'}): {'ok' if ok == want else 'WRONG'}")
        bad += ok != want
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    ok, msg = gate(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1e-60)
    print(f"{'converged' if ok else 'failed'}: {msg}")
    sys.exit(0 if ok else 1)
