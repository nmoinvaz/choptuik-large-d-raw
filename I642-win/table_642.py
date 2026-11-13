#!/usr/bin/env python3
"""#642: the table of release.jsonl: per D whether the full release converged, the start's and the end's |F|, the Newton steps, Delta_released - Delta_held, and how far p1's held harmonics moved.
usage: python table_642.py          (from this folder; reads release.jsonl)
Converged = max|F| <= 1e-50, or the accepted stall max|F| <= 1e-44 (the record's `ok`); the last D that converges and the first that does not are named. Delta_released - Delta_held is the record's `diff`
(Delta_full - Delta_start, summed from the four parts in mpmath); the coefficient columns are max |coeffs_end - coeffs_start| over harmonics 5, 7, 9, 11, 13 (cos, sin) and the harmonic that moves most."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
recs = [json.loads(ln) for ln in open(os.path.join(HERE, "release.jsonl")) if ln.strip()]
recs.sort(key=lambda r: r["D"])
print("| D | converged | max abs F at start | max abs F at end | Newton steps | seconds | Delta_released - Delta_held | max change of held coefficients | harmonic |\n|---|---|---|---|---|---|---|---|---|")
last_ok, first_bad = None, None
for r in recs:
    ch = [(max(abs(e[0] - s[0]), abs(e[1] - s[1])), k) for s, e, k in zip(r["coeffs_start"], r["coeffs_end"], r["held_ks"])]
    mx, k = max(ch)
    if r["ok"]:
        last_ok = r["D"]
    elif first_bad is None:
        first_bad = r["D"]
    stop = "" if r["ok"] else " (stopped, no trial step accepted)" if r["stalled"] is False and not r["converged"] else ""
    how = "yes" if r["converged"] else ("accepted stall" if r["ok"] else "no" + stop)
    dd = f"{r['diff']:+.3e}" if r["ok"] else f"not a value (stalled iterate {r['diff']:+.3e})"
    cc = f"{mx:.2e}" if r["ok"] else f"(stalled iterate {mx:.2e})"
    print(f"| {r['D']:.0f} | {how} | {r['F_start']:.2e} | {r['F']:.2e} | {r['steps']} | {r['seconds']} | {dd} | {cc} | {k} |")
print(f"\nlast D that converges: {last_ok}; first D that does not: {first_bad}")
