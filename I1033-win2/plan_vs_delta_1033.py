"""#1033: is the reference the confound? Tabulates every run 3 and run 4 solve of D 3.0475 (records of tau_map_gain.py solve):
L, M', the start's plan, the plan the final solve ran on, the own plan, converged, Delta - Delta(384), and the group, then
tests the coordinator's prediction (hc of 2026-11-20): the +3.8e-11 group is the solves whose own plan is far longer than
the stored 1623 steps, and the within-1e-12 group is those near 1623, whatever L and M'.
Reads only stored records (no solver, no kernel): the two solve_*.jsonl files and the stored T82-win M 384 and M 320 states
(for Delta(384), Delta(320) and the stored plan's step count). Does not touch the report.

Rules fixed before the counts (written into this file before it was run on the records):
  dDelta = Delta - Delta(384) in exact rational arithmetic from the two doubles (Delta, Delta_lo).
  group hi    : 3.6e-11 <= dDelta <= 4.0e-11 (the group of the uniform M 320 error, 3.77e-11)
  group lo    : |dDelta| < 1e-12
  group other : a converged or unconverged value in neither;  failed: no Delta recorded.
  rho = own plan steps / stored plan steps (1623).  far: rho >= 1.5.  near: 0.75 <= rho <= 1.25 (sensitivity 0.6..1.4).
  P1: every hi solve has a far own plan.  P2: every lo solve has a near own plan.
  holds: P1 and P2 for every member;  fails: no hi solve is far, or fewer than half of each group satisfy its part;
  mixed: otherwise.  Unconverged solves are counted in their group and listed (counts also given without them).
usage: python -I plan_vs_delta_1033.py [--out plan_vs_delta_1033.md] [--csv plan_vs_delta_1033.csv]
       python -I plan_vs_delta_1033.py --selftest
"""
import json
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
STATE = RAW + "/T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M%d.npz"
RUN4_T0 = "2026-11-20 00:23"


def group(d):
    if d is None:
        return "failed"
    if 3.6e-11 <= d <= 4.0e-11:
        return "hi"
    if abs(d) < 1e-12:
        return "lo"
    return "other"


def plan_class(own, stored, near=(0.75, 1.25), far=1.5):
    rho = own / stored
    if rho >= far:
        return "far"
    if near[0] <= rho <= near[1]:
        return "near"
    return "inter" if rho > near[1] else "short"


def verdict(rows, stored, near=(0.75, 1.25), drop_unconverged=False):
    """rows: dicts with grp, own, converged. Returns (verdict, n_hi, k1, n_lo, k2)."""
    rs = [r for r in rows if not (drop_unconverged and not r["converged"])]
    hi = [r for r in rs if r["grp"] == "hi"]
    lo = [r for r in rs if r["grp"] == "lo"]
    k1 = sum(plan_class(r["own"], stored, near) == "far" for r in hi)
    k2 = sum(plan_class(r["own"], stored, near) == "near" for r in lo)
    if hi and lo and k1 == len(hi) and k2 == len(lo):
        v = "holds"
    elif not hi or not lo or k1 == 0 or (k1 / len(hi) < 0.5 and k2 / len(lo) < 0.5):
        v = "fails"
    else:
        v = "mixed"
    return v, len(hi), k1, len(lo), k2


def selftest():
    """the verdict must be able to fail: planted tables with a known verdict (the prediction true, reversed, half true)"""
    def mk(hi_own, lo_own):
        return ([dict(grp="hi", own=o, converged=True) for o in hi_own] + [dict(grp="lo", own=o, converged=True) for o in lo_own])
    cases = [("planted: prediction true", mk([3000, 2900, 3100], [1600, 1700, 1500]), "holds"),
             ("planted: prediction reversed", mk([1600, 1700, 1500], [3000, 2900, 3100]), "fails"),
             ("planted: long plans in both groups", mk([3000, 2900, 1600], [1600, 1700, 3000]), "mixed"),
             ("planted: no solve in the hi group", mk([], [1600, 1700]), "fails")]
    ok = True
    for name, rows, want in cases:
        got = verdict(rows, 1623)[0]
        print("selftest %-40s verdict %-6s (must be %s) %s" % (name, got, want, "ok" if got == want else "WRONG"))
        ok &= got == want
    print("selftest", "passes" if ok else "FAILS")
    return 0 if ok else 1


def load_state_delta(path):
    import numpy as np
    z = np.load(path, allow_pickle=True)
    meta = json.loads(str(z["meta"]))
    stored = sum(len(g) - 1 for g in meta["segs"])
    return Fr(float(z["zh"][-1])) + Fr(float(z["zl"][-1])), stored


def main():
    if "--selftest" in sys.argv:
        return selftest()
    arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    out = arg("--out", HERE + "/plan_vs_delta_1033.md")
    csv = arg("--csv", HERE + "/plan_vs_delta_1033.csv")
    ref, stored = load_state_delta(STATE % 384)
    ref2, stored2 = load_state_delta(STATE % 320)
    e_u = float(ref2 - ref)
    rows = []
    for fn, run in (("solve_D3.0475.jsonl", "A"), ("solve_D3.0475b.jsonl", "B")):
        for line in open(HERE + "/" + fn):
            r = json.loads(line)
            r4 = r["t_start"] >= RUN4_T0
            d = None
            if "Delta" in r:
                d = float(Fr(r["Delta"]) + Fr(r.get("Delta_lo", 0.0)) - ref)
            rows.append(dict(run=("4" + run) if r4 else "3", L=r["L"], Mp=r["Mp"], tag=r["tag"], state=os.path.basename(r["state"]),
                             gate=r.get("gate", r.get("failed")), start=r.get("steps_start"), p1=r.get("steps_p1"),
                             own=r.get("steps_own"), converged=bool(r.get("converged")), failed=r.get("failed"), d=d,
                             F_start=r.get("F_start"), pass1=r.get("pass1", "solved"), seconds=r.get("seconds"),
                             full=(Fr(r["Delta"]) + Fr(r.get("Delta_lo", 0.0))) if "Delta" in r else None, grp=group(d)))
    rows.sort(key=lambda r: (-r["L"], -r["Mp"]))
    # the checks (each can fail): record count, the identity, the stored plan, agreement with the report's own numbers
    assert len(rows) == 18, "expected 18 records (3 of run 3, 15 of run 4), got %d" % len(rows)
    ident = [r for r in rows if r["L"] == 1.0 and r["Mp"] == 384][0]
    assert abs(ident["d"]) < 1e-20, "the L 1 identity at M 384 must reproduce Delta(384): %g" % ident["d"]
    assert stored == 1623, "the stored M 384 plan was 1623 steps in the report, got %d" % stored
    rep = json.load(open(HERE + "/report_D3.0475_run4.json"))
    for rr in rep["rows"] + list(rep["need"].values()):
        mine = [r for r in rows if r["L"] == rr["L"] and r["Mp"] == rr["Mp"]][0]
        if mine["d"] is None or rr.get("dDelta") is None:
            assert mine["d"] is None and rr.get("dDelta") is None, ("failed rows must agree", mine["tag"], mine["d"], rr.get("dDelta"))
            continue
        assert abs(mine["d"] - rr["dDelta"]) < 1e-25 or abs(abs(mine["d"]) - abs(rr["dDelta"])) < 1e-25, (mine["tag"], mine["d"], rr["dDelta"])
    fmt = lambda x, f="%+.3e": ("n/a" if x is None else f % x)
    L = []
    P = L.append
    P("# #1033 run 3 and run 4: Delta - Delta(384) against the plans (plan_vs_delta_1033.py)\n")
    P("Delta(384) = T82-win's stored M 384 state, Delta %.16f, stored plan %d steps; Delta(320) = its stored M 320 state, stored plan %d steps; "
      "|Delta(384) - Delta(320)| = %.3e. Start state of every solve: the stored M 384 state (T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M384.npz) "
      "interpolated in double-double onto the arctan map (L, M', s0), the state itself at L 1, M' 384, and its truncation at L 1, M' 320.\n"
      % (float(ref), stored, stored2, e_u))
    P("Plan columns: start = the start state's own plan (the stored M 384 plan, split as the gate label says, then re-planned at the start "
      "state); pass 2 = the plan of the pass-1 state, the plan the final solve to |F| < 1e-28 ran on (the L 1 identity skips pass 1, so it ran on its start plan); "
      "own = the plan of the converged state, made after the solve (a size measure, not used to solve). rho = own / %d.\n" % stored)
    P("| run | L | M' | start state | plan source (gate) | start | pass 2 | own | rho | converged | Delta - Delta(384) | group | own class |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        if r["own"] is None:
            P("| %s | %g | %d | stored M 384, interpolated | %s | %s | - | - | - | **failed** | none recorded | failed | - |"
              % (r["run"], r["L"], r["Mp"], "%s (failed: %s)" % (r["gate"] if r["start"] else "no start plan", r["failed"]), r["start"]))
            continue
        src = r["gate"] + ("; pass 1 skipped (start below tol1)" if r["pass1"] != "solved" else "")
        P("| %s | %g | %d | %s | %s | %d | %d | %d | %.3f | %s | %s | %s | %s |"
          % (r["run"], r["L"], r["Mp"], "stored M 384" + (" itself" if (r["L"] == 1.0 and r["Mp"] == 384) else (", truncated" if r["L"] == 1.0 else ", interpolated")),
             src, r["start"], r["p1"], r["own"], r["own"] / stored, "yes" if r["converged"] else "**no**", "%+.3e" % r["d"], r["grp"],
             plan_class(r["own"], stored)))
    P("\nGroups: hi = 3.6e-11 to 4.0e-11, lo = |d| < 1e-12, other = neither, failed = no Delta. Own class: far = rho >= 1.5, near = 0.75 to 1.25, inter = 1.25 to 1.5, short < 0.75.\n")
    P("## The prediction\n")
    res = {}
    for name, near, drop in (("as ordered (near 0.75 to 1.25, all solves)", (0.75, 1.25), False),
                             ("unconverged solves dropped", (0.75, 1.25), True),
                             ("wider near band 0.6 to 1.4", (0.6, 1.4), False)):
        v, nh, k1, nl, k2 = verdict(rows, stored, near, drop)
        res[name] = v
        P("- %s: **%s**. P1, hi group with a far own plan: %d of %d. P2, lo group with a near own plan: %d of %d." % (name, v, k1, nh, k2, nl))
    hi = [r for r in rows if r["grp"] == "hi"]
    lo = [r for r in rows if r["grp"] == "lo"]
    oth = [r for r in rows if r["grp"] == "other"]
    P("\nhi group (%d): %s." % (len(hi), "; ".join("L %g M' %d: own %d, pass 2 %d, start %d, %+.3e" % (r["L"], r["Mp"], r["own"], r["p1"], r["start"], r["d"]) for r in hi)))
    P("lo group (%d), own plan steps: %s." % (len(lo), ", ".join("%d (L %g M' %d%s)" % (r["own"], r["L"], r["Mp"], "" if r["converged"] else ", unconverged") for r in sorted(lo, key=lambda r: r["own"]))))
    P("other (%d): %s." % (len(oth), "; ".join("L %g M' %d: own %d, %+.3e" % (r["L"], r["Mp"], r["own"], r["d"]) for r in oth)))
    for col, nm in (("start", "start plan"), ("p1", "pass-2 plan"), ("own", "own plan")):
        h = [r[col] for r in hi]
        l = [r[col] for r in lo]
        P("- %s steps: hi group %d to %d, lo group %d to %d%s." % (nm, min(h), max(h), min(l), max(l),
          " (the ranges overlap: no threshold separates the groups)" if max(h) >= min(l) and max(l) >= min(h) else " (separated)"))
    P("\n## Is Delta moved by the plan? The two identity solves\n")
    P("Each starts from a stored T82-win state and solves on a plan longer than the stored one; Delta - Delta(own state) after the solve:\n")
    P("| solve | stored plan | plan the solve ran on | Delta - stored Delta of that state |")
    P("|---|---|---|---|")
    P("| L 1, M' 384 (from M 384) | %d | %d (pass 1 skipped) | %+.2e |" % (stored, ident["p1"], ident["d"]))
    ident320 = [r for r in rows if r["L"] == 1.0 and r["Mp"] == 320][0]
    P("| L 1, M' 320 (M 384 truncated; Delta compared with the stored M 320 state) | %d | %d (start plan %d) | %+.2e |"
      % (stored2, ident320["p1"], ident320["start"], float(ident320["full"] - ref2)))
    P("\n## Delta - Delta(384) against M' at each L (converged solves; the largest M' of each L is the last row)\n")
    P("| L | M' : Delta - Delta(384) |")
    P("|---|---|")
    for l in sorted({r["L"] for r in rows}, reverse=True):
        rs = sorted([r for r in rows if r["L"] == l], key=lambda r: r["Mp"])
        P("| %g | %s |" % (l, ", ".join("%d: %s%s" % (r["Mp"], ("%+.2e" % r["d"]) if r["d"] is not None else "failed", "" if r["converged"] or r["d"] is None else " (unconverged)") for r in rs)))
    lad = []
    for l in sorted({r["L"] for r in rows}):
        rs = sorted([r for r in rows if r["L"] == l and r["converged"] and r["d"] is not None], key=lambda r: r["Mp"])
        if len(rs) >= 2:
            lad.append((l, all(abs(a["d"]) >= abs(b["d"]) for a, b in zip(rs, rs[1:]))))
    P("\n|Delta - Delta(384)| does not increase with M' in %d of %d L ladders with two or more converged M' (L %s)."
      % (sum(ok for _, ok in lad), len(lad), ", ".join("%g%s" % (l, "" if ok else " (not)") for l, ok in lad)))
    plateau = [r for r in rows if r["converged"] and r["d"] is not None and -3.3e-13 <= r["d"] <= -3.1e-13]
    if plateau:
        P("\nConverged solves between -3.3e-13 and -3.1e-13 (different L and M'): %s; spread %.1e." % (
            ", ".join("L %g M' %d %+.3e" % (r["L"], r["Mp"], r["d"]) for r in plateau), max(r["d"] for r in plateau) - min(r["d"] for r in plateau)))
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    with open(csv, "w", encoding="utf-8") as f:
        f.write("run,L,Mp,start_steps,pass2_steps,own_steps,rho,converged,dDelta,group,own_class,gate\n")
        for r in rows:
            f.write("%s,%g,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (r["run"], r["L"], r["Mp"], r["start"], r["p1"], r["own"],
                    "%.4f" % (r["own"] / stored) if r["own"] else "", r["converged"], "%.6e" % r["d"] if r["d"] is not None else "", r["grp"],
                    plan_class(r["own"], stored) if r["own"] else "", r["gate"]))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
