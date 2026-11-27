#!/usr/bin/env python3
"""ext_side.py READ_LOWER.txt [--mutate=flip] | selftest [--mutate=flip] : which side to extend the scan of kc143_d23125x on (t5's pre-authorization, #1025 hc 27 Nov 08:4x UTC):
a window with no robust change whose hybrid signs read '-' at every point extends to lower lambda (-0.035, -0.040): prints "low"; '+' at every point extends to higher lambda (-0.015, -0.010): prints "high";
anything else (a robust change, a non-robust point, mixed signs, no signs line) prints "none" (not covered by the order). Exit 0 for low and high, 1 for none.
--mutate=flip swaps the two outputs (a control: the selftest and the planted reads must then fail)."""
import re, sys
MUT = "--mutate=flip" in sys.argv


def side(text):
    m = re.search(r"hybrid signs:(.*)", text)
    if not m: return "none"
    signs = re.findall(r"(-?\d+\.\d+)([+-])(?=\s|$)", m.group(1))
    if len(signs) < 3: return "none"
    c = re.search(r"robust changes: (\d+)", text)
    if not c or int(c.group(1)) != 0: return "none"
    if not re.search(r"not noise-robust: none", text): return "none"
    if not re.search(r"touching a non-robust point \(not counted\): none", text): return "none"
    ss = {s for _, s in signs}
    r = "low" if ss == {"-"} else "high" if ss == {"+"} else "none"
    if MUT and r != "none": r = "high" if r == "low" else "low"
    return r


BASE = "== window: read_lower.py scan -0.030 -0.020\npoints 4 in -0.030--0.020; not noise-robust: none\nhybrid signs: %s\n%srobust changes: %d; touching a non-robust point (not counted): none\nendpoint signs: x\n"
CASES = [("all minus", BASE % ("-0.030- -0.025- -0.020-", "", 0), "low"), ("all plus", BASE % ("-0.030+ -0.025+ -0.020+", "", 0), "high"),
         ("mixed signs", BASE % ("-0.030+ -0.025+ -0.020-", "", 0), "none"), ("a robust change", BASE % ("-0.030- -0.025- -0.020+", "  robust change (-0.025, -0.020), - to +, det-linear -0.024\n", 1), "none"),
         ("all minus but a non-robust point", (BASE % ("-0.030- -0.025- -0.020-", "", 0)).replace("not noise-robust: none", "not noise-robust: -0.025"), "none"),
         ("all minus but touching a non-robust point", (BASE % ("-0.030- -0.025- -0.020-", "", 0)).replace("(not counted): none", "(not counted): (-0.025, -0.020)"), "none"),
         ("no signs line", "nothing\n", "none")]
if len(sys.argv) > 1 and sys.argv[1] == "selftest":
    bad = 0
    for name, text, want in CASES:
        got = side(text); ok = got == want; bad += not ok; print("%-45s wanted %-4s got %-4s %s" % (name, want, got, "ok" if ok else "FAIL"))
    print("failures: %d" % bad); sys.exit(1 if bad else 0)
r = side(open(sys.argv[1]).read()); print(r); sys.exit(0 if r != "none" else 1)
