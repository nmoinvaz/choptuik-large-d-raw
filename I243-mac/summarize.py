#!/usr/bin/env python3
"""I243-mac: per re-evaluated count, the old and new wind(g) of every box, resolved flags, new determinants and the
alias rule's bisections. Writes summary.txt (and prints it).  python3 summarize.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BOXES = ["B0", "U0", "B1a", "B1b", "B1c", "B1", "U", "full"]
lines = []
for name in sorted(os.listdir(HERE)):
    p = os.path.join(HERE, name, "data", "modecount_results.jsonl")
    if not os.path.exists(p):
        continue
    old = json.loads(open(os.path.join(HERE, "records", name + ".jsonl")).readline())
    new = [r for r in (json.loads(l) for l in open(p)) if r["tag"] == old["tag"]][-1]
    cl = open(os.path.join(HERE, name, "cache_lines.txt")).read().split("\n")[1]
    ow = " ".join(f"{b} {old['boxes'][b]['winding_g_int']:+d}" for b in BOXES)
    nw = " ".join(f"{b} {new['boxes'][b]['winding_g_int']:+d}" for b in BOXES)
    changed = [b for b in BOXES if old["boxes"][b]["winding_g_int"] != new["boxes"][b]["winding_g_int"]]
    unres = [b for b in BOXES if not new["boxes"][b]["resolved"]]
    nal = sum(e["alias_bisections"] for e in new["edges"].values())
    mm = sum(e["verify_mismatch"] for e in new["edges"].values())
    mml = sum(e["verify_mismatch_last"] for e in new["edges"].values())
    mx = max(e["max_step"] for e in new["edges"].values())
    lines += [f"{name}: {cl}",
              f"  old {ow}",
              f"  new {nw}",
              f"  {'CORRECTED ' + ', '.join(changed) if changed else 'unchanged'}; new rule: {nal} alias bisections, "
              f"{new['sweeps']} sweeps, max step {mx:.3f} rad, verification mismatches {mm} (last pass {mml}), "
              f"unresolved boxes {unres or 'none'}"]
    po = os.path.join(HERE, name, "offset.json")
    if os.path.exists(po):
        o = json.load(open(po))
        p1 = os.path.join(HERE, name, "offset_run1.json")
        nd = json.load(open(p1))["new_determinants"] if os.path.exists(p1) else o["new_determinants"]
        bx = [b for b, x in o["boxes"].items() if abs(x["new"] - x["old"]) > 1e-6]
        lines.append(f"  second-scale check: {o['flags']} of {o['intervals']} intervals flagged, {nd} new determinants, "
                     f"largest piece {max(v['max_piece'] for v in o['edges'].values()):.3f} rad, largest sum error "
                     f"{max(v['max_sum_error'] for v in o['edges'].values()):.1e}; boxes "
                     + (f"changed: {bx}" if bx else "unchanged"))
open(os.path.join(HERE, "summary.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
