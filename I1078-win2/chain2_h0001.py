"""#1078 on win2, after the coordinator's split of 2026-11-25 (dh370 takes the M' 160 root): the hmax 0.001 root at
M' 96, as chain1078.py's step 6 would have run it (same follow(): ends at r96 -+ 2e-4, widened while they agree).
r96 is the single accepted M' 96 root (4_root_m96_*.jsonl verdict). Launched by swap_m160.sh once chain1078.py has
finished M' 128 and was stopped at the start of its M' 160 step."""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chain1078 as C

v = [json.loads(l) for f in sorted(glob.glob(os.path.join(C.OUT, "4_root_m96_*.jsonl"))) for l in open(f)]
acc = [r for r in v if r.get("kind") == "verdict" and r.get("passed")]
if len(acc) != 1:
    C.stop("chain2", f"{len(acc)} accepted M' 96 roots in 4_root_m96_*.jsonl, expected 1")
r96 = acc[0]["lam"]
C.step(f"chain2_h0001 start: r96 {r96!r}")
vh = C.follow("m96_h0.001", C.S96, r96, extra=("--hmax=0.001",), cap_det=3 * 3600)
C.step(f"chain2_h0001: r96 hmax 0.001 {vh and vh['lam']!r} (gamma {vh and vh['gamma']!r})")
with open(os.path.join(C.OUT, "chain2.done"), "w") as fh:
    fh.write(f"done {C.stamp()}\n")
