"""#1025 D 18.5: the lambda_1 guess at k_c 63, a line through D 17's hybrid root at k_c 63 (P4, the Mac's re-root of winb's
l1kc63Fw1025 record, read under P4 amendment 5) and the D 18 hybrid root (ell_d18_hybrid_1025.jsonl), the coordinator's ruling of
2026-11-21; and the stub record p4_hybrid.py reads (the Mac's leap record at D 18.5 plus lam_guess, lam set to the guess).
usage: d185_guess.py P4.jsonl D18.jsonl D_TARGET LEAP_JSONL OUT_STUB"""
import sys, json
p4f, d18f, Dt, leapf, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5]
a = [json.loads(l) for l in open(p4f) if json.loads(l).get("record") == "l1kc63Fw1025.jsonl" and json.loads(l)["mode"] == "hybrid"
     and json.loads(l)["D"] == 17.0][-1]
b = [json.loads(l) for l in open(d18f) if json.loads(l)["D"] == 18.0 and json.loads(l)["mode"] == "hybrid"][-1]
assert a["lam"] and b["lam"], "a root is missing"
s = (b["lam"] - a["lam"]) / (18.0 - 17.0); g = b["lam"] + s * (Dt - 18.0)
print(f"D 17 hybrid root (k_c 63, {a['record']}): {a['lam']!r}; D 18 hybrid root: {b['lam']!r}")
print(f"slope over D 17-18: {s!r}; guess at D {Dt:g}: {g!r}")
for w in (0.02, 0.06, 0.15, 0.35):
    print(f"  window {w}: grid {g * (1 - w):.7f}, {g:.7f}, {g * (1 + w):.7f}")
rec = [json.loads(l) for l in open(leapf) if json.loads(l).get("D") == Dt][-1]
assert "lam" not in rec, "the leap record already has a lambda"
rec.update(lam_guess=g, lam=g, lam_is_guess=True, stub_note=f"the Mac's leap record at D {Dt:g} ({leapf.split('/')[-1]}) with lam_guess "
           f"on the line through the D 17 and D 18 hybrid roots at k_c 63; lam is the guess, so minus_record is root minus guess")
open(out, "w").write(json.dumps(rec) + "\n")
print(f"stub {out}: D {rec['D']} k_c {rec['kc']} kappa {rec['kappa']} u0 {rec['u0']} Ks {rec['Ks']} F {rec['F']!r} steps {rec['steps']}")
