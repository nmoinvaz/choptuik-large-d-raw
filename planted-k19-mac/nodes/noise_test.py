"""Noise test for section 11.0 item 3 under the second amendment: how far the K = 17, 18 estimates of the 960-bit node
data (scan39J1000, sigma_0..18) move when each sigma_k (k = 1..18) is perturbed by Gaussian noise of its own plateau
error, against the observed differences between the 1280-bit node data's estimates and the stored 960-bit record.
    python3 noise_test.py SCRATCH_DIR
"""
import json
import os
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/solver/inner_amp")
import planted_k14 as K14  # noqa: E402
import planted_k18 as K18  # noqa: E402
import planted_k19 as K19  # noqa: E402
import planted_plants as PP  # noqa: E402
import planted_run as R  # noqa: E402

S = sys.argv[1]
K19.configure(K19.HERE)
mp.mp.dps = PP.DPS
real = K19.load_real(K19.SCAN19, "*_p960.json")
R.OUT, R.KS = os.path.join(S, "noise_records.jsonl"), (17, 18)
R.DONE.clear()
if os.path.exists(R.OUT):
    os.remove(R.OUT)
base = {wf: list(real[wf][0][:19]) for wf in PP.NODES}
R.run_plant("N0 base", "N0", base, None, os.path.join(S, "scr"))
NS = 20
for seed in range(NS):
    rng = np.random.default_rng(1000 + seed)
    nodes = {}
    for wf in PP.NODES:
        sig = list(base[wf])
        for k in range(1, 19):
            n = rng.standard_normal(2) / np.sqrt(2)
            sig[k] = sig[k] + mp.mpf(real[wf][1][k]) * mp.mpc(n[0], n[1])
        nodes[wf] = sig
    R.run_plant(f"N0 noise seed={seed}", "N0 noise", nodes, None, os.path.join(S, "scr"))
recs = {r["name"]: r for r in (json.loads(l) for l in open(R.OUT) if l.strip())}
new19 = {r["name"]: r for r in (json.loads(l) for l in open(K19.OUT19) if l.strip())}["N0 scan41J1250"]
old = {r["name"]: r for r in (json.loads(l) for l in open(K18.OUT18) if l.strip())}["N0 scan37J1000"]
out = {}
for K in (17, 18):
    vb, vo, vn = K14.est_vector(recs["N0 base"], K), K14.est_vector(old, K), K14.est_vector(new19, K)
    d, key = K14.max_diff(vb, vo)
    print(f"K = {K}: control, the 960-bit sigma_0..18 through this harness against the stored N0 scan37J1000: largest "
          f"difference {d:.1e} ({key})")
    rows = []
    for key in vb:
        vals = [K14.est_vector(recs[f"N0 noise seed={s}"], K).get(key) for s in range(NS)]
        if vb[key] is None or any(v is None for v in vals) or vn.get(key) is None:
            rows.append((key, None, None, None))
            continue
        dev = [abs(v - vb[key]) for v in vals]
        rows.append((key, float(np.sqrt(np.mean([x * x for x in dev]))), max(dev), abs(vn[key] - vo[key])))
    rows.sort(key=lambda r: -(r[3] or 0))
    print(f"K = {K}: key, noise rms over {NS} seeds, noise max, the observed 1280-bit minus 960-bit difference, observed / rms")
    for key, sd, mx, obs in rows:
        if sd is None:
            print(f"   {key:10s} none")
        else:
            print(f"   {key:10s} rms {sd:.1e}  max {mx:.1e}  observed {obs:.1e}  ratio {obs / sd if sd else float('inf'):.2f}")
    out[str(K)] = {key: {"noise_rms": sd, "noise_max": mx, "observed": obs} for key, sd, mx, obs in rows}
json.dump(out, open(os.path.join(S, "noise_test.json"), "w"), indent=1)
print("written", os.path.join(S, "noise_test.json"))
