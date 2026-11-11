"""#485: lets the commit's OWN modecount_cx/src/lib.rs (the 973-line version of 2ef50229 to 649ec63e) compile on hp crates whose lane trait is split (93402cf8: `Lane: BaseLane`, the lane operations in multidouble's `BaseLane`).
`impl Lane for Dc { ... }` becomes `impl BaseLane for Dc { ... }` plus an empty `impl Lane for Dc {}` (dmat_apply keeps its default), and `BaseLane` is imported. No arithmetic changes. Line endings are kept."""
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
s1, n1 = re.subn(r"use hpk::lane::Lane;", "use hpk::lane::{BaseLane, Lane};", s)
s2, n2 = re.subn(r"impl Lane for Dc \{", "impl Lane for Dc {}" + nl + nl + "impl BaseLane for Dc {", s1)
assert n1 == 1 and n2 == 1, (n1, n2)
open(p, "w", encoding="utf-8", newline="").write(s2)
print("patch_splitlane: Dc implements BaseLane, Lane is empty")
