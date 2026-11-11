"""#485: lets 1dcde949's modecount_cx/src/lib.rs compile on hp crates whose lane trait (multidouble::dual::Lane at a pin before the backend type S) has no `type S` and whose crate has no `hpk::simd`.
Removes `use hpk::simd::Native;` and `type S = Native;`. The associated type only selects the SIMD backend, which at those commits is the one backend there is, so the arithmetic is unchanged.
Line endings are kept as they are in the file."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
s2, n1 = re.subn(r"\r?\nuse hpk::simd::Native;", "", s)
s3, n2 = re.subn(r"\r?\n[ \t]*type S = Native;", "", s2)
assert n1 == 1 and n2 == 1, (n1, n2)
open(p, "w", encoding="utf-8", newline="").write(s3)
print(f"patch_nosimd: removed {n1} use and {n2} associated type line(s)")
