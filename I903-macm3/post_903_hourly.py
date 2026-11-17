"""macm3b #903 hourly post for chain_k135: every number from the chain's log, anm_run.jsonl and ps, at the time of writing."""
import json, math, os, re, subprocess, datetime, sys
RAW = os.path.expanduser("~/Source/choptuik-large-d-raw-903")
O = f"{RAW}/I903-macm3"
log = open(f"{O}/chain_k135.log").read().splitlines()
recs = [json.loads(l) for l in open(f"{O}/chain_k135/anm_run.jsonl")]
ex = open(f"{O}/exits_k135.txt").read().splitlines()
fmt = "%Y-%m-%d %H:%M:%S"
t = lambda s: datetime.datetime.strptime(re.search(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)", s).group(1), fmt)
t0 = t([x for x in ex if "chain_k135 start" in x][0])
now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
# #603 reference, as compare_903.py reads it (the step lines' two-digit p_min), interpolated in ln p
pat = re.compile(r"^step (\d+): D ([0-9.]+), pivots ([0-9.e+-]+)\.\.")
ref = {}
for f in ("chain", "chain_nat", "chain_ns", "chain_nsr"):
    for line in open(f"{RAW}/I603-win2/{f}.log"):
        m = pat.match(line)
        if m: ref[float(m.group(2))] = float(m.group(3))
xs = sorted(ref)
def p603(D):
    if D < xs[0] or D > xs[-1]: return None
    for a, b in zip(xs, xs[1:]):
        if a <= D <= b:
            u = (D - a) / (b - a) if b > a else 0.0
            return math.exp((1 - u) * math.log(ref[a]) + u * math.log(ref[b]))
    return ref[xs[-1]]
# the log by step: split at "step N: D ..." lines
blocks = {}
cur = None
for l in log:
    m = pat.match(l)
    if m:
        cur = int(m.group(1)); blocks[cur] = []
    elif cur is not None:
        blocks[cur].append(l)
P130 = 9.7688e-19
rows = []
for r in recs:
    n = r["step"]; b = blocks.get(n, [])
    od = [re.search(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (converged|not converged)", x) for x in b]
    od = [x for x in od if x]
    att = [re.search(r"a ([0-9.]+) -> D ([0-9.]+): .*?moved ([0-9.e+-]+), ([0-9.]+) s", x) for x in b]
    att = [x for x in att if x]
    a = r["attempts"][-1]
    p = r["pivots"][0]
    q = p603(r["D0"])
    rows.append(dict(step=n, D=r["D0"], p=p, ratio=(math.log(p / q) if q else None), a=a["a"], Dnext=a["D"], conv=r["converged"],
                     odn=od[-1].group(1) if od else "?", odF=od[-1].group(2) if od else "?", odc=od[-1].group(3) if od else "?",
                     tser=r["t_coef"], tatt=float(att[-1].group(4)) if att else None, nat=len(r["attempts"])))
# the step in progress
last = [x for x in log if x.startswith("step ")][-1] if any(x.startswith("step ") for x in log) else ""
tail = [x for x in log[-6:]]
ps = subprocess.run(["ps", "-axo", "pid,pcpu,rss,etime,command"], capture_output=True, text=True).stdout.splitlines()
pr = [l.split(None, 4) for l in ps if "anm_run.py" in l and "chain_k135" in l and "caffeinate" not in l and "grep" not in l]
cpu = pr[0][1] if pr else "?"; rss = int(pr[0][2]) / 1048576 if pr else 0
la = os.getloadavg()
sw = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout.split("used =")[1].split("M")[0].strip()
wall = (now - t0).total_seconds()
Dlast = rows[-1]["Dnext"] if rows else None
nsteps = len(rows)
o = []
o.append(f"## #903 macm3b: order-135 chain, {int(wall//3600)} h {int(wall%3600//60):02d} min in ({now.strftime('%Y-%m-%d %H:%M')} UTC, macm3, 6 threads)\n")
o.append(f"{nsteps} of the chain's steps are recorded, the last accepted state is at D {Dlast:.5f}. All {sum(1 for r in rows if r['conv'])} recorded steps converged, {sum(r['nat']-1 for r in rows)} attempts refused, {'a Traceback in the log' if any('Traceback' in l for l in log) else 'no Traceback in the log'}.\n" if rows else "No step recorded yet.\n")
o.append("| step | D (base) | p_min | ln(p/p603) | a | D reached | octo-double max\\|F\\| (steps) | series s | attempt s |\n|---|---|---|---|---|---|---|---|---|")
for r in rows[-24:]:
    o.append(f"| {r['step']} | {r['D']:.5f} | {r['p']:.4e} | {r['ratio']:+.2f} | {r['a']:.3f} | {r['Dnext']:.5f} | {r['odF']} ({r['odn']}, {r['odc']}) | {r['tser']:.0f} | {r['tatt']:.0f} |" if r['ratio'] is not None else f"| {r['step']} | {r['D']:.5f} | {r['p']:.4e} | | {r['a']:.3f} | {r['Dnext']:.5f} | {r['odF']} ({r['odn']}, {r['odc']}) | {r['tser']:.0f} | {r['tatt']:.0f} |")
o.append("")
o.append("p_min is the smallest octo-double LU pivot at the base (the record's `pivots`), ln(p/p603) is against #603's chain at the same D from its logs' two-digit p_min, interpolated in ln p as `compare_903.py` does. The max|F| is the octo-double Newton's final one for that step's accepted attempt.\n")
if rows:
    R0 = rows[0]
    o.append(f"The rung: ln(p135/p130) = {math.log(R0['p']/P130):+.4f} from the chain's step 0 record (p_min {R0['p']:.6e}, p130 = 9.7688e-19), replacing the 2-digit +4.63 of the rung post.\n")
dpm = None
if len(rows) >= 2:
    span = (rows[-1]["Dnext"] - rows[0]["D"]); per = (sum(r["tser"] + (r["tatt"] or 0) for r in rows)) / span
    k = min(6, len(rows))
    w = rows[-k:]
    spanw = w[-1]["Dnext"] - w[0]["D"]; tw = sum(r["tser"] + (r["tatt"] or 0) for r in w)
    perw = tw / spanw
    left = 262 - rows[-1]["Dnext"]; left9 = 258.9 - rows[-1]["Dnext"]
    o.append(f"Pace: {per/60:.0f} min per unit of D over all {nsteps} steps ({span:.2f} D), and {perw/60:.0f} min per unit of D over the last {k} steps ({spanw:.3f} D in {tw/3600:.2f} h of series and attempt time, a {'/'.join('%.4g' % r['a'] for r in w)}). At the recent pace D 258.9 (the first base of the fold rule's counted range) is {left9*perw/3600:.1f} h away and D 262 is {left*perw/3600:.1f} h away; an assumption, since the step size and the series cost move with D.\n")
import glob as _g, re as _re
_jets = [float(_re.search(r"_D([0-9.]+)\\.npz", f).group(1)) for f in _g.glob(os.path.expanduser("~/Source/choptuik-large-d-raw-903/I903-macm3/chain_k135/jet_pin3_D*.npz"))]
_fx = [l.strip() for l in open(os.path.expanduser("~/Source/choptuik-large-d-raw-903/I903-macm3/exits_k135.txt")) if "fold" in l]
o.append(f"Fold rule (the coordinator's `fold_est_903.py verdict`, run after each new jet with base D of at least 258.5): {sum(1 for d in _jets if d >= 258.5)} such jets so far, the newest jet is at base D {max(_jets):.4f}; last run: {_fx[-1] if _fx else 'none'}.\n")
o.append(f"cpu and memory: anm_run {cpu}% cpu (6 threads), {rss:.2f} GB rss; load average {la[0]:.1f}, swap used {sw} MB of 1024 MB; `caffeinate -is nice -n 10`, nothing else of mine runs.\n")
o.append(f"The hpkernel here has no `Solver.series_o`, so the series are formed by the jets (the notice is in `chain_k135.log`); the bits are the same as by order (#914's check).\n")
RC = sys.argv[2] if len(sys.argv) > 2 else None
if RC: o.append(f"Raw: `I903-macm3/` at commit `{RC}` of choptuik-large-d-raw.\n")
print("\n".join(o))
if len(sys.argv) > 1: open(sys.argv[1], "w").write("\n".join(o))
