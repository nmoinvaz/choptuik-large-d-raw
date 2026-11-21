"""#1025 (b), the numbers of the post, information only: the D 18.25 root's bracket, range, delta and orientation; the
signs at lambda 1.55, 1.90 and 1.95 at D 18, 18.25 and 18.5; the lower root's slopes per unit D over D 18 -> 18.25 -> 18.5
(intervals from the ranges); the least rate at which D 18's upper root would have left 1.55-1.95 upward by D 18.25; and the
first differences of the hybrid ln|det| at the top of each window.
usage: d1825_post_numbers.py D18_SCANS(,) D1825_SCAN D185_SCAN D18_LOWER_BISECTED WT_MATTER"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
f18, f25, f185, lo18, wt = sys.argv[1].split(","), sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
sys.argv = [sys.argv[0], "x"]; sys.path.insert(0, HERE); sys.path.insert(0, wt)
import d185_scan_read as rd
import ell_delta

def load(fs):
    S = {}
    for f in fs:
        for l in open(f):
            r = json.loads(l); S.setdefault(round(r["lam"], 6), r)
    return [S[k] for k in sorted(S)]

sg = lambda s: "+" if s > 0 else "-"
A, B, C = load(f18), load([f25]), load([f185])
for D, S in ((18.0, A), (18.25, B), (18.5, C)):
    by = {round(r["lam"], 2): r for r in S}
    rob, non = rd.changes(S)
    o = [f"({c['br'][0]:.2f}, {c['br'][1]:.2f}) {sg(by[round(c['br'][0], 2)]['sign'])} to {sg(by[round(c['br'][1], 2)]['sign'])} "
         f"[{c['lo']:.6f}, {c['hi']:.6f}]" for c in rob]
    print(f"D {D:g}: window {S[0]['lam']:.2f}-{S[-1]['lam']:.2f}, {len(S)} points; robust changes {o}; not counted {[c['br'] for c in non] or 'none'}")
    print(f"  signs at 1.55, 1.90, 1.95: {[sg(by[x]['sign']) if x in by else 'n/a' for x in (1.55, 1.90, 1.95)]}")
    top = S[-6:]
    print(f"  ln|det| first differences over {top[0]['lam']:.2f}-{top[-1]['lam']:.2f}: {[round(b['ln'] - a['ln'], 4) for a, b in zip(top, top[1:])]}")
l0 = ell_delta.lam0_at(18.25, *ell_delta.lam0_table())[0]
r25 = rd.changes(B)[0][0]; r185 = rd.changes(C)[0][0]; up18 = rd.changes(A)[0][1]
print(f"D 18.25 root: range [{r25['lo']:.6f}, {r25['hi']:.6f}], delta [{r25['lo'] - l0:+.6f}, {r25['hi'] - l0:+.6f}] (lambda_0 {l0:.10f})")
print(f"lower root slopes per unit D: D 18 ({lo18:.6f}) -> D 18.25 [{(r25['lo'] - lo18) / 0.25:+.4f}, {(r25['hi'] - lo18) / 0.25:+.4f}]; "
      f"D 18.25 -> D 18.5 [{(r185['lo'] - r25['hi']) / 0.25:+.4f}, {(r185['hi'] - r25['lo']) / 0.25:+.4f}]")
print(f"D 18 upper root [{up18['lo']:.6f}, {up18['hi']:.6f}] above 1.95 by D 18.25: a rate of at least "
      f"{(1.95 - up18['hi']) / 0.25:+.4f} per unit D")
