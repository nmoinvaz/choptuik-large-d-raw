#!/usr/bin/env python3
"""score_leg.py: the numbers of the k_c 103 leg's points from the files (states/l1kc103Lmacm3.jsonl, leg_points.txt, leg_STOP.txt, exits_leg103.txt, mem_samples.csv, leap.log) for the README scoring.
usage: score_leg.py [--mutate=delta]   (the mutation shifts Delta by +1e-3: the 'Delta in range' line must then read False)"""
import csv, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(H + "/states/l1kc103Lmacm3.jsonl") if l.strip()]
seedB = json.loads(open(H + "/leg_seedB.jsonl").read()); seedA = json.loads(open(H + "/leg_seedA.jsonl").read())
for r in rows:
    if "--mutate=delta" in sys.argv: r["Delta"] += 1e-3
    prev = seedB if r is rows[0] else rows[rows.index(r) - 1]
    sl = (r["Delta"] - prev["Delta"]) / (r["D"] - prev["D"])
    w = sorted(range(4), key=lambda i: -r["cos_t_reg"][i])[0]
    print("D %r: Delta %.12f (Delta_pred %.12f), dDelta/dD %.6f, |F| %.4e (F_start %.3e), steps %d, psi-constraint %.4e, n_null %d, h %g, leap seconds %d, tan_norm %.4f" % (r["D"], r["Delta"], r["Delta_pred"], sl, r["F"], r["F_start"], r["steps"], r["constraint"], r["n_null"], r["h"], r["seconds"], r["tan_norm"]))
    print("  weak regular values %s, tangent cosines %s (largest on the regular mode #%d), delta_reg %s" % (["%.4e" % v for v in r["sv_reg_small"]], ["%.4f" % v for v in r["cos_t_reg"]], w + 1, ["%.4f" % v for v in r["delta_reg"]]))
    print("  seeds' slope dDelta/dD %.6f (A to B); Delta in [1.17612, 1.17624]: %s; dDelta/dD in [0.0292, 0.0300]: %s; constraint in (4.9e-3, 5.8e-3): %s, below 1e-2: %s; steps within 15 of 3391: %s; |F| <= 5e-10: %s; n_null == 95: %s, within 2: %s; seconds in [2000, 6000]: %s" % (
        (seedB["Delta"] - seedA["Delta"]) / (seedB["D"] - seedA["D"]), 1.17612 <= r["Delta"] <= 1.17624, 0.0292 <= sl <= 0.0300, 4.9e-3 < r["constraint"] < 5.8e-3, r["constraint"] < 1e-2, abs(r["steps"] - 3391) <= 15, r["F"] <= 5e-10, r["n_null"] == 95, abs(r["n_null"] - 95) <= 2, 2000 <= r["seconds"] <= 6000))
print("STOP file: " + (open(H + "/leg_STOP.txt").readline().strip() if os.path.exists(H + "/leg_STOP.txt") else "none"))
lg = open(H + "/exits_leg103.txt").read()
m = re.search(r"leap exit (\d+) wall (\d+) s.*?Tracebacks in leap.log: (\d+)", lg)
print("leap exit %s (137 = killed by the guard's exact-pid stop), wall %s s, Tracebacks %s, halvings: %s" % (m.group(1), m.group(2), m.group(3), "none (h stays %g)" % rows[-1]["h"] if all(r["h"] == 0.0625 for r in rows) else "SEE leap.log"))
av, lr = [], 0
for r in csv.DictReader(open(H + "/mem_samples.csv")):
    av.append(float(r["avail_GiB"])); lr = max(lr, int(r["leap_rss_kb"]))
print("memory: %d samples, lowest available %.1f GiB, peak RSS of the leap %.2f GiB, alert.log exists: %s" % (len(av), min(av), lr / 2**20, os.path.exists(H + "/alert.log")))
