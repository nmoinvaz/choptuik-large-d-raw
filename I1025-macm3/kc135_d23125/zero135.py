#!/usr/bin/env python3
"""zero135.py [--mutate=sign] > zero_arithmetic_135.txt : the zero in D of lambda_1 at k_c 135 by the straight line through its two secant roots
(D 23.0625 from kc135_d230625/point_summary.txt, D 23.125 from kc135_d23125/point_summary.txt), the slope, the zero over the four bracket-end
combinations, the k_c 127-to-135 shift of the root at both D, and the comparison with the registered numbers of README.md (second registration
entry). Arithmetic on two points, not a result. Exit 1 when the two roots do not change sign or the zero lies outside [23.0625, 23.125].
--mutate=sign flips the sign of the D 23.125 root: must exit 1."""
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
    ra, la, ha = read(R + "kc135_d230625/point_summary.txt")
    rb, lb, hb = read(R + "kc135_d23125/point_summary.txt")
    r127a = read(R + "kc127_d230625/point_summary.txt")[0]
    r127b = read(R + "kc127_leg/point_D23.125_summary.txt")[0]
    if mut:
        rb, lb, hb = -rb, -hb, -lb
    z = lz(Da, ra, Db, rb); sl = (rb - ra) / (Db - Da)
    zs = [lz(Da, x, Db, y) for x in (la, ha) for y in (lb, hb)]
    z127 = lz(Da, r127a, Db, r127b); sl127 = (r127b - r127a) / (Db - Da)
    sa = ra - r127a; sb = rb - r127b
    print("k_c 135 roots: D %s %+.8f [%.8f, %.8f]; D %s %+.8f [%.8f, %.8f]" % (Da, ra, la, ha, Db, rb, lb, hb))
    print("k_c 127 roots: D %s %+.8f; D %s %+.8f" % (Da, r127a, Db, r127b))
    print("slope per unit D: k_c 135 %+.5f, k_c 127 %+.5f" % (sl, sl127))
    print("zero by the line through the two roots: k_c 135 D %.5f, k_c 127 D %.5f, step %+.5f" % (z, z127, z - z127))
    print("zero over the four bracket-end combinations: %.5f to %.5f" % (min(zs), max(zs)))
    print("k_c 127-to-135 shift of the root: D %s %+.6f, D %s %+.6f, growth factor %.4f" % (Da, sa, Db, sb, sb / sa))
    c = ra - 0.70 * (Db - Da); h = 0.03 * (Db - Da)
    print("registered root (mine): %.6f +- %.6f, interval (%.6f, %.6f); read %+.8f, difference from the centre %+.6f, from the nearer end %+.2e, inside %s" % (c, h, c - h, c + h, rb, rb - c, (rb - (c - h)) if rb < c - h else ((rb - (c + h)) if rb > c + h else 0.0), c - h <= rb <= c + h))
    rule = r127b + sa
    print("t5's rule alone (the k_c 127 root at D %s plus the shift at D %s): %+.6f; read minus it %+.6f; t5's quoted -0.0362: read minus it %+.6f" % (Db, Da, rule, rb - rule, rb + 0.0362))
    print("registered slope magnitude below k_c 127's %.5f (75%%): read %.5f, %s" % (abs(sl127), abs(sl), abs(sl) < abs(sl127)))
    print("registered zero in (23.0745, 23.0770) (65%%): read %.5f, %s; the register's arithmetic examples 23.07539 (slope 0.7288), 23.07592 (0.70), 23.07652 (0.67); t5's quoted 23.0754-23.0765: read %+.5f from its lower end" % (z, 23.0745 < z < 23.0770, z - 23.0754))
    ok = ra * rb < 0 and Da < z < Db
    print("sign change between the two D and the zero between them: %s" % ok)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
