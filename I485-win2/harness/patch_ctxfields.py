"""#485: lets the commit's own modecount_cx/src/lib.rs compile on hp crates that have the Ctx fields `mutate` and `f64_dd` (u8, 0 = none, the defaults of the kernel) (0a131faf and the commits after it up to 93402cf8).
Adds `mutate: 0,` and `f64_dd: 0,` after `lam: DD::ZERO,` in the Ctx literal. The kernel's own default for both is 0, so the arithmetic is unchanged. Line endings are kept as they are in the file."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
s2, n = re.subn(r"([ \t]*)lam: DD::ZERO,(\r?\n)", lambda m: f"{m.group(1)}lam: DD::ZERO,{m.group(2)}{m.group(1)}mutate: 0,{m.group(2)}{m.group(1)}f64_dd: 0,{m.group(2)}", s)
assert n == 1, n
open(p, "w", encoding="utf-8", newline="").write(s2)
print("patch_ctxfields: added mutate and f64_dd to the Ctx literal")
