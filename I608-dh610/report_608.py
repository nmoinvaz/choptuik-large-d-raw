#!/usr/bin/env python3
"""#608: the accepted steps of the d6 and d10 chains from their logs, as markdown for the progress posts.

    python3 -I report_608.py RAWDIR

Per chain and accepted step: D, step size a, attempts (re-seed lines of the step), octo-double Newton steps, the max|F|
after each of them, seconds of the corrector, and the exact eight-part Delta of the saved state (summed in mpmath from
the npz, as hp/export_delta_all.py does). Then Delta(new chain) - Delta(I462-win's chain at the same D, on the
double-double projector's rows) and Delta(d6) - Delta(d10) at each D both chains have reached. Lines that read like a
refusal or an error are counted and printed, never skipped."""
import glob
import os
import re
import sys

import numpy as np
from mpmath import mp, mpf

mp.dps = 60
RAW = sys.argv[1]
OUT = os.path.join(RAW, "I608-dh610")
PARTS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
ACC = re.compile(r"^    a (\S+) -> D (\S+): predicted .*? od (\d+) steps .*?, (\d+) s$")
ON = re.compile(r"^  on (\d+): \|F\| ([^\s,]+) -> ([^\s,]+)")
ONC = re.compile(r"^  on (\d+): \|F\| ([^\s,]+) converged")
ATT = re.compile(r"^    a (\S+): re-seeded")
BAD = re.compile(r"refus|halv|not converged|Traceback|Error|FAILED|killed|cap of", re.I)


def delta(path):
    z = np.load(path)
    return sum((mpf(float(z[k][-1])) for k in PARTS if k in z.files), mpf(0))


def state(chain, D, folder):
    # states are named by D to four decimals, as anm_run.py writes them
    p = os.path.join(RAW, folder, f"anm_pin3_D{float(D):.4f}.npz")
    return p if os.path.exists(p) else None


def steps(chain):
    rows, cur, bad = [], None, []
    for line in open(os.path.join(OUT, f"chain_{chain}.log"), errors="replace"):
        line = line.rstrip("\n")
        if line.startswith("step "):
            cur = dict(F=[], att=0)
        if cur is None:
            continue
        m = ATT.match(line)
        if m:
            cur["att"] += 1
        m = ON.match(line)
        if m:
            if not cur["F"]:
                cur["F"].append(m.group(2))
            cur["F"].append(m.group(3))
        m = ONC.match(line)
        if m and (not cur["F"] or cur["F"][-1] != m.group(2)):
            cur["F"].append(m.group(2))
        m = ACC.match(line)
        if m:
            cur.update(a=m.group(1), D=m.group(2), od=int(m.group(3)), sec=int(m.group(4)))
            rows.append(cur)
            cur = None
        elif "elim projections" not in line and BAD.search(line):
            bad.append(line.strip()[:200])
    return rows, bad


def fmt(x):
    return f"{float(x):.1e}"


def main():
    D = {}
    for chain in ("d6", "d10"):
        rows, bad = steps(chain)
        print(f"### chain_{chain}: {len(rows)} accepted steps\n")
        print("| D | a | attempts | od steps | max\\|F\\| after each solve | corrector s | Delta (eight parts) | minus I462 on old rows |")
        print("|---|---|---|---|---|---|---|---|")
        for r in rows:
            p = state(chain, r["D"], f"I608-dh610/chain_{chain}")
            o = state(chain, r["D"], f"I462-win/chain_{chain}")
            d = delta(p) if p else None
            D.setdefault(chain, {})[r["D"]] = d
            old = (mp.nstr(d - delta(o), 6) if d is not None and o else "no I462 state")
            fs = " → ".join(f"{float(x):.1e}" for x in r["F"])
            print(f"| {r['D']} | {r['a']} | {r['att']} | {r['od']} | {fs} | {r['sec']} | "
                  f"{mp.nstr(d, 22) if d is not None else 'state missing'} | {old} |")
        print(f"\nlines that read like a refusal or an error: {len(bad)}")
        for b in bad[:10]:
            print(f"- `{b}`")
        print()
    both = [d for d in D.get("d6", {}) if d in D.get("d10", {}) and D["d6"][d] is not None and D["d10"][d] is not None]
    if both:
        print("### the fits' spread, Delta(d6) - Delta(d10)\n")
        print("| D | Delta(d6) - Delta(d10) |")
        print("|---|---|")
        for d in both:
            print(f"| {d} | {mp.nstr(D['d6'][d] - D['d10'][d], 8)} |")


if __name__ == "__main__":
    main()
