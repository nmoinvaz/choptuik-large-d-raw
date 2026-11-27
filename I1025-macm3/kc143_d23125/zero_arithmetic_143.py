#!/usr/bin/env python3
"""zero_arithmetic_143.py [--mutate=sign|r2] > zero_arithmetic_143.txt : the zero in D of lambda_1 at k_c 143 by the straight line through its two secant roots
(D 23.0625 from kc143_d230625/point_summary.txt, D 23.125 from kc143_d23125/point_summary.txt), the slope, the zero over the four bracket-end combinations,
the shifts of the roots from k_c 127 and 135 (their point summaries), and the registered items of kc143_d23125/README.md (first and second entry).
Arithmetic on two points, not a result: the roots are the det-linear roots inside the final brackets (read by position), the brackets are not enclosures of the zero.
Exit 1 when the two roots do not change sign or the zero lies outside [23.0625, 23.125].
--mutate=sign flips the sign of the D 23.125 root (must exit 1); --mutate=r2 adds 0.001 to the D 23.125 root (the zero, the slope and every item built on them must move)."""
import os, re, sys
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/")
Da, Db = 23.0625, 23.125


def read(p):
    t = open(p).read()
    b = re.search(r"root bracket \[(\S+), (\S+)\], width (\S+), signs", t)
    r = re.search(r"det-linear root (-?[\d.]+)", t).group(1)
    return float(r), float(b.group(1)), float(b.group(2))


def lz(ra, rb):
    return Da - ra * (Db - Da) / (rb - ra)


def compute(argv=()):
    mut = [a.split("=")[1] for a in argv if a.startswith("--mutate=")]; mut = mut[0] if mut else ""
    ra, la, ha = read(R + "kc143_d230625/point_summary.txt")
    rb, lb, hb = read(R + "kc143_d23125/point_summary.txt")
    if mut == "sign": rb, lb, hb = -rb, -hb, -lb
    if mut == "r2": rb, lb, hb = rb + 0.001, lb + 0.001, hb + 0.001
    d = dict(ra=ra, la=la, ha=ha, rb=rb, lb=lb, hb=hb)
    d["z"] = lz(ra, rb); d["slope"] = (rb - ra) / (Db - Da)
    zs = [lz(x, y) for x in (la, ha) for y in (lb, hb)]; d["zmin"], d["zmax"] = min(zs), max(zs)
    r135a = read(R + "kc135_d230625/point_summary.txt")[0]; r135b = read(R + "kc135_d23125/point_summary.txt")[0]
    r127a = read(R + "kc127_d230625/point_summary.txt")[0]; r127b = read(R + "kc127_leg/point_D23.125_summary.txt")[0]
    d.update(r135a=r135a, r135b=r135b, r127a=r127a, r127b=r127b)
    d["z135"] = lz(r135a, r135b); d["z127"] = lz(r127a, r127b)
    d["sl135"] = (r135b - r135a) / (Db - Da); d["sl127"] = (r127b - r127a) / (Db - Da)
    d["ok"] = ra * rb < 0 and Da < d["z"] < Db
    # arithmetic only: the narrower sign-change interval of the secant (the non-robust interior point as one end), from the secant records
    return d


def main():
    d = compute(sys.argv)
    ra, rb, z = d["ra"], d["rb"], d["z"]
    print("k_c 143 roots: D %s %+.8f [%.8f, %.8f]; D %s %+.8f [%.8f, %.8f]" % (Da, ra, d["la"], d["ha"], Db, rb, d["lb"], d["hb"]))
    print("k_c 135 roots: D %s %+.8f; D %s %+.8f.  k_c 127 roots: D %s %+.8f; D %s %+.8f" % (Da, d["r135a"], Db, d["r135b"], Da, d["r127a"], Db, d["r127b"]))
    print("slope per unit D: k_c 143 %+.5f, k_c 135 %+.5f, k_c 127 %+.5f" % (d["slope"], d["sl135"], d["sl127"]))
    print("zero by the line through the two roots: k_c 143 D %.5f, k_c 135 D %.5f, k_c 127 D %.5f; steps 127 -> 135 %+.5f, 135 -> 143 %+.5f (ratio %.4f)" % (z, d["z135"], d["z127"], d["z135"] - d["z127"], z - d["z135"], (z - d["z135"]) / (d["z135"] - d["z127"])))
    print("zero over the four bracket-end combinations: %.5f to %.5f (the D 23.125 bracket is 5.3e-4 wide, the D 23.0625 one 5e-6; brackets are not enclosures of the zero)" % (d["zmin"], d["zmax"]))
    sa, sb = ra - d["r135a"], rb - d["r135b"]; sa1, sb1 = d["r135a"] - d["r127a"], d["r135b"] - d["r127b"]
    print("shifts of the root with k_c: D %s 127 -> 135 %+.6f, 135 -> 143 %+.6f (ratio %.4f); D %s 127 -> 135 %+.6f, 135 -> 143 %+.6f (ratio %.4f)" % (Da, sa1, sa, sa / sa1, Db, sb1, sb, sb / sb1))
    rule = d["r135b"] + 0.976 * sa
    print("registered (second entry) root %+.5f by the shift route (g 0.976): read %+.8f, read minus it %+.6f; t5's -0.0319 +- 0.003: read minus -0.0319 = %+.6f, inside his band %s" % (rule, rb, rb - rule, rb + 0.0319, abs(rb + 0.0319) < 0.003))
    print("registered slope magnitude above k_c 135's 0.73102 (75%%): read %.5f, %s; in (0.7310, 0.7360) (60%%): %s" % (abs(d["slope"]), abs(d["slope"]) > 0.73102, 0.7310 < abs(d["slope"]) < 0.7360))
    stp = z - d["z135"]
    print("registered zero, first entry in (23.0795, 23.0830) (65%%): read %.5f, %s; its step +0.0063 +- 0.0010: read %+.5f, %s" % (z, 23.0795 < z < 23.0830, stp, abs(stp - 0.0063) < 0.0010))
    print("registered zero, second entry in (23.0829, 23.0835) (80%%): %s; in (23.0830, 23.0833) (60%%): %s; step in (+0.0075, +0.0082) (80%%): %s; step at least 0.9 of the last step %+.5f (95%%): %s" % (
        23.0829 < z < 23.0835, 23.0830 < z < 23.0833, 0.0075 < stp < 0.0082, d["z135"] - d["z127"], stp >= 0.9 * (d["z135"] - d["z127"])))
    print("t5's zero 23.0816 +- 0.003 (his band (23.0786, 23.0846)): read %.5f, %s; read above his central: %s (%+.5f)" % (z, 23.0786 < z < 23.0846, z > 23.0816, z - 23.0816))
    print("sign change between the two D and the zero between them: %s" % d["ok"])
    sys.exit(0 if d["ok"] else 1)


if __name__ == "__main__":
    main()
