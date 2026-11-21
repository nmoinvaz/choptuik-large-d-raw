"""#1025 (g), the numbers of the post, information only: D 18.25's robust changes in 2.25-2.60 (the same merge and change finder as
d18f_read.py window), each with its estimator range and delta against lambda_0(18.25) (ell_delta.lam0_at) as an interval, and the
hybrid ln|det| at every point of the window.
usage: d1825_g_numbers.py WT_MATTER FILES(,)"""
import sys, os, json
wt, A = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], "x"]; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, wt)
import d185_scan_read as rd
import d18d_read as dr
import ell_delta
D, lo, hi = 18.25, 2.25, 2.60
l0, l0e = ell_delta.lam0_at(D, *ell_delta.lam0_table())
rows = [r for f in A.split(",") for r in map(json.loads, open(f)) if r["D"] == D and r["lam"] <= hi + 0.1 + 1e-9]
S, rep = dr.merge(rows)
W = [r for r in S if lo - 1e-9 <= r["lam"] <= hi + 1e-9]
print(f"lambda_0({D:g}) {l0:.10f} (error {l0e:.1e})")
print("ln|det|: " + ", ".join(f"{r['lam']:.2f} {'+' if r['sign'] > 0 else '-'}{r['ln']:.4f}" for r in W))
for c in rd.changes(S)[0]:
    if c["br"][0] >= lo - 1e-9 and c["br"][1] <= hi + 1e-9:
        print(f"change in ({c['br'][0]:.2f}, {c['br'][1]:.2f}): range [{c['lo']:.6f}, {c['hi']:.6f}], delta [{c['lo'] - l0:+.6f}, {c['hi'] - l0:+.6f}]")
