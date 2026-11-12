#!/usr/bin/env python3
"""Generate the jobs of stage 2 and the mirrors from the finished stage-1 circles of #573 and #574.
usage: python stage2_57x.py OUT.json [--mirrors]       (reads <RAW>/<task>/<circle>/res.jsonl)
Stage 2 (both tasks): a circle of R 0.06 on every zero position that a finished circle with winding 1, 2 or 3 reports (rec['zeros']), at the same kf, named k<K>_z_re<re>_im<im>; a zero reported by several overlapping circles gets one
circle (positions of the same kf closer than 0.03 in both Re and Im are one zero, taken at the estimate with the smallest error). --mirrors (#574): the mirror (Im -> -Im, same R 0.36) of every upper circle that winds nonzero, plus the two mirror controls at 2.35 - 1.25i and 3.35 - 1.25i, which
must wind as their upper twins."""
import glob, json, os, sys
RAW = "D:/choptuik-large-d-raw"


def finished(task):
    out = []
    for d in sorted(glob.glob(os.path.join(RAW, task, "k*"))):
        res = os.path.join(d, "res.jsonl")
        if os.path.exists(res) and os.path.getsize(res):
            out.append((os.path.basename(d), [json.loads(l) for l in open(res)][-1]))
    return out


jobs, cand = [], []
for task in ("I573-win2", "I574-win2"):
    for name, r in finished(task):
        if "_z_" in name or "mirror" in name or "mctl" in name:
            continue
        K = int(name.split("_")[0][1:])
        for (a, b), e in zip(r.get("zeros", []), r.get("zeros_est", [])):
            cand.append((K, a, b, e, task))
# one circle per zero: candidates of the same kf closer than 0.03 are one zero (the estimates of the position are 1e-5 to 3e-2), represented by the one with the smallest estimate
cand.sort(key=lambda c: c[3])
kept = []
for K, a, b, e, task in cand:
    if any(k == K and abs(a - x) < 0.03 and abs(b - y) < 0.03 for k, x, y, _, _ in kept):
        continue
    kept.append((K, a, b, e, task))
for K, a, b, e, task in sorted(kept):
    jobs.append(dict(task=task, name=f"k{K}_z_re{a:.4f}_im{b:+.4f}", K=K, re=round(a, 6), im=round(b, 6), R=0.06))
if "--mirrors" in sys.argv:
    for name, r in finished("I574-win2"):
        if "_z_" in name or "mirror" in name or "mctl" in name or abs(r["winding"]) < 0.5:
            continue
        c = r.get("centre") or None
        re_, im_ = (float(name.split("_re")[1].split("_")[0]), float(name.split("_im")[1]))
        jobs.append(dict(task="I574-win2", name=f"k27_mirror_re{re_:.2f}_im{-im_:+.2f}", K=27, re=re_, im=-im_, R=0.36))
    for re_ in (2.35, 3.35):
        jobs.append(dict(task="I574-win2", name=f"k27_mctl_re{re_:.2f}_im-1.25", K=27, re=re_, im=-1.25, R=0.36))
json.dump(jobs, open(sys.argv[1], "w"), indent=1)
print(len(jobs), "jobs written to", sys.argv[1])
for j in jobs:
    print(j["task"], j["name"], j["re"], j["im"], j["R"])
