#!/usr/bin/env python3
"""#813: ln|det| of kf 41's control circle at D 61.0264, M 48, at each point, on three runs: macm3's own (#749,
I749-macm3/kf41/control), win2's own (#749, I749-win2/kf41, the control's points among its five circles), and win2 on
macm3's saved state (I813-win2/control). Points are matched by (re, im) to 1e-12.

    python3 -I compare813.py RAW [--mutate=shift]

Bar, fixed before the run (#813): win2 on macm3's state equals macm3's own to 1e-9 absolute in ln|det| at every matched
point, so the evaluation agrees across the machines and #749's difference lies in the states. Otherwise the evaluation
differs, and the size and the points are reported. Exit 0 when the bar holds, 1 when it does not, 2 when a file is
missing or fewer than 20 points match. --mutate=shift adds 1e-8 to every ln|det| of the new run, and the bar must fail.
"""
import json
import os
import sys

R = sys.argv[1]
F = "modecount_D61.0264_M48_kf41_ball320_evals.jsonl"
paths = {"macm3": f"{R}/I749-macm3/kf41/control/data/{F}", "win2": f"{R}/I749-win2/kf41/data/{F}",
         "new": f"{R}/I813-win2/control/data/{F}"}
try:
    runs = {k: [json.loads(l) for l in open(p) if l.strip()] for k, p in paths.items()}
except OSError as e:
    print(e)
    sys.exit(2)
if "--mutate=shift" in sys.argv:
    print("MUTATION shift: 1e-8 added to the new run's ln|det|; the bar must fail")
    for r in runs["new"]:
        r["lnabs"] += 1e-8
def find(rs, p):
    return next((r for r in rs if abs(r["re"] - p["re"]) <= 1e-12 and abs(r["im"] - p["im"]) <= 1e-12), None)
rows = []
for p in runs["macm3"]:
    w, n = find(runs["win2"], p), find(runs["new"], p)
    rows.append((p, w, n))
m_new = [abs(n["lnabs"] - p["lnabs"]) for p, w, n in rows if n]
m_w2 = [abs(w["lnabs"] - p["lnabs"]) for p, w, n in rows if w]
m_nw = [abs(n["lnabs"] - w["lnabs"]) for p, w, n in rows if n and w]
print(f"points: macm3 {len(runs['macm3'])}, matched in win2's own {len(m_w2)}, in the new run {len(m_new)}")
print(f"max |ln|det| difference|: new - macm3 {max(m_new, default=float('nan')):.3e}; win2's own - macm3 "
      f"{max(m_w2, default=float('nan')):.3e}; new - win2's own {max(m_nw, default=float('nan')):.3e}")
for p, w, n in rows:
    print(f"  {p['re']:+.6f} {p['im']:+.6f}: macm3 {p['lnabs']:.10f}  new-macm3 "
          + (f"{n['lnabs'] - p['lnabs']:+.2e}" if n else "  -     ") + "  win2-macm3 "
          + (f"{w['lnabs'] - p['lnabs']:+.2e}" if w else "  -"))
if len(m_new) < 20:
    print("fewer than 20 points matched")
    sys.exit(2)
ok = max(m_new) <= 1e-9
print("bar (new - macm3 <= 1e-9 at every point):", "HOLDS: the evaluation agrees, the states differ" if ok else
      "FAILS: the evaluation differs between the machines")
sys.exit(0 if ok else 1)
