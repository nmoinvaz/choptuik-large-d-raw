# #928: the last two converged chain states of one coupling at M = 32 with D <= A (out/sm_records.jsonl), as
# "<state at the larger D> <state before it> <the larger D>"
import json, os, sys
out, eta, A = sys.argv[1], sys.argv[2], float(sys.argv[3])
best = {}
for l in open(os.path.join(out, "sm_records.jsonl")):
    r = json.loads(l)
    if str(r["eta"]) == eta and r["converged"] and r["M"] == 32 and float(r["D"]) <= A + 1e-9 and "polish" not in r["tag"]:
        best[float(r["D"])] = r["tag"]
ds = sorted(best)[-2:]
print(os.path.join(out, f"sm_{best[ds[1]]}.npz"), os.path.join(out, f"sm_{best[ds[0]]}.npz"), "%.10g" % ds[1])
