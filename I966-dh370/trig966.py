#!/usr/bin/env python3
"""#966: the coordinator's early-restart triggers (hc 2026-11-20) for the newest accepted step of the newest leg:
a_max < 0.5, tail e_N+1 > 1e-18, a refused attempt, or two steps in a row at 3 or more corrections (od steps - 1).
usage: python3 -I trig966.py [CHAIN_OUT]     prints one row per step (last 3) and 'TRIGGER: ...' lines, exit 0 always;
the in-flight step's header values are shown as 'preview' (not a trigger)."""
import glob, json, re, sys
out = sys.argv[1] if len(sys.argv) > 1 else "ks_chain3b"
leg = sorted(glob.glob(out + "/leg*/"))[-1]
log = open(leg + "anm_run.log").read()
recs = [json.loads(l) for l in open(leg + "anm_run.jsonl") if l.strip()]
seg = {}
for m in re.finditer(r"^step (\d+): D ([0-9.]+),.*?a_max ([0-9.]+)", log, re.M):
    seg[int(m.group(1))] = dict(D=m.group(2), a_max=float(m.group(3)), pos=m.start())
tails = {}
for n, d in seg.items():
    m = re.search(r"a_rule reseed: a_h tail e_N\+1 ([0-9.e+-]+)", log[d["pos"]:])
    tails[n] = float(m.group(1)) if m else None
rows = []
for r in recs:
    n = r["step"]; a = r["attempts"][-1]
    txt = log[seg[n]["pos"]: seg[n + 1]["pos"]] if n + 1 in seg else log[seg[n]["pos"]:]
    refused = (len(r["attempts"]) > 1) or bool(re.search(r"re-seeded \(FAILED|attempt stopped|no trial step accepted|stopping \(stalled\)", txt))
    rows.append(dict(step=n, D=a["D_str"][:10], a=round(a["a"], 4), a_max=seg[n]["a_max"], tail=tails[n], corr=a["steps"] - 1,
                     t_corr=round(a["t_corr"]), refused=refused, accepted=bool(r.get("converged"))))
for x in rows[-3:]:
    print(x)
last = rows[-1]; fired = []
if last["a_max"] < 0.5: fired.append(f"a_max {last['a_max']} < 0.5")
if last["tail"] is not None and last["tail"] > 1e-18: fired.append(f"tail e_N+1 {last['tail']:.2e} > 1e-18")
if last["refused"]: fired.append("a refused attempt")
if len(rows) > 1 and last["corr"] >= 3 and rows[-2]["corr"] >= 3: fired.append(f"two steps in a row at 3+ corrections ({rows[-2]['step']}: {rows[-2]['corr']}, {last['step']}: {last['corr']})")
for f in fired: print("TRIGGER:", f)
if not fired: print("no trigger")
nxt = max(seg)
if nxt > last["step"]:
    print(f"preview (in flight) step {nxt}: base D {seg[nxt]['D']}, a_max {seg[nxt]['a_max']}, tail {tails[nxt]}")
