#!/usr/bin/env python3
"""#1025 winb, the k_c 79 convergence check at D 18.5: t5's reading (fixed before the run) applied to the `d18f_read.py window 18.5 1.66 1.69` output: the robust minus-to-plus
change's det-linear estimate is lambda_1 at k_c 79; it is printed beside 1.677016 (k_c 63) and 1.675995 (k_c 71), with the two differences. Whether the difference shrinks is information
printed as numbers, the call is the coordinator's. usage: read_kc79_1025.py READ_kc79_D185.log   (--selftest runs it on planted text)"""
import re, sys

K63, K71 = 1.677016, 1.675995


def read(t):
    ch = [dict(br=(float(a), float(b)), o1=o1, o2=o2, lin=float(l), lo=float(lo), hi=float(hi))
          for a, b, o1, o2, l, lo, hi in re.findall(r"change in \(([\d.]+), ([\d.]+)\), ([+-]) to ([+-]) in this state: det-linear ([\d.]+), range \[([\d.]+), ([\d.]+)\]", t)]
    non = re.search(r"touching a non-robust point \(not counted\): (.*)", t)
    nonrob = re.search(r"not noise-robust: (.*)", t)
    mins = re.search(r"ln\|det\| local minima without a sign change in the window: (.*)", t)
    sig = re.search(r"^signs: (.*)$", t, re.M)
    f64 = re.search(r"float64 in the window: (.*)", t)
    out = [f"k_c 79, D 18.5, window 1.66-1.69: signs {sig.group(1) if sig else '?'}"]
    for c in ch:
        out.append(f"   robust change in ({c['br'][0]:.2f}, {c['br'][1]:.2f}), {c['o1']} to {c['o2']} in this state: det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]")
    if not ch:
        out.append("   no robust change in the window")
    out.append(f"   points not noise-robust: {nonrob.group(1) if nonrob else '?'}; changes touching a non-robust point (not counted): {non.group(1).strip() if non else '?'}; "
               f"ln|det| minima without a sign change: {mins.group(1).strip() if mins else '?'}; float64: {f64.group(1) if f64 else '?'}")
    clean = (nonrob is None or nonrob.group(1).strip() == "none") and (non is None or non.group(1).strip() == "none")
    mp = [c for c in ch if (c["o1"], c["o2"]) == ("-", "+")]
    if len(ch) == 1 and len(mp) == 1 and clean:
        x = mp[0]["lin"]
        out.append(f"lambda_1 at k_c 79 (det-linear, range [{mp[0]['lo']:.6f}, {mp[0]['hi']:.6f}]): {x:.6f}; k_c 71: {K71:.6f}; k_c 63: {K63:.6f}")
        out.append(f"information: k_c 79 - k_c 71 = {x - K71:+.3e}; k_c 71 - k_c 63 = {K71 - K63:+.3e}; |k_c 79 - k_c 71| is {'smaller' if abs(x - K71) < abs(K71 - K63) else 'not smaller'} than |k_c 71 - k_c 63| (the call is the coordinator's)")
        out.append(f"READING: one robust minus-to-plus change, lambda_1 at k_c 79 = {x:.6f}")
    else:
        out.append(f"READING: not the expected pattern ({len(ch)} robust change(s), {len(mp)} minus-to-plus, {'clean' if clean else 'a point or a change is not noise-robust'}): no lambda_1 value; the coordinator rules")
    return "\n".join(out)


if "--selftest" in sys.argv:
    good = ("window 1.66-1.69: 4 points; not noise-robust: none\nsigns: 1.66- 1.67- 1.68+ 1.69+\nrepeated points: none\n  change in (1.67, 1.68), - to + in this state: det-linear 1.675500, range [1.675500, 1.676000]\n"
            "robust changes in the window: 1; touching a non-robust point (not counted): none\nln|det| local minima without a sign change in the window: none\nfloat64 in the window: sign changes none; differs from the hybrid at 1 of 4 points\n")
    cases = [("one minus-to-plus", good, "lambda_1 at k_c 79 = 1.675500"), ("plus-to-minus", good.replace("- to + in", "+ to - in"), "not the expected pattern"),
             ("no change", good.replace("  change in (1.67, 1.68), - to + in this state: det-linear 1.675500, range [1.675500, 1.676000]\n", ""), "not the expected pattern"),
             ("a non-robust point", good.replace("not noise-robust: none", "not noise-robust: [1.67]"), "not the expected pattern")]
    ok = True
    for name, t, want in cases:
        got = read(t)
        good_c = want in got
        print(f"planted: {name}: {'PASS' if good_c else 'FAIL'}")
        ok = ok and good_c
    print("selftest:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
print(read(open(sys.argv[1]).read()))
