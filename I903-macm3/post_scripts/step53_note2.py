import re, json, statistics as st, datetime
O = "/Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3"
L = open(f"{O}/chain_k135b.log").read().splitlines()
i4 = next(i for i, l in enumerate(L) if l.startswith("step 4: D "))
hd = L[i4]
seg = L[i4 + 1:]
ends = [i for i, l in enumerate(seg) if re.match(r"\s+a [0-9.]+ -> D ", l)]
blocks, prev = [], 0
for e in ends:
    blocks.append(seg[prev:e + 1]); prev = e + 1
blocks.append(seg[prev:])
def corr(blk):
    rows = {}
    for l in blk:
        m = re.match(r"\s+on (\d+) trial lam ([0-9.]+): max\|F\| (\S+); simplified correction / \|dz\| = (\S+) \(bound (\S+)\); (refused|accepted)", l)
        if m:
            rows.setdefault(int(m.group(1)), {"tr": []})["tr"].append((float(m.group(2)), float(m.group(4)), m.group(6)))
        m = re.match(r"\s+on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam ([0-9.]+),.*?, ([0-9.]+) s$", l)
        if m:
            rows.setdefault(int(m.group(1)), {"tr": []}).update(F=float(m.group(3)), lam=float(m.group(6)), t=float(m.group(7)))
    return [rows[k] for k in sorted(rows) if "F" in rows[k]]
def head(blk, done):
    a = re.search(r"a ([0-9.]+): re-seeded", " ".join(blk)).group(1)
    r = dict(a=a, c=corr(blk), pf=sum(1 for l in blk if "projection failed" in l))
    if done:
        r["tgt"] = re.match(r"\s+a [0-9.]+ -> D ([0-9.]+)", blk[-1]).group(1)
        r["wall"] = re.search(r"moved \S+, (\d+) s", blk[-1]).group(1)
        r["ods"] = next(l.strip() for l in blk if "octo-double Newton" in l)
    return r
at = [head(b, i < len(blocks) - 1) for i, b in enumerate(blocks)]
fv = json.load(open(f"{O}/fold_verdict.json"))
now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
print(f"## #903 macm3b: step 53 after 6 h, attempt 2 refused at the cap of 40, attempt 3 running ({now})\n")
print(f"From `chain_k135b.log` (local step 4), base D {re.search(r'D ([0-9.]+)', hd).group(1)}. The coordinator asked for each base's fold-rule lines and the shrinking a, so both are here.\n")
print("The a of the chain since the restart, and what happened at each: " + ", ".join(
    f"step {r['step']+49} {r['attempts'][0]['a']:.4g} accepted" for r in [json.loads(l) for l in open(f'{O}/chain_k135b/anm_run.jsonl')]) + "; step 53: " + ", ".join(f"{float(x['a']):.4g} {'refused' if 'tgt' in x else 'running'}" for x in at) + ".\n")
print("| attempt | a | target D | corrections | outcome | failed projections | wall s |\n|---|---|---|---|---|---|---|")
for k, x in enumerate(at, 1):
    if "tgt" in x:
        m = re.search(r"(\d+) steps, max\|F\| (\S+), (not converged|converged)", x["ods"])
        oc = f"{'refused' if m.group(3) == 'not converged' else 'accepted'} ({m.group(1)} steps, max\\|F\\| {m.group(2)}, {m.group(3)})"
        print(f"| {k} | {float(x['a']):.4g} | {x['tgt']} | {len(x['c'])} | {oc} | {x['pf']} | {x['wall']} |")
    else:
        print(f"| {k} | {float(x['a']):.4g} | not yet | {len(x['c'])} so far | running | {x['pf']} | {sum(c['t'] for c in x['c']):.0f} so far |")
a2 = at[1]["c"]
def ph(lo, hi): return a2[lo:hi + 1]
fmt = lambda v: "%.2e" % v
r1 = lambda c: c["tr"][0][1]
print("\nAttempt 2's corrections, by the lam-1 trial's simplified-correction ratio (bound 0.75) and the accepted lam:\n")
print("| corrections | accepted lam | lam-1 trial ratio | max\\|F\\| after |\n|---|---|---|---|")
segs = [(0, 6), (7, 9), (10, 35), (36, 39)]
for lo, hi in segs:
    p = ph(lo, hi)
    print(f"| {lo}-{hi} | {', '.join(sorted(set(('%g' % c['lam']) for c in p), key=float))} | {fmt(r1(p[0]))} to {fmt(r1(p[-1]))} | {fmt(p[0]['F'])} to {fmt(p[-1]['F'])} |")
q = [r1(a2[k]) / r1(a2[k + 1]) for k in range(10, 35)]
print(f"\nIn corrections 10-35 the lam-1 ratio falls by a factor of {min(q):.2f} to {max(q):.2f} (median {st.median(q):.2f}) per correction and max|F| halves, 26 corrections at lam 0.5. At correction 36 the ratio was {r1(a2[36]):.3f}, lam 1 was accepted, and from correction 36 to 39 max|F| went {', '.join(fmt(c['F']) for c in a2[36:40])} with the lam-1 ratios {', '.join('%.3f' % r1(c) for c in a2[36:40])}. The attempt stopped at the cap (40 corrections) with max|F| {fmt(a2[-1]['F'])}, whose last correction was a lam-1 step at ratio {r1(a2[-1]):.3f}. Whether one more correction would have converged was not run, so it is not known.")
rows = fv["rows"]
last = [r for r in rows if r["D"] > 259.0]
print("\nThe fold rule's lines for every base it has read (`fold_verdict.json`, main 3c1b9582, ref #841 D* 259.90361142), unchanged since the 19:31 UTC run, the next run waits for the next jet:\n")
print("| base D | M1 | M2 | counted | #603 base | #603 D* |\n|---|---|---|---|---|---|")
for r in rows:
    print(f"| {r['D']:.6f} | {r['M1']['n']}/7, {'; '.join(r['M1']['why']) if r['M1']['n']==0 else r['M1']['med']} | {r['M2']['n']}/7, {'; '.join(r['M2']['why']) if r['M2']['n']==0 else ('%.6f' % r['M2']['med'])} | {r['counted']} | {r['ref_D']:.6f} | {('%.8f' % r['ref_Dstar']) if r['ref_Dstar'] else '-'} |")
print("\nThe registered rule says to report steps that shrink near the fold with no base counting; with one base in range (259.107, 0.80 below D* 259.9033) this is that report, and it concludes nothing, since the coordinator reads the blown-up trials as a fixed-order chain's approach to its own fold. The chain keeps running as the coordinator said. Attempt 3 at a 0.0909 is the second halving of this step (the run allows three).")
