#!/usr/bin/env python3
"""merge_scans.py OUTDIR SRC1 SRC2 [--mutate=dup|state|log] : merges two scans of the same state (no --kappa_mm: the state's own steps; kc87_leg_lambda/<SRC>/scan/scan_D23.0_1025.jsonl) into OUTDIR/scan/scan_D23.0_1025.jsonl and, under the name read_lower.py
reads (scan_*_p*.jsonl), OUTDIR/scan/scan_D23.0_p0.jsonl, sorted by lambda. Refuses (exit 1) when a scan's scan_p0.log lacks the record-system line ('the record system') or has 'NOT the record system', when the records name different states, or when a lambda
occurs twice. --mutate=dup copies the first source's first record into the second (must exit 1), --mutate=state renames the state of the second source's records (must exit 1), --mutate=log reads the first log as 'NOT the record system' (must exit 1)."""
import json, os, re, sys
L = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/"
out, srcs = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
mut = [a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")]; mut = mut[0] if mut else ""
rd = lambda p: [json.loads(l) for l in open(p) if l.strip()]
rows = []; states = set()
for i, sname in enumerate(srcs):
    log = open(L + sname + "/scan/scan_p0.log").read()
    if mut == "log" and i == 0: log = log.replace("the record system", "NOT the record system")
    if "NOT the record system" in log or "the record system" not in log: print("the log of %s does not say 'the record system'" % sname); sys.exit(1)
    r = rd(L + sname + "/scan/scan_D23.0_1025.jsonl")
    if mut == "dup" and i == 1: r = r + [rows[0]]
    if mut == "state" and i == 1: r = [dict(x, state="other.npy") for x in r]
    rows += r; states |= {x["state"] for x in r}
    print("%s: %d records, the record system line present, lambda %s" % (sname, len(r), ", ".join("%.3f" % x["lam"] for x in r)))
lams = [x["lam"] for x in rows]
if len(set(lams)) != len(lams): print("a lambda occurs twice:", sorted(lams)); sys.exit(1)
if len(states) != 1: print("the records name %d states: %s" % (len(states), states)); sys.exit(1)
rows.sort(key=lambda x: x["lam"])
os.makedirs(L + out + "/scan", exist_ok=True)
txt = "".join(json.dumps(x) + "\n" for x in rows)
open(L + out + "/scan/scan_D23.0_1025.jsonl", "w").write(txt); open(L + out + "/scan/scan_D23.0_p0.jsonl", "w").write(txt)
print("merged %d records into %s/scan/scan_D23.0_1025.jsonl and scan_D23.0_p0.jsonl: lambda %s, one state %s" % (len(rows), out, ", ".join("%.3f" % x for x in sorted(lams)), next(iter(states))))
