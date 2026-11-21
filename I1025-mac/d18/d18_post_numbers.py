"""#1025 D 18 (A), the numbers of the post, information only: the gap of the two roots, the estimate's error on the
bisected root, and the slopes per unit D from the k_c 63 hybrid roots at D 17 and 17.5 to each D 18 root.
usage: d18_post_numbers.py SCAN.jsonl ROOT.jsonl P4_MAC.jsonl P4HI_WIN.jsonl U0TEST.jsonl"""
import sys, json
import numpy as np

scan, rootf, p4m, p4w, u0f = sys.argv[1:6]
S = sorted((json.loads(l) for l in open(scan)), key=lambda r: r["lam"])
ref = max(r["ln"] for r in S)
est = []
for a, b in zip(S, S[1:]):
    if a["sign"] != b["sign"]:
        fa, fb = a["sign"] * np.exp(a["ln"] - ref), b["sign"] * np.exp(b["ln"] - ref)
        est.append(a["lam"] + (b["lam"] - a["lam"]) * fa / (fa - fb))
ra = json.loads(open(rootf).readlines()[-1])["lam"]
print(f"estimates {[round(e, 6) for e in est]}; lower estimate - bisected root {est[0] - ra:+.2e}; "
      f"upper estimate - bisected lower root {est[1] - ra:+.4f}")
l17 = [json.loads(l)["lam"] for l in open(p4m) if json.loads(l)["D"] == 17.0 and json.loads(l)["kc"] == 63][0]
l175 = [json.loads(l)["lam"] for l in open(p4w) if json.loads(l)["D"] == 17.5 and json.loads(l)["kc"] == 63][0]
u55 = [json.loads(l) for l in open(u0f)]
u55 = [r["lam"] for r in u55 if r["D"] == 17.5 and r["kc"] == 55 and r["u0"] == 0.04 and r["mode"] == "hybrid"][0]
print(f"D 17 k_c 63 {l17:.10f}; D 17.5 k_c 63 (winb row A) {l175:.10f}; D 17.5 k_c 55 hybrid (u0test) {u55:.10f}; "
      f"k_c 63 - k_c 55 at D 17.5 {l175 - u55:+.3e}")
print(f"slope D 17-17.5 (k_c 63) {(l175 - l17) / 0.5:+.4f}; D 17.5-18: to the bisected lower root {(ra - l175) / 0.5:+.4f}, "
      f"to the upper estimate {(est[1] - l175) / 0.5:+.4f}")
