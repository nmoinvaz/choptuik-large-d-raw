"""#1025, beside the sign-convention check, information: each k_c 63 state's frozen RK4 step counts per segment (dss_ell.freeze_from
with the record's kappa), their totals against the records, and which segments change their count between consecutive states.
M's discrete system changes there, so a det sign that changes between states without a root crossing would come from it.
usage: d18_state_steps.py REC.jsonl:STATE.npy:D,...   (in D order)"""
import sys, os, json, numpy as np
WTM = os.environ.get("P4_WT_MATTER", "/Users/nathan/Source/choptuik-1025/solver/matter")
sys.path.insert(0, WTM); os.chdir(WTM)
from dss_ell import DSSEll, NODES_STD
prev = None
for item in sys.argv[1].split(","):
    recf, st, D = item.split(":"); D = float(D)
    rec = [json.loads(l) for l in open(recf) if json.loads(l).get("D") == D][-1]
    z = np.load(st)
    S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk") or 1)
    steps = S.freeze_from(z, rec["kappa"])
    tot = sum(steps.values())
    print(f"D {D:g} ({os.path.basename(st)}): total {tot} (record {rec['steps']}, {'same' if tot == rec['steps'] else 'DIFFERENT'}); {steps}")
    if prev is not None:
        ch = {k: (prev[1][k], steps[k]) for k in steps if prev[1].get(k) != steps[k]}
        print(f"  segments changed from D {prev[0]:g}: {len(ch)} of {len(steps)}: {ch}")
    prev = (D, steps)
