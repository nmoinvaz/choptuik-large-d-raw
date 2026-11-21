#!/usr/bin/env python3
"""#966 pause post (coordinator, hc 2026-11-21 ~22:10 UTC): for the step in progress (the log after its 'step N: D ...' line) print, per attempt, the
re-seed and refinement lines, a per-iteration table (max |F| before and after, accepted lam, |dz| before and after, the smallest pivot of the iteration's Jacobian, the
refused trials' lam, max |F| and raw |dz_t| against |dz|, the 'trial |dz| table'), the octo-double line and the attempt's summary line.
usage: python3 -I pausepost966.py LEGDIR [STEP]   (default: the last 'step N:' line of the log)"""
import re, sys
leg = sys.argv[1].rstrip("/")
log = open(leg + "/anm_run.log").read().split("\n")
steps = [i for i, l in enumerate(log) if re.match(r"^step \d+: D ", l)]
want = int(sys.argv[2]) if len(sys.argv) > 2 else None
if want is None:
    s0 = steps[-1]
else:
    s0 = next(i for i in steps if re.match(rf"^step {want}: D ", log[i]))
print(log[s0][:260])
for l in log[s0 + 1:s0 + 3]:
    if "a_rule" in l: print(l.strip()[:260])
starts = [i for i in range(s0, len(log)) if re.match(r"^    a [0-9.]+: re-seeded", log[i])]
for n, st in enumerate(starts):
    en = starts[n + 1] if n + 1 < len(starts) else len(log)
    seg = log[st:en]
    print(f"\n### attempt {n + 1}: {seg[0].strip()[:200]}")
    for l in seg[1:6]:
        if "refined in octo-double" in l or "above --reseed_o_bar" in l: print("  " + l.strip()[:260])
    its = {}
    def it(k): return its.setdefault(int(k), dict(trials=[], done=None, chord=None, stop=None))
    for l in seg:
        m = re.match(r"^    on (\d+) trial lam ([0-9./e-]+): max\|F\| ([0-9.e+-]+); raw \|dz_t\| ([0-9.e+-]+) vs \|dz\| ([0-9.e+-]+) \((<|not <)\); (accepted|refused)[^,]*, ([0-9.]+) s", l)
        if m: it(m.group(1))["trials"].append(m.groups()[1:]); continue
        m = re.match(r"^  on (\d+): \|F\| ([0-9.e+-]+) -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+), lam ([0-9./e-]+), dDelta ([+0-9.e-]+), piv ([0-9.e+-]+)\.\.([0-9.e+-]+), ([0-9.]+) s", l)
        if m: it(m.group(1))["done"] = m.groups()[1:]; continue
        m = re.match(r"^  on (\d+): strong chord .*theta at its point ([0-9.e+inf-]+).*: (accepted|refused), ([0-9.]+) s", l)
        if m: it(m.group(1))["chord"] = m.groups()[1:]; continue
        m = re.match(r"^  on (\d+): .*(no trial step accepted, stopping|stalled)", l)
        if m: it(m.group(1))["stop"] = m.group(2)
    if its:
        print("| it | chord check | max abs F before to after | lam accepted | abs dz before to after | smallest pivot | refused trials (lam: max abs F, raw abs dz_t / abs dz) | s |")
        print("|---|---|---|---|---|---|---|---|")
        for k in sorted(its):
            d = its[k]; dn = d["done"]
            tr = "; ".join(f"{t[0]}: {t[1]}, {t[2]} / {t[3]}" for t in d["trials"] if t[5] == "refused") or "none"
            ch = f"theta {d['chord'][0]} {d['chord'][1]}" if d["chord"] else "-"
            ba = f"{dn[0]} to {dn[1]}" if dn else ("no trial accepted" if d["stop"] else "running")
            print(f"| {k} | {ch} | {ba} | {dn[4] if dn else '-'} | {(dn[2] + ' to ' + dn[3]) if dn else '-'} | {dn[6] if dn else '-'} | {tr} | {dn[8] if dn else '-'} |")
    for l in seg:
        if re.match(r"^      octo-double Newton:", l) or re.match(r"^    a [0-9.]+ -> D ", l) or "elim projections" in l:
            print("  " + l.strip()[:300])
