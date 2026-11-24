"""summarize a probe.py log: the steps of each solve (residual before and after, contraction, the Jacobian's kind,
accepted or not) and each refresh (max|r| there, whether the fresh step has the stale step's bits, how many ulps apart,
the relative change of J). Steps are the residual calls that follow a linear solve; the others are Jacobian columns or
the solve's first call."""
import json
import sys

ev = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
rows = []
cur = None
first_lu = True
pending = None          # the last lu event, waiting for its step's residual call
for e in ev:
    if e["ev"] == "res":
        if cur is None or e["dps"] != cur["dps"]:
            cur = dict(dps=e["dps"], calls=0, steps=[], start=None, n=None)
            rows.append(cur)
        cur["calls"] += 1
        if cur["start"] is None:
            cur["start"] = float(e["maxr"])
            cur["n"] = float(e["maxr"])
            continue
        if pending is not None:
            n0, n1 = float(pending["n0"]), float(e["maxr"])
            acc = n1 < n0
            cur["steps"].append(dict(call=cur["calls"], n0=n0, n1=n1, ratio=n1 / n0, J="fresh" if pending.get("fresh") else "chord",
                                     accepted=acc, refresh=pending.get("refresh_info")))
            pending = None
    elif e["ev"] == "lu":
        pending = dict(n0=e["n0"], fresh=e["refresh"] or first_lu, dv_ulps=e.get("dv_ulps"))
        first_lu = False
    elif e["ev"] == "refresh":
        if pending is not None:
            pending["fresh"] = True
            pending["refresh_info"] = dict(same_bits=e["same_bits"], dvn_ulps=e["dvn_ulps"], dJ_rel=e["dJ_rel"])
    elif e["ev"] == "row":
        row = e["row"]
for s in rows:
    print(f"dps {s['dps']}: {s['calls']} calls, start max|r| {s['start']:.3g}")
    for st in s["steps"]:
        ri = st["refresh"]
        extra = "" if ri is None else f"  [after a refresh: fresh step's bits {'= ' if ri['same_bits'] else '!= '}stale step's, {ri['dvn_ulps']} ulps apart, |dJ|/|J| {ri['dJ_rel']}]"
        print(f"  call {st['call']:2d}: {st['n0']:.3e} -> {st['n1']:.3e} ({st['ratio']:.2g}) {st['J']:5s} {'accepted' if st['accepted'] else 'FAILED'}{extra}")
if "row" in globals():
    print("row:", json.dumps({k: row.get(k) for k in ("re", "im", "sig", "info", "F3re", "F3im", "calls", "seconds")}))
