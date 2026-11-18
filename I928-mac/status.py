# #928: the hand-over points of one coupling from the records, for the posts (every number quoted is computed here)
import json, sys
J = sys.argv[1]; eta = sys.argv[2]
rows = []
for l in open(J + "/sm_records.jsonl"):
    r = json.loads(l)
    q = r.get("qd")
    if not q or "qdcheck" in r["tag"] or "handover_F" not in q or str(r["eta"]) != eta or q.get("first_rise", 1.0) == 1.0:
        continue
    st = q["steps"]
    seq = [st[0]["F"]] + [s["F_next"] for s in st if s.get("F_next") is not None]
    rows.append((float(r["D"]), r["M"], q["handover_F"], r["converged"], q["accepted"], seq, [s["dz"] for s in st if s.get("dz") is not None], q["F_final"], r["t"], {k for k, v in q["basin"].items() if not v}))
for D, M, hf, conv, acc, seq, dz, Ff, t, bad in rows:
    print(f"D {D:<8} M {M} hand-over {hf:.2e} (dd conv {conv}) accepted {acc} ratio1 {seq[1] / seq[0]:.3g} final {Ff:.1e} steps {len(seq) - 1} t {t:.0f} s {bad or ''}")
a = [x for x in rows if x[4] and x[1] == 32]
if a:
    print(f"accepted at M 32: {len(a)} points, D {min(x[0] for x in a)} to {max(x[0] for x in a)}; hand-over {min(x[2] for x in a):.2e} to {max(x[2] for x in a):.2e}; "
          f"stall hand-overs (dd not converged) at {[x[0] for x in a if not x[3]]}; largest first-step ratio {max(x[5][1] / x[5][0] for x in a):.3g} at D {max(a, key=lambda x: x[5][1] / x[5][0])[0]}; "
          f"largest final max|F| {max(x[7] for x in a):.2e}")
lam = {}
for l in open(J + "/sm_lam.jsonl"):
    r = json.loads(l)
    if r.get("lam") and r["M"] == 32 and str(r["eta"]) == eta and r["D"] > 11: lam[float(r["D"])] = (r["lam"], r["gauge_diff"])
g = [d for d in sorted(lam) if abs(d / 0.0625 - round(d / 0.0625)) < 1e-9]
d1 = [(lam[b][0] - lam[a][0]) / 0.0625 for a, b in zip(g, g[1:])]
print(f"rates past D 11: {len(lam)} ({len(g)} on the grid); last D {max(lam)}; grid last {g[-1]} lam {lam[g[-1]][0]:.9f} gamma {1 / lam[g[-1]][0]:.6f}; worst gauge {max(v[1] for v in lam.values()):.1e}")
print("  last first differences:", " ".join("%+.5f" % x for x in d1[-4:]), "| last second:", " ".join("%+.4f" % ((q - p) / 0.0625) for p, q in zip(d1[-4:], d1[-3:])))
