"""#1025 (d), D 18, the numbers of the post, information only: the hybrid ln|det| first differences over 1.90-2.10 (least, greatest,
last five), and the hybrid signs at lambda 1.55, 1.90 and 2.10 at D 18, 18.25 and 18.5 (n/a outside a scan), each state's own.
usage: d18_d_numbers.py D18_SCANHI D18_SCANS(,) D1825_SCAN D185_SCANS(,)"""
import sys, json
load = lambda fs: {round(r["lam"], 2): r for f in fs for r in map(json.loads, open(f))}
H = sorted(map(json.loads, open(sys.argv[1])), key=lambda r: r["lam"])
d = [round(b["ln"] - a["ln"], 4) for a, b in zip(H, H[1:])]
sg = lambda s: "+" if s > 0 else "-"
print(f"D 18, {H[0]['lam']:.2f}-{H[-1]['lam']:.2f}, {len(H)} points: signs {sorted(set(sg(r['sign']) for r in H))}, noise-robust {all(r['noise_robust'] for r in H)}; "
      f"seconds per point {min(r['sec'] for r in H)}-{max(r['sec'] for r in H)}")
print(f"ln|det| first differences per 0.01: least {min(d)}, greatest {max(d)}; last five {d[-5:]}; from {H[0]['ln']:.4f} to {H[-1]['ln']:.4f}")
for D, fs in ((18, sys.argv[2].split(",") + [sys.argv[1]]), (18.25, [sys.argv[3]]), (18.5, sys.argv[4].split(","))):
    S = load(fs)
    print(f"D {D:g}: signs at 1.55, 1.90, 2.10: {[sg(S[x]['sign']) if x in S else 'n/a' for x in (1.55, 1.90, 2.10)]}")
