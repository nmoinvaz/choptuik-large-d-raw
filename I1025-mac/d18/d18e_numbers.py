"""#1025 (e), the numbers of the post at one D, information only: the hybrid ln|det| over the scan (first differences per 0.01: least,
greatest, last five; its largest value and where), and the signs at the scan's top and at the reference 2.60 with the parity of the
root count between them in this state.
usage: d18e_numbers.py D SCANUP REFS.jsonl"""
import sys, json
D = float(sys.argv[1])
S = sorted(map(json.loads, open(sys.argv[2])), key=lambda r: r["lam"])
assert all(r["D"] == D for r in S)
ref = [r for r in map(json.loads, open(sys.argv[3])) if r["D"] == D and abs(r["lam"] - 2.6) < 1e-9][0]
d = [round(b["ln"] - a["ln"], 4) for a, b in zip(S, S[1:])]
sg = lambda s: "+" if s > 0 else "-"
top = max(S, key=lambda r: r["ln"])
print(f"D {D:g}, {S[0]['lam']:.2f}-{S[-1]['lam']:.2f}, {len(S)} points; seconds per point {min(r['sec'] for r in S)}-{max(r['sec'] for r in S)}")
print(f"ln|det| first differences per 0.01: least {min(d)}, greatest {max(d)}; last five {d[-5:]}; from {S[0]['ln']:.4f} to {S[-1]['ln']:.4f}; "
      f"largest {top['ln']:.4f} at {top['lam']:.2f}")
print(f"sign at {S[-1]['lam']:.2f} {sg(S[-1]['sign'])}, at 2.60 {sg(ref['sign'])} (ln|det| {ref['ln']:.4f}): ({S[-1]['lam']:.2f}, 2.60) "
      f"{'even' if S[-1]['sign'] == ref['sign'] else 'odd'}")
