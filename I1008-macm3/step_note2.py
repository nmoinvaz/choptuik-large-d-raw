"""Post for one accepted arc step of #1008. Usage: step_note2.py MODE STEP RAWCOMMIT [extra paragraph file]
MODE/STEP name the record (MODE/arc.jsonl step STEP) and its log block (MODE.log between 'step STEP-1:' and 'step STEP:')."""
import re, json, datetime, sys, os, subprocess
import mpmath as mp
mp.mp.dps = 40
mode, N, RC = sys.argv[1], int(sys.argv[2]), sys.argv[3]
extra = open(sys.argv[4]).read().strip() if len(sys.argv) > 4 else ""
O = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1008-macm3")
D130 = mp.mpf("259.903269724106")
def recs_of(m):
    return [r for r in (json.loads(l) for l in open(f"{O}/{m}/arc.jsonl")) if "attempts" in r]
hist = [("pilot2", r) for r in recs_of("pilot2")]
if os.path.exists(f"{O}/run1/arc.jsonl"):
    hist += [("run1", r) for r in recs_of("run1")]
r = next(r for m, r in hist if m == mode and r["step"] == N)
cum = {}
s = mp.mpf(0)
for i, (m, rr) in enumerate(hist):
    if rr.get("converged"): s += mp.mpf(rr["a"])
    cum[(m, rr["step"])] = (i, s)
L = open(f"{O}/{mode}.log").read().splitlines()
i1 = next(i for i, l in enumerate(L) if re.match(rf"step {N}:", l))
i0 = next((i for i in range(i1, -1, -1) if i != i1 and re.match(rf"step {N - 1}:", L[i])), 0) if N > 0 else 0
seg = L[i0:i1 + 1]
ser = [l.strip() for l in seg if l.strip().startswith("series at D")]
att_lines = [l.strip() for l in seg if l.strip().startswith("attempt at D")]
# corrections of the last attempt
ia = max(i for i, l in enumerate(seg) if l.strip().startswith("attempt at D"))
cseg = seg[ia:]
cor = {}
for l in cseg:
    m = re.match(r"\s+on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+), dDelta (\S+), piv \S+, ([0-9.]+) s$", l)
    if m: cor[int(m.group(1))] = dict(F0=m.group(2), F1=m.group(3), dz0=m.group(4), dz1=m.group(5), lam=m.group(6), s=float(m.group(8)))
trials = []
for l in cseg:
    m = re.match(r"\s+on (\d+) trial lam (\S+): max\|F\| (\S+); .*?; (\w+), ([0-9.]+) s", l)
    if m: trials.append((int(m.group(1)), m.group(2), m.group(4)))
nref = sum(1 for t in trials if t[2] == "refused")
pfl = [int(re.match(r"\s+on (\d+),", l).group(1)) for l in cseg if "projection failed" in l]
sc = next((l.strip() for l in cseg if "strong chord" in l), "")
final = next(l for l in cseg if l.strip().startswith("corrector:"))
mfin = re.search(r"corrector: (\d+) steps, pinned max\|F\| (\S+) at D (\S+), (\w+), ([0-9.]+) s", final)
a = r["attempts"][-1]
Dn = mp.mpf(r["D_str"])
now = datetime.datetime.now(datetime.UTC)
idx, scum = cum[(mode, N)]
prev_tD = [x["tD_end"] for m, x in hist[:idx] if x.get("converged")]
tDs = [x["tD0"] for m, x in hist[:1]] + [x["tD_end"] for m, x in hist if x.get("converged")]
falling = [(tDs[j], tDs[j + 1]) for j in range(len(tDs) - 1) if tDs[j + 1] < tDs[j]]
turn = [x for m, x in hist if x.get("turn")]
print(f"## #1008 macm3b: arc step {idx} accepted ({mode} step {N}, {now.strftime('%Y-%m-%d %H:%M UTC')})\n")
print(f"Arc step {idx} is accepted: a {r['a']:.6g}, D {mp.nstr(Dn, 16)}, {mfin.group(1)} corrector steps, max|F| {mfin.group(2)}, {mfin.group(5)} s, "
      f"{len(r['attempts'])} attempt. |t_D| {r['tD0']:.10f} at the base, {r['tD_end']:.10f} at the new point: "
      + ("it has not fallen below the base's" if r["tD_end"] >= r["tD0"] else "IT FELL") +
      f"; over all steps {'it fell at ' + str(falling) if falling else 'it has not fallen at any step'}. "
      f"D_max {mp.nstr(Dn, 16)} is {mp.nstr(D130 - Dn, 6)} below order 130's {mp.nstr(D130, 15)}. "
      + ("A turn is recorded at " + ", ".join(t['turn'][0]['D'][:22] for t in turn) if turn else "No turn is recorded yet (t_D has not changed sign).") + "\n")
print("| arc step | run, step | a (s total) | D0 -> D | max\\|F\\| | corrector steps | corrector s | \\|t_D\\| base -> end | sign | cond max | attempts |\n|---|---|---|---|---|---|---|---|---|---|---|")
for j, (m, rr) in enumerate(hist):
    if not rr.get("converged"): continue
    aa = rr["attempts"][-1]; c = aa["corrector"]
    print(f"| {j} | {m}, {rr['step']} | {rr['a']:.6g} ({mp.nstr(cum[(m, rr['step'])][1], 6)}) | {mp.nstr(mp.mpf(rr['D0_str']), 16)} -> {mp.nstr(mp.mpf(rr['D_str']), 16)} | {c['F']:.3g} | {len(c['its'])} | {c['seconds']:.1f} | {rr['tD0']:.10f} -> {rr['tD_end']:.10f} | {rr['sign']:+d} | {rr['cond_max']:.6f} | {len(rr['attempts'])} |")
print(f"\n{(ser[0] if ser else 'series: none in this block')}\n")
print(f"{att_lines[-1]}\n")
print(f"First correction: {sc}\n" if sc else "")
print(f"max|F| per correction (`{mode}.log`):\n")
print("| correction | max\\|F\\| before -> after | \\|dz\\| after (before) | lam | seconds |\n|---|---|---|---|---|")
for k in sorted(cor):
    d = cor[k]
    print(f"| {k} | {d['F0']} -> {d['F1']} | {d['dz1']} ({d['dz0']}) | {d['lam']} | {d['s']} |")
print(f"| {max(cor) + 1} | {mfin.group(2)} (converged check) | | | |")
lams = {}
for k in cor: lams[cor[k]["lam"]] = lams.get(cor[k]["lam"], 0) + 1
big = [k for k in sorted(cor) if mp.mpf(cor[k]["F1"]) > mp.mpf(cor[k]["F0"])]
print(f"\nAccepted lam over the {len(cor)} corrections: " + ", ".join(f"lam {k} x{v}" for k, v in sorted(lams.items(), key=lambda kv: float(kv[0]))) +
      f". Trials {len(trials)} ({nref} refused), failed projections {len(pfl)}" + (f" (at corrections {', '.join(str(x) for x in sorted(set(pfl)))})" if pfl else "") +
      f". Corrections where max|F| rose: {big if big else 'none'}.\n")
if extra: print(extra + "\n")
print(f"Raw `I1008-macm3/` at commit `{RC}`.")
