#!/usr/bin/env python3
"""#966: the accepted steps of a ks_chain run as a table, and its wall per unit D.

    python3 -I steps966.py CHAIN_OUT [--from D] [--to D] [--wall H]
    python3 -I steps966.py --selftest [--mutate]

'corrector s' is the accepted attempt's t_corr (its octo-double Newton, without the re-seed). The last two columns are the base the step started from (D0) and its smallest pivot (p_min, pivots[0] of the record). One row per converged step of every leg's anm_run.jsonl: leg ks, D reached (the accepted attempt's), a, attempts, the a rule's
level at the accepted attempt (blank without the rule), the octo-double corrector's steps, the series seconds (t_coef) and the
step seconds, the sum of the logged parts: t_coef plus, for each attempt, its re-seed seconds and t_corr. That sum leaves out each
leg's base polish and the setup of each attempt, so it is the same quantity for ks_chain2 (whose log has no clock) and ks_chain3.
'logged s per D' is the step seconds summed over the steps whose accepted D lies in [--from, --to] over the D they cover.
--wall H adds the clock: the modification times of the leg's anm_pin*_D*.npz over the last H hours, hours per unit D by clock.
--selftest builds a planted chain whose table and sums are known; --mutate drops the re-seed seconds from the sum, so the
selftest exits 1."""
import glob
import json
import os
import re
import sys
import tempfile
import time

LEG = re.compile(r"leg\d+_D([0-9.]+)_ks(\d+)$")
MUTATE = False


def step_seconds(rec):
    s = rec.get("t_coef", 0.0)
    for a in rec.get("attempts", []):
        s += a.get("t_corr", 0.0) + (0 if MUTATE else (a.get("reseed") or {}).get("seconds", 0.0))
    return s


def rows(chain):
    out = []
    for d in sorted(glob.glob(os.path.join(chain, "leg*")), key=lambda p: float(LEG.search(p).group(1)) if LEG.search(p) else 0):
        m = LEG.search(d)
        p = os.path.join(d, "anm_run.jsonl")
        if not m or not os.path.exists(p):
            continue
        for ln in open(p):
            r = json.loads(ln)
            if not r.get("converged"):
                continue
            acc = [a for a in r["attempts"] if a["accepted"]][-1]
            out.append(dict(ks=int(m.group(2)), step=r["step"], D0=r["D0"], pmin=(r.get("pivots") or [None])[0], D=acc["D"], a=acc["a"], att=len(r["attempts"]),
                            level=acc.get("rule_level"), cs=acc["steps"], series=r.get("t_coef", 0.0), sec=step_seconds(r),
                            corr=(r["attempts"][0] if MUTATE else acc).get("t_corr", 0.0)))
    return out


def table(rs):
    print("| ks | step | D | a | attempts | level | corrector steps | corrector s | series s | step s | base D0 | base p_min |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rs:
        lv = "" if r["level"] is None else f"{r['level']:.4f}"
        print(f"| {r['ks']} | {r['step']} | {r['D']:.4f} | {r['a']:.4f} | {r['att']} | {lv} | {r['cs']} | {r['corr']:.0f} | {r['series']:.0f} | {r['sec']:.0f} | {r['D0']:.4f} | {'' if r['pmin'] is None else format(r['pmin'], '.3e')} |")


def per_D(rs, lo, hi):
    sel = [r for r in rs if lo <= r["D"] <= hi]
    if not sel:
        return None
    d = sel[-1]["D"] - sel[0]["D0"]
    s = sum(r["sec"] for r in sel)
    return len(sel), d, s, s / d


def clock(chain, hours):
    pts = []
    for p in glob.glob(os.path.join(chain, "leg*", "anm_pin*_D*.npz")):
        pts.append((os.path.getmtime(p), float(re.search(r"_D([0-9.]+)\.npz$", p).group(1))))
    pts.sort()
    if len(pts) < 2:
        return None
    t1 = pts[-1][0]
    win = [q for q in pts if q[0] >= t1 - hours * 3600]
    if len(win) < 2:
        return None
    dt, dD = win[-1][0] - win[0][0], win[-1][1] - win[0][1]
    return dt / 3600, dD, dt / 3600 / dD if dD > 0 else float("nan")


def selftest(mutate):
    global MUTATE
    MUTATE = mutate
    ok = True
    with tempfile.TemporaryDirectory() as t:
        d = os.path.join(t, "leg00_D10.0000_ks304")
        os.makedirs(d)
        recs = [dict(step=0, D0=10.0, t_coef=100.0, converged=True, attempts=[
                    dict(a=2.0, D=12.0, accepted=False, steps=0, t_corr=1.0, reseed=dict(ok=False, seconds=7.0)),
                    dict(a=1.0, D=11.0, accepted=True, steps=3, t_corr=20.0, rule_level=0.07, reseed=dict(ok=True, seconds=30.0))]),
                dict(step=1, D0=11.0, t_coef=110.0, converged=True, attempts=[
                    dict(a=1.0, D=12.0, accepted=True, steps=5, t_corr=40.0, reseed=dict(ok=True, seconds=50.0))]),
                dict(step=2, D0=12.0, t_coef=1.0, converged=False, attempts=[dict(a=1.0, D=13.0, accepted=False, steps=0, t_corr=1.0)])]
        with open(os.path.join(d, "anm_run.jsonl"), "w") as f:
            for r in recs:
                f.write(json.dumps(r) + "\n")
        rs = rows(t)
        want_sec = [100 + 1 + 7 + 20 + 30, 110 + 40 + 50]        # 158 and 200
        res = [len(rs) == 2, [round(r["sec"]) for r in rs] == want_sec, rs[0]["att"] == 2, rs[0]["cs"] == 3, rs[1]["level"] is None,
               [round(r["corr"]) for r in rs] == [20, 40]]
        pd = per_D(rs, 0, 100)
        res += [pd is not None and round(pd[3]) == round((158 + 200) / 2.0)]
        for i, r in enumerate(res):
            print(("ok   " if r else "FAIL ") + f"check {i}")
        ok = all(res)
    return ok


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(0 if selftest("--mutate" in a) else 1)
    opt = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
    rs = rows(a[0])
    table([r for r in rs if opt("--from", 0) <= r["D"] <= opt("--to", 1e9)])
    pd = per_D(rs, opt("--from", 0), opt("--to", 1e9))
    if pd:
        print(f"\n{pd[0]} steps, D {pd[1]:.4f}, logged {pd[2]:.0f} s, logged s per D {pd[3]:.0f}")
    if "--wall" in a:
        c = clock(a[0], opt("--wall", 3))
        print("clock: " + (f"{c[0]:.2f} h over D {c[1]:.4f}, {c[2]:.3f} h per D ({c[2] * 3600:.0f} s per D)" if c else "fewer than two states in the window"))


if __name__ == "__main__":
    main()
