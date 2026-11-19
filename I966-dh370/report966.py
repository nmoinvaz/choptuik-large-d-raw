#!/usr/bin/env python3
"""#966: the markdown table of every attempt of a ks_chain run since a D, from the legs' anm_run.jsonl and anm_run.log.

    python3 -I report966.py CHAIN_OUT [--from D]
    python3 -I report966.py --selftest [--mutate]

One row per attempt (accepted and refused): leg ks, step, D reached, a, the a rule's level, the re-seed verdict, polish_q's |R| and steps
(the first rung record of the re-seed), the octo-double refinement's first and last rung max|R| (the k-th 'horizon data refined' line
of the leg's log goes to the k-th successful re-seed), the octo-double corrector's steps, its seconds (t_corr), the series seconds
(t_coef of the step) and the base's smallest pivot (pivots[0]) of the step's base. --selftest builds a planted leg whose rows are
known; --mutate pairs the refinement lines with the wrong re-seeds, so the selftest exits 1."""
import glob
import json
import os
import re
import sys
import tempfile

REF = re.compile(r"horizon data refined in octo-double, rung max\|R\| (.*)")
LEG = re.compile(r"leg\d+_D([0-9.]+)_ks(\d+)$")
MUTATE = False


def rows(chain, d_from=0.0):
    out = []
    for d in sorted(glob.glob(os.path.join(chain, "leg*")), key=lambda p: float(LEG.search(p).group(1)) if LEG.search(p) else 0):
        m = LEG.search(d)
        jp, lp = os.path.join(d, "anm_run.jsonl"), os.path.join(d, "anm_run.log")
        if not m or not os.path.exists(jp):
            continue
        refs = []
        for ln in open(lp):
            q = REF.search(ln)
            if q:
                refs.append([float(x) for x in q.group(1).split(" -> ")])
        if MUTATE:
            refs = refs[::-1]
        k = 0
        for ln in open(jp):
            r = json.loads(ln)
            for a in r["attempts"]:
                rs = a.get("reseed") or {}
                g = (rs.get("rungs") or [{}])[0]
                ref = None
                if rs.get("ok"):
                    ref = refs[k] if k < len(refs) else None
                    k += 1
                if a["D"] >= d_from:
                    out.append(dict(ks=int(m.group(2)), step=r["step"], D=a["D"], a=a["a"], level=a.get("rule_level"), ok=rs.get("ok"),
                                    R=g.get("R"), its=g.get("its"), ref=ref, od=a["steps"], corr=a["t_corr"], acc=a["accepted"],
                                    series=r.get("t_coef", 0.0), pmin=(r.get("pivots") or [None])[0]))
    return out


def render(rs):
    L = ["| ks | step | D | a | level | re-seed | polish_q \\|R\\| (steps) | refinement first .. last | od steps | corrector s | series s | base p_min | accepted |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rs:
        lv = "" if r["level"] is None else f"{r['level']:.4f}"
        ref = "none" if r["ref"] is None else f"{r['ref'][0]:.2e} .. {r['ref'][-1]:.2e}"
        pm = "" if r["pmin"] is None else f"{r['pmin']:.3e}"
        L.append(f"| {r['ks']} | {r['step']} | {r['D']:.4f} | {r['a']:.4f} | {lv} | {'ok' if r['ok'] else 'FAILED'} | {r['R']:.2e} ({r['its']}) | {ref} | "
                 f"{r['od']} | {r['corr']:.0f} | {r['series']:.0f} | {pm} | {'yes' if r['acc'] else 'no'} |")
    return "\n".join(L)


def selftest(mutate):
    global MUTATE
    MUTATE = mutate
    with tempfile.TemporaryDirectory() as t:
        d = os.path.join(t, "leg00_D10.0000_ks293")
        os.makedirs(d)
        recs = [dict(step=0, D0=10.0, t_coef=100.0, pivots=[1e-16, 1e40], attempts=[
                    dict(a=1.0, D=11.0, accepted=False, steps=0, t_corr=5.0, rule_level=0.2, reseed=dict(ok=False, rungs=[dict(R=4e-8, its=8)])),
                    dict(a=0.5, D=10.5, accepted=True, steps=4, t_corr=50.0, rule_level=0.02, reseed=dict(ok=True, rungs=[dict(R=1e-20, its=23)]))]),
                dict(step=1, D0=10.5, t_coef=110.0, pivots=[8e-17, 1e40], attempts=[
                    dict(a=0.5, D=11.0, accepted=True, steps=7, t_corr=70.0, rule_level=0.07, reseed=dict(ok=True, rungs=[dict(R=5e-17, its=23)]))])]
        with open(os.path.join(d, "anm_run.jsonl"), "w") as f:
            for r in recs:
                f.write(json.dumps(r) + "\n")
        with open(os.path.join(d, "anm_run.log"), "w") as f:
            f.write("      horizon data refined in octo-double, rung max|R| 1.0e-18 -> 2.0e-31\n")
            f.write("      horizon data refined in octo-double, rung max|R| 3.0e-17 -> 4.0e-25\n")
        rs = rows(t)
        res = [len(rs) == 3, rs[0]["ref"] is None and rs[0]["ok"] is False, rs[1]["ref"] == [1.0e-18, 2.0e-31], rs[2]["ref"] == [3.0e-17, 4.0e-25],
               rs[1]["pmin"] == 1e-16 and rs[2]["pmin"] == 8e-17, [round(r["corr"]) for r in rs] == [5, 50, 70], rs[2]["level"] == 0.07]
        txt = render(rs)
        res.append("3.00e-17 .. 4.00e-25" in txt)
        for i, x in enumerate(res):
            print(("ok   " if x else "FAIL ") + f"check {i}")
        return all(res)


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(0 if selftest("--mutate" in a) else 1)
    d_from = float(a[a.index("--from") + 1]) if "--from" in a else 0.0
    print(render(rows(a[0], d_from)))


if __name__ == "__main__":
    main()
