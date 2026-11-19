import re, statistics as st, datetime
O = "/Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3"
L = open(f"{O}/chain_k135b.log").read().splitlines()
i3 = next(i for i, l in enumerate(L) if l.startswith("step 3: D "))
i4 = next(i for i, l in enumerate(L) if l.startswith("step 4: D "))
pat = re.compile(r"projection failed \((\d+)\): point max\|F\| (\S+); u0 rung (\d+) its, \|R\| (\S+) -> (\S+), (NOT converged|converged); u0 quad-double (\d+) its, \|R\| (\S+) -> (\S+), (NOT converged|converged); ladder (FAILED|ok) after (\d+) rungs, last rung u (\S+) (quad-double )?(\d+) its, \|R\| (\S+) -> (\S+), (NOT converged|converged)")
def attempts(rng):
    ends = [i for i, l in enumerate(rng) if re.match(r"\s+a [0-9.]+ -> D ", l)]
    out, prev = [], 0
    for e in ends:
        out.append(rng[prev:e + 1]); prev = e + 1
    out.append(rng[prev:])
    return out
def rows(blk):
    r = []
    for l in blk:
        if "projection failed" in l:
            m = pat.search(l); assert m, l[:200]
            g = m.groups()
            r.append(dict(nf=float(g[1]), u0R=float(g[4]), uqits=int(g[6]), uqR=float(g[8]), rungs=int(g[11]), u=g[12], qd=bool(g[13]), its=int(g[14]), lR=float(g[16]), conv=g[17]))
    return r
sets = []
for k, blk in enumerate(attempts(L[i3:i4]), 1):
    if blk and any("projection failed" in l for l in blk): sets.append((f"step 52, attempt {k}", rows(blk)))
for k, blk in enumerate(attempts(L[i4 + 1:]), 1):
    sets.append((f"step 53, attempt {k}", rows(blk)))
f = lambda v: "%.2e to %.2e (median %.2e)" % (min(v), max(v), st.median(v))
now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
print(f"## #903 macm3b: the failed projections of step 52 and 53, quad-double polish at the u 0.3 rung ({now})\n")
print("The coordinator asked (hc) what the u 0.3 rung's quad-double polish (`polish_q`) ends at in each failed projection of step 53, to compare with win2b's re-seed floor of 1e-24 to 1e-22 (#903 comment 6990709157). From `chain_k135b.log`, every `projection failed` line (the line gives the point's max|F|, the u0 rung in double-double, the u0 quad-double polish, and the ladder with its last rung):\n")
print("| attempt | failed projections | point max\\|F\\| | u0 rung, double-double, final \\|R\\| | u0 quad-double polish, final \\|R\\| (its) | ladder's last rung: u, stage, its, final \\|R\\| |\n|---|---|---|---|---|---|")
allr = []
for name, r in sets:
    if not r: print(f"| {name} | 0 | | | | |"); continue
    allr += r
    us = sorted(set(x["u"] for x in r)); its = sorted(set(x["its"] for x in r)); uq = sorted(set(x["uqits"] for x in r))
    print(f"| {name} | {len(r)} | {f([x['nf'] for x in r])} | {f([x['u0R'] for x in r])} | {f([x['uqR'] for x in r])} ({'/'.join(map(str, uq))} its) | u {'/'.join(us)}, {'quad-double' if all(x['qd'] for x in r) else 'mixed'}, {'/'.join(map(str, its))} its, {f([x['lR'] for x in r])}, {'/'.join(sorted(set(x['conv'] for x in r)))} |")
print(f"\nAll {len(allr)} failed projections: the ladder fails after {'/'.join(str(x) for x in sorted(set(r['rungs'] for r in allr)))} rungs at its last rung u 0.3 (quad-double, {'/'.join(str(x) for x in sorted(set(r['its'] for r in allr)))} steps) with final |R| {f([r['lR'] for r in allr])}, and the u0 quad-double polish ends at {f([r['uqR'] for r in allr])}. The smallest is {min(r['lR'] for r in allr):.2e}, against win2b's 1.0e-24 to 4.1e-24 after 23 steps, so these are not at 1e-24 to 1e-22: the residuals are 1e6 or more above the floor, and the polish stops after 8 steps, not 23.")
print("\nThese failures are in the corrector's trial points (point max|F| 1e7 to 1e10 in the double-double display, in trials the simplified-correction ratio refused), not in the attempts' start re-seeds: both attempts of step 53 report `re-seeded (ok)` (94.63 s and 87.45 s). The log does not print the start re-seed's polish residual, so the floor test cannot be read for the start re-seeds from it.")
