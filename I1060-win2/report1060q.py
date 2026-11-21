#!/usr/bin/env python3
"""report1060q.py: #1060's two controls after parts 1 to 3.
(1) series_split_check.py at the D 260.6706 state with --N 31 (split2_D260_N31.log): d_split per order against the check's 5.5e-35, orders past 24 apart.
(2) the step 17 A/B with --keep_plan 1 (step17_k1_s1, step17_k1_s2): a, D, od steps, series s, corrector s, step s, S = 2 against S = 1 by cmp1060 close, and the
    saved series per order (series_agree_k1_s1_s2.txt) against the check's 5.5e-35; the S = 1 series against the keep_plan 0 S = 1's (information).
The readings (the coordinator's, fixed before the runs): (1) d_split above 5.5e-35 at orders past 24 -> the check missed it by its order count;
(2) per-order differences at or below 5.5e-35 at all orders -> the re-plan at the base is the cause; neither -> the base polish before the series is the last named candidate."""
import json
import os
import re
import subprocess
import sys

H = os.path.dirname(os.path.abspath(__file__)) + "/"
PY = sys.executable
BAR = 5.5e-35


def cmp(*a):
    r = subprocess.run([PY, H + "cmp1060.py", *a], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def rec(path):
    if not os.path.exists(path):
        return None
    L = [json.loads(x) for x in open(path) if x.strip()]
    if not L:
        return None
    r = L[-1]
    at = r.get("attempts") or []
    a = at[-1] if at else {}
    return dict(a=a.get("a"), D=a.get("D_str"), accepted=a.get("accepted"), attempts=len(at), od=a.get("steps"),
                t_coef=r.get("t_coef"), t_corr=sum(x.get("t_corr", 0) for x in at))


def wall(summ, name):
    m = re.search(name + r": expected exit 0, got (\d+), (\d+) s wall", summ)
    return (m.group(1), int(m.group(2))) if m else (None, None)


def orders(fname):
    out = []
    for line in open(H + fname):
        if line.strip().startswith("order"):
            k = int(re.search(r"order\s+(\d+)", line).group(1))
            v = float(re.search(r"= ([0-9.e+-]+) \(", line).group(1))
            out.append((k, v))
    return out


summ = open(H + "summary_1060.txt").read() if os.path.exists(H + "summary_1060.txt") else ""

# ---- (1)
print("## (1) series_split_check.py at D 260.6706 with --N 31")
v1 = None
f = H + "split2_D260_N31.log"
if os.path.exists(f):
    L = open(f).read().splitlines()
    rows = []
    for line in L:
        m = re.match(r"\s*(\d+)\s+([0-9.e+-]+)\s+([0-9.e+-]+)\s+([0-9.e+-]+)\s+([0-9.e+-]+)", line)
        if m:
            rows.append((int(m.group(1)), float(m.group(3)), float(m.group(4)), float(m.group(5))))
    for line in L:
        if "newton_o" in line or line.strip().startswith("N ") or "PASS" in line or "FAIL" in line:
            print("    " + line.strip()[:240])
    print("    d_split per order (k: d_split, d_split/(1e3 d_oa)): " + ", ".join("%d: %.2e, %.1e" % (k, d, t) for k, d, _, t in rows))
    past = [(k, d) for k, d, _, _ in rows if k > 24]
    upto = [(k, d) for k, d, _, _ in rows if 3 <= k <= 24]
    if past:
        above = [(k, d) for k, d in past if d > BAR]
        print("    orders past 24 (k = %d to %d): d_split from %.2e to %.2e; above %.1e: %s" % (
            past[0][0], past[-1][0], min(d for _, d in past), max(d for _, d in past), BAR,
            ", ".join("%d (%.2e)" % x for x in above) if above else "none"))
        print("    orders 3 to 24: d_split from %.2e to %.2e; above %.1e: %s" % (
            min(d for _, d in upto), max(d for _, d in upto), BAR,
            ", ".join("%d (%.2e)" % x for x in upto if x[1] > BAR) or "none"))
        v1 = bool(above)
        print("    READING (1): " + ("d_split above 5.5e-35 at orders past 24: the check missed the gap by its order count" if v1
                                     else "d_split at or below 5.5e-35 at all orders past 24: the check did not miss it by its order count"))
    else:
        print("    no orders past 24 in the log (the check did not finish?)")
else:
    print("    no split2_D260_N31.log")

# ---- (2)
print()
print("## (2) the step 17 A/B with --keep_plan 1")
print("| run | exit, step s | a | D | accepted, attempts, od steps | series s | corrector s |")
print("|---|---|---|---|---|---|---|")
for S in (1, 2):
    name = "step17_k1_s%d" % S
    ex, w = wall(summ, name)
    t = rec(H + name + "/anm_run.jsonl")
    if ex is None or not t:
        print("| %s | not run or no record | | | | | |" % name)
        continue
    print("| %s (--keep_plan 1) | exit %s, %d s | %r | %s | %s, %d, %s | %.0f | %.0f |" % (
        name, ex, w, t["a"], t["D"][:20], t["accepted"], t["attempts"], t["od"], t["t_coef"], t["t_corr"]))
print("for comparison (--keep_plan 0, the first A/B): S = 1 622 s, series 139 s, corrector 377 s, 4 od steps; S = 2 703 s, series 112 s, corrector 495 s, 5 od steps")
n1, n2 = H + "step17_k1_s1/anm_pin3_D260.8483.npz", H + "step17_k1_s2/anm_pin3_D260.8483.npz"
if os.path.exists(n1) and os.path.exists(n2):
    print("k1: S = 2 vs S = 1, bits: " + cmp("bits", n1, n2)[1].replace("\n", " / ")[:500])
    rc, txt = cmp("close", n1, n2, "--tol", "1e-100")
    print("k1: S = 2 vs S = 1, close (tol 1e-100): " + " / ".join(x.strip() for x in txt.splitlines()))
v2 = None
for fn in ("series_agree_k1_s1_s2.txt", "series_agree_s1_kp0_vs_kp1.txt"):
    if os.path.exists(H + fn):
        vals = orders(fn)
        print(fn + ": " + open(H + fn).read().splitlines()[0][:130])
        if vals:
            print("    per order max |dS| / max |S|: " + ", ".join("%d:%.1e" % (k, v) for k, v in vals))
            print("    orders above the check's %.1e: %d of %d; worst %.3e" % (BAR, len([1 for _, v in vals if v > BAR]), len(vals), max(v for _, v in vals)))
            if fn == "series_agree_k1_s1_s2.txt":
                v2 = max(v for _, v in vals) <= BAR
if v2 is not None:
    print("    READING (2): " + ("per-order differences at or below 5.5e-35 at all orders: the re-plan at the base is the cause" if v2
                                 else "per-order differences above 5.5e-35: the re-plan at the base is not (the whole) cause"))
print()
if v1 is None and v2 is None:
    print("WHICH: not determined (a control did not finish)")
elif v1:
    print("WHICH: (1) the check missed it by its order count" + ("" if not v2 else "; and (2) also at or below the check's level with keep_plan 1"))
elif v2:
    print("WHICH: (2) the re-plan at the base is the cause")
else:
    print("WHICH: neither: the base polish before the series is the last named candidate")
