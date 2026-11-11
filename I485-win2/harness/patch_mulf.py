"""#485: lets 1dcde949's modecount_cx/src/lib.rs compile on hp crates whose multidouble pin has no `mul_pwr2` (d66b410d, 0802e86a), where the kernel's scaled series multiplies with `mulf` / `mul_f`.
Removes the `mul_pwr2` method of `impl BaseLane for Dc`, turns `DD::from_f64(...).mul_pwr2(` and `ctx.u0().mul_pwr2(` into `.mul_f(` (double-double scalars) and every other `.mul_pwr2(` into `.mulf(`.
Multiplying by a power of two is exact in both, so each replacement gives the same bits as the kernel's own call at that commit. Line endings are kept as they are in the file."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
s1, n0 = re.subn(r"\r?\n[ \t]*#\[inline\(always\)\]\r?\n[ \t]*fn mul_pwr2\(self, s: f64\) -> Self \{\r?\n[^\r\n]*\r?\n[ \t]*\}", "", s)
s2, n1 = re.subn(r"(DD::from_f64\(cx\.ctx\.nodes\[0\]\))\.mul_pwr2\(", r"\1.mul_f(", s1)
s3, n2 = re.subn(r"(ctx\.u0\(\))\.mul_pwr2\(", r"\1.mul_f(", s2)
s4, n3 = re.subn(r"\.mul_pwr2\(", ".mulf(", s3)
assert n0 == 1 and n1 == 1 and n2 == 1 and n3 >= 1, (n0, n1, n2, n3)
open(p, "w", encoding="utf-8", newline="").write(s4)
print(f"patch_mulf: removed {n0} trait method, {n1 + n2} .mul_f, {n3} .mulf")
