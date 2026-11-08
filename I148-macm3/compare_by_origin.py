"""Fresh kf13 determinants against October's cache at the shared lambdas, split by each October line's origin (I148-macm3).

October's cache october_inputs/modecount_D30.0688_M48_kf13_evals.jsonl has lines with Windows line endings (CR LF) and lines without;
the ending is the only provenance mark the lines carry. The fresh cache is hp/data's (or hp_data_after/'s) file of the same name.
    python3 compare_by_origin.py [FRESH_CACHE]
"""
import json
import math
import statistics
import sys

OCT = "october_inputs/modecount_D30.0688_M48_kf13_evals.jsonl"
fresh_path = sys.argv[1] if len(sys.argv) > 1 else "hp_data_after/modecount_D30.0688_M48_kf13_evals.jsonl"

oct_lines = []
with open(OCT, "rb") as fh:
    for raw in fh:
        cr = raw.endswith(b"\r\n")
        r = json.loads(raw.decode().strip())
        oct_lines.append((r, cr))
fresh = {(r["re"], r["im"]): r for r in map(json.loads, open(fresh_path))}
print(f"October kf13 cache: {len(oct_lines)} lines, {sum(1 for _, c in oct_lines if c)} with CR, {sum(1 for _, c in oct_lines if not c)} without")
print(f"fresh evaluations: {len(fresh)}")
groups = {"CR lines": [], "non-CR lines": []}
for r, cr in oct_lines:
    k = (r["re"], r["im"])
    if k in fresh:
        f = fresh[k]
        d_ln = f["lnabs"] - r["lnabs"]
        d_ar = (f["arg"] - r["arg"] + math.pi) % (2 * math.pi) - math.pi
        groups["CR lines" if cr else "non-CR lines"].append((k, r["lnabs"], d_ln, d_ar, f["pmin"] / r["pmin"] - 1))
shared = sum(len(v) for v in groups.values())
print(f"shared lambdas: {shared} of {len(fresh)} fresh points")
print()
print("| group | shared points | largest abs d ln|det| | median abs d ln|det| | signed mean d ln|det| | largest abs d arg | median abs d arg | largest rel d pivot min |")
print("|---|---|---|---|---|---|---|---|")
for name, rows in groups.items():
    if not rows:
        print(f"| {name} | 0 | | | | | | |")
        continue
    dl = [abs(x[2]) for x in rows]; da = [abs(x[3]) for x in rows]
    print(f"| {name} | {len(rows)} | {max(dl):.3e} | {statistics.median(dl):.3e} | {statistics.mean(x[2] for x in rows):+.3e} | "
          f"{max(da):.3e} | {statistics.median(da):.3e} | {max(abs(x[4]) for x in rows):.2e} |")
print()
for name, rows in groups.items():
    print(f"{name}: per point (lambda, October ln|det|, d ln|det|, d arg)")
    for k, l0, dl, da, dp in sorted(rows):
        print(f"  ({k[0]:.5f}, {k[1]:.5f})  {l0:11.4f}  {dl:+.3e}  {da:+.3e}")
