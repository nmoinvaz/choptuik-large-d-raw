"""macm3b #903 closing summary for the order-135 chain: every number from the raw folder's files (exits, logs, jsonl, fold_verdict.json)."""
import json, math, os, re, sys, datetime, statistics as st
O = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I903-macm3")
RC = sys.argv[2] if len(sys.argv) > 2 else "RAWCOMMIT"
D603, D841, E841 = 259.9033, 259.90361142, 5.3e-4
d = json.load(open(sys.argv[1]))
rows = d["rows"]
ex = open(f"{O}/exits_k135.txt").read().splitlines()
T = lambda s: datetime.datetime.strptime(re.search(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)", s).group(1), "%Y-%m-%d %H:%M:%S")
wl = lambda pat: re.search(r"wall (\d+) ?s", next(x for x in ex if pat in x)).group(1)
tm = lambda pat: next(x for x in ex if pat in x)
rung_wall = int(wl("rung135 exit")); a_wall = int(wl("chain_k135 exit")); b_wall = int(wl("chain_k135b exit"))
s_a, s_b = T(tm("chain_k135 start")), T(tm("chain_k135b start")); e_b = T(tm("chain_k135b exit"))
LA = open(f"{O}/chain_k135.log").read().splitlines(); LB = open(f"{O}/chain_k135b.log").read().splitlines()
ra = [json.loads(l) for l in open(f"{O}/chain_k135/anm_run.jsonl")]; rb = [json.loads(l) for l in open(f"{O}/chain_k135b/anm_run.jsonl")]
n = len(rows); assert n == len(ra) + len(rb)
refused_rec = sum(r["nat"] - 1 for r in rows)
# step 53 (chain_k135b local step 4), attempts from the log
i4 = next(i for i, l in enumerate(LB) if l.startswith(f"step {len(rb)}: D "))
hd = LB[i4]; seg = LB[i4 + 1:]
p53 = float(re.search(r"pivots ([0-9.e+-]+)\.\.", hd).group(1)); D53 = float(re.search(r"step \d+: D ([0-9.]+)", hd).group(1))
ser53 = int(re.search(r", (\d+) s$", hd).group(1)); rat53 = re.search(r"ratios 2-5 (.*), a_max ([0-9.]+),", hd).groups()
ends = [i for i, l in enumerate(seg) if re.match(r"\s+a [0-9.]+ -> D ", l)]
blocks, prev = [], 0
for e in ends: blocks.append(seg[prev:e + 1]); prev = e + 1
tailblk = seg[prev:]
att = []
for blk in blocks:
    a = re.search(r"a ([0-9.]+): re-seeded \((\w+)\), ([0-9.]+) s", " ".join(blk)); m = re.match(r"\s+a ([0-9.]+) -> D ([0-9.]+).*moved \S+, (\d+) s", blk[-1])
    cs = [re.match(r"\s+on (\d+): \|F\| (\S+) -> (\S+), \|dz\| \S+ -> \S+, lam ([0-9.]+),", l) for l in blk]; cs = [c for c in cs if c]
    od = re.search(r"(\d+) steps, max\|F\| (\S+), (not converged|converged)", next(l for l in blk if "octo-double Newton" in l))
    stop = next((l.strip() for l in blk if "stopping" in l), "ran to the cap of 40 corrections")
    att.append(dict(a=float(a.group(1)), rs=a.group(2), rst=a.group(3), D=m.group(2), wall=int(m.group(3)), nc=len(cs), lams=[float(c.group(4)) for c in cs], F=cs[-1].group(3),
                    pf=sum(1 for l in blk if "projection failed" in l), ref=sum(1 for l in blk if re.match(r"\s+on \d+ trial lam", l) and "refused" in l),
                    acc=sum(1 for l in blk if re.match(r"\s+on \d+ trial lam", l) and "accepted" in l), odn=od.group(1), odF=od.group(2), odc=od.group(3), stop=stop,
                    chord=any("strong chord" in l and "refused" in l for l in blk)))
tot_att53 = sum(x["wall"] for x in att)
def all_attempts(L, off, cap):
    hdr = [(i, int(re.match(r"step (\d+): D ", l).group(1))) for i, l in enumerate(L) if re.match(r"step \d+: D .*pivots", l)]
    out = []
    for k, (i, st_) in enumerate(hdr):
        j = hdr[k + 1][0] if k + 1 < len(hdr) else len(L)
        sg = [l for l in L[i + 1:j] if not re.match(r"step \d+: the series saved", l)]
        pv = 0
        for ei in [x for x, l in enumerate(sg) if re.match(r"\s+a [0-9.]+ -> D ", l)]:
            blk = sg[pv:ei + 1]; pv = ei + 1
            m = re.match(r"\s+a ([0-9.]+) -> D ([0-9.]+).*moved \S+, (\d+) s", blk[-1])
            od = next((re.search(r"(\d+) steps, max\|F\| (\S+), (not converged|converged)", l) for l in blk if "octo-double Newton" in l), None)
            out.append(dict(step=st_ + off, a=float(m.group(1)), D=m.group(2), wall=int(m.group(3)), od=od.groups() if od else None,
                            stall=any("stopping (stalled)" in l for l in blk), chord=any("strong chord" in l and "refused" in l for l in blk), cap=cap))
    return out
ALL = all_attempts(LA, 0, 20) + all_attempts(LB, len(ra), 40)
REF = [x for x in ALL if x["od"] is None or x["od"][2] == "not converged"]
ser_hdr = sum(int(re.search(r", (\d+) s$", l).group(1)) for l in LA + LB if re.match(r"step \d+: D .*pivots", l))
att_sum = sum(x["wall"] for x in ALL)
saved = [l for l in LB if "Delta of the saved state" in l][-1].split(": ")[1].strip()
fv = json.load(open(f"{O}/fold_verdict.json"))
# pace and time budget
D0, Dend = rows[0]["D"], rows[-1]["Dnext"]
mt = lambda p: datetime.datetime.fromtimestamp(os.path.getmtime(p), datetime.timezone.utc).replace(tzinfo=None)
e_a = T(tm("chain_k135 exit"))
cut49 = (e_a - mt(f"{O}/chain_k135/anm_pin3_D{ra[-1]['attempts'][-1]['D']:.4f}.npz")).total_seconds() / 60
cut53 = (e_b - mt(f"{O}/chain_k135b/pred_pin3_D{D53+0.0455:.4f}.npz")).total_seconds()
o = []
o.append(f"## #903 macm3b: order-135 chain closed at D {Dend:.5f}, step 53 never accepted, fold not read ({datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M UTC')})\n")
o.append(f"The chain stopped at D {Dend:.9f}, {D603 - Dend:.4f} below #603's order-130 fold D* {D603}. I stopped it myself, on the coordinator's order to let attempt 3 finish and then stop by the exact pid (hc after my 01:23 UTC post): SIGTERM to pid 96629 at {e_b.strftime('%Y-%m-%d %H:%M:%S')} UTC, exit 143. It did not crash: no Traceback in either log. The fold rule read five bases (258.248 to 259.107), counted none, and gave no D*.\n")
o.append("### Runs and exits\n\n| run | start (UTC) | end (UTC) | wall | exit |\n|---|---|---|---|---|")
rs_s = T(tm("rung135 start")); rs_e = T(tm("rung135 exit"))
o.append(f"| rung 135 (from q130's base D 225.13125) | {rs_s} | {rs_e} | {rung_wall} s | 0, converged |")
o.append(f"| `chain_k135` (`--qd_it 20`, steps 0-48) | {s_a} | {T(tm('chain_k135 exit'))} | {a_wall} s ({a_wall/3600:.2f} h) | 143, stopped by me for the cap restart |")
o.append(f"| `chain_k135b` (`--qd_it 40`, from step 48's base, steps 49-52 accepted, step 53 not) | {s_b} | {e_b} | {b_wall} s ({b_wall/3600:.2f} h) | 143, stopped by me on the coordinator's order |")
o.append(f"\nTotal chain wall {(a_wall+b_wall)/3600:.2f} h ({(a_wall+b_wall)/86400:.2f} d), 6 threads, `nice -n 10` under `caffeinate`, code main 5897ee28 with the 1f3cda09 hpkernel (no `Solver.series_o`, the series by the jets), 25-order jets saved (`--N 24 --save_jet 1 --jet_o 1`). The series took {ser_hdr/3600:.1f} h and the attempts {att_sum/3600:.1f} h (all attempts, accepted and refused, with their re-seeds), step 53's three attempts {tot_att53/3600:.2f} h of that. The remaining {((a_wall+b_wall)-ser_hdr-att_sum)/3600:.1f} h of the wall is not in the logs' series or attempt times (it includes the two pieces cut off by the stops, {cut49:.0f} min into step 49's series and {cut53:.0f} s into step 53's attempt 4).\n")
o.append("### Final state\n")
o.append(f"- Last accepted state: step {n-1} ended at D {Dend:.9f}, `chain_k135b/anm_pin3_D{Dend:.4f}.npz` (eight parts), Delta {saved[:24]}, with its 25-order jet `chain_k135b/jet_pin3_D{Dend:.4f}.npz`.\n- Records: {n} steps (0-{n-1}), all converged, {refused_rec} attempts refused inside them, plus the three refused attempts of step {n} ({refused_rec+len(att)} in all), and no Traceback in `chain_k135.log` or `chain_k135b.log`.\n- Step {n} (base D {D53:.9f}) was never accepted. Attempt 4 (a 0.0455, target D {D53+0.0455:.4f}) had written its prediction file `pred_pin3_D{D53+0.0455:.4f}.npz` and nothing else when the SIGTERM came.\n- The state advanced {Dend-D0:.4f} in D ({D0} to {Dend:.5f}) from the order-135 rung.\n")
o.append("### The a and the corrections\n")
r = rows
def seg_(lo, hi): return [x for x in r if lo <= x["step"] <= hi]
tb = [("0-24", 0, 24), ("25-37", 25, 37), ("38-48", 38, 48), ("49-52 (cap 40)", 49, 52)]
o.append("| steps | a | D range | refused attempts | corrections per accepted step (damped) |\n|---|---|---|---|---|")
for nm, lo, hi in tb:
    s = seg_(lo, hi)
    cr = [x["ncorr"] for x in s]; dm = [x["nlow"] for x in s]
    o.append(f"| {nm} | {('%.3g' % min(x['a'] for x in s)) if min(x['a'] for x in s) == max(x['a'] for x in s) else '%.3g to %.3g' % (min(x['a'] for x in s), max(x['a'] for x in s))} | {s[0]['D']:.2f} to {s[-1]['Dnext']:.2f} | {sum(x['nat']-1 for x in s)} | {min(cr)} to {max(cr)} (median {st.median(cr):g}; damped {min(dm)} to {max(dm)}) |")
o.append("\nEvery refused attempt of the run, with how it ended (`not converged` is the octo-double Newton's own verdict):\n")
o.append("| step | a | target D | octo-double steps | max\\|F\\| | ended | `--qd_it` | wall s |\n|---|---|---|---|---|---|---|---|")
for x in REF:
    if x["od"] is None: why, ods, f_ = "refused at the start", "none", "none"
    else:
        ods, f_ = x["od"][0], x["od"][1]
        why = "stall rule (lam below 0.04 twice)" if x["stall"] else ("strong chord refused (theta inf) at correction 0, then stopped" if x["chord"] and int(ods) < 5 else ("ran to the cap" if int(ods) >= x["cap"] else "other"))
    o.append(f"| {x['step']} | {x['a']:.4g} | {x['D']} | {ods} | {f_} | {why} | {x['cap']} | {x['wall']} |")
nc20 = sum(1 for x in REF if x["od"] is not None and int(x["od"][0]) >= x["cap"] == 20)
o.append(f"\nUnder `--qd_it 20` {sum(1 for x in REF if x['cap']==20)} attempts were refused, {nc20} of them at the cap of 20 (steps 38, 42, 45 and 47, max|F| 1e-39 to 1e-45, a 0.5 to 0.238) and the others at the first corrector step or the start; after the restart to `--qd_it 40` the coordinator asked whether the larger cap lets a grow, and it did: 0.149, 0.186, 0.233, 0.291 for steps 49-52, each accepted at its first attempt in 25-26 corrections, then step 53 refused 0.364, 0.182 and 0.091.\n")
o.append("### Step 53's three attempts\n")
o.append(f"Base D {D53:.9f}, p_min {p53:.2e}, ratios 2-5 {rat53[0]}, a_max {rat53[1]}, series {ser53} s.\n")
o.append("| attempt | a | target D | start re-seed | corrections | lam of the corrections | max\\|F\\| after the last | failed projections | trials refused / accepted | ended | wall s |\n|---|---|---|---|---|---|---|---|---|---|---|")
for k, x in enumerate(att, 1):
    lam = ", ".join("%g" % v for v in x["lams"]) if len(x["lams"]) <= 8 else f"{x['lams'].count(0.5)} at 0.5, {x['lams'].count(1.0)} at 1, {sum(1 for v in x['lams'] if v < 0.5)} below 0.5, {sum(1 for v in x['lams'] if v>0.5 and v<1)} other"
    o.append(f"| {k} | {x['a']:.4g} | {x['D']} | {x['rs']}, {x['rst']} s | {x['nc']} | {lam} | {x['F']} | {x['pf']} | {x['ref']} / {x['acc']} | {x['stop']} ({x['odn']} steps, {x['odc']}) | {x['wall']} |")
o.append(f"\nAttempts 1 and 3 stopped on the corrector's stall rule (`--lam_stall 0.04`) with max|F| stuck near 1e-29 (each of the three attempts began with a strong-chord first correction that was refused with theta inf). Attempt 2 got through the stuck phase (lam-1 trial ratios of 1e53 to 1e54 fell to 4e-3 by correction 7, F to 8.5e-39), crawled 26 corrections at lam 0.5 with the ratio falling by 8x per correction and max|F| halving to 1.3e-46, and ended at the cap of 40 corrections with a lam-1 correction at ratio 0.198 and max|F| 2.43e-43. Whether a 41st correction would have converged was not run. The failed projections ({sum(x['pf'] for x in att)} in all) were the corrector's refused trial points; their u 0.3 rung's quad-double polish ended at |R| 1.4e6 to 5.7e6 after 8 steps, not at the 1e-24 re-seed floor of win2b's chains (comment 6993321196).\n")
o.append("### The fold rule's table\n")
o.append(f"`fold_est_903.py verdict` at main 3c1b9582 with `--ref_Dstar=259.90361142 --ref_err=5.3e-4`, run after each jet with base D of at least 258.5 (`fold_verdict_k135.log`, `fold_verdict.json`). Control 1 (#603's chain_nsr, 45 bases in [258.9, 259.84]): max miss {fv['control1']['max_miss']:.2e}, bound 0.005, pass, at every run. All three runs exit 2 (continue), 0 counted bases, so there is no D*, no shift and no band.\n")
o.append("| base D | M1 | M2 | plant worst | counted | #603 base | #603 D* |\n|---|---|---|---|---|---|---|")
for q in fv["rows"]:
    m1 = f"{q['M1']['n']}/7, " + ("; ".join(q["M1"]["why"]) if q["M1"]["n"] == 0 else f"median {q['M1']['med']:.6f}")
    m2 = f"{q['M2']['n']}/7, " + ("; ".join(q["M2"]["why"]) if q["M2"]["n"] == 0 else f"median {q['M2']['med']:.6f}")
    o.append(f"| {q['D']:.6f} | {m1} | {m2} | {q['plant_worst'] if q['plant_worst'] is not None else '-'} | {q['counted']} | {q['ref_D']:.6f} | {('%.8f' % q['ref_Dstar']) if q['ref_Dstar'] else '-'} |")
o.append(f"\nM2 found one root at the first base (258.248, median 260.210219, a single approximant of 7, no plant rerun) and none at the four bases after it. Nothing counts: a base counts only when the plant rerun there recovers its shifts within 0.005, and the plant column is empty for every base. This is the case the registered rule names for a chain whose steps shrink near the fold without a counting base, with one base in range (259.107, {D603-259.107228:.3f} below D*); the rule reads it as a fold moved by more than the 0.5 window. The coordinator reads step 53's blown-up trials as a fixed-order chain nearing its own fold, and neither reading was tested here. Order 135 therefore gives no D* against #603's {D603} or #841's {D841} ({E841:.1e}).\n")
o.append("### What was unexpected\n")
st_ = [x["tser"] + x["tatt"] for x in rows if 49 <= x["step"] <= 52]
rt = [(x[2], x[3]) for x in d["ratios"][47:]] if False else [(v[2], v[3]) for v in d["ratios"][47:]]
lo_, hi_ = min(min(v) for v in rt), max(max(v) for v in rt)
o.append(f"- The `--qd_it 20` cap refused attempts that were still converging (the four at the cap, steps 38, 42, 45, 47); `--qd_it 40` removed that for steps 49-52, then step 53 failed in a different way, with stuck corrections and failed projections (two of its three attempts stopped on the stall rule at max|F| near 1e-29, one at the cap of 40).\n- Step 53's three attempts took {tot_att53/3600:.2f} h ({' + '.join(str(x['wall']) for x in att)} = {tot_att53} s) and none was accepted, while steps 49-52 each took {min(st_)/3600:.1f} to {max(st_)/3600:.1f} h with their series.\n- The series' ratios 4 and 5 (of ratios 2-5) ranged {lo_:.1f} to {hi_:.1f} over steps 47-52 and were {rat53[0].split()[2]} and {rat53[0].split()[3]} at step 53's base, noted, not interpreted.\n")
o.append("### Trail of p_min and a (all 53 steps)\n")
o.append("<details><summary>table</summary>\n\n| step | D (base) | p_min | ln(p/p603) | a | D reached | octo max\\|F\\| (steps) | corrections (damped) | `--qd_it` | series s | attempt s | attempts |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
for x in rows:
    o.append(f"| {x['step']} | {x['D']:.5f} | {x['p']:.4e} | {('%+.2f' % x['ratio']) if x['ratio'] is not None else ''} | {x['a']:.4g} | {x['Dnext']:.5f} | {x['odF']} ({x['odn']}) | {x['ncorr']} ({x['nlow']}) | {x['cap']} | {x['tser']:.0f} | {x['tatt']:.0f} | {x['nat']} |")
o.append(f"| {n} (not accepted) | {D53:.5f} | {p53:.4e} | | {', '.join('%.4g' % x['a'] for x in att)} | | | | 40 | {ser53} | {tot_att53} | {len(att)} refused |\n\n</details>\n")
o.append("p_min is the smallest octo-double LU pivot at the base; ln(p/p603) is against #603's chain at the same D (two-digit p_min from its logs, interpolated in ln p, `compare_903.py`); ln(p135/p130) at the rung was +4.6429.\n")
o.append("### How to resume\n")
o.append(f"`run_903_k135b.sh` from `chain_k135b/anm_pin3_D{Dend:.4f}.npz` with its flags and `--a0` at 0.0909 or below (step 53 refused 0.364, 0.182 and 0.091 from this base). The state, its jet and the prediction files of the refused attempts (`pred_pin3_D259.*.npz`) are in the folder.\n")
o.append("### Recommended tasks (the coordinator opens the issues)\n")
o.append(f"1. **Cross the fold at order 135 by arclength** from `chain_k135b/anm_pin3_D{Dend:.4f}.npz`, as #842 did at order 130 (its chain stopped by its own rule at D 259.903269724106 with cond max 7e28, note 1795027769455), so the fold's D is read instead of approached. What: arclength chain at `--ks 135`, same corrector flags and `--qd_it 40`. Why: a chain in D has no accepted step past D {Dend:.3f}, and the D*-reading needs bases near 259.9. Acceptance: at least two bases within 1.0 of the fold with the rule's plant rerun passing, D* from the verdict, or a stop with its reason. Depends on #903 (this) and #842.\n2. **Test whether step 53's attempt 2 converges with more corrections.** What: rerun the a 0.1819 attempt from the base with `--qd_it 60` (about 4 h at 6 threads). Why: it stopped at the cap with a lam-1 correction at ratio 0.198. Acceptance: it converges or reaches 60 corrections with its max|F| trail; a failure mode is a stall below 1e-29 as in attempts 1 and 3. Depends on #903. The coordinator declined this raise for now.\n")
o.append(f"Raw: `I903-macm3/` at commit `{RC}` of choptuik-large-d-raw. The label `running` stays on #903 and the issue stays open, since other agents' chains are on it.")
print("\n".join(o))
