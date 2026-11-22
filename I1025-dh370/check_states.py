"""#1025 continuation seed check: which saved leap states reproduce their record.
usage: check_states.py TAG [--mutate] [--last K]
For the K newest D-named states of the tag (default 4), as d18_hybsign.py does: z[-1] equals the record's Delta, and
freeze_from + residual give the record's step count and |F| (within 1%, floor 1e-13). Prints the newest two that pass
and the h the run left (the last 'h ->' line of leap.log after its newest record, else the newest record's h).
--mutate adds 1e-6 to one entry of z before the check; every state must then FAIL (the check's control)."""
import sys, os, re, glob, json
import numpy as np
WT = "/home/nathan/Source/choptuik-large-d-1025/solver/matter"
LOG = "/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc63_leap/leap.log"
sys.path.insert(0, WT)
os.chdir(WT)
from dss_ell import DSSEll, NODES_STD

tag = sys.argv[1]
mutate = "--mutate" in sys.argv
K = int(sys.argv[sys.argv.index("--last") + 1]) if "--last" in sys.argv else 4
recs = {}
for l in open(f"data/{tag}.jsonl"):
    if l.strip():
        r = json.loads(l)
        recs[r["D"]] = r
files = {}
for f in glob.glob(f"data/sol_{tag}_D*.npy"):
    m = re.search(r"_D(\d+\.\d+)\.npy$", f)
    if m and len(m.group(1).split(".")[1]) == 6:
        files[round(float(m.group(1)), 10)] = f
cand = sorted(files, reverse=True)[:K]
good = []
for D in cand:
    rec = recs.get(D)
    if rec is None:
        print(f"D {D}: no record line: FAIL", flush=True)
        continue
    try:
        z = np.load(files[D])
    except Exception as e:
        print(f"D {D}: cannot load ({type(e).__name__}): FAIL", flush=True)
        continue
    if mutate:
        z = z.copy(); z[len(z) // 2] += 1e-6
    ok_d = abs(z[-1] - rec["Delta"]) <= 1e-15
    S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
    steps = sum(S.freeze_from(z, rec["kappa"]).values())
    with np.errstate(all="ignore"):
        F = float(np.linalg.norm(S.residual(z[None, :])[0]))
    ok_f = abs(F - rec["F"]) <= max(1e-2 * rec["F"], 1e-13) and steps == rec["steps"]
    ok = ok_d and ok_f
    print(f"D {D}: z[-1] {'=' if ok_d else '!='} Delta, |F| {F:.6e} (record {rec['F']:.6e}), steps {steps} (record {rec['steps']}): "
          f"{'PASS' if ok else 'FAIL'}  {os.path.basename(files[D])}", flush=True)
    if ok:
        good.append(D)
if mutate:
    print("mutation control:", "every state failed (as it must)" if not good else f"STATES PASSED {good}: THE CHECK CANNOT FAIL")
    sys.exit(0 if not good else 4)
h = None
for l in open(LOG, errors="replace"):
    m = re.search(r"h -> ([0-9.eE+-]+)\s*$", l)
    if m:
        h = float(m.group(1))
if h is None:
    h = recs[max(recs)]["h"]
print("h the run left:", h)
if len(good) >= 2:
    print(f"seed: solA {files[good[1]]} DA {good[1]}  solB {files[good[0]]} DB {good[0]}")
else:
    print("FEWER THAN TWO STATES PASS: look at older ones (--last K)"); sys.exit(2)
