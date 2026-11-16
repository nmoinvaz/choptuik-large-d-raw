#!/usr/bin/env python3
"""#608's closing numbers from the nine chain logs, read only.

    python3 -I summary608.py RAWDIR      (RAWDIR is I608-dh610's folder)

For each log (chain_*, restart_*, restart2_*, restart3_*, restart4_*) the accepted steps are the attempts whose end line
"a X -> D Y: ... od N steps -> ..., S s" is followed by "Delta of the saved state, its eight parts summed exactly: Z"; the
attempt's final max|F| is that of the "octo-double Newton: N steps, max|F| M, converged" line just before. The other
attempts are counted by how they ended (the 20-step limit not converged, the abort, "no trial step accepted", a failed
re-seed). Writes deltas_608.csv (stage, chain, D, a, od steps, seconds, max|F|, Delta) and prints the markdown tables:
per stage, the totals, the criterion "each accepted step converges to max|F| <= 1e-60", and Delta(d6) - Delta(d10) at every
D (to 9 digits) that both chains accepted, in exact mpmath arithmetic."""
import csv
import os
import re
import sys

from mpmath import mp, mpf

mp.dps = 60
RAW = sys.argv[1]
STAGES = [("chain", "chain_%s.log"), ("restart", "restart_%s.log"), ("restart2", "restart2_%s.log"),
          ("restart3", "restart3_%s.log"), ("restart4", "restart4_%s.log")]
NEWTON = re.compile(r"^\s+octo-double Newton: (\d+) steps, max\|F\| (\S+), (converged|not converged)")
END = re.compile(r"^\s+a (\S+) -> D (\S+): .*?od (\d+) steps.*?, (\d+) s\s*$")
DELTA = re.compile(r"^\s+Delta of the saved state, its eight parts summed exactly: (\S+)")
SEED = re.compile(r"^\s+a (\S+): re-seeded \((.*?)\)")
ABORT = re.compile(r"attempt refused at iteration (\d+)")
NOTRIAL = re.compile(r"no trial step accepted, stopping")

rows = []          # accepted steps
kinds = {}         # (stage, chain) -> dict of counts
for stage, pat in STAGES:
    for chain in ("d6", "d10"):
        path = os.path.join(RAW, pat % chain)
        if not os.path.exists(path):
            continue
        lines = open(path, errors="replace").read().splitlines()
        k = kinds.setdefault((stage, chain), dict(accepted=0, limit=0, abort=0, notrial=0, reseed=0, other=0))
        last_newton, ev = None, None
        for i, ln in enumerate(lines):
            m = NEWTON.match(ln)
            if m:
                last_newton = (int(m.group(1)), m.group(2), m.group(3))
            if ABORT.search(ln):
                ev = "abort"
            if NOTRIAL.search(ln):
                ev = "notrial"
            m = SEED.match(ln)
            if m and "FAILED" in m.group(2):
                ev = "reseed"
            m = END.match(ln)
            if not m:
                continue
            a, D, steps, secs = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            md = DELTA.match(nxt)
            if md and last_newton and last_newton[2] == "converged":
                rows.append(dict(stage=stage, chain=chain, D=D, a=a, steps=steps, secs=secs, F=last_newton[1],
                                 Delta=md.group(1)))
                k["accepted"] += 1
            elif ev == "abort":
                k["abort"] += 1
            elif ev == "notrial":
                k["notrial"] += 1
            elif ev == "reseed" or steps == 0:
                k["reseed"] += 1
            elif last_newton and last_newton[2] == "not converged":
                k["limit"] += 1
            else:
                k["other"] += 1
            last_newton, ev = None, None

with open(os.path.join(RAW, "deltas_608.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["stage", "chain", "D", "a", "od_steps", "seconds", "max_F", "Delta"])
    for r in rows:
        w.writerow([r["stage"], r["chain"], r["D"], r["a"], r["steps"], r["secs"], r["F"], r["Delta"]])

print("| stage | chain | accepted | refused at the limit | aborted | no trial accepted | failed re-seed | other |")
print("|---|---|---|---|---|---|---|---|")
tot = {}
for (stage, chain), k in kinds.items():
    print(f"| {stage} | {chain} | {k['accepted']} | {k['limit']} | {k['abort']} | {k['notrial']} | {k['reseed']} | {k['other']} |")
    t = tot.setdefault(chain, dict(accepted=0, limit=0, abort=0, notrial=0, reseed=0, other=0))
    for key in t:
        t[key] += k[key]
for chain, t in tot.items():
    print(f"| all | {chain} | {t['accepted']} | {t['limit']} | {t['abort']} | {t['notrial']} | {t['reseed']} | {t['other']} |")

print()
for chain in ("d6", "d10"):
    rs = [r for r in rows if r["chain"] == chain]
    big = max(rs, key=lambda r: float(r["F"]))
    over = [r for r in rs if float(r["F"]) > 1e-60]
    print(f"{chain}: {len(rs)} accepted steps, highest final max|F| {big['F']} ({big['stage']}, D {big['D']}), "
          f"{len(over)} above 1e-60; D {min(float(r['D']) for r in rs):.5f} to {max(float(r['D']) for r in rs):.9f}")

print()
d = {}
for r in rows:
    d.setdefault((r["chain"], round(float(r["D"]), 5)), []).append(r)
shared = sorted(set(D for c, D in d if c == "d6") & set(D for c, D in d if c == "d10"))
print(f"{len(shared)} D values accepted by both chains (rounded to 1e-5)")
print("| D | Delta(d6) - Delta(d10) | stage d6 | stage d10 |")
print("|---|---|---|---|")
for D in shared:
    a, b = d[("d6", D)][-1], d[("d10", D)][-1]
    diff = mpf(a["Delta"]) - mpf(b["Delta"])
    print(f"| {D:.5f} | {mp.nstr(diff, 8)} | {a['stage']} | {b['stage']} |")
