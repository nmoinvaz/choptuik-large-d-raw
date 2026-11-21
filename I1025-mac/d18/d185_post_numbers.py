"""#1025 D 18.5 scan, the numbers of the post, information only: the root's estimator range and delta, the local minima of
the hybrid ln|det| that are not beside a sign change (where a pair closer than the grid would show), at D 18 and 18.5,
and the slopes per unit D from D 17.5 (winb's row A) and from each D 18 root to the D 18.5 root (intervals from ranges).
usage: d185_post_numbers.py D185_SCAN D18_SCAN D18_LOWER_BISECTED P4HI_WIN.jsonl WT_MATTER"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
s185, s18, lo18, p4w, wt = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5]
sys.argv = [sys.argv[0], "x"]; sys.path.insert(0, HERE); sys.path.insert(0, wt)
import d185_scan_read as rd
import ell_delta

load = lambda f: sorted((json.loads(l) for l in open(f)), key=lambda r: r["lam"])
A, B = load(s18), load(s185)
for D, S in ((18.0, A), (18.5, B)):
    rob, non = rd.changes(S)
    near = {round(v, 2) for c in rob + non for v in c["br"]}
    mins = [S[i]["lam"] for i in range(1, len(S) - 1) if S[i]["ln"] < S[i - 1]["ln"] and S[i]["ln"] < S[i + 1]["ln"]]
    print(f"D {D:g}: robust changes {[c['br'] for c in rob]}; ln|det| local minima {mins}; not beside a change: "
          f"{[m for m in mins if round(m, 2) not in near] or 'none'}")
l0 = ell_delta.lam0_at(18.5, *ell_delta.lam0_table())[0]
r = rd.changes(B)[0][0]
print(f"D 18.5 root: bracket {r['br']}, range [{r['lo']:.6f}, {r['hi']:.6f}], delta [{r['lo'] - l0:+.6f}, {r['hi'] - l0:+.6f}]")
up = rd.changes(A)[0][1]
l175 = [json.loads(l)["lam"] for l in open(p4w) if json.loads(l)["D"] == 17.5 and json.loads(l)["kc"] == 63][0]
sl = lambda a0, a1, b0, b1, dD: ((b0 - a1) / dD, (b1 - a0) / dD)
print(f"slopes per unit D: D 17.5 ({l175:.6f}) -> D 18 lower {(lo18 - l175) / 0.5:+.4f}, -> D 18 upper "
      f"[{sl(l175, l175, up['lo'], up['hi'], 0.5)[0]:+.4f}, {sl(l175, l175, up['lo'], up['hi'], 0.5)[1]:+.4f}]")
print(f"  D 18 lower ({lo18:.6f}) -> D 18.5 [{sl(lo18, lo18, r['lo'], r['hi'], 0.5)[0]:+.4f}, {sl(lo18, lo18, r['lo'], r['hi'], 0.5)[1]:+.4f}]; "
      f"D 18 upper [{up['lo']:.6f}, {up['hi']:.6f}] -> D 18.5 [{sl(up['lo'], up['hi'], r['lo'], r['hi'], 0.5)[0]:+.4f}, "
      f"{sl(up['lo'], up['hi'], r['lo'], r['hi'], 0.5)[1]:+.4f}]")
