"""#1025, D 18.25's map over 1.20-2.60 within this one state, information only: every robust change of the merged D 18.25 points
(the check's 1.20 and 2.60, (ii), (b), (e), (g)), with its estimator range and delta against lambda_0(18.25) as an interval.
usage: d1825_map_numbers.py WT_MATTER FILES(,)"""
import sys, os, json
wt, A = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], "x"]; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, wt)
import d185_scan_read as rd
import d18d_read as dr
import ell_delta
l0, l0e = ell_delta.lam0_at(18.25, *ell_delta.lam0_table())
S, rep = dr.merge([r for f in A.split(",") for r in map(json.loads, open(f)) if r["D"] == 18.25])
rob, non = rd.changes(S)
print(f"D 18.25: {len(S)} points {S[0]['lam']:.2f}-{S[-1]['lam']:.2f}; repeats {[(k, a) for k, a, _ in rep]}; lambda_0 {l0:.10f} (error {l0e:.1e})")
print(f"robust changes {len(rob)}, non-robust {[c['br'] for c in non] or 'none'}")
for c in rob:
    print(f"  ({c['br'][0]:.2f}, {c['br'][1]:.2f}): range [{c['lo']:.6f}, {c['hi']:.6f}], delta [{c['lo'] - l0:+.6f}, {c['hi'] - l0:+.6f}]")
