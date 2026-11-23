#!/usr/bin/env python3
"""#1025 eval_dh170_d1975 (dh610) freeze_compare.py IN_DIR (env P4_WT_MATTER = solver/matter of the worktree): INFORMATION, not an evaluation of det. Builds DSSEll for each of the four k_c 87 D 19.75 states exactly as
d18_hybsign.py does (record's kc, Ks, u0, rk; Delta_ref = z[-1]; freeze_from(z, record's kappa)) and compares the RK step counts per segment (st = freeze_from's dict: the count is max(4, ceil(L g / kappa rk)), so a state move of 4e-10 can change one
count by one when the argument is near an integer, and the discrete system then differs). Prints each state's counts total, the segments whose counts differ for each pair. Controls (exit 1 if either fails): a state against itself differs in no segment;
dh170's state at kappa 0.7 against kappa 0.69 differs in at least one."""
import sys, os, json, itertools
import numpy as np
IN = os.path.abspath(sys.argv[1])
WTM = os.environ["P4_WT_MATTER"]
sys.path.insert(0, WTM); os.chdir(WTM)
from dss_ell import DSSEll, NODES_STD
D = 19.75
TAGS = [("dh170 start", "l1kc87dh170d1975"), ("linRe", "l1kc87linRe"), ("macRe", "l1kc87macRe"), ("macm3 start", "l1kc87macm3d1975")]


def freeze(tag, kappa=None):
    rec = [json.loads(l) for l in open(f"{IN}/{tag}.jsonl") if json.loads(l).get("D") == D][-1]
    z = np.load(f"{IN}/sol_{tag}_D19.7500.npy")
    S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
    st = S.freeze_from(z, kappa if kappa else rec["kappa"])
    with np.errstate(all="ignore"):
        F = float(np.linalg.norm(S.residual(z[None, :])[0]))
    return dict(st), F, rec


def diff(a, b):
    return [(k, a.get(k), b.get(k)) for k in sorted(set(a) | set(b), key=str) if a.get(k) != b.get(k)]


FR = {}
for name, tag in TAGS:
    st, F, rec = freeze(tag)
    FR[name] = st
    print(f"{name}: {len(st)} segments, {sum(st.values())} steps, |F| at this freeze {F:.10e} (its record {rec['F']:.10e})", flush=True)
print()
for (na, _), (nb, _) in itertools.combinations(TAGS, 2):
    d = diff(FR[na], FR[nb])
    print(f"{na} against {nb}: {len(d)} segments differ" + ("" if not d else ": " + "; ".join(f"{k}: {x} -> {y}" for k, x, y in d)))
print()
c1 = len(diff(FR["dh170 start"], FR["dh170 start"]))
st69, F69, _ = freeze("l1kc87dh170d1975", 0.69)
c2 = len(diff(FR["dh170 start"], st69))
print(f"control 1: dh170's state against itself: {c1} segments differ (wanted 0)")
print(f"control 2: dh170's state at kappa 0.7 against kappa 0.69: {c2} segments differ, {sum(st69.values())} steps (wanted at least 1)")
sys.exit(0 if c1 == 0 and c2 >= 1 else 1)
