"""#1025 D 18.46875: the system check of d18_hybsign.py alone (its lines from the record row to the exit 3, same calls and bars, no determinant): the state rebuilds
its record line's discrete system, |F| within 1% of the record's (or 1e-13) and the same step count. Exit 0 the record system, 3 not.
usage (absolute paths; env P4_WT_MATTER = solver/matter): accept_check.py REC.jsonl STATE.npy D"""
import sys, os, json, numpy as np
WTM = os.environ["P4_WT_MATTER"]
sys.path.insert(0, WTM)
os.chdir(WTM)
from dss_ell import DSSEll, NODES_STD
recf, st, D = sys.argv[1], sys.argv[2], float(sys.argv[3])
rec = [json.loads(l) for l in open(recf) if json.loads(l).get("D") == D][-1]
z = np.load(st)
S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
steps = S.freeze_from(z, rec["kappa"])
with np.errstate(all="ignore"):
    F = float(np.linalg.norm(S.residual(z[None, :])[0]))
same = abs(F - rec["F"]) <= max(1e-2 * rec["F"], 1e-13) and sum(steps.values()) == rec["steps"]
print(f"D {D} k_c {rec['kc']}: |F| {F:.10e} (record {rec['F']:.10e}), steps {sum(steps.values())} (record {rec['steps']}): "
      f"{'the record system' if same else 'NOT the record system'}", flush=True)
sys.exit(0 if same else 3)
