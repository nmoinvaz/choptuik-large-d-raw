import re, json, datetime, sys
O = "/Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3"
LS = int(sys.argv[1])          # local step of chain_k135b
OFF = 49
L = open(f"{O}/chain_k135b.log").read().splitlines()
rs = [json.loads(l) for l in open(f"{O}/chain_k135b/anm_run.jsonl")]
assert len(rs) == LS, (len(rs), LS)
i0 = next(i for i, l in enumerate(L) if l.startswith(f"step {LS}: D ") and "pivots" in l)
hd = L[i0]
D0 = re.search(r"step \d+: D ([0-9.]+)", hd).group(1)
pm = re.search(r"pivots ([0-9.e+-]+)\.\.", hd).group(1)
rat = re.search(r"ratios 2-5 (.*), a_max ([0-9.]+), (\d+) s", hd)
seg = L[i0 + 1:]
ends = [i for i, l in enumerate(seg) if re.match(r"\s+a [0-9.]+ -> D ", l)]
blocks, prev = [], 0
for e in ends:
    blocks.append((seg[prev:e + 1], True)); prev = e + 1
blocks.append((seg[prev:], False))
def info(blk, done):
    a = re.search(r"a ([0-9.]+): re-seeded", " ".join(blk))
    a = a.group(1) if a else "?"
    rs_ = next((re.sub(r"^a [0-9.]+: ", "", l.strip()) for l in blk if "re-seeded" in l), "")
    cor = [re.match(r"\s+on (\d+): \|F\| (\S+) -> (\S+), \|dz\| \S+ -> (\S+), lam ([0-9.]+),.*?, ([0-9.]+) s$", l) for l in blk]
    cor = [m for m in cor if m]
    pf = sum(1 for l in blk if "projection failed" in l)
    ref = sum(1 for l in blk if re.match(r"\s+on \d+ trial lam", l) and "refused" in l)
    acc = sum(1 for l in blk if re.match(r"\s+on \d+ trial lam", l) and "accepted" in l)
    tgt = wall = ods = None
    if done:
        m = re.match(r"\s+a ([0-9.]+) -> D ([0-9.]+)", blk[-1]); tgt = m.group(2)
        wall = re.search(r"moved \S+, (\d+) s", blk[-1]).group(1)
        ods = next((l.strip() for l in blk if "octo-double Newton" in l), "")
    return dict(a=a, rs=rs_, cor=cor, pf=pf, ref=ref, acc=acc, tgt=tgt, wall=wall, ods=ods)
inf = [info(b, d) for b, d in blocks]
gs = LS + OFF
now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
out = []
out.append(f"## #903 macm3b: step {gs} (base D {float(D0):.5f}), the first attempt refused with failed projections, the second running ({now})\n")
out.append(f"Read from `chain_k135b.log` (its local step {LS}). The chain runs `--qd_it 40`, so the cap is not what stopped this attempt. Base p_min {pm}, ratios 2-5 {rat.group(1)}, a_max {rat.group(2)}, series {rat.group(3)} s. Nothing is interpreted here.\n")
out.append("| attempt | a | target D | octo-double corrections | lam of each | max\\|F\\| after the last | projection failures | trials refused / accepted | outcome | wall s |\n|---|---|---|---|---|---|---|---|---|---|")
for k, x in enumerate(inf, 1):
    c = x["cor"]
    lam = ", ".join(m.group(5) for m in c) or "none"
    lastF = c[-1].group(3) if c else "none"
    if x["tgt"]:
        m = re.search(r"(\d+) steps, max\|F\| (\S+), (not converged|converged)", x["ods"])
        outc = f"refused ({m.group(1)} steps, {m.group(3)})" if m and m.group(3) == "not converged" else "accepted"
    else:
        outc = "running"
    out.append(f"| {k} | {float(x['a']):.4g} | {x['tgt'] or 'not yet'} | {len(c)} | {lam} | {lastF} | {x['pf']} | {x['ref']} / {x['acc']} | {outc} | {x['wall'] or ('%.0f' % sum(float(m.group(6)) for m in c) if c else '0') + ' so far'} |")
out.append("")
a1 = inf[0]
rat_all = [float(m.group(1)) for l in seg for m in [re.search(r"simplified correction / \|dz\| = (\S+) \(bound", l)] if m and "refused" in l]
bnd = [float(m.group(1)) for l in seg for m in [re.search(r"\(bound (\S+)\); refused", l)] if m]
out.append(f"In every correction the larger-lam trials were refused by the monotonicity test (the simplified correction over |dz| from {min(rat_all):.1e} to {max(rat_all):.1e} in the {len(rat_all)} refused trials of this step so far, bounds {min(bnd):.3f} to {max(bnd):.3f}) and each refused trial's point failed its projection (the ladder failed after 8 rungs) until a small lam was accepted; max|F| after each accepted correction, attempt 1: " + ", ".join(m.group(3) for m in a1["cor"]) + (", attempt 2 so far: " + ", ".join(m.group(3) for m in inf[-1]["cor"]) if not inf[-1]["tgt"] else "") + ".")
out.append("\nThe earlier refusals (steps 45 and 47) were different: there the lam 1 trial's ratio was refused and lam 0.5 accepted each time, the max|F| halving per correction.")
fv = json.load(open(f"{O}/fold_verdict.json"))
rows = [r for r in fv["rows"] if abs(r["D"] - float(D0)) < 1e-4]
if rows:
    r = rows[0]
    out.append(f"\nThe fold rule at this base (`fold_verdict.json`, run after its jet at {r['file']}): M1 {r['M1']['n']}/7 ({'; '.join(r['M1']['why'])}), M2 {r['M2']['n']}/7 ({'; '.join(r['M2']['why'])}), counted {r['counted']}, #603's base at {r['ref_D']:.6f} gives D* {r['ref_Dstar']:.8f}. This is the first base inside 1.0 of D* 259.9 and none counts yet. The earlier note from xfkappa (via the coordinator) says steps that shrink near the fold with no base counting would mean the fold has moved by more than the 0.5 window; one base and one failing attempt do not show that, so this is reported, not concluded. The chain keeps running, the watcher wakes at an a below 0.1.")
print("\n".join(out))
