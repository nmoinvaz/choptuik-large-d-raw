#!/usr/bin/env python3
"""#1025 kc95_d22375 (dh610) wide_read.py READ_LOWER.txt | selftest [--mutate]: the reading of a WIDE hybrid sign scan (lambda -0.10 to 0.50 by 0.04) from the printed output of read_lower.py (blob 89309d3c): every robust
change by position (bracket, orientation as the reader prints it, det-linear estimate, estimator range) with negative lambda allowed (leg_read.py's pattern reads positive numbers only), the hybrid signs, the float64
differences, the repeat, the endpoint signs and the minima lines as the reader printed them. No prediction line. selftest: a planted text with a change at negative lambda and two more must parse to the planted fields;
--mutate uses leg_read's positive-only pattern, which misses the negative change, so the selftest exits 1."""
import re, sys

RC = re.compile(r"robust change \((-?\d\.\d+), (-?\d\.\d+)\), (.+?), det-linear (-?\d\.\d+), range \[(-?\d\.\d+), (-?\d\.\d+)\]")
RC_POS = re.compile(r"robust change \((\d\.\d+), (\d\.\d+)\), (.+?), det-linear (\d\.\d+), range \[(\d\.\d+), (\d\.\d+)\]")


def parse(text, positive_only=False):
    pat = RC_POS if positive_only else RC
    return [dict(a=float(m[0]), b=float(m[1]), orient=m[2], det=float(m[3]), r0=float(m[4]), r1=float(m[5])) for m in pat.findall(text)]


PLANT = ("hybrid signs: -0.10+ -0.06+ -0.02- 0.02- 0.06- 0.10- 0.14+ 0.18+ 0.22+ 0.26+ 0.30+ 0.34+ 0.38+ 0.42- 0.46- 0.50-\n"
         "  robust change (-0.060, -0.020), + to -, det-linear -0.041250, range [-0.042000, -0.041250]\n"
         "  robust change (0.100, 0.140), - to +, det-linear 0.112500, range [0.111000, 0.112500]\n"
         "  robust change (0.380, 0.420), + to -, det-linear 0.401000, range [0.399000, 0.401000]\nrobust changes: 3; touching a non-robust point (not counted): none\n")


def selftest(mutate):
    ch = parse(PLANT, mutate)
    ok = len(ch) == 3 and ch[0]["a"] == -0.06 and ch[0]["orient"] == "+ to -" and ch[1]["orient"] == "- to +" and ch[2]["det"] == 0.401 and ch[0]["r0"] < ch[0]["r1"]
    print("selftest" + (" --mutate" if mutate else ""), "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest("--mutate" in sys.argv))
    text = open(sys.argv[1]).read()
    for key in ("points ", "hybrid signs:", "float64 sign differs", "repeated points:", "ln|det| local minima", "endpoint signs:"):
        for l in text.split("\n"):
            if l.startswith(key):
                print(l)
    ch = parse(text)
    print(f"robust changes: {len(ch)}")
    for c in ch:
        print(f"   change ({c['a']:.3f}, {c['b']:.3f}), {c['orient']}, det-linear {c['det']:.6f}, range [{c['r0']:.6f}, {c['r1']:.6f}]")
    nread = len(re.findall(r"robust change \(", text))
    print(f"reader lines 'robust change': {nread}; parsed: {len(ch)}" + ("" if nread == len(ch) else "  WARNING: a change line was not parsed"))
