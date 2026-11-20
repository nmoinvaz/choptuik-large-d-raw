import json
O = "/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac/out/"
dd = [json.loads(l) for l in open(O + "ell_ddm_D17.5_1025.jsonl")]
hy = {r["lam"]: r for r in map(json.loads, open(O + "ell_ddm_hybrid_1025.jsonl"))}
d0 = {r["lam"]: r for r in dd if not r["mutate"]}; hi = {r["lam"]: r for r in dd if r["mutate"] == "hionly"}
sg = lambda s: "+" if s > 0 else "−"
print("| λ | float64 | dd M | dd, double arithmetic | hybrid | ln\\|det\\| hybrid | hybrid − dd |")
print("|---|---|---|---|---|---|---|")
for lam in sorted(set(hy) | set(d0)):
    h = hy.get(lam); d = d0.get(lam); m = hi.get(lam)
    f = sg(h["f64"][0]) if h else sg(d["f64_sign"])
    print(f"| {lam} | {f} | {sg(d['dd'][0]['sign']) if d else ''} | {sg(m['dd'][0]['sign']) if m else ''} | {sg(h['hybrid'][0])} | "
          f"{h['hybrid'][1]:.4f} | {(h['hybrid'][1] - d['dd'][0]['ln']):+.1e} |" if d else
          f"| {lam} | {f} |  |  | {sg(h['hybrid'][0])} | {h['hybrid'][1]:.4f} |  |")
print("max dd variant spread", max(max(x["ln"] for x in r["dd"]) - min(x["ln"] for x in r["dd"]) for r in d0.values()))
print("hionly ln - dd ln", {l: round(hi[l]["dd"][0]["ln"] - d0[l]["dd"][0]["ln"], 4) for l in hi})
print("f64 ln - dd ln", {l: round(d0[l]["f64_ln"] - d0[l]["dd"][0]["ln"], 3) for l in d0})
