#!/usr/bin/env python3
"""#608: the attempts of the d6 and d10 chains from their logs, as markdown for the progress posts.

    python3 -I report_608.py RAWDIR

Every attempt of every step is read from the chain's log: the step's base, the attempt's step size a, the re-seed
verdict, each octo-double Newton iteration (max|F| before and after, the step |dz| before and after, lam), whether the
octo-double Newton converged, and whether the attempt was accepted (the log then prints the exact eight-part Delta of
the saved state). Printed per chain: the accepted steps, with the exact eight-part Delta summed in mpmath from the saved
npz (as hp/export_delta_all.py does), Delta minus #462-win's state of the same chain at the same D (the double-double
projector's rows), and the refused attempts with their Newton iterations (the first moves, as #461's tables give).
Then Delta(d6) - Delta(d10) at each D both chains have accepted. Lines that read like an error are printed, never
skipped."""
import os
import re
import sys

import numpy as np
from mpmath import mp, mpf

mp.dps = 60
RAW = sys.argv[1]
OUT = os.path.join(RAW, "I608-dh610")
PARTS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
STEP = re.compile(r"^step (\d+): D (\S+),")
ATT = re.compile(r"^    a (\S+): re-seeded \((.*?)\), (\S+) s")
ON = re.compile(r"^  on (\d+): \|F\| ([^\s,]+) -> ([^\s,]+), \|dz\| ([^\s,]+) -> ([^\s,]+), lam ([^\s,]+)")
ONC = re.compile(r"^  on (\d+): \|F\| ([^\s,]+) converged")
ONS = re.compile(r"^  on (\d+): \|F\| ([^\s,]+), \|dz\| ([^\s,]+): (.*)$")
OD = re.compile(r"^      octo-double Newton: (\d+) steps, max\|F\| (\S+), (not converged|converged)")
END = re.compile(r"^    a (\S+) -> D (\S+): predicted .*?, (\d+) s$")
SAVED = re.compile(r"^      Delta of the saved state, its eight parts summed exactly: (\S+)")
BAD = re.compile(r"Traceback|Error|FAILED|killed|cap of|Exception", re.I)


def delta(path):
    z = np.load(path)
    return sum((mpf(float(z[k][-1])) for k in PARTS if k in z.files), mpf(0))


def state(D, folder):
    p = os.path.join(RAW, folder, f"anm_pin3_D{float(D):.4f}.npz")
    return p if os.path.exists(p) else None


def attempts(chain):
    """one dict per attempt, in the order of the log"""
    out, cur, step, base, bad = [], None, None, None, []
    for line in open(os.path.join(OUT, f"chain_{chain}.log"), errors="replace"):
        line = line.rstrip("\n")
        m = STEP.match(line)
        if m:
            step, base, cur = int(m.group(1)), m.group(2), None
            continue
        if step is None:
            continue
        m = ATT.match(line)
        if m:
            cur = dict(step=step, base=base, a=m.group(1), reseed=m.group(2), on=[], stop="", od=None, conv=None,
                       accepted=False, D=None, sec=None, delta=None)
            continue
        if cur is None:
            continue
        m = ON.match(line)
        if m:
            cur["on"].append(m.groups()[1:])
        m = ONC.match(line)
        if m:
            cur["on"].append((m.group(2), "converged", "", "", ""))
        m = ONS.match(line)
        if m:
            cur["stop"] = f"on {m.group(1)}: |F| {m.group(2)}, |dz| {m.group(3)}: {m.group(4)}"
        m = OD.match(line)
        if m:
            cur["od"], cur["Fod"], cur["conv"] = int(m.group(1)), m.group(2), m.group(3) == "converged"
        m = END.match(line)
        if m:
            cur["D"], cur["sec"] = m.group(2), int(m.group(3))
            out.append(cur)
        m = SAVED.match(line)
        if m and out and out[-1] is cur:
            cur["accepted"], cur["delta"] = True, m.group(1)
        if "elim projections" not in line and BAD.search(line):
            bad.append(line.strip()[:200])
    return out, bad


def fseq(c):
    """max|F| at the start and after each Newton iteration, a repeated value once"""
    s = []
    for o in c["on"]:
        if o[1] == "converged":
            s.append(o[0])
        else:
            if not s:
                s.append(o[0])
            s.append(o[1])
    r = []
    for x in s:
        if not r or r[-1] != x:
            r.append(x)
    return " → ".join(f"{float(x):.1e}" for x in r)


def main():
    D = {}
    for chain in ("d6", "d10"):
        att, bad = attempts(chain)
        acc = [c for c in att if c["accepted"]]
        ref = [c for c in att if not c["accepted"]]
        print(f"### chain_{chain}: {len(acc)} accepted steps, {len(ref)} refused attempts\n")
        print("| D | a | refused before | od steps | max\\|F\\| after each solve | corrector s | Delta (eight parts) | minus I462 on old rows |")
        print("|---|---|---|---|---|---|---|---|")
        for i, c in enumerate(att):
            if not c["accepted"]:
                continue
            nref = sum(1 for p in att[:i] if not p["accepted"] and p["step"] == c["step"])
            p = state(c["D"], f"I608-dh610/chain_{chain}")
            o = state(c["D"], f"I462-win/chain_{chain}")
            d = delta(p) if p else None
            D.setdefault(chain, {})[c["D"]] = d
            old = mp.nstr(d - delta(o), 6) if d is not None and o else "no I462 state"
            print(f"| {c['D']} | {c['a']} | {nref} | {c['od']} | {fseq(c)} | {c['sec']} | "
                  f"{mp.nstr(d, 22) if d is not None else 'state missing'} | {old} |")
        if ref:
            print("\nrefused attempts (the octo-double Newton did not converge, so the driver halves a):\n")
            print("| step base D | a | target D | od steps | max\\|F\\| at the end | Newton iterations: \\|F\\| before → after, \\|dz\\| before → after, lam | how it ended | s |")
            print("|---|---|---|---|---|---|---|---|")
            for c in ref:
                its = "; ".join(f"{o[0]}→{o[1]}, {o[2]}→{o[3]}, lam {o[4]}" for o in c["on"] if o[1] != "converged")
                print(f"| {c['base']} | {c['a']} | {c['D']} | {c['od']} | {c.get('Fod', '?')} | {its} | {c['stop'] or 'not converged'} | {c['sec']} |")
        print(f"\nlines that read like an error: {len(bad)}")
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
