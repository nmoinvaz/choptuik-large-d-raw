"""#1025 (d), D 18.5, the numbers of the post, information only: the hybrid ln|det| first differences over 1.90-2.10 (their
least and greatest, and the last five), the signs at 1.90 and 2.10, and the least rate at which D 18's upper root (hi end of
its range) or lower root (bisected) would have passed 2.10 by D 18.5.
usage: d185_d_numbers.py D185_SCANHI D18_SCAN D18_LOWER_BISECTED"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
fh, f18, lo18 = sys.argv[1], sys.argv[2], float(sys.argv[3])
sys.argv = [sys.argv[0], "x"]; sys.path.insert(0, HERE)
import d185_scan_read as rd
S = sorted((json.loads(l) for l in open(fh)), key=lambda r: r["lam"])
d = [(b["lam"], round(b["ln"] - a["ln"], 4)) for a, b in zip(S, S[1:])]
sg = lambda s: "+" if s > 0 else "-"
print(f"D 18.5, {S[0]['lam']:.2f}-{S[-1]['lam']:.2f}, {len(S)} points; signs at the ends {sg(S[0]['sign'])}, {sg(S[-1]['sign'])}")
print(f"ln|det| first differences per 0.01: least {min(x for _, x in d)}, greatest {max(x for _, x in d)}; last five {[x for _, x in d[-5:]]}")
print(f"ln|det| from {S[0]['ln']:.4f} at 1.90 to {S[-1]['ln']:.4f} at 2.10")
up = rd.changes(sorted((json.loads(l) for l in open(f18)), key=lambda r: r["lam"]))[0][1]
print(f"least rate to pass 2.10 by D 18.5: from D 18's upper root ({up['hi']:.6f}) {(2.10 - up['hi']) / 0.5:+.4f} per unit D; "
      f"from the lower root ({lo18:.6f}) {(2.10 - lo18) / 0.5:+.4f}")
