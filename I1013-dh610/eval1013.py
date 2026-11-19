#!/usr/bin/env python3
"""eval1013.py COUNT_PILOT.json [RECOUNT.json ...]: the pilot's four unresolved cells after the recount rungs (coordinator's order, #1013: recount them at xi1 0.25 and 0.17; if they resolve, step 2
starts; a zero they add is reported with its sign; a rim cell that stays unresolved at every radius stops the run). Prints, per file, the unresolved cells and the zeros (sign, cell, located A and wf);
exit 0 when the last file has no unresolved cells, 1 otherwise. A recount file's 'unresolved' is the list of its own cells still unresolved. Control: with only the pilot's own count the check
must fail (4 unresolved)."""
import json
import sys

ok = None
for i, p in enumerate(sys.argv[1:]):
    d = json.load(open(p))
    un = d["unresolved"]
    print(f"{p}: xi1 {d.get('r1')}, {len(un)} unresolved cells, {len(d['zeros'])} zeros, leaf sum {d.get('leaf_sum')}, boundary winding {d.get('boundary_winding')}")
    for u in un:
        print(f"   unresolved: A {u[0]:.4f}-{u[1]:.4f}, wf {u[2]:.4f}-{u[3]:.4f}")
    for z in d["zeros"]:
        loc = z.get("located")
        print(f"   zero of sign {z['W']:+d} in cell A {z['cell'][0]:.4f}-{z['cell'][1]:.4f}, wf {z['cell'][2]:.4f}-{z['cell'][3]:.4f}: "
              + (f"located at A {loc['A']:.6f}, wf {loc['wf']:.6f}" if loc else "not located"))
    ok = not un
print("RESOLVED" if ok else "UNRESOLVED CELLS REMAIN")
sys.exit(0 if ok else 1)
