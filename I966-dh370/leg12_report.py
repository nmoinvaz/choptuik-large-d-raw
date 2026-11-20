#!/usr/bin/env python3
"""#966: per-iteration report of a corrector attempt in the fallback leg (coordinator's hc 2026-11-20 22:3x): for every iteration the |F| before and after,
the accepted lam, |dz|, and for every trial lam: the point max|F|, the NATURAL ratio (simplified correction / |dz|), its bound, accepted or refused, seconds;
the lam = 1 trial first. usage: python3 -I leg12_report.py [LEGDIR] [AFTER_REGEX]   (default: the attempt after the last 're-seeded' line)"""
import glob, re, sys
leg = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("ks_chain3b/leg12_*/"))[-1]
log = open(leg.rstrip("/") + "/anm_run.log").read().split("\n")
start = max(i for i, l in enumerate(log) if re.search(r"^    a [0-9.]+: re-seeded", l))
print(log[start].strip()[:140])
for l in log[start + 1: start + 4]:
    if "refined in octo-double" in l: print(" ", l.strip()[:140])
its = {}
for l in log[start + 1:]:
    m = re.match(r"^    on (\d+) trial lam ([0-9./e-]+): max\|F\| ([0-9.e+-]+); simplified correction / \|dz\| = ([0-9.e+-]+) \(bound ([0-9.]+)\); (accepted|refused), ([0-9.]+) s", l)
    if m: its.setdefault(int(m.group(1)), dict(trials=[], done=None))["trials"].append(m.groups()[1:]); continue
    m = re.match(r"^  on (\d+): \|F\| ([0-9.e+-]+) -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+), lam ([0-9./e-]+), dDelta ([+0-9.e-]+).*, ([0-9.]+) s", l)
    if m: its.setdefault(int(m.group(1)), dict(trials=[], done=None))["done"] = m.groups()[1:]; continue
    m = re.match(r"^  on (\d+): strong chord .*theta at its point ([0-9.e+inf-]+).*: (accepted|refused), ([0-9.]+) s", l)
    if m: its.setdefault(int(m.group(1)), dict(trials=[], done=None))["chord"] = m.groups()[1:]
print("| it | chord check | |F| before to after | lam accepted | |dz| before to after | lam 1: max|F|, natural ratio (bound), result | other trials (lam: max|F|, ratio, result) | s |")
print("|---|---|---|---|---|---|---|---|")
for k in sorted(its):
    d = its[k]; t1 = [t for t in d["trials"] if t[0] == "1"]
    one = f"{t1[0][1]}, {t1[0][2]} ({t1[0][3]}), {t1[0][4]}" if t1 else "no trial"
    other = "; ".join(f"{t[0]}: {t[1]}, {t[2]}, {t[4][0].upper()}" for t in d["trials"] if t[0] != "1")
    ch = f"theta {d['chord'][0]} {d['chord'][1]}" if "chord" in d else "-"
    dn = d["done"]
    ba = f"{dn[0]} to {dn[1]}" if dn else "running"
    print(f"| {k} | {ch} | {ba} | {dn[4] if dn else '-'} | {(dn[2] + ' to ' + dn[3]) if dn else '-'} | {one} | {other} | {dn[6] if dn else '-'} |")
