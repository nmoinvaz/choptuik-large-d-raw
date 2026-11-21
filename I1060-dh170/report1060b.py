#!/usr/bin/env python3
"""report1060b.py: #1060's base-polish-off rerun (--base_polish 0), the report from step17_s1_nobp/; the readings are the coordinator's (21 Nov), see reading(). From step17_s1/ (leg 10's own --series_split 1; the split-2 A/B is win2's): the step's a, D, series, corrector and wall seconds against leg 10's step 17 (dh370, I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_run.jsonl),
and cmp1060.py's readings: each run's accepted state, series (jet_pin3_D260.6706.npz) and prediction (pred_pin3_D260.8483.npz) against leg 10's byte for byte (bits, files), then S = 2 and S = 0 against S = 1
(bits, and close for the agreement to 1e-100)."""
import json
import os
import re
import subprocess
import sys

H = os.path.dirname(os.path.abspath(__file__)) + "/"
REFD = os.path.expanduser("~/scratch1060/raw/I966-dh370/ks_chain3b/leg10_D256.1776_ks293/")   # dh170: leg 10's blobs from raw origin/main bd0c3b93 (path only changed)
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


def reading(rb, row0):
    """rb: exit of cmp1060.py bits (0: D_str, a, Delta and the exactly summed parts equal); row0: entries of this run's series row 0 that differ from the stored base"""
    if rb == 0:
        return "equal bits with --base_polish 0: the 1.188e-20 of step 1 came from the base polish, so main's build reproduces dh370's chain."
    if row0 == 0:
        return "unequal bits with the base unmoved (series row 0 equals the stored base): the build (1aa4a4fb python on a 40f4b4a5 kernel against main 8179068d) or the platform."
    return f"unequal bits and the base moved even with --base_polish 0 ({row0} entries of series row 0 differ): neither reading applies, reported as it is."


if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
    brk = "--break" in sys.argv
    cases = [(0, 0, "came from the base polish"), (1, 0, "or the platform"), (1, 64, "neither reading applies")]
    bad = 0
    for rb, r0, want in cases:
        got = reading(rb, r0)
        ok = (want in got) != (brk and rb == 1 and r0 == 0)
        print(f"  cmp exit {rb}, row 0 differs in {r0}: {'ok' if ok else 'WRONG'}: {got[:90]}")
        bad += not ok
    print("selftest", "FAIL" if bad else "PASS")
    sys.exit(1 if bad else 0)


ref = times(rec(REFD + "anm_run.jsonl", 17))
print("leg 10 step 17 on dh370 (1aa4a4fb build, --series_split 1): " + (f"a {ref['a']!r}, D {ref['D'][:14]}, {ref['attempts']} attempt, {ref['od_steps']} od steps, series (t_coef) {ref['t_coef']:.0f} s, corrector {ref['t_corr']:.0f} s" if ref else "no record"))
print()
summ = open(H + "summary_1060b.txt").read() if os.path.exists(H + "summary_1060b.txt") else ""
print("| run | exit, wall | a | D | attempts, od steps | series s | corrector s | state vs leg 10 (bits) | series file vs leg 10 | prediction vs leg 10 |")
print("|---|---|---|---|---|---|---|---|---|---|")
for S in (1,):
    m = re.search(rf"step17_s{S}_nobp: exit (\d+), (\d+) s wall", summ)
    t = times(rec(H + f"step17_s{S}_nobp/anm_run.jsonl"))
    N = H + f"step17_s{S}_nobp/anm_pin3_D260.8483.npz"
    if not m:
        print(f"| split {S} --base_polish 0 | not run | | | | | | | | |")
        continue
    if not t or not os.path.exists(N):
        print(f"| split {S} --base_polish 0 | exit {m.group(1)}, {m.group(2)} s | no accepted state at D 260.8483 | | | | | | | |")
        continue
    rb, tb = cmp("bits", REFD + "anm_pin3_D260.8483.npz", N)
    rj, tj = cmp("files", REFD + "jet_pin3_D260.6706.npz", H + f"step17_s{S}_nobp/jet_pin3_D260.6706.npz")
    rp, tp = cmp("files", REFD + "pred_pin3_D260.8483.npz", H + f"step17_s{S}_nobp/pred_pin3_D260.8483.npz")
    def word(r, tx):
        if r == 0 and "differing bytes none" in tx:
            return "identical"
        ex = [x for x in tx.splitlines() if "exactly summed" in x or "differing bytes" in x]
        return ("identical in exact sums, bytes differ" if r == 0 else "DIFFERENT") + ": " + "; ".join(x.strip()[:140] for x in ex)
    print(f"| split {S} --base_polish 0 | exit {m.group(1)}, {m.group(2)} s | {t['a']!r} | {t['D'][:14]} | {t['attempts']}, {t['od_steps']} | {t['t_coef']:.0f} | {t['t_corr']:.0f} | {word(rb, tb)} | {word(rj, tj)} | {word(rp, tp)} |")
    print()
    print("cmp1060.py bits, leg 10's step 17 state against this run's (verdict: D_str, a, Delta and the exactly summed parts; bytes and M1 are information):")
    print(tb)
    print()
    rs = subprocess.run([PY, H + "seriesdiff1060.py", REFD.rstrip("/"), H + f"step17_s{S}_nobp"], capture_output=True, text=True)
    print("series and prediction against leg 10's, by order (seriesdiff1060.py, information; its own controls first):")
    print(rs.stdout.strip() + (rs.stderr.strip() if rs.returncode else ""))
    m0 = re.search(r"this run's series row 0 against the stored base state: (\d+) entries differ", rs.stdout)
    print()
    print("READING (the coordinator's, fixed before the run): " + reading(rb, int(m0.group(1)) if m0 else None))

