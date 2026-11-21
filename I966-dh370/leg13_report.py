#!/usr/bin/env python3
"""#966: per-iteration report of a corrector attempt under --od_accept own (leg 13, the A/B). Per iteration: |F| before and
after, the accepted lam, |dz| before and after, and every refused trial: lam, point max|F|, raw |dz_t| against the |dz| it had
to beat (the own test: accepted when |dz_t| < |dz|). Accepted trials print no line at verbose 1: the accepted lam comes from the
iteration's closing line. usage: python3 -I leg13_report.py [LEGDIR]   (the attempt after the last 're-seeded' line)"""
import glob, re, sys
leg = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("ks_chain3b/leg13_*/"))[-1]
log = open(leg.rstrip("/") + "/anm_run.log").read().split("\n")
start = max(i for i, l in enumerate(log) if re.search(r"^    a [0-9.]+: re-seeded", l))
print(log[start].strip()[:140])
for l in log[start + 1: start + 4]:
    if "refined in octo-double" in l: print(" ", l.strip()[:140])
its = {}
def it(k): return its.setdefault(int(k), dict(trials=[], done=None, chord=None, stop=None))
for l in log[start + 1:]:
    m = re.match(r"^    on (\d+) trial lam ([0-9./e-]+): max\|F\| ([0-9.e+-]+); raw \|dz_t\| ([0-9.e+-]+) vs \|dz\| ([0-9.e+-]+) \((<|not <)\); (accepted|refused)[^,]*, ([0-9.]+) s", l)
    if m: it(m.group(1))["trials"].append(m.groups()[1:]); continue
    m = re.match(r"^  on (\d+): \|F\| ([0-9.e+-]+) -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+), lam ([0-9./e-]+), dDelta ([+0-9.e-]+).*, ([0-9.]+) s", l)
    if m: it(m.group(1))["done"] = m.groups()[1:]; continue
    m = re.match(r"^  on (\d+): strong chord .*theta at its point ([0-9.e+inf-]+).*: (accepted|refused), ([0-9.]+) s", l)
    if m: it(m.group(1))["chord"] = m.groups()[1:]; continue
    m = re.match(r"^  on (\d+): .*(no trial step accepted, stopping|stalled)", l)
    if m: it(m.group(1))["stop"] = m.group(2)
print("| it | chord check | max abs F before to after | lam accepted | abs dz before to after | refused trials (lam: max abs F, raw abs dz_t / abs dz) | s |")
print("|---|---|---|---|---|---|---|")
for k in sorted(its):
    d = its[k]; dn = d["done"]
    tr = "; ".join(f"{t[0]}: {t[1]}, {t[2]} / {t[3]}" for t in d["trials"] if t[5] == "refused") or "none"
    ch = f"theta {d['chord'][0]} {d['chord'][1]}" if d["chord"] else "-"
    ba = f"{dn[0]} to {dn[1]}" if dn else ("no trial accepted" if d["stop"] else "running")
    print(f"| {k} | {ch} | {ba} | {dn[4] if dn else '-'} | {(dn[2] + ' to ' + dn[3]) if dn else '-'} | {tr} | {dn[6] if dn else '-'} |")
