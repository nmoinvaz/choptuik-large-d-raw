#!/usr/bin/env python3
"""#1025 winb follow-on: the verdict of one hybrid row. usage: verdict_p4hi_1025.py HYBRID.jsonl D SIGNTEST.log [--ref V] [--tag T]
(exit 0 when checks 1-5 pass, 1 otherwise; prints the evidence; --tag T writes verdict_D<D>_T.json instead of verdict_D<D>.json)
Version 2, the coordinator's amendment of 2026-11-21 06:30 UTC (v1 is verdict_p4hi_1025_v1.py, which gave row A's FAIL at 06:23):
 1 record system true; 2 one sign change on the grid; 3 one over all evaluations; 4 noise robust; 5 final bracket <= 1e-7;
 EDGE RULE (amended): the root is at least 0.05 grid steps from the window's OUTER grid points guess * (1 -/+ w) (w the first of 0.02, 0.06,
 0.15, 0.35 whose three points show a sign change, read from the row's own evaluations), and inside the window. The first-written rule (both
 edges of the bracketing grid interval, which also counts the middle point) is printed, not decisive.
 SIGN CHECK: moved to the full dd M (ell_ddm at lambda -/+ 0.02, run by win2): PENDING here. The float64 signtest (raw I1025-mac/signtest.py,
 around=...:D:0.02) is printed for the record and is no longer a criterion: the float64 sign is noise past D 17 (the D 17.5 record's own failed signtest)."""
import json, sys
WS, EDGE_BAR = (0.02, 0.06, 0.15, 0.35), 0.05
js, D, stlog = sys.argv[1], float(sys.argv[2]), sys.argv[3]
ref = float(sys.argv[sys.argv.index("--ref") + 1]) if "--ref" in sys.argv else None
tag = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else None
rec = [json.loads(l) for l in open(js) if l.strip() and abs(json.loads(l)["D"] - D) < 1e-9][-1]
lam, g = rec["lam"], rec["lam_guess"]
ev = {float(k): v for k, v in rec["evals"].items()}
def find(x):
    k = min(ev, key=lambda k: abs(k - x))
    return k if abs(k - x) <= 1e-12 * max(1.0, abs(x)) else None
checks, info, lines = {}, {}, []
checks["record_system"] = bool(rec["record_system"])
checks["grid_one_change"] = rec["n_signchanges_grid"] == 1
checks["all_one_change"] = rec["n_changes_all"] == 1
checks["noise_robust"] = bool(rec["noise_robust"])
checks["bracket_le_1e-7"] = rec["bracket_width"] is not None and rec["bracket_width"] <= 1e-7
lines.append(f"D {D} k_c {rec['kc']}: hybrid lam {lam!r}, guess {g}, record lam {rec['lam_record']!r}, {rec['n_eval']} evaluations, "
             f"bracket {rec['bracket']} (width {rec['bracket_width']}), {rec['sec']} s")
edge = None
for w in WS:
    grid = [g * (1 + w * s) for s in (-1.0, 0.0, 1.0)]
    ks = [find(x) for x in grid]
    if None in ks:
        continue
    sg = [ev[k]["sign"] for k in ks]
    ch = [i for i in range(2) if sg[i] != sg[i + 1]]
    if ch:
        step = g * w
        i = ch[0] if len(ch) == 1 else min(ch, key=lambda i: abs(0.5 * (grid[i] + grid[i + 1]) - lam))
        lo, hi = grid[i], grid[i + 1]
        edge = dict(w=w, grid=grid, signs=sg, interval=[lo, hi], step=step, d_lo=(lam - lo) / step, d_hi=(hi - lam) / step,
                    d_outer_lo=(lam - grid[0]) / step, d_outer_hi=(grid[2] - lam) / step)
        break
if edge is None:
    checks["edge_rule_amended_outer_points"] = False
    lines.append("edge rule (amended, outer grid points): no grid with a sign change found in the evaluations -> FAIL")
else:
    ok_e = grid[0] <= lam <= grid[2] and min(edge["d_outer_lo"], edge["d_outer_hi"]) >= EDGE_BAR
    checks["edge_rule_amended_outer_points"] = ok_e
    info["edge_rule_as_first_written_both_edges_of_interval"] = lo <= lam <= hi and min(edge["d_lo"], edge["d_hi"]) >= EDGE_BAR
    lines.append(f"edge rule (amended 06:30 UTC, outer grid points only): w {edge['w']}, grid {[round(x, 6) for x in grid]} signs {sg}, root {lam:.9f}: "
                 f"{edge['d_outer_lo']:.3f} grid steps from the lower outer point, {edge['d_outer_hi']:.3f} from the upper outer point (bar {EDGE_BAR}) "
                 f"-> {'pass' if ok_e else 'FAIL'}")
    lines.append(f"  as first written (both edges of the bracketing interval [{lo:.6f}, {hi:.6f}]): {edge['d_lo']:.3f} and {edge['d_hi']:.3f} steps "
                 f"-> {'pass' if info['edge_rule_as_first_written_both_edges_of_interval'] else 'fail'} (not decisive)")
lines.append(f"hybrid minus the float64 record (row B: minus the guess): {lam - rec['lam_record']:+.6e}")
if ref is not None:
    lines.append(f"distance to the reference value {ref}: {lam - ref:+.4e} ({100 * (lam - ref) / ref:+.3f}%)")
sysl, sts = None, []
for l in open(stlog, errors="replace"):
    l = l.strip()
    if l.startswith('{"system_check"'):
        sysl = json.loads(l)
    elif l.startswith('{"state"'):
        sts.append(json.loads(l))
ok_st = sysl is not None and sysl["same"] and len(sts) == 2 and all(s["agree"] for s in sts) and sts[0]["signs"][0] * sts[1]["signs"][0] < 0 \
    and abs(sts[0]["lam"] - (lam - 0.02)) < 1e-9 and abs(sts[1]["lam"] - (lam + 0.02)) < 1e-9
info["float64_signtest_pm_0.02"] = bool(ok_st)
if len(sts) == 2:
    lines.append("float64 signtest (no longer a criterion): " + "; ".join(f"lam {s['lam']:.9f} signs {s['signs']} agree {s['agree']} ({s['n_below_1e_12']} sv below 1e-12, {s['sec']} s)" for s in sts)
                 + f" -> {'pass' if ok_st else 'fail'}")
else:
    lines.append(f"float64 signtest (no longer a criterion): {len(sts)} result lines in {stlog}, system line {'present' if sysl else 'missing'}")
ok = all(checks.values())
for l in lines:
    print(l)
print("checks:", json.dumps(checks), "| informational:", json.dumps(info))
print(f"VERDICT D {D}: checks 1-5 and the amended edge rule {'PASS' if ok else 'FAIL'}; dd sign check (ell_ddm at lam -/+ 0.02) PENDING; lam {lam!r}")
out = stlog.replace("signtest_", "verdict_").replace(".log", f"_{tag}.json" if tag else ".json")
json.dump(dict(D=D, lam=lam, checks_1_5_and_amended_edge="PASS" if ok else "FAIL", dd_sign_check="PENDING", checks=checks, informational=info, edge=edge), open(out, "w"), indent=1)
sys.exit(0 if ok else 1)
