"""#485: lets 1dcde949's modecount_cx/src/lib.rs compile on the hp crate of 93402cf8, whose model.rs has no `series_scale` (the series is in the plain variable).
Replaces the import of `hpk::model::series_scale` by a local `fn series_scale(_x: f64) -> f64 { 1.0 }`, so every scaling factor of modecount_cx's series (sig, isig) is exactly 1 and the recursion is the unscaled one.
Line endings are kept as they are in the file."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
s1, n1 = re.subn(r"use hpk::model::\{self as hm, series_scale, Ctx\};", "use hpk::model::{self as hm, Ctx};", s)
assert n1 == 1, n1
fn = nl.join(["", "/// the series is in the plain variable at this hp commit (no model::series_scale): every scale is exactly 1", "fn series_scale(_x: f64) -> f64 {", "    1.0", "}", ""])
m = re.search(r"use hpk::model::\{self as hm, Ctx\};", s1)
s2 = s1[:m.end()] + nl + fn.rstrip(nl) + s1[m.end():]
open(p, "w", encoding="utf-8", newline="").write(s2)
print("patch_noscale: series_scale defined as 1")
