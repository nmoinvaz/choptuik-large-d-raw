"""#1025 (m), the numbers of the post, information only: the k_c 63 path through the roots read k_c-stable (D 17.75 upper, D 18.125)
and the roots between them (D 17.5 winb's row A, D 18 win2b's bisected upper, D 18.25's 1.7425, D 18.5 winb's bisected), with the
slopes per unit D between neighbours (det-linear estimates where not bisected); and the k_c 55 - k_c 63 differences at D 17.75 and 18.125.
usage: d18125k_numbers.py P4HI_WIN.jsonl D1775_KC63(,) D1775_KC55 D18125_KC63 D18125_KC55 D1825_SCAN"""
import sys, os, json
sys.argv, A = [sys.argv[0], "x"], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d185_scan_read as rd
import d18d_read as dr
ch = lambda fs: [c["lin"] for c in rd.changes(dr.merge([json.loads(l) for f in fs.split(",") for l in open(f)])[0])[0]]
l175 = [json.loads(l)["lam"] for l in open(A[0]) if json.loads(l)["D"] == 17.5 and json.loads(l)["kc"] == 63][0]
u1775_63, u1775_55 = ch(A[1])[1], ch(A[2])[1]
m63, m55 = ch(A[3])[0], ch(A[4])[0]
r1825 = [x for x in ch(A[5]) if 1.70 < x < 1.80][0]
P = [(17.5, l175), (17.75, u1775_63), (18.0, 1.8074339746), (18.125, m63), (18.25, r1825), (18.5, 1.6772090983)]
print("k_c 63 path: " + " -> ".join(f"D {D:g} {x:.6f}" for D, x in P))
print("slopes per unit D: " + ", ".join(f"{(b[1] - a[1]) / (b[0] - a[0]):+.4f}" for a, b in zip(P, P[1:])))
print(f"k_c 55 - k_c 63: D 17.75 {u1775_55 - u1775_63:+.6f}, D 18.125 {m55 - m63:+.6f}")
