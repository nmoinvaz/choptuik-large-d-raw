"""#1025 (ii), the numbers of the post, information only: the hybrid ln|det| at D 18.25 over 1.20-1.55 (all points merged, in lambda
order) and its least value, the root's estimator range from d1825_low_read.log's reader, and the least rate per unit D at which this
root would reach 1.20 by D 18.3125, where (iii) reads 1.20's sign flipped back.
usage: d1825_low_numbers.py FILES(,)"""
import sys, os, json
sys.argv, A = [sys.argv[0], "x"], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d185_scan_read as rd
import d18d_read as dr
rows = [r for f in A[0].split(",") for r in map(json.loads, open(f)) if r["D"] == 18.25 and r["lam"] <= 1.65 + 1e-9]
S, rep = dr.merge(rows)
W = [r for r in S if r["lam"] <= 1.55 + 1e-9]
print("ln|det| at D 18.25: " + ", ".join(f"{r['lam']:.2f} {r['ln']:.4f}" for r in W))
m = min(W, key=lambda r: r["ln"]); print(f"least ln|det| in 1.20-1.55: {m['ln']:.4f} at {m['lam']:.2f}")
c = [c for c in rd.changes(S)[0] if 1.20 <= c["br"][0] and c["br"][1] <= 1.55][0]
print(f"root: bracket {c['br']}, range [{c['lo']:.6f}, {c['hi']:.6f}]; to reach 1.20 by D 18.3125: at least "
      f"{(c['lo'] - 1.20) / 0.0625:.4f} per unit D (from the range's low end)")
