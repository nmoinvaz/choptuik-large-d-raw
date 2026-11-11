"""#485: lets the commit's own modecount_cx/src/lib.rs compile on hp crates whose BaseLane (multidouble 1.0.0) has `type S` and `mul_pwr2` (aafe0cb4, 203cb0b9 and the commits around them), and the Ctx field `horizon_alpha`.
Adds `use hpk::simd::Native;`, `type S = Native;` and `fn mul_pwr2` (the same three-lane body as 1dcde949's Dc) to `impl BaseLane for Dc`, and `horizon_alpha: 0,` to the Ctx literal where the field exists. Multiplying by a power of two is exact, so the arithmetic is unchanged. Line endings are kept."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
s1, n1 = re.subn(r"use hpk::lane::\{BaseLane, Lane\};", "use hpk::lane::{BaseLane, Lane};" + nl + "use hpk::simd::Native;", s)
s2, n2 = re.subn(r"impl BaseLane for Dc \{" + nl, "impl BaseLane for Dc {" + nl + "    type S = Native;" + nl, s1)
body = nl.join(["    #[inline(always)]", "    fn mul_pwr2(self, s: f64) -> Self {", "        Dc { v: self.v.mul_pwr2(s), r: self.r.mul_pwr2(s), i: self.i.mul_pwr2(s) }", "    }", ""])
s3, n3 = re.subn(r"(    #\[inline\(always\)\]" + nl + r"    fn addc\(self, c: DV\) -> Self \{)", lambda m: body + m.group(1), s2)
s4, n4 = re.subn(r"([ \t]*)lam: DD::ZERO,(\r?\n)", lambda m: f"{m.group(1)}lam: DD::ZERO,{m.group(2)}{m.group(1)}horizon_alpha: 0,{m.group(2)}", s3)
assert n1 == 1 and n2 == 1 and n3 == 1 and n4 == 1, (n1, n2, n3, n4)
open(p, "w", encoding="utf-8", newline="").write(s4)
print("patch_swrap: S, mul_pwr2 and horizon_alpha added")
