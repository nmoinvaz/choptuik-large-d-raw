"""#1025 (d), the coordinator's continuity reading beside the orientation one, information only: the slopes per unit D of the two
paths into D 18.25's root 1.7425 and on to D 18.5's 1.6772 (intervals from the estimator ranges; D 18's lower root bisected), from
D 17.5 (winb's row A) on; and the least rate at which the eigenvalue not on each path left 1.55-1.95 upward by D 18.25.
usage: d18d_continuity.py D18_SCANS(,) D1825_SCAN D185_SCAN D18_LOWER_BISECTED P4HI_WIN.jsonl"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
f18, f25, f185, lo18, p4w = sys.argv[1].split(","), sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
sys.argv = [sys.argv[0], "x"]; sys.path.insert(0, HERE)
import d185_scan_read as rd

def load(fs):
    S = {}
    for f in fs:
        for l in open(f):
            r = json.loads(l); S.setdefault(round(r["lam"], 6), r)
    return [S[k] for k in sorted(S)]

iv = lambda r: (r["lo"], r["hi"])
low, up = rd.changes(load(f18))[0]; r25 = rd.changes(load([f25]))[0][0]; r185 = rd.changes(load([f185]))[0][0]
l175 = [json.loads(l)["lam"] for l in open(p4w) if json.loads(l)["D"] == 17.5 and json.loads(l)["kc"] == 63][0]
sl = lambda a, b, dD: ((b[0] - a[1]) / dD, (b[1] - a[0]) / dD)
f = lambda s: f"[{s[0]:+.4f}, {s[1]:+.4f}]"
P = {"orientation (through D 18's lower root)": (lo18, lo18), "continuity (through D 18's upper root)": iv(up)}
for name, a in P.items():
    print(f"{name}: D 17.5 {l175:.6f} -> D 18 [{a[0]:.6f}, {a[1]:.6f}] -> D 18.25 [{r25['lo']:.6f}, {r25['hi']:.6f}] -> D 18.5 "
          f"[{r185['lo']:.6f}, {r185['hi']:.6f}]")
    print(f"  slopes per unit D: {f(sl((l175, l175), a, 0.5))}, {f(sl(a, iv(r25), 0.25))}, {f(sl(iv(r25), iv(r185), 0.25))}")
print(f"least upward rate, D 18 -> 18.25, of the eigenvalue off the path: orientation reading (from the upper root, hi end "
      f"{up['hi']:.6f}) {(1.95 - up['hi']) / 0.25:+.4f}; continuity reading (from the lower root {lo18:.6f}) {(1.95 - lo18) / 0.25:+.4f}")
