#!/usr/bin/env python3
"""#1025 winb follow-on: the verdict of one hybrid row under the P4 rules, the edge rule and the signtest at lambda -/+ 0.02.
usage: verdict_p4hi_1025.py HYBRID.jsonl D SIGNTEST.log [--ref V]     (exit 0 on PASS, 1 otherwise; prints the evidence)
P4 rules (p4_driver_w.sh): record system true, one sign change on the grid, one over all evaluations, noise robust, final bracket <= 1e-7.
Edge rule (check_1025.py's, 2026-11-20): the root is at least 0.05 grid steps from both edges of the grid interval that holds it; the grid is
the guess * (1 + w * (-1, 0, 1)) of the first w in (0.02, 0.06, 0.15, 0.35) whose three points show a sign change, read from the row's own
evaluations. Signtest (raw I1025-mac/signtest.py around=...:D:0.02): both lines agree (det sign from LU of M and of Q M, 3 random Q) and the signs at
lambda - 0.02 and lambda + 0.02 are opposite; its system line must be same true."""
import json, sys
WS, EDGE_BAR = (0.02, 0.06, 0.15, 0.35), 0.05
js, D, stlog = sys.argv[1], float(sys.argv[2]), sys.argv[3]
ref = float(sys.argv[sys.argv.index("--ref") + 1]) if "--ref" in sys.argv else None
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
        edge = dict(w=w, grid=grid, signs=sg, interval=[lo, hi], step=step, d_lo=(lam - lo) / step, d_hi=(hi - lam) / step)
        break
if edge is None:
    checks["edge_rule"] = False
    lines.append("edge rule: no grid with a sign change found in the evaluations -> FAIL")
else:
    checks["edge_rule"] = lo <= lam <= hi and min(edge["d_lo"], edge["d_hi"]) >= EDGE_BAR
    lines.append(f"edge rule: w {edge['w']}, grid {[round(x, 6) for x in grid]} signs {sg}, root in [{lo:.6f}, {hi:.6f}], {edge['d_lo']:.3f} grid steps from the lower "
                 f"edge, {edge['d_hi']:.3f} from the upper (bar {EDGE_BAR}) -> {'pass' if checks['edge_rule'] else 'FAIL'}")
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
checks["signtest_pm_0.02"] = bool(ok_st)
if len(sts) == 2:
    lines.append("signtest: " + "; ".join(f"lam {s['lam']:.9f} signs {s['signs']} agree {s['agree']} ({s['n_below_1e_12']} sv below 1e-12, {s['sec']} s)" for s in sts)
                 + f" -> {'pass' if ok_st else 'FAIL'}")
else:
    lines.append(f"signtest: {len(sts)} result lines in {stlog} (need 2), system line {'present' if sysl else 'missing'} -> FAIL")
ok = all(checks.values())
for l in lines:
    print(l)
print("checks:", json.dumps(checks))
print(f"VERDICT D {D}: {'PASS' if ok else 'FAIL'} lam {lam!r}")
json.dump(dict(D=D, lam=lam, verdict="PASS" if ok else "FAIL", checks=checks, edge=edge), open(stlog.replace("signtest_", "verdict_").replace(".log", ".json"), "w"), indent=1)
sys.exit(0 if ok else 1)
