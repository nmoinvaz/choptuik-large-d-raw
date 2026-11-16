#!/usr/bin/env python3
"""#892: the readings table from the raw folder's jsonl records.

    python3 read892.py RAW_FOLDER

Per prior-carrying state: the march's Delta and its width W (width.jsonl), the walk (walk_<n>.jsonl, up to 150 Jacobians),
the width at the walk's end (width_end.jsonl). Rules of the issue:
  prior-held : the walk ends 1e-3 or more from the march's Delta, or does not settle while Delta moves by more than 1e-3;
  prior-free : the walk ends within W (the march state's own) of the march's Delta, and the end's own W is at most 1e-4;
  otherwise undecided, with the walk's last |F|, Delta and rate.
The control (D 8.0, walk.jsonl) must stay within its W. Exit 1 when it does not, or a g pair disagrees.
"""
import json, os, sys

R = sys.argv[1]
STATES = [("up_9.0", "data/sigdss_m03up.npz@9.0", 9.0), ("up_10.0", "data/sigdss_m03up.npz@10.0", 10.0),
          ("up_10.5", "data/sigdss_m03up.npz@10.5", 10.5), ("hi_10.5", "data/sigdss_m03hi.npz@10.5", 10.5),
          ("hi_11.0", "data/sigdss_m03hi.npz@11.0", 11.0)]


def jl(path):
    return [json.loads(l) for l in open(os.path.join(R, path)) if l.strip()] if os.path.exists(os.path.join(R, path)) else []


width = {r["state"]: r for r in jl("width.jsonl")}
wend = {}
for r in jl("width_end.jsonl"):
    wend[r["state"]] = r
bad = []
ctrl = jl("walk.jsonl")
w8 = width.get("data/sigdss_m03up.npz@8.0")
if ctrl and w8:
    c = ctrl[-1]
    mv = abs(c["Delta"] - w8["Delta"])
    print(f"control D 8.0: {len(c['hist'])} Jacobians ({'settled' if c['settled'] else 'stalled' if c['stalled'] else 'not settled'}), "
          f"Delta moved {mv:.3e} against W {w8['W']:.3e}: {'within W' if mv <= w8['W'] else 'MOVED BY MORE THAN W'}")
    if mv > w8["W"]:
        bad.append("control moved Delta by more than W")
print()
print("| state | Delta (march) | \\|F\\| (march) | W (march) | Jacobians | end | Delta (end) | Delta end - march | \\|F\\| (end) | W (end) | rate per Jacobian (last, mean of last 10) | reading |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for n, spec, D in STATES:
    w = width.get(spec)
    ws = jl(f"walk_{n}.jsonl")
    if not w or not ws:
        print(f"| {spec} | not run yet |"); continue
    k = ws[-1]
    h = k["hist"]
    mv = k["Delta"] - w["Delta"]
    e = wend.get(f"{R}/walk_{n}.npy") or wend.get(os.path.join(R, f"walk_{n}.npy"))
    We = e["W"] if e else None
    end = "settled" if k["settled"] else "stalled" if k["stalled"] else f"not settled ({len(h)} Jacobians)"
    last = h[-1]["dDelta"]
    mean10 = sum(x["dDelta"] for x in h[-10:]) / len(h[-10:])
    if abs(mv) >= 1e-3 or (not k["settled"] and not k["stalled"] and abs(mv) > 1e-3):
        rd = "prior-held"
    elif abs(mv) <= w["W"] and We is not None and We <= 1e-4:
        rd = "prior-free"
    else:
        rd = f"undecided (last |F| {k['F']:.3e}, Delta {k['Delta']:.9f}, rate {last:+.2e} per Jacobian)"
    if e is not None and not e["agree"]:
        bad.append(f"g pair at the end of {n} disagrees")
    print(f"| {spec} | {w['Delta']:.9f} | {w['F']:.2e} | {w['W']:.2e} | {len(h)} | {end} | {k['Delta']:.9f} | {mv:+.3e} | {k['F']:.2e} | "
          f"{('%.2e' % We) if We is not None else 'n/a'} | {last:+.2e}, {mean10:+.2e} | {rd} |")
for s, r in width.items():
    if not r["agree"]:
        bad.append(f"g pair disagrees at the march state {s}: {r['g_svd']:.6e} against {r['g_solve']:.6e}")
print()
print("flags:", "; ".join(bad) if bad else "none")
sys.exit(1 if bad else 0)
