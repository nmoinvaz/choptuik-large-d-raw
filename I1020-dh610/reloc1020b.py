#!/usr/bin/env python3
"""reloc1020b.py [--dir m3] [--prefix reloc2] [--names newzero,minus,plus] [--tol 1e-4] [--mutate=shift|sign|norb]: #1020's second-radius checks (the coordinator's order after step 2). Boxes count_reloc2_<name>.json (argcount.py, xi1 r1, zero located again at r1b):
newzero (xi1 0.3 then 0.35), minus and plus (xi1 0.35 then 0.3). Each box must contain a zero of the expected sign located at both radii within tol (absolute, in A and in wf) of its xi1 0.25 place:
newzero's is the located zero of m3/count_M3_ext_r0.25.json, the partners' those of inputs1013/count_M3_cand_r0.25.json. Judging is reloc1020.judge (its selftest and mutations are reloc1020.py's). Exit 0 when every
box passes, 1 otherwise."""
import json
import os
import sys

from reloc1020 import TOL, judge

HERE = os.path.dirname(os.path.abspath(__file__))


def expect():
    ex = {}
    for z in json.load(open(os.path.join(HERE, "inputs1013", "count_M3_cand_r0.25.json")))["zeros"]:
        ex["minus" if z["W"] < 0 else "plus"] = (z["W"], z["located"]["A"], z["located"]["wf"])
    z = json.load(open(os.path.join(HERE, "m3", "count_M3_ext_r0.25.json")))["zeros"][0]
    ex["newzero"] = (z["W"], z["located"]["A"], z["located"]["wf"])
    return ex


def main(argv):
    tol = float(argv[argv.index("--tol") + 1]) if "--tol" in argv else TOL
    d = argv[argv.index("--dir") + 1] if "--dir" in argv else os.path.join(HERE, "m3")
    mut = next((a.split("=")[1] for a in argv if a.startswith("--mutate=")), "")
    pre = argv[argv.index("--prefix") + 1] if "--prefix" in argv else "reloc2"
    names = (argv[argv.index("--names") + 1] if "--names" in argv else "newzero,minus,plus").split(",")
    ex, allok = expect(), True
    for name in names:
        s, a, w = ex[name]
        print(f"{name}: expected sign {s:+d} at ({a:.6f}, {w:.6f}) (tolerance {tol:g} in A and in wf, at both radii)")
        p = os.path.join(d, f"count_{pre}_{name}.json")
        if not os.path.exists(p):
            print("   no count file")
            allok = False
            continue
        ok, lines = judge(ex[name], json.load(open(p)), tol, mut)
        print("\n".join(lines))
        print(f"   {name}: {'PASS' if ok else 'FAIL'}")
        allok = allok and ok
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
