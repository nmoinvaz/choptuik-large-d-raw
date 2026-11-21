#!/usr/bin/env python3
"""#1025 winb, the D 18.5 root: the verdict of the hybrid row. usage: verdict_d185_1025.py HYBRID.jsonl D [--between LO,HI] [--out FILE]
(exit 0 when every check passes; prints the evidence). The checks are those of verdict_p4hi_1025.py v2 (the coordinator's Amendment 1 of 2026-11-21 06:30 UTC)
without the float64 signtest, plus the coordinator's bracket check:
 1 record system true; 2 one sign change on the grid; 3 one over all evaluations; 4 noise robust; 5 final bracket <= 1e-7;
 edge rule: the root is inside the window and at least 0.05 grid steps from the window's OUTER grid points guess * (1 -/+ w) (w the first of 0.02,
 0.06, 0.15, 0.35 whose three points show a sign change, read from the row's own evaluations);
 bracket check (--between LO,HI): the root and its final bracket lie strictly inside (LO, HI).
The dd sign check (ell_ddm.py det at root -/+ 0.02, read by read_ddB_1025.py v2) is not here: the verdict line says PENDING.
The orientation (signs at the final bracket's ends) is printed as information."""
import json, sys
WS, EDGE_BAR = (0.02, 0.06, 0.15, 0.35), 0.05
js, D = sys.argv[1], float(sys.argv[2])
opt = lambda k: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None
between = [float(x) for x in opt("--between").split(",")] if opt("--between") else None
outfn = opt("--out")
rec = [json.loads(l) for l in open(js) if l.strip() and abs(json.loads(l)["D"] - D) < 1e-9][-1]
lam, g = rec["lam"], rec["lam_guess"]
ev = {float(k): v for k, v in rec["evals"].items()}
def find(x):
    k = min(ev, key=lambda k: abs(k - x))
    return k if abs(k - x) <= 1e-12 * max(1.0, abs(x)) else None
checks, lines = {}, []
checks["record_system"] = bool(rec["record_system"])
checks["grid_one_change"] = rec["n_signchanges_grid"] == 1
checks["all_one_change"] = rec["n_changes_all"] == 1
checks["noise_robust"] = bool(rec["noise_robust"])
checks["bracket_le_1e-7"] = rec["bracket_width"] is not None and rec["bracket_width"] <= 1e-7
lines.append(f"D {D} k_c {rec['kc']}: hybrid lam {lam!r}, guess {g}, {rec['n_eval']} evaluations, bracket {rec['bracket']} (width {rec['bracket_width']}), {rec['sec']} s; "
             f"system: |F| {rec['F']:.10e}, record_system {rec['record_system']}")
edge = None
for w in WS:
    grid = [g * (1 + w * s) for s in (-1.0, 0.0, 1.0)]
    ks = [find(x) for x in grid]
    if None in ks:
        continue
    sg = [ev[k]["sign"] for k in ks]
    if any(sg[i] != sg[i + 1] for i in range(2)):
        step = g * w
        edge = dict(w=w, grid=grid, signs=sg, step=step, d_outer_lo=(lam - grid[0]) / step, d_outer_hi=(grid[2] - lam) / step)
        break
if edge is None:
    checks["edge_rule_amended_outer_points"] = False
    lines.append("edge rule (amended, outer grid points): no grid with a sign change found in the evaluations -> FAIL")
else:
    ok_e = grid[0] <= lam <= grid[2] and min(edge["d_outer_lo"], edge["d_outer_hi"]) >= EDGE_BAR
    checks["edge_rule_amended_outer_points"] = ok_e
    lines.append(f"edge rule (amended, outer grid points only): w {edge['w']}, grid {[round(x, 6) for x in grid]} signs {sg}, root {lam:.9f}: "
                 f"{edge['d_outer_lo']:.3f} grid steps from the lower outer point, {edge['d_outer_hi']:.3f} from the upper outer point (bar {EDGE_BAR}) -> {'pass' if ok_e else 'FAIL'}")
if between is not None:
    br = rec["bracket"]
    ok_b = between[0] < lam < between[1] and br is not None and between[0] < br[0] and br[1] < between[1]
    checks["root_and_bracket_in_(%g,%g)" % tuple(between)] = bool(ok_b)
    lines.append(f"bracket check: root {lam!r} and final bracket {br} inside ({between[0]}, {between[1]}) -> {'pass' if ok_b else 'FAIL'}")
if rec["bracket"]:
    s0, s1 = ev[find(rec["bracket"][0])]["sign"], ev[find(rec["bracket"][1])]["sign"]
    lines.append(f"orientation (information): sign {s0:+.0f} at the bracket's lower end, {s1:+.0f} at the upper end: " +
                 {(-1.0, 1.0): "minus below, plus above (the usual one)", (1.0, -1.0): "plus below, minus above"}.get((s0, s1), "same sign"))
lines.append(f"hybrid minus the stub's lam (the guess, not a record): {lam - rec['lam_record']:+.6e}")
ok = all(checks.values())
for l in lines:
    print(l)
print("checks:", json.dumps(checks))
print(f"VERDICT D {D}: every check above {'PASS' if ok else 'FAIL'} (record system, one change on the grid and over all evaluations, noise robust, bracket <= 1e-7, amended edge rule"
      + (", bracket check" if between else "") + f"); dd sign check (ell_ddm at lam -/+ 0.02) PENDING; lam {lam!r}")
if outfn:
    json.dump(dict(D=D, lam=lam, all_checks="PASS" if ok else "FAIL", dd_sign_check="PENDING", checks=checks, edge=edge), open(outfn, "w"), indent=1)
sys.exit(0 if ok else 1)
