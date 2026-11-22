#!/usr/bin/env python3
"""next_window.py TARGET_D [DIR] | --selftest: the window of the next D of #1025 kc71_leap by the coordinator's rule of 2026-11-22 (hc): "scan a 0.40-wide window at 0.01, centered on the path extrapolated from the last two measured lambda_1 of your own k_c
(D 18.5 and D 19, then D 19 and D 19.5), rounded to 0.01". p(D) = lambda_b + (lambda_b - lambda_a) / (D_b - D_a) * (D - D_b), the two last measured lambda_1 being the det-linear estimates of the readings (LAMBDA_1 lines of read_D<D>.txt or
read_D<D>_ext<K>.txt, the last one for that D, taken only when no EDGE line follows it; lambda_1(18.5) = 1.675995 at k_c 71, ../kc71_d185/kc71_read.txt). The window is [center - 0.20, center + 0.20] at 0.01 (41 points), center = round(p, 2);
the path used by the reading is p itself. Prints 'LO HI PATH'. D 19 is not computed (ordered: 1.40 to 1.80, path 1.545995)."""
import glob
import os
import re
import sys

L185 = 1.675995


def path_of(pa, pb, D):
    (Da, la), (Db, lb) = pa, pb
    return lb + (lb - la) / (Db - Da) * (D - Db)


def window(p):
    c = round(p, 2)
    return round(c - 0.20, 2), round(c + 0.20, 2)


def last_lambda1(H, D):
    tag = "%g" % D
    files = sorted(glob.glob(H + "read_D%s_ext*.txt" % tag), key=lambda f: int(re.search(r"_ext(\d+)", f).group(1)), reverse=True) + [H + "read_D%s.txt" % tag]
    for f in files:
        if os.path.exists(f):
            t = open(f).read()
            m = re.search(r"^LAMBDA_1: ([0-9.]+) ", t, re.M)
            if m and not re.search(r"^EDGE ", t, re.M):
                return float(m.group(1)), f
    return None, None


def selftest():
    p = path_of((18.5, L185), (19.0, 1.55), 19.5)
    lo, hi = window(p)
    ok1 = abs(p - 1.424005) < 1e-9 and (lo, hi) == (1.22, 1.62)
    p2 = path_of((19.0, 1.55), (19.5, 1.43), 20.0)
    lo2, hi2 = window(p2)
    ok2 = abs(p2 - 1.31) < 1e-9 and (lo2, hi2) == (1.11, 1.51)
    print("planted: lambda_1(19) = 1.55 gives p(19.5) = %.6f, window %s %s: %s" % (p, lo, hi, "PASS" if ok1 else "FAIL"))
    print("planted: lambda_1(19) = 1.55, lambda_1(19.5) = 1.43 gives p(20) = %.6f, window %s %s: %s" % (p2, lo2, hi2, "PASS" if ok2 else "FAIL"))
    print("selftest: %s" % ("PASS" if ok1 and ok2 else "FAIL"))
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest())
    D = float(sys.argv[1])
    H = (sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))).replace("\\", "/").rstrip("/") + "/"
    if D == 19.5:
        l19, f = last_lambda1(H, 19.0)
        if l19 is None:
            sys.exit("no read lambda_1 at D 19 (an unresolved EDGE or no reading): no window")
        pa, pb = (18.5, L185), (19.0, l19)
    elif D == 20.0:
        l19, f1 = last_lambda1(H, 19.0)
        l195, f2 = last_lambda1(H, 19.5)
        if l19 is None or l195 is None:
            sys.exit("no read lambda_1 at D 19 or D 19.5: no window")
        pa, pb = (19.0, l19), (19.5, l195)
    else:
        sys.exit("only D 19.5 and D 20 are computed by this rule")
    p = path_of(pa, pb, D)
    lo, hi = window(p)
    print("# from lambda_1(%g) = %.6f and lambda_1(%g) = %.6f: p(%g) = %.6f, center %.2f" % (pa[0], pa[1], pb[0], pb[1], D, p, round(p, 2)), file=sys.stderr)
    print("%.2f %.2f %.6f" % (lo, hi, p))
