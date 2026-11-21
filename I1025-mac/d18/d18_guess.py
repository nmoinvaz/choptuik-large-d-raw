"""#1025 D 18: the lambda_1 guess at k_c 63 from the signtested k_c 63 rows' trend over D 16.5-17 (the coordinator's rule), and the
stub record p4_hybrid.py reads (winb's leap record at D 18, which has no lambda, plus lam_guess; lam is set to the guess so that
p4_hybrid's record filter takes it, and its minus_record then reads root minus guess). usage: d18_guess.py RAW D_TARGET LEAP_JSONL OUT_STUB"""
import sys, json
raw, Dt, leapf, out = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
rows = [("I1025-win/out/l1kc63Fw1025b.jsonl", 16.5), ("I1025-win/out/l1kc63Fw1025.jsonl", 17.0)]   # signtested (ell_lam_signtested.json)
pts = []
for f, D in rows:
    r = [json.loads(l) for l in open(f"{raw}/{f}") if json.loads(l).get("D") == D and json.loads(l).get("lam")][-1]
    pts.append((D, r["lam"])); print(f"{f} D {D}: lam {r['lam']!r}")
(D1, l1), (D2, l2) = pts
s = (l2 - l1) / (D2 - D1); g = l2 + s * (Dt - D2)
print(f"slope over D {D1:g}-{D2:g}: {s!r}; guess at D {Dt:g}: {g!r}")
for w in (0.02, 0.06, 0.15, 0.35):
    print(f"  window {w}: grid {g * (1 - w):.7f}, {g:.7f}, {g * (1 + w):.7f}")
rec = [json.loads(l) for l in open(leapf) if json.loads(l).get("D") == Dt][-1]
assert "lam" not in rec, "the leap record already has a lambda"
rec.update(lam_guess=g, lam=g, lam_is_guess=True, stub_note=f"winb's leap record at D {Dt:g} ({leapf.split('/')[-1]}) with lam_guess "
           f"from the k_c 63 trend over D {D1:g}-{D2:g}; lam is the guess (no float64 root), so minus_record is root minus guess")
open(out, "w").write(json.dumps(rec) + "\n")
print(f"stub {out}: D {rec['D']} k_c {rec['kc']} kappa {rec['kappa']} u0 {rec['u0']} Ks {rec['Ks']} F {rec['F']!r} steps {rec['steps']}")
