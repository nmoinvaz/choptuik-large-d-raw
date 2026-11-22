"""#1025 (k), the numbers of the post, information only: the slopes per unit D, at k_c 63, of the path through the root that (k) finds
k_c-stable at D 17.75 (D 17.5 winb's row A -> D 17.75 dh170's upper root -> D 18 win2b's bisected upper root), and of the path through
the k_c-dependent lower root (D 17.75 dh170's lower -> D 18 the bisected lower root); det-linear estimates.
usage: d1775k_numbers.py P4HI_WIN.jsonl D1775_KC63_SCANS(,)"""
import sys, os, json
sys.argv, A = [sys.argv[0], "x"], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d185_scan_read as rd
import d18d_read as dr
l175 = [json.loads(l)["lam"] for l in open(A[0]) if json.loads(l)["D"] == 17.5 and json.loads(l)["kc"] == 63][0]
S, _ = dr.merge([json.loads(l) for f in A[1].split(",") for l in open(f)])
lo, up = [c["lin"] for c in rd.changes(S)[0]]
u18, l18 = 1.8074339746, 1.7749781027
print(f"upper path (k_c-stable at 17.75): D 17.5 {l175:.6f} -> 17.75 {up:.6f} -> 18 {u18:.10f}: slopes {(up - l175) / 0.25:+.4f}, {(u18 - up) / 0.25:+.4f}")
print(f"lower path (k_c-dependent at 17.75): D 17.75 {lo:.6f} -> 18 {l18:.10f}: slope {(l18 - lo) / 0.25:+.4f}")
