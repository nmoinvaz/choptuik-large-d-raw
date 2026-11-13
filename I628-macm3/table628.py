#!/usr/bin/env python3
"""#628: gamma(3.5) in the lowDhm and lowDvh families at M 96 and M 128 (lowD_gamma_D3.5_{hm,vh}_M{96,128}.jsonl), the stored lowDvh M 96 value of
hp/data/lowD_gamma_local.jsonl, and the differences. Usage: python3 table628.py [path of lowD_gamma_local.jsonl]"""
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
stored_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/nathan/Source/choptuik-large-d-b640/hp/data/lowD_gamma_local.jsonl"
stored = next(json.loads(l) for l in open(stored_path) if '"lowDvh_D3.5000_M96.npz"' in l)
R = {(f, M): json.loads(open(os.path.join(here, f"lowD_gamma_D3.5_{f}_M{M}.jsonl")).readline()) for f in ("hm", "vh") for M in (96, 128)}
for r in R.values(): assert r["n_signchanges"] == 1
print("| family, M | state | λ | γ | F after the polish | determinants | seconds (threads) |")
print("|---|---|---|---|---|---|---|")
for (f, M), r in sorted(R.items(), key=lambda kv: (kv[0][1], kv[0][0])):
    print(f"| low{'Dhm' if f == 'hm' else 'Dvh'}, {M} | `{r['state']}` | {r['lam']!r} | {r['gamma']!r} | {r['F']:.3e} | {r['n_det']} | {r['seconds']:.0f} (3) |")
print(f"| lowDvh, 96, stored (dh370, lam_guess {stored['lam_guess']!r}) | `{stored['state']}` | {stored['lam']!r} | {stored['gamma']!r} | {stored['F']:.3e} | {stored['n_det']} | {stored['seconds']:.0f} (6) |")
g = lambda f, M: R[(f, M)]["gamma"]
l = lambda f, M: R[(f, M)]["lam"]
print()
print("| difference | γ | λ |")
print("|---|---|---|")
rows = [("γ(hm 128) − γ(hm 96)", g("hm", 128) - g("hm", 96), l("hm", 128) - l("hm", 96)),
        ("γ(vh 128) − γ(vh 96)", g("vh", 128) - g("vh", 96), l("vh", 128) - l("vh", 96)),
        ("vh 96 − hm 96", g("vh", 96) - g("hm", 96), l("vh", 96) - l("hm", 96)),
        ("vh 128 − hm 128", g("vh", 128) - g("hm", 128), l("vh", 128) - l("hm", 128)),
        ("vh 96 (this run) − stored vh 96", g("vh", 96) - stored["gamma"], l("vh", 96) - stored["lam"]),
        ("hm 96 − stored vh 96", g("hm", 96) - stored["gamma"], l("hm", 96) - stored["lam"])]
for lab, dg, dl in rows: print(f"| {lab} | {dg:+.3e} | {dl:+.3e} |")
print()
print(f"vh 96 and hm 96 identical in λ and γ: {R[('vh', 96)]['lam'] == R[('hm', 96)]['lam'] and R[('vh', 96)]['gamma'] == R[('hm', 96)]['gamma']}")
print(f"Ecker et al. 0.32239 − γ(hm 128) = {0.32239 - g('hm', 128):+.3e}; − γ(vh 128) = {0.32239 - g('vh', 128):+.3e}")
