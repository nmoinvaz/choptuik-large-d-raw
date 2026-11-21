#!/usr/bin/env python3
"""report1060w.py: #1060 step 2 on win2: the two runs step17_s1 and step17_s2 (leg 10's step 17, D 260.6706 -> 260.8483) against each other and against leg 10's stored step 17 (dh370, 1aa4a4fb, series_split 1).
Series s = the record's t_coef, corrector s = the sum of its attempts' t_corr, step s = the run's wall seconds from summary_1060.txt (it includes the base's polish and plan). Uses dh610's cmp1060.py (bits, files, close)."""
import json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)) + "/"
REFD = "D:/choptuik-large-d-raw-push/I966-dh370/ks_chain3b/leg10_D256.1776_ks293/"
PY = sys.executable


def cmp(*a):
    r = subprocess.run([PY, H + "cmp1060.py", *a], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def rec(path, step=None):
    if not os.path.exists(path):
        return None
    L = [json.loads(x) for x in open(path) if x.strip()]
    if not L:
        return None
    return L[-1] if step is None else next((r for r in L if r["step"] == step), None)


def times(r):
    if not r:
        return None
    at = r.get("attempts") or []
    a = at[-1] if at else {}
    return dict(a=a.get("a"), D=a.get("D_str"), accepted=a.get("accepted"), attempts=len(at), od_steps=a.get("steps"), Delta=a.get("Delta"),
                t_coef=r.get("t_coef"), t_corr=sum(x.get("t_corr", 0) for x in at))


ref = times(rec(REFD + "anm_run.jsonl", 17))
print(f"leg 10 step 17 on dh370 (1aa4a4fb build, --series_split 1): a {ref['a']!r}, D {ref['D']}, {ref['attempts']} attempt, {ref['od_steps']} od steps, series (t_coef) {ref['t_coef']:.0f} s, corrector {ref['t_corr']:.0f} s")
print()
summ = open(H + "summary_1060.txt").read() if os.path.exists(H + "summary_1060.txt") else ""
res = {}
print("| run | exit, wall (step s) | a | D | accepted, attempts, od steps | series s | corrector s | state vs leg 10 stored (bits) | series file vs leg 10 | prediction vs leg 10 |")
print("|---|---|---|---|---|---|---|---|---|---|")
for S in (1, 2):
    m = re.search(rf"step17_s{S}: expected exit 0, got (\d+), (\d+) s wall", summ)
    t = times(rec(H + f"step17_s{S}/anm_run.jsonl"))
    N = H + f"step17_s{S}/anm_pin3_D260.8483.npz"
    res[S] = dict(t=t, wall=int(m.group(2)) if m else None, N=N)
    if not m:
        print(f"| split {S} | not run | | | | | | | | |"); continue
    if not t or not os.path.exists(N):
        print(f"| split {S} | exit {m.group(1)}, {m.group(2)} s | no accepted state at D 260.8483 | | | | | | | |"); continue
    rb, tb = cmp("bits", REFD + "anm_pin3_D260.8483.npz", N)
    rj, tj = cmp("files", REFD + "jet_pin3_D260.6706.npz", H + f"step17_s{S}/jet_pin3_D260.6706.npz")
    rp, tp = cmp("files", REFD + "pred_pin3_D260.8483.npz", H + f"step17_s{S}/pred_pin3_D260.8483.npz")
    word = lambda r, tx: "identical" if r == 0 else "DIFFERENT: " + tx.splitlines()[0][:150]  # noqa: E731
    print(f"| split {S} | exit {m.group(1)}, {m.group(2)} s | {t['a']!r} | {t['D']} | {t['accepted']}, {t['attempts']}, {t['od_steps']} | {t['t_coef']:.0f} | {t['t_corr']:.0f} | {word(rb, tb)} | {word(rj, tj)} | {word(rp, tp)} |")
print()
t0, t2 = res[1]["t"], res[2]["t"]
if t0 and t2:
    same = (t0["a"] == t2["a"]) and (t0["D"] == t2["D"]) and t0["accepted"] and t2["accepted"]
    print(f"both accept the same a and D: {same} (split 1: a {t0['a']!r}, D {t0['D']}; split 2: a {t2['a']!r}, D {t2['D']})")
    if res[1]["wall"] and res[2]["wall"]:
        print(f"split 2 against split 1: step {res[2]['wall']}/{res[1]['wall']} = {res[2]['wall'] / res[1]['wall']:.3f}, series {t2['t_coef']:.0f}/{t0['t_coef']:.0f} = {t2['t_coef'] / t0['t_coef']:.3f}, corrector {t2['t_corr']:.0f}/{t0['t_corr']:.0f} = {t2['t_corr'] / t0['t_corr']:.3f}")
    n0, n2 = res[1]["N"], res[2]["N"]
    if os.path.exists(n0) and os.path.exists(n2):
        print("split 2 vs split 1, bits: " + cmp("bits", n0, n2)[1].replace("\n", " / ")[:600])
        print("split 2 vs split 1, close (tol 1e-100):")
        rc, txt = cmp("close", n0, n2, "--tol", "1e-100")
        for ln in txt.splitlines():
            print("    " + ln)
        m1 = [ln for ln in txt.splitlines() if ln.strip().startswith("M1 per part")]
        if m1:
            vals = re.findall(r"(zh|zl|z\d) ([0-9.]+e[+-]\d+|nan|0\.0e\+00)", m1[0])
            worst = max((float(v) for _, v in vals if v != "nan"), default=0.0)
            print(f"    the coordinator's reading (every state part within 1e-100 of its max, M1): worst part {worst:.2e}: {'PASS' if worst <= 1e-100 else 'FAIL'}; parts: " + ", ".join(f"{k} {v}" for k, v in vals))
        print(f"    cmp1060 close exit {rc} (Delta and M2 within 1e-100: {'agree' if rc == 0 else 'DISAGREE'})")
