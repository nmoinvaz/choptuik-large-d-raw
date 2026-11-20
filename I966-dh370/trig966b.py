#!/usr/bin/env python3
"""#966 (fallback leg at ks 293, coordinator hc 2026-11-20 after leg 11 capped): for the newest accepted step of the newest leg
REPORT AND WAIT (no restart) on: a refused attempt; two steps in a row at 3 or more corrections (od steps - 1); a at or below 0.05.
RAISE (restart at ks 315, 3 h cap, --ks_retry 3 via restart966p.sh) when the accepted D is 262.0 or more; the other raise condition, dh170's #1057 read
showing the classified Delta share at 0.9 or more again, is read from #1057 by hand. The a_max < 0.5 and tail > 1e-18 lines are printed but no longer trigger.
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
last = rows[-1]; fired = []; raise_ = []
if last["refused"]: fired.append("a refused attempt")
if len(rows) > 1 and last["corr"] >= 3 and rows[-2]["corr"] >= 3: fired.append(f"two steps in a row at 3+ corrections ({rows[-2]['step']}: {rows[-2]['corr']}, {last['step']}: {last['corr']})")
if last["a"] <= 0.05: fired.append(f"a {last['a']} <= 0.05")
if float(last["D"]) >= 262.0 - 1e-9: raise_.append(f"accepted D {last['D']} >= 262.0")
for f in fired: print("TRIGGER (report and wait):", f)
for f in raise_: print("RAISE (restart at ks 315):", f)
if not fired and not raise_: print("no trigger")
print(f"info: a_max {last['a_max']}, tail {last['tail']}")
nxt = max(seg)
if nxt > last["step"]:
    print(f"preview (in flight) step {nxt}: base D {seg[nxt]['D']}, a_max {seg[nxt]['a_max']}, tail {tails[nxt]}")
