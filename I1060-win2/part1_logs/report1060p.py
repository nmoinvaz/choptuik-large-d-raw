#!/usr/bin/env python3
"""report1060p.py PART: #1060's parts 1 and 2 after the controls.
PART 1: step15_s<S>, step16_s<S> (S = 1, 2) from leg 10's steps 15 and 16.
PART 2: step17_t0_s<S> (--jet_tangent_from 0).
Per run: a, D, accepted, attempts, od steps, series s (t_coef), corrector s (sum of t_corr), step s (the run's wall seconds);
S = 2 against S = 1 by cmp1060.py (bits, close tol 1e-100); against the stored next state of leg 10 (information)."""
import json
import os
import re
import subprocess
import sys

H = os.path.dirname(os.path.abspath(__file__)) + "/"
REFD = "D:/choptuik-large-d-raw-push/I966-dh370/ks_chain3b/leg10_D256.1776_ks293/"
PY = sys.executable
part = int(sys.argv[1])


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
    return dict(step=r.get("step"), a=a.get("a"), D=a.get("D_str"), accepted=a.get("accepted"), attempts=len(at),
                od=a.get("steps"), t_coef=r.get("t_coef"), t_corr=sum(x.get("t_corr", 0) for x in at))


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

if part == 1:
    nxt = {15: "anm_pin3_D260.4708.npz", 16: "anm_pin3_D260.6706.npz"}
    print("leg 10 on dh370 (1aa4a4fb, split 1, 10 threads): step 15 a 0.21931277659360876, D 260.47082389, 4 od steps, "
          "series 394 s, corrector 1614 s; step 16 a 0.19978558306115476, D 260.67060947, 3 od steps, series 396 s, "
          "corrector 1534 s")
    print()
    print("| state | run | exit, step s | a | D | accepted, attempts, od steps | series s | corrector s | "
          "state vs leg 10 stored next state (bits) |")
    print("|---|---|---|---|---|---|---|---|---|")
    out = {}
    for k in (15, 16):
        for S in (1, 2):
            name = "step%d_s%d" % (k, S)
            ex, w = wall(summ, name)
            t = rec(H + name + "/anm_run.jsonl")
            out[(k, S)] = (t, w)
            if ex is None or not t:
                print("| step %d | S = %d | not run or no record | | | | | | |" % (k, S))
                continue
            N = H + name + "/" + nxt[k]
            word = "no state file"
            if os.path.exists(N):
                rb, tb = cmp("bits", REFD + nxt[k], N)
                word = "identical" if rb == 0 else "DIFFERENT: " + tb.splitlines()[0][-160:]
            print("| step %d | S = %d | exit %s, %d s | %r | %s | %s, %d, %s | %.0f | %.0f | %s |" % (
                k, S, ex, w, t["a"], t["D"][:20], t["accepted"], t["attempts"], t["od"], t["t_coef"], t["t_corr"], word))
    print()
    more = []
    equal = []
    for k in (15, 16):
        (t1, w1), (t2, w2) = out[(k, 1)], out[(k, 2)]
        if not (t1 and t2):
            continue
        same = t1["a"] == t2["a"] and t1["D"] == t2["D"]
        line = ("step %d: same a and D by S = 1 and 2: %s; od steps S = 1 %s, S = 2 %s; series %.0f/%.0f = %.3f; "
                "corrector %.0f/%.0f = %.3f") % (
            k, same, t1["od"], t2["od"], t2["t_coef"], t1["t_coef"], t2["t_coef"] / t1["t_coef"],
            t2["t_corr"], t1["t_corr"], t2["t_corr"] / t1["t_corr"])
        if w1 and w2:
            line += "; step %d/%d = %.3f" % (w2, w1, w2 / w1)
        print(line)
        n1, n2 = H + "step%d_s1/%s" % (k, nxt[k]), H + "step%d_s2/%s" % (k, nxt[k])
        if os.path.exists(n1) and os.path.exists(n2):
            rc, txt = cmp("close", n1, n2, "--tol", "1e-100")
            print("    S = 2 vs S = 1 close (information): " + " / ".join(x.strip() for x in txt.splitlines()))
        more.append(t2["od"] > t1["od"])
        equal.append(t2["od"] == t1["od"])
    if len(more) == 2:
        if all(more):
            verdict = ("S = 2 took MORE od steps than S = 1 at BOTH states: split 2 costs a corrector step "
                       "systematically (the coordinator's reading)")
        elif all(equal):
            verdict = "equal od steps at both states: step 17 was chance (the coordinator's reading)"
        else:
            verdict = "neither reading: " + "; ".join(
                "step %d: S = 1 %s, S = 2 %s" % (k, out[(k, 1)][0]["od"], out[(k, 2)][0]["od"]) for k in (15, 16)
            ) + " (step 17: S = 1 4, S = 2 5)"
        print()
        print("READING: " + verdict)
else:
    print("| run | exit, step s | a | D | accepted, attempts, od steps | series s | corrector s |")
    print("|---|---|---|---|---|---|---|")
    for S in (1, 2):
        name = "step17_t0_s%d" % S
        ex, w = wall(summ, name)
        t = rec(H + name + "/anm_run.jsonl")
        if ex is None or not t:
            print("| %s | not run or no record | | | | | |" % name)
            continue
        print("| %s (--jet_tangent_from 0) | exit %s, %d s | %r | %s | %s, %d, %s | %.0f | %.0f |" % (
            name, ex, w, t["a"], t["D"][:20], t["accepted"], t["attempts"], t["od"], t["t_coef"], t["t_corr"]))
    print()
    print("for comparison (--jet_tangent_from 1, the A/B): S = 1 622 s, series 139 s, corrector 377 s, 4 od steps; "
          "S = 2 703 s, series 112 s, corrector 495 s, 5 od steps")
    n1, n2 = H + "step17_t0_s1/anm_pin3_D260.8483.npz", H + "step17_t0_s2/anm_pin3_D260.8483.npz"
    if os.path.exists(n1) and os.path.exists(n2):
        print("t0: S = 2 vs S = 1, bits: " + cmp("bits", n1, n2)[1].replace("\n", " / ")[:500])
        rc, txt = cmp("close", n1, n2, "--tol", "1e-100")
        print("t0: S = 2 vs S = 1, close (tol 1e-100): " + " / ".join(x.strip() for x in txt.splitlines()))
    for f in ("series_agree_t0_s1_s2.txt", "series_agree_s1_t1_vs_t0.txt"):
        if os.path.exists(H + f):
            vals = orders(f)
            print(f + ": " + open(H + f).read().splitlines()[0][:130])
            if vals:
                print("    per order max |dS| / max |S|: " + ", ".join("%d:%.1e" % (k, v) for k, v in vals))
                above = [v for _, v in vals if v > 5.5e-35]
                print("    orders above the check's 5.5e-35: %d of %d; worst %.3e" % (
                    len(above), len(vals), max(v for _, v in vals)))
    if os.path.exists(H + "series_agree_t0_s1_s2.txt"):
        vals = orders("series_agree_t0_s1_s2.txt")
        if vals:
            w = max(v for _, v in vals)
            print()
            if w <= 5.5e-35:
                print("READING: every per-order difference at or below the check's 5.5e-35: "
                      "the larger gap comes from the tangent_from 1 path")
            else:
                print("READING: per-order differences up to %.2e, above the check's 5.5e-35: "
                      "series_split_check does not cover part of the pipeline" % w)
