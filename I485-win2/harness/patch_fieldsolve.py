"""#485: lets the commit's own modecount_cx compile on 93402cf8, where `DDLu::solve_lanes` (a method of linalg.rs) moved to the trait `hpk::field::FieldSolve`: imports the trait. No arithmetic changes. Line endings are kept."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
s1, n1 = re.subn(r"use hpk::lane::\{BaseLane, Lane\};", "use hpk::lane::{BaseLane, Lane};" + nl + "use hpk::field::FieldSolve;", s)
assert n1 == 1, n1
open(p, "w", encoding="utf-8", newline="").write(s1)
print("patch_fieldsolve: FieldSolve imported")
