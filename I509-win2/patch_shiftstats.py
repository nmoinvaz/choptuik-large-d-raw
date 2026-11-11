"""#509 instrumentation, applied to e043be2's hp/modecount_cx/src/lib.rs: counts the applications of the complex shift in `dtau_c` and records the difference between the two forms at each.
At each application (8 lanes x re, im per field block) it computes both forms (new: double-double products and sum; old: DotAcc), keeps the NEW form's result (today's code), and accumulates in a process-wide Mutex:
calls, elements (lanes with a nonzero old value), nonzero (elements where the forms differ), max and sum of squares of the relative difference |(new - old) / old|, max absolute difference.
`shift_stats()` returns (calls, elements, nonzero, max_rel, rms_rel, max_abs) and resets; `set_shift_plant(rel)` adds rel x (the old hi part) to the OLD form's lo part before the comparison (1.0 + rel is 1.0 in f64 for rel < 1e-16) (the control: with rel = 1e-20 the reported rms_rel must be 1e-20).
Does not change any value of the determinant. Line endings are kept."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
def L(*lines): return nl.join(lines)

# 1. imports
s, n = re.subn(r"use hpk::dv::DV;", "use hpk::dv::{DotAcc, DV};", s); assert n == 1, n
s, n = re.subn(r"use std::sync::Arc;", L("use std::sync::atomic::{AtomicU64, Ordering};", "use std::sync::{Arc, Mutex};"), s); assert n == 1, n

# 2. the statics and the recorder, before dtau_c
stats = L(
"/// #509 instrumentation: calls, elements, nonzero differences, max and sum of squares of the relative difference of the two forms of the complex shift, max absolute difference.",
"static SHIFT_STATS: Mutex<[f64; 6]> = Mutex::new([0.0; 6]);",
"static SHIFT_PLANT: AtomicU64 = AtomicU64::new(0);",
"",
"fn shift_record(new: &DV, old: &DV) {",
"    let plant = f64::from_bits(SHIFT_PLANT.load(Ordering::Relaxed));",
"    let (nh, nl, oh, ol) = (new.hi.to_array(), new.lo.to_array(), old.hi.to_array(), old.lo.to_array());",
"    let mut loc = [0.0f64; 6];",
"    loc[0] = 1.0;",
"    for j in 0..8 {",
"        let (oh, ol) = (oh[j], ol[j] + oh[j] * plant);",
"        if oh == 0.0 {",
"            continue;",
"        }",
"        let d = (nh[j] - oh) + (nl[j] - ol);",
"        let rel = (d / oh).abs();",
"        loc[1] += 1.0;",
"        if d != 0.0 {",
"            loc[2] += 1.0;",
"        }",
"        loc[3] = loc[3].max(rel);",
"        loc[4] += rel * rel;",
"        loc[5] = loc[5].max(d.abs());",
"    }",
"    let mut g = SHIFT_STATS.lock().unwrap();",
"    g[0] += loc[0];",
"    g[1] += loc[1];",
"    g[2] += loc[2];",
"    g[3] = g[3].max(loc[3]);",
"    g[4] += loc[4];",
"    g[5] = g[5].max(loc[5]);",
"}",
"",
"#[pyfunction]",
"fn shift_stats() -> (f64, f64, f64, f64, f64, f64) {",
"    let mut g = SHIFT_STATS.lock().unwrap();",
"    let r = (g[0], g[1], g[2], g[3], if g[1] > 0.0 { (g[4] / g[1]).sqrt() } else { 0.0 }, g[5]);",
"    *g = [0.0; 6];",
"    r",
"}",
"",
"#[pyfunction]",
"fn set_shift_plant(rel: f64) {",
"    SHIFT_PLANT.store(rel.to_bits(), Ordering::Relaxed);",
"}",
"",
"")
s, n = re.subn(r"(/// d/dtau = omega D, plus lambda)", lambda m: stats + m.group(1), s, count=1); assert n == 1, "dtau_c doc line"

# 3. the loop in dtau_c
old = L("    let b = DV::splat(cx.li);", "    for k in 0..B {", "        let t = x.0[k];",
        "        r.0[k].r = r.0[k].r + (t.r * a - t.i * b);", "        r.0[k].i = r.0[k].i + (t.i * a + t.r * b);", "    }")
new = L("    let b = DV::splat(cx.li);", "    let nb = DV::splat(-cx.li);", "    for k in 0..B {", "        let t = x.0[k];",
        "        let re_new = t.r * a - t.i * b;", "        let im_new = t.i * a + t.r * b;",
        "        let re_old = DotAcc::zero().add_prod(t.r, a).add_prod(t.i, nb).finish();",
        "        let im_old = DotAcc::zero().add_prod(t.i, a).add_prod(t.r, b).finish();",
        "        shift_record(&re_new, &re_old);", "        shift_record(&im_new, &im_old);",
        "        r.0[k].r = r.0[k].r + re_new;", "        r.0[k].i = r.0[k].i + im_new;", "    }")
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)

# 4. registration
s, n = re.subn(r"(    m\.add_function\(wrap_pyfunction!\(cdet, m\)\?\)\?;)", lambda m: m.group(1) + nl + "    m.add_function(wrap_pyfunction!(shift_stats, m)?)?;" + nl + "    m.add_function(wrap_pyfunction!(set_shift_plant, m)?)?;", s); assert n == 1, n
open(p, "w", encoding="utf-8", newline="").write(s)
print("patch_shiftstats: dtau_c instrumented")
