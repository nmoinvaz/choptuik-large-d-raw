#!/usr/bin/env python3
"""table973.py: the table of every base polish from ks_chain2's D 237.7132 state (ks 291): #971's ks 293, 295, 299 (I971-dh610), #966's ks 304
(its numbers as quoted in #971, comment 6991847118) and #973's ks 297, 301, 303, 307 and the ks 293 rerun, read from their anm_run logs and exits
files. Prints markdown, written to table973.md. Usage: table973.py [RAWDIR]"""
import os
import re
import sys

raw = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def exits(folder, fname):
    out = {}
    p = os.path.join(raw, folder, fname)
    if os.path.exists(p):
        for line in open(p):
            m = re.match(r"\d+ (\S+) exit (\d+) wall (\d+) s", line)
            if m:
                out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out


def row(ks, log, ex, label=None):
    text = open(log, errors="replace").read()
    c0 = re.search(r"on 0 chord 0: max\|F\| (\S+), \|dw\| (\S+)", text)
    c1 = re.search(r"on 0 chord 1: max\|F\| (\S+), \|dw\| (\S+)", text)
    th = re.search(r"theta at its point (\S+) \(bound [0-9.]+\): (accepted|refused)", text)
    nw = re.findall(r"octo-double Newton: (\d+) steps, max\|F\| (\S+), (NOT converged|converged)", text)
    lad = re.search(r"ladder FAILED after (\d+) rungs.*?\|R\| ([0-9.e+]+) -> ([0-9.e+]+)", text)
    code, wall = ex if ex else (None, None)
    if nw and nw[-1][2] == "converged":
        outcome, steps, fin = "converged", nw[-1][0], nw[-1][1]
    else:
        outcome = "capped at 3600 s" if code == 124 else ("failed" if code is not None else "running")
        steps, fin = "none", (f"ladder FAILED after {lad.group(1)} rungs, |R| {lad.group(2)} to {lad.group(3)}" if lad else "none")
    return (label or str(ks), "%d" % (ks % 4), c0.group(1) if c0 else "n/a", c0.group(2) if c0 else "n/a",
            f"{c1.group(1)}, {c1.group(2)}" if c1 else "not formed", f"{th.group(1)}, {th.group(2)}" if th else "n/a", outcome, steps, fin,
            f"{wall} s" if wall else "n/a")


e971, e973 = exits("I971-dh610", "exits_971.txt"), exits("I973-dh610", "exits_973.txt")
rows = [("291", "3", "the state itself, ks_chain2's leg 0 base (its own polish at D 232 was +11 from ks 280: first chord 2.05e-42, 4 steps)",
         "", "", "", "", "", "", "")]
rows = []
rows.append(("291 (+0)", "3", "n/a (the state)", "n/a", "n/a", "n/a", "state of ks_chain2 leg 0", "n/a", "n/a", "n/a"))
for k in (293, 295):
    rows.append(row(k, os.path.join(raw, "I971-dh610", f"ks{k}.log"), e971.get(f"ks{k}"), f"{k} (+{k - 291}) #971"))
for k in (297,):
    p = os.path.join(raw, "I973-dh610", f"ks{k}.log")
    rows.append(row(k, p, e973.get(f"ks{k}"), f"{k} (+{k - 291})") if os.path.exists(p) else (f"{k}", "1", "n/a", "n/a", "n/a", "n/a", "not run", "", "", ""))
rows.append(row(299, os.path.join(raw, "I971-dh610", "ks299.log"), e971.get("ks299"), "299 (+8) #971"))
for k in (301, 303, 307):
    p = os.path.join(raw, "I973-dh610", f"ks{k}.log")
    rows.append(row(k, p, e973.get(f"ks{k}"), f"{k} (+{k - 291})") if os.path.exists(p) else (f"{k}", str(k % 4), "n/a", "n/a", "n/a", "n/a", "not run", "", "", ""))
rows.append(("304 (+13) #966", "0", "5.1e-06", "n/a", "1.9e+33", "inf, refused", "failed", "none", "ladder FAILED, |R| 2.9e12 (as quoted in #971)", "n/a"))
p = os.path.join(raw, "I973-dh610", "ks293_rerun.log")
if os.path.exists(p):
    rows.append(row(293, p, e973.get("ks293_rerun"), "293 (+2) rerun alone"))
rows.sort(key=lambda r: int(r[0].split()[0]))
head = ("| ks (jump) | ks mod 4 | first chord max\\|F\\| | \\|dw\\| | chord 1 max\\|F\\|, \\|dw\\| | theta of the first step | outcome | steps | polished max\\|F\\| or failure | wall |\n"
        "|---|---|---|---|---|---|---|---|---|---|")
md = head + "\n" + "\n".join("| " + " | ".join(str(x).replace("|", "\\|") for x in r) + " |" for r in rows)
print(md)
open(os.path.join(raw, "I973-dh610", "table973.md"), "w").write(md + "\n")
