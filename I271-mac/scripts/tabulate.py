#!/usr/bin/env python3
"""I271-mac's table: the rerun M 48 records (gamma_dd.jsonl, series_truncation.jsonl) against #266's quad-double
references (I266-mac) and the old records of the main repository's hp/data/local/gamma_dd.jsonl, with the README's
criteria. Run in this folder:

    python3 scripts/tabulate.py MAIN_REPO > table.txt
"""
import json
import os
import sys

import mpmath as mp

mp.mp.dps = 40
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.dirname(HERE)
main_repo = sys.argv[1]


def jl(path):
    return [json.loads(l) for l in open(path) if l.strip()] if os.path.exists(path) else []


qd = {(r["state"], r["M"]): r for r in jl(os.path.join(RAW, "I266-mac", "states", "qd.jsonl"))}
lamq = {r["state"]: r for r in jl(os.path.join(RAW, "I266-mac", "lam.jsonl"))}
# the quad-double M 48 solutions of #266: Delta from qd.jsonl, lam from lam.jsonl's lam_fine on the same file
REF = {"up8_D50.0075.npz": dict(Delta=qd[("up8_D50.0075_M48_r2.npz", 48)]["Delta_qd"],
                                lam=lamq["up8_D50.0075_M48_r2_qd.npz"]["lam_fine"]["str"], lam_res=1e-14),
       "up12_D58.0060.npz": dict(Delta=qd[("up12_D58.0060_M48_r2.npz", 48)]["Delta_qd"],
                                 lam=lamq["up12_D58.0060_M48_r2_qd.npz"]["lam_fine"]["str"], lam_res=5e-13)}
old = {r["state"]: r for r in jl(os.path.join(main_repo, "hp", "data", "local", "gamma_dd.jsonl")) if "M48" in r}
new = jl(os.path.join(HERE, "gamma_dd.jsonl"))
exits = open(os.path.join(HERE, "logs", "exits.txt")).read().splitlines() if os.path.exists(
    os.path.join(HERE, "logs", "exits.txt")) else []


def dd(h, l):
    return mp.mpf(h) + mp.mpf(l)


print("gamma_dd.py --M48 records (I271-mac/gamma_dd.jsonl)\n")
print(f"{'state':20s} {'mutate':9s} {'|F| 48':>8s} {'stop':6s} {'est':>10s} {'floor':6s} {'Delta(48)-Delta(32)':>20s} "
      f"{'old':>10s} {'lam(48)-lam(32)':>16s} {'old':>10s} {'lam32 = old':12s} {'tails start c/h':>17s} "
      f"{'tails sol c/h':>17s}")
for r in new:
    h = r["M48"]
    o = old.get(r["state"], {})
    ts = h.get("tails_start", [])
    t = h.get("tails", [])
    print(f"{r['state']:20s} {h.get('mutate', ''):9s} {h.get('F', float('nan')):8.1e} {h.get('solve', {}).get('stop', '-'):6s} "
          f"{h.get('est', float('nan')):+10.2e} {h.get('floor', '-'):6s} {h.get('Delta_diff', float('nan')):+20.3e} "
          f"{o.get('M48', {}).get('Delta_diff', float('nan')):+10.2e} "
          f"{(h['lam_diff'] if h.get('lam_diff') is not None else float('nan')):+16.2e} "
          f"{(o.get('M48', {}).get('lam_diff') or 0.0):+10.2e} {str(r['lam'] == o.get('lam')) if o else '-':12s} "
          + (" ".join(f"{x['tail']:.0e}" for x in ts) if ts else "-").rjust(17) + " "
          + (" ".join(f"{x['tail']:.0e}" for x in t) if t else "-").rjust(17)
          + (f"  REFUSED: {h['refused']}" if "refused" in h else ""))

print("\nagainst #266's quad-double M 48 solutions (I266-mac)\n")
print(f"{'state':20s} {'mutate':9s} {'Delta(48) - Delta_qd(48)':>25s} {'lam(48) - lam_qd(48)':>21s} {'lam res':>8s}  verdict")
verdicts = []
for r in new:
    ref = REF.get(r["state"])
    h = r["M48"]
    if not ref or "Delta" not in h:
        continue
    dD = dd(h["Delta"], h["Delta_lo"]) - mp.mpf(ref["Delta"])
    dl = (mp.mpf(h["lam"]) - mp.mpf(ref["lam"])) if h.get("lam") else None
    if h.get("mutate") == "old_rule":
        ok = abs(h["Delta_diff"] / 1.2e-11 - 1) <= 0.05 and h["floor"] == "ABOVE"
        v = ("(b) control fires: Delta_diff reproduces 1.2e-11 and the floor check fails" if ok
             else "(b) CONTROL DID NOT FIRE")
    else:
        floor = h["floor"] == "ok"
        lam_ok = dl is not None and abs(dl) <= ref["lam_res"]
        if abs(dD) <= 1e-20:
            dv = "Delta within 1e-20"
        elif abs(dD) <= 1e-18:
            dv = "Delta at the double-double floor (1e-20 < |d| <= 1e-18), not within 1e-20"
        else:
            dv = "Delta FAILS (> 1e-18)"
        v = (f"floor {'ok' if floor else 'FAILS'}; {dv}; lam {'within' if lam_ok else 'NOT within'} "
             f"{ref['lam_res']:.0e}")
    verdicts.append(v)
    print(f"{r['state']:20s} {h.get('mutate', ''):9s} {mp.nstr(dD, 3):>25s} "
          f"{(mp.nstr(dl, 3) if dl is not None else '-'):>21s} {ref['lam_res']:8.0e}  {v}")

st = jl(os.path.join(HERE, "series_truncation.jsonl"))
if st:
    print("\nseries_truncation.py --Mhi=48 records (I271-mac/series_truncation.jsonl)\n")
    for r in st:
        h = r.get("Mhi", {})
        tails = " ".join("%.0e" % x["tail"] for x in h.get("tails", []))
        ok = abs(h.get("Delta_diff", 1)) <= 1e-18 and h.get("floor") == "ok"
        print(f"{os.path.basename(r['state']):20s} |F| {h.get('F', float('nan')):.1e} solve: {h.get('solve')}; "
              f"Delta_diff {h.get('Delta_diff', float('nan')):+.3e}; floor {h.get('floor')}; tails {tails}  "
              f"(d) {'passes' if ok else 'FAILS'}")

print("\nexits (logs/exits.txt)\n")
for e in exits:
    print("  " + e.split(": ", 1)[0])
