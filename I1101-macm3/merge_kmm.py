#!/usr/bin/env python3
"""merge_kmm.py OUTDIR SRC1 SRC2 [--mutate=dup|steps] : merges the scans of the same state at --kappa_mm=0.25 (kc87_leg_lambda/<SRC>/scan/scan_D23.0_1025.jsonl) into OUTDIR/scan/scan_D23.0_1025.jsonl, sorted by lambda, for read_lower.py.
Refuses (exit 1) when a source's scan_p0.log lacks the line 'kappa_mm 0.25: ... N steps' with N in 11400 to 12000, when the records name different states, or when a lambda occurs twice.
--mutate=dup copies the first source's first record into the second source (a duplicate lambda: must exit 1), --mutate=steps reads the steps of the first log as 5847 (must exit 1)."""
import json, os, re, sys
L = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/"
out, srcs = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
mut = [a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")]; mut = mut[0] if mut else ""
rd = lambda p: [json.loads(l) for l in open(p) if l.strip()]
rows = []; states = set()
for i, sname in enumerate(srcs):
    m = re.search(r"^kappa_mm 0\.25: .*?, (\d+) steps \(the record", open(L + sname + "/scan/scan_p0.log").read(), re.M)
    if not m: print("no kappa_mm 0.25 line in", sname); sys.exit(1)
    steps = 5847 if (mut == "steps" and i == 0) else int(m.group(1))
    if not 11400 <= steps <= 12000: print("steps %d of %s outside 11400 to 12000" % (steps, sname)); sys.exit(1)
    r = rd(L + sname + "/scan/scan_D23.0_1025.jsonl")
    if mut == "dup" and i == 1: r = r + [rows[0]]
    rows += r; states |= {x["state"] for x in r}
    print("%s: %d records, kappa_mm 0.25 line steps %d, lambda %s" % (sname, len(r), steps, ", ".join("%.3f" % x["lam"] for x in r)))
lams = [x["lam"] for x in rows]
if len(set(lams)) != len(lams): print("a lambda occurs twice:", sorted(lams)); sys.exit(1)
if len(states) != 1: print("the records name %d states: %s" % (len(states), states)); sys.exit(1)
rows.sort(key=lambda x: x["lam"])
os.makedirs(L + out + "/scan", exist_ok=True)
open(L + out + "/scan/scan_D23.0_1025.jsonl", "w").write("".join(json.dumps(x) + "\n" for x in rows))
print("merged %d records into %s/scan/scan_D23.0_1025.jsonl: lambda %s, one state %s" % (len(rows), out, ", ".join("%.3f" % x for x in sorted(lams)), next(iter(states))))
