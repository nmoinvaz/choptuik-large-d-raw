"""#512, applied to e043be2's hp/modecount_cx/src/lib.rs: a random relative change of the complex shift's output in `dtau_c`, and a switch to the old (DotAcc) form.
`set_shift_noise(rel, seed)`: every element (8 lanes, re and im) of the shift's output gets its lo part increased by hi x rel x u, u uniform in [-1, 1) from a hash of (seed, the bits of the
element's input t.r.hi and t.i.hi, re/im, lane): deterministic whatever the thread scheduling, different for every seed. rel = 0 (the default) changes nothing.
`set_shift_old(flag)`: flag = true uses the old DotAcc form for the shift's output (the fixed known change of #509). Both default to today's code. Line endings are kept."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
def L(*lines): return nl.join(lines)

s, n = re.subn(r"use hpk::dv::DV;", L("use hpk::dv::{DotAcc, DV};", "use hpk::v8::V8;"), s); assert n == 1, n
s, n = re.subn(r"use std::sync::Arc;", L("use std::sync::atomic::{AtomicU64, Ordering};", "use std::sync::Arc;"), s); assert n == 1, n

helpers = L(
"/// #512: a random relative change of the complex shift's output (rel, seed), and the switch to its old DotAcc form.",
"static SHIFT_REL: AtomicU64 = AtomicU64::new(0);",
"static SHIFT_SEED: AtomicU64 = AtomicU64::new(0);",
"static SHIFT_OLD: AtomicU64 = AtomicU64::new(0);",
"",
"fn mix(z: u64) -> u64 {",
"    let mut z = z.wrapping_add(0x9E37_79B9_7F4A_7C15);",
"    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);",
"    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);",
"    z ^ (z >> 31)",
"}",
"",
"fn shift_noise(out: DV, tr: &DV, ti: &DV, which: u64) -> DV {",
"    let rel = f64::from_bits(SHIFT_REL.load(Ordering::Relaxed));",
"    if rel == 0.0 {",
"        return out;",
"    }",
"    let seed = SHIFT_SEED.load(Ordering::Relaxed);",
"    let (oh, ol) = (out.hi.to_array(), out.lo.to_array());",
"    let (a, b) = (tr.hi.to_array(), ti.hi.to_array());",
"    let mut nl = [0.0f64; 8];",
"    for j in 0..8 {",
"        let h = mix(seed ^ mix(a[j].to_bits() ^ mix(b[j].to_bits() ^ (which << 8) ^ j as u64)));",
"        let u = ((h >> 11) as f64) * (1.0 / 9007199254740992.0) * 2.0 - 1.0;",
"        nl[j] = ol[j] + oh[j] * rel * u;",
"    }",
"    DV { hi: out.hi, lo: V8::from_array(nl) }",
"}",
"",
"#[pyfunction]",
"fn set_shift_noise(rel: f64, seed: u64) {",
"    SHIFT_REL.store(rel.to_bits(), Ordering::Relaxed);",
"    SHIFT_SEED.store(seed, Ordering::Relaxed);",
"}",
"",
"#[pyfunction]",
"fn set_shift_old(flag: bool) {",
"    SHIFT_OLD.store(flag as u64, Ordering::Relaxed);",
"}",
"",
"")
s, n = re.subn(r"(/// d/dtau = omega D, plus lambda)", lambda m: helpers + m.group(1), s, count=1); assert n == 1, "doc line"

old = L("    let b = DV::splat(cx.li);", "    for k in 0..B {", "        let t = x.0[k];",
        "        r.0[k].r = r.0[k].r + (t.r * a - t.i * b);", "        r.0[k].i = r.0[k].i + (t.i * a + t.r * b);", "    }")
new = L("    let b = DV::splat(cx.li);", "    let nb = DV::splat(-cx.li);", "    let old_form = SHIFT_OLD.load(Ordering::Relaxed) != 0;", "    for k in 0..B {", "        let t = x.0[k];",
        "        let (re, im) = if old_form {",
        "            (DotAcc::zero().add_prod(t.r, a).add_prod(t.i, nb).finish(), DotAcc::zero().add_prod(t.i, a).add_prod(t.r, b).finish())",
        "        } else {",
        "            (t.r * a - t.i * b, t.i * a + t.r * b)",
        "        };",
        "        let re = shift_noise(re, &t.r, &t.i, 0);",
        "        let im = shift_noise(im, &t.r, &t.i, 1);",
        "        r.0[k].r = r.0[k].r + re;", "        r.0[k].i = r.0[k].i + im;", "    }")
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
s, n = re.subn(r"(    m\.add_function\(wrap_pyfunction!\(cdet, m\)\?\)\?;)", lambda m: m.group(1) + nl + "    m.add_function(wrap_pyfunction!(set_shift_noise, m)?)?;" + nl + "    m.add_function(wrap_pyfunction!(set_shift_old, m)?)?;", s); assert n == 1, n
open(p, "w", encoding="utf-8", newline="").write(s)
print("patch_shiftnoise: dtau_c has the noise and the old-form switch")
