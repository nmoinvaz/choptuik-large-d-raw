#!/usr/bin/env python3
"""#640: the 12 releases (releases/release_D<D>_kf<K>.jsonl) against delta_all.csv's fits error of the same D. Usage: python3 table640.py [delta_all.csv]"""
import csv, json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
csvp = sys.argv[1] if len(sys.argv) > 1 else "/Users/nathan/Source/choptuik-large-d-b640/hp/data/delta_all.csv"
fits = {}
for r in csv.DictReader(open(csvp)):
    try:
        d = float(r["D"])
    except ValueError:
        continue
    if d in (80.0, 100.0, 150.0, 200.0) and r["kind"] == "chain_fit":
        fits[d] = (r["err"], r["err_kind"])
print("| D | K (kfreeze) | converged | steps | |F| at the start | |F| at the end | Δ_released − Δ_held | fits err (delta_all.csv) | last Newton step |dz| (rejected) | seconds |")
print("|---|---|---|---|---|---|---|---|---|---|")
for D in (80, 100, 150, 200):
    for K in (13, 9, 7):
        f = os.path.join(here, "releases", f"release_D{D}_kf{K}.jsonl")
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            print(f"| {D} | {K} | not finished | | | | | {fits.get(float(D), ('?', ''))[0]} | | |"); continue
        r = json.loads(open(f).readlines()[-1])
        lg = open(os.path.join(here, "releases", f"release_D{D}_kf{K}.log")).read()
        m = re.findall(r"qn \d+: \|F\| \S+, \|dz\| (\S+): no trial step accepted", lg)
        dz = m[-1] if m else "(iteration limit)"
        word = "yes" if r["ok"] else ("stalled" if r["stalled"] else "no (iteration limit)")
        meas = f"{r['diff']:+.3e}" if r["ok"] else f"({r['diff']:+.3e}, not a measurement: not converged)"
        e = fits.get(float(D), ("?", ""))
        print(f"| {D} | {K} | {word} | {r['steps']} | {r['F_start']:.2e} | {r['F']:.2e} | {meas} | {e[0]} ({e[1]}) | {dz} | {r['seconds']:.0f} |")
