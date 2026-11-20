#!/usr/bin/env python3
"""#966: the coordinator's cap report for leg 11's base polish: per iteration the trials (lam, point max|F|, accepted or refused, seconds)
and the iteration's |F| before to after, |dz|, lam and seconds, from every ks_chain3b/leg11_*/anm_run.log (one per ks tried).
usage: python3 -I cap966_report.py [CHAIN_OUT]"""
import glob, re, sys
out = sys.argv[1] if len(sys.argv) > 1 else "ks_chain3b"
for log in sorted(glob.glob(out + "/leg11_*/anm_run.log")):
    print("==", log.split("/")[-2])
    base = True
    for l in open(log):
        if re.match(r"^step \d+:", l) or "a_rule reseed:" in l: base = False
        if not base: break
        m = re.match(r"^    on (\d+) chord (\d+): max\|F\| ([0-9.e+-]+)", l)
        if m: print(f"  it {m.group(1)} chord {m.group(2)}: max|F| {m.group(3)}"); continue
        m = re.match(r"^  on (\d+): strong chord .*theta at its point ([0-9.e+inf-]+).*: (accepted|refused), ([0-9.]+) s", l)
        if m: print(f"  it {m.group(1)} chord check: theta {m.group(2)} {m.group(3)}, {m.group(4)} s"); continue
        m = re.match(r"^    on (\d+) trial lam ([0-9./]+): max\|F\| ([0-9.e+-]+); simplified correction / \|dz\| = ([0-9.e+-]+).*; (accepted|refused), ([0-9.]+) s", l)
        if m: print(f"  it {m.group(1)} trial lam {m.group(2)}: point max|F| {m.group(3)}, ratio {m.group(4)}, {m.group(5)}, {m.group(6)} s"); continue
        m = re.match(r"^  on (\d+): \|F\| ([0-9.e+-]+) -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+), lam ([0-9./]+), dDelta ([+0-9.e-]+).*, ([0-9.]+) s", l)
        if m: print(f"  it {m.group(1)} DONE: |F| {m.group(2)} -> {m.group(3)}, |dz| {m.group(4)} -> {m.group(5)}, lam {m.group(6)}, dDelta {m.group(7)}, {m.group(8)} s"); continue
        if re.search(r"converged|stopping|no trial step accepted|not converged", l): print("  ", l.strip()[:200])
