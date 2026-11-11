"""#485 experiment: puts the OLD `dtau_c` complex-shift operations (the `DotAcc` form of aafe0cb4's modecount_cx) back into 1dcde949's modecount_cx/src/lib.rs.
New:  r.r += t.r * a - t.i * b ; r.i += t.i * a + t.r * b   (separate double-double products and sums)
Old:  re = DotAcc(t.r a + t.i (-b)), im = DotAcc(t.i a + t.r b) ; r.r += re ; r.i += im
Imports `DotAcc` from hpk::dv when the file does not (e043be2). Line endings are kept."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
new = ("    let b = DV::splat(cx.li);" + nl + "    for k in 0..B {" + nl + "        let t = x.0[k];" + nl +
       "        r.0[k].r = r.0[k].r + (t.r * a - t.i * b);" + nl + "        r.0[k].i = r.0[k].i + (t.i * a + t.r * b);" + nl + "    }")
old = ("    let b = DV::splat(cx.li);" + nl + "    let nb = DV::splat(-cx.li);" + nl + "    for k in 0..B {" + nl + "        let t = x.0[k];" + nl +
       "        let re = DotAcc::zero().add_prod(t.r, a).add_prod(t.i, nb).finish();" + nl +
       "        let im = DotAcc::zero().add_prod(t.i, a).add_prod(t.r, b).finish();" + nl +
       "        r.0[k].r = r.0[k].r + re;" + nl + "        r.0[k].i = r.0[k].i + im;" + nl + "    }")
assert s.count(new) == 1, s.count(new)
s2 = s.replace(new, old)
if not re.search(r"use hpk::dv::\{[^}]*DotAcc", s2):
    s2, n = re.subn(r"use hpk::dv::DV;", "use hpk::dv::{DotAcc, DV};", s2)
    assert n == 1, "no DV import to extend"
open(p, "w", encoding="utf-8", newline="").write(s2)
print("patch_olddtau: dtau_c uses DotAcc again")
