#!/usr/bin/env python3
"""#949 (coordinator's question, hc 2026-11-18 about 21:00 UTC): does sigma_pair's drop start where win2b's re-seed failures start, from D 236.7?
Reads track949.csv (sigma_pair and its interval slope per state) and win2b's I903-win2/refused903.txt (every attempt from base D 236.7: its
base D, step factor a, target D, accepted or refused, and the quad-double polish's R of the u 0.3 rung), and prints one table per chain section.
    python pair_reseed949.py [FOLDER] [refused903.txt]      (default: this folder; the file from the raw repository's origin/main)
sigma_pair's interval slope is -d ln sigma_pair / dD over the interval ending at the base (positive where the pair falls): a reading, never a trigger."""
import csv
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def read_refused(path):
    text = open(path).read() if path else subprocess.run(
        ["git", "-C", os.path.expanduser("~/Source/choptuik-large-d-raw-push"), "show", "origin/main:I903-win2/refused903.txt"],
        capture_output=True, text=True, check=True).stdout
    out, sec, cur = [], None, None
    for line in text.splitlines():
        m = re.match(r"===== (ks\d+) (\S+) \((failed|successful) re-seeds", line)
        if m:
            sec = (m.group(1), m.group(2), m.group(3))
            continue
        m = re.match(r"base D ([\d.]+) p_min ([\d.e+-]+) \| a ([\d.]+) -> D ([\d.]+) \| accepted (True|False)(.*)", line)
        if m and sec:
            cur = dict(sec=sec, base=float(m.group(1)), pmin=float(m.group(2)), a=float(m.group(3)), target=float(m.group(4)),
                       ok=m.group(5) == "True", R=None)
            pm = re.search(r"pre-polish u0\.3: (\d+) its R ([\d.e+-]+)", m.group(6))
            if pm:
                cur["R"] = float(pm.group(2))
            out.append(cur)
            continue
        m = re.match(r"\s+u0\.3:23 its R ([\d.e+-]+) NOT", line)
        if m and cur and cur["R"] is None and not cur["ok"]:
            cur["R"] = float(m.group(1))
    return out


def main():
    folder = HERE
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        folder = args[0]
    rows = list(csv.DictReader(open(os.path.join(folder, "track949.csv"))))
    by = {}
    for r in rows:
        by[(int(r["ks"]), round(float(r["D"]), 4))] = r
    att = read_refused(args[1] if len(args) > 1 else None)
    for sec in sorted({a["sec"][0] for a in att}):
        print(f"\n== {sec}: attempts from base D 236.7 (win2b's refused903.txt) against sigma_pair at the base (this folder's track949.csv)")
        print("  base D     sigma_pair   pair slope into base   a      -> target D  result    R of the u 0.3 polish")
        for a in att:
            if a["sec"][0] != sec:
                continue
            ks = int(sec[2:])
            r = by.get((ks, round(a["base"], 4)))
            sp = f"{float(r['sigma_pair']):.4e}" if r else "n/a"
            sl = f"{float(r['pair_interval_slope']):+.3f}" if r and r["pair_interval_slope"] else "n/a"
            print(f"  {a['base']:9.4f}  {sp:>11}  {sl:>21}   {a['a']:.4f} -> {a['target']:9.4f}  {'accepted' if a['ok'] else 'REFUSED':<8}  "
                  f"{'' if a['R'] is None else format(a['R'], '.2e')}")
    print("\nsigma_pair along each chain (D, sigma_pair, its slope), from D 232.5:")
    for ks in (250, 291):
        ser = [(float(r["D"]), float(r["sigma_pair"]), r["pair_interval_slope"]) for r in rows if int(r["ks"]) == ks and float(r["D"]) >= 232.4]
        print(f"  ks {ks}: " + "; ".join(f"{d:.3f}: {p:.4e} ({s if s else '-'})" for d, p, s in ser))


main()
