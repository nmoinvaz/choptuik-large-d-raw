# #928: the chain's states of one coupling with A < D <= B, in the order of D (the last converged record per D of
# out/sm_records.jsonl), and the two rates before them as mode_lam.py's --prev (from out/sm_lam.jsonl, else given)
import json, os, sys
out, eta, A, B, prev0 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
def ok(r):
    """a converged record; a hand-over run (--tol above 1e-28 with --qd) exactly when its quad-double stage accepted it
    (its first version also asked for the double-double stage's own convergence, which left out D 12.9375 and 13)"""
    q = r.get("qd", {})
    if q.get("handover_tol", 0) > 1e-28:
        return bool(q.get("accepted"))                      # also when its double-double stage stalled above its tolerance
    return r["converged"]


best = {}
for l in open(os.path.join(out, "sm_records.jsonl")):
    r = json.loads(l)
    if str(r["eta"]) == eta and ok(r) and r["M"] == 32 and "qdcheck" not in r["tag"] and A + 1e-9 < float(r["D"]) <= B + 1e-9:
        if "polish" in r["tag"] or float(r["D"]) not in best or "polish" not in best[float(r["D"])]:
            best[float(r["D"])] = r["tag"]
lam = {}
p = os.path.join(out, "sm_lam.jsonl")
if os.path.exists(p):
    for l in open(p):
        r = json.loads(l)
        if str(r["eta"]) == eta and r["M"] == 32 and r["K"] == 21 and r.get("lam") and float(r["D"]) <= A + 1e-9:
            lam[float(r["D"])] = r["lam"]
ds = sorted(lam)[-2:]
prev = ",".join(f"{d!r}:{lam[d]!r}" for d in ds) if len(ds) == 2 else prev0
print(prev)
print(" ".join(os.path.join(out, f"sm_{best[d]}.npz") for d in sorted(best)))
