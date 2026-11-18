# #928: the last two converged chain states of one coupling at M = 32 with D <= A (out/sm_records.jsonl), as
# "<state at the larger D> <state before it> <the larger D>"
import json, os, sys
out, eta, A = sys.argv[1], sys.argv[2], float(sys.argv[3])
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
    if str(r["eta"]) == eta and ok(r) and r["M"] == 32 and float(r["D"]) <= A + 1e-9 and "polish" not in r["tag"] \
            and "qdcheck" not in r["tag"]:
        best[float(r["D"])] = r["tag"]
ds = sorted(best)[-2:]
print(os.path.join(out, f"sm_{best[ds[1]]}.npz"), os.path.join(out, f"sm_{best[ds[0]]}.npz"), "%.10g" % ds[1])
