#!/usr/bin/env python3
"""report1060.py: #1060's report from step17_s0/ (the split-2 A/B is win2's): the step's a, D, series, corrector and wall seconds against leg 10's step 17 (dh370, I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_run.jsonl),
and cmp1060.py's readings: each run's accepted state, series (jet_pin3_D260.6706.npz) and prediction (pred_pin3_D260.8483.npz) against leg 10's byte for byte (bits, files), then S = 2 and S = 0 against S = 1
(bits, and close for the agreement to 1e-100)."""
import json
import os
import re
import subprocess
import sys

H = os.path.dirname(os.path.abspath(__file__)) + "/"
REFD = os.path.expanduser("~/Source/choptuik-large-d-raw/I966-dh370/ks_chain3b/leg10_D256.1776_ks293/")
PY = sys.executable


def cmp(*a):
    r = subprocess.run([PY, H + "cmp1060.py", *a], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def rec(path, step=None):
    if not os.path.exists(path):
        return None
    L = [json.loads(x) for x in open(path) if x.strip()]
    return (L[-1] if step is None else next(r for r in L if r["step"] == step)) if L else None


def times(r):
    if not r:
        return None
    at = r.get("attempts") or []
    a = at[-1] if at else {}
    return dict(a=a.get("a"), D=a.get("D_str"), accepted=a.get("accepted"), attempts=len(at), od_steps=a.get("steps"), t_coef=r.get("t_coef"), t_corr=sum(x.get("t_corr", 0) for x in at))


ref = times(rec(REFD + "anm_run.jsonl", 17))
print("leg 10 step 17 on dh370 (1aa4a4fb build, --series_split 1): " + (f"a {ref['a']!r}, D {ref['D'][:14]}, {ref['attempts']} attempt, {ref['od_steps']} od steps, series (t_coef) {ref['t_coef']:.0f} s, corrector {ref['t_corr']:.0f} s" if ref else "no record"))
print()
summ = open(H + "summary_1060.txt").read() if os.path.exists(H + "summary_1060.txt") else ""
print("| run | exit, wall | a | D | attempts, od steps | series s | corrector s | state vs leg 10 (bits) | series file vs leg 10 | prediction vs leg 10 |")
print("|---|---|---|---|---|---|---|---|---|---|")
for S in (0,):
    m = re.search(rf"step17_s{S}: exit (\d+), (\d+) s wall", summ)
    t = times(rec(H + f"step17_s{S}/anm_run.jsonl"))
    N = H + f"step17_s{S}/anm_pin3_D260.8483.npz"
    if not m:
        print(f"| split {S} | not run | | | | | | | | |")
        continue
    if not t or not os.path.exists(N):
        print(f"| split {S} | exit {m.group(1)}, {m.group(2)} s | no accepted state at D 260.8483 | | | | | | | |")
        continue
    rb, tb = cmp("bits", REFD + "anm_pin3_D260.8483.npz", N)
    rj, tj = cmp("files", REFD + "jet_pin3_D260.6706.npz", H + f"step17_s{S}/jet_pin3_D260.6706.npz")
    rp, tp = cmp("files", REFD + "pred_pin3_D260.8483.npz", H + f"step17_s{S}/pred_pin3_D260.8483.npz")
    word = lambda r, tx: "identical" if r == 0 else "DIFFERENT: " + re.sub(r"^.*?(parts with differing bytes|differing bytes)", r"\1", tx.splitlines()[0])[:150]  # noqa: E731
    print(f"| split {S} | exit {m.group(1)}, {m.group(2)} s | {t['a']!r} | {t['D'][:14]} | {t['attempts']}, {t['od_steps']} | {t['t_coef']:.0f} | {t['t_corr']:.0f} | {word(rb, tb)} | {word(rj, tj)} | {word(rp, tp)} |")
