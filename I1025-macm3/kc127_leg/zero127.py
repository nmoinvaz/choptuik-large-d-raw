#!/usr/bin/env python3
"""zero127.py [--mutate=sign] > zero_arithmetic_127.txt : the zero in D of lambda_1 at k_c 127 by the straight line through its two secant roots
(D 23.0625 from kc127_d230625/point_summary.txt, D 23.125 from point_D23.125_summary.txt), the slope, the zero over the four bracket-end
combinations, and the comparison with the registered intervals. Arithmetic on two points, not a result. Exit 1 when the two roots do not
change sign or the zero lies outside [23.0625, 23.125]. --mutate=sign flips the sign of the D 23.125 root: must exit 1."""
import os, re, sys
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/")

def read(p):
    t = open(p).read()
    b = re.search(r"root bracket \[(\S+), (\S+)\], width (\S+), signs", t)
    r = re.search(r"det-linear root (-?[\d.]+)", t).group(1)
    return float(r), float(b.group(1)), float(b.group(2))

def lz(Da, ra, Db, rb):
    return Da - ra * (Db - Da) / (rb - ra)

def main():
    mut = "--mutate=sign" in sys.argv
    Da, Db = 23.0625, 23.125
    ra, la, ha = read(R + "kc127_d230625/point_summary.txt")
    rb, lb, hb = read(R + "kc127_leg/point_D23.125_summary.txt")
    if mut:
        rb, lb, hb = -rb, -hb, -lb
    z = lz(Da, ra, Db, rb); sl = (rb - ra) / (Db - Da)
    zs = [lz(Da, x, Db, y) for x in (la, ha) for y in (lb, hb)]
    print("k_c 127 roots: D %s %+.8f [%.8f, %.8f]; D %s %+.8f [%.8f, %.8f]" % (Da, ra, la, ha, Db, rb, lb, hb))
    print("slope per unit D: %+.5f" % sl)
    print("zero by the line through the two roots: D %.5f" % z)
    print("zero over the four bracket-end combinations: %.5f to %.5f" % (min(zs), max(zs)))
    print("registered: mine 23.066 to 23.070 (central 23.068, slope -0.683), t5 near 23.068 (slope about -0.71): read %.5f, in my interval %s, differs from t5's 23.068 by %+.5f" % (z, 23.066 <= z <= 23.070, z - 23.068))
    print("root at D 23.125: mine -0.039 +- 0.006: difference %+.6f, within %s; t5 -0.040 +- 0.010: difference %+.6f, within %s; t5's band (-0.050, -0.030): %s" % (
        rb + 0.039, abs(rb + 0.039) <= 0.006, rb + 0.040, abs(rb + 0.040) <= 0.010, -0.050 < rb < -0.030))
    ok = ra * rb < 0 and Da < z < Db
    print("sign change between the two D and the zero between them: %s" % ok)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
