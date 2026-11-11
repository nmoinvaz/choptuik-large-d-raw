"""#485: the one patch that lets 1dcde949's modecount_cx/src/lib.rs compile on hp crates older than 203cb0b9 (no Ctx::horizon_alpha).
Removes the guard `if ctx.horizon_alpha != 0 { return Err(...) }` and the field `horizon_alpha: 0,` of the Ctx literals. Both are no-ops at horizon_alpha 0 (the default), so the arithmetic is unchanged.
Line endings are kept as they are in the file."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
s2, n1 = re.subn(r"\r?\n[ \t]*if ctx\.horizon_alpha != 0 \{\r?\n[ \t]*return Err\([^\r\n]*\);\r?\n[ \t]*\}", "", s)
s3, n2 = re.subn(r"\r?\n[ \t]*horizon_alpha: 0,", "", s2)
assert n1 == 1 and n2 >= 1, (n1, n2)
open(p, "w", encoding="utf-8", newline="").write(s3)
print(f"patch_halpha: removed {n1} guard and {n2} field line(s)")
