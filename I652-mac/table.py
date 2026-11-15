# the D chain at eta = 1 from the records (the last record of each tag), against SIGMA_DSS.md section 5's sigdss k_c 15
import json, sys, os
S = os.path.dirname(os.path.abspath(__file__))
REF = {4: 0.462226, 5: 0.805845, 5.5: 0.890368, 6: 0.944491, 7: 1.001249, 8: 1.022509, 9: 1.026904, 10: 1.026142}
recs = {}
for l in open(os.path.join(S, "out", "sm_records.jsonl")):
    r = json.loads(l)
    recs[r["tag"]] = r
rows = []
for t, r in recs.items():
    if t == "eta1_M32" or (t.startswith("eta1_D") and t.endswith("_M32")) or t.startswith("start"):
        D = float(r["D"])
        piv = min(float(x.split("pivots ")[1].split("..")[0]) for x in [str(h) for h in r["newton"]] if "pivots" in x) if any("pivots" in str(h) for h in r["newton"]) else None
        rows.append((D, t, r))
print("| D | tag | converged | Delta | max abs F | constraint | Newton steps | sigdss (SIGMA_DSS 5) | difference |")
print("|---|---|---|---|---|---|---|---|---|")
for D, t, r in sorted(rows, key=lambda x: (x[0], x[1])):
    ref = REF.get(D)
    dl = float(r["Delta_hi"]) + float(r["Delta_lo"])
    print("| %g | %s | %s | %s | %.1e | %.1e | %d | %s | %s |" % (D, t, r["converged"], r["Delta"][:22], float(r["F"]),
          float(r["constraint"]), len(r["newton"]), "%.6f" % ref if ref else "", "%+.1e" % (dl - ref) if ref else ""))
