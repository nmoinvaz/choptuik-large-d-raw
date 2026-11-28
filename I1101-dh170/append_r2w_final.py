"""#1101 R2 widened scan and secant: writes the result section (README text with Status line and predictions scorecard) and the issue post from
scan_r2all/*.jsonl, secant_r2w.jsonl, results_r2w_secant.md, read_lower_r2w.txt, read_lower_k2.txt and steps.txt, with the clock read here.
usage: append_r2w_final.py README_SECTION_OUT POST_OUT      (does not touch README.md itself; the section is appended by the caller)
Every table is asserted to have the same cell count in each row; the texts below are written for the asserted pattern and stop on any other."""
import datetime
import glob
import json
import re
import sys

ROOT_B = 0.045967998             # state B's own root at kappa 0.7 (dh370)
R1_ROOT = 0.09500769             # t5's R1 (kappa 0.5) root, comment 7223316450 (macm3)
STEPS = {"B": 4179, "R1": 5847, "R2": 8351}   # record steps of the kappa 0.7, 0.5 and 0.35 states (R1: t5's comment; R2: its record)
T0 = datetime.datetime(2026, 11, 27, 14, 1, 9)  # secant start (steps.txt [r2w])

rows = sorted((json.loads(l) for f in glob.glob("scan_r2all/scan_D23.0_p*.jsonl") for l in open(f) if l.strip()), key=lambda r: r["lam"])
assert [r["lam"] for r in rows] == [0.035, 0.045, 0.05, 0.06, 0.07, 0.085, 0.1, 0.13], [r["lam"] for r in rows]
assert all(r["robust"] and r["noise_robust"] and r["b12"] == "rust" for r in rows)
assert "".join("+" if r["sign"] > 0 else "-" for r in rows) == "+++++++-"
ev = [json.loads(l) for l in open("secant_r2w.jsonl") if l.strip()]
root = [r for r in ev if r.get("kind") == "root"]
ev = [r for r in ev if r.get("kind") == "eval"]
assert len(root) == 1 and root[0]["status"] == "tol" and root[0]["robust"] == [True, True] and root[0]["signs"] == [1.0, -1.0] and root[0]["n_eval"] == len(ev) == 10
root = root[0]
a, b = root["bracket"]
lin = root["lam_lin"]
assert a < lin < b and 0.1 < a and b < 0.13 and root["width"] < 5e-5
assert all(r["robust"] and r["noise_robust"] and r["b12"] == "rust" for r in ev)
assert ev[-1]["sign"] > 0 and ev[-2]["sign"] < 0 and (ev[-1]["lam"], ev[-2]["lam"]) == (a, b), (ev[-1]["lam"], ev[-2]["lam"], a, b)
delta = lin - ROOT_B
e_root = delta * 16 / 15
sr = open("results_r2w_secant.md").read()
assert "|E_root| >= 0.003: the step error is real" in sr and f"{lin:.9f}" in sr and "robust changes: [(0.1, 0.13)]" in sr, sr
st = open("steps.txt").read()
m = re.search(r"(\d\d:\d\d:\d\d) UTC \[r2w\] secant exit 0 .*?, (\d+) s; ", st)
assert m, "secant exit line"
t_end, wall = m.group(1), int(m.group(2))
m = re.search(r"\[r2w\] scan done: (\d+) s", st)
scan_wall = int(m.group(1))
assert sum(r["sec"] for r in ev) in range(wall - 20, wall + 1), (sum(r["sec"] for r in ev), wall)
rk = open("read_lower_k2.txt").read()
mk = re.search(r"robust change \(([\d.]+), ([\d.]+)\), \+ to -", rk)
ka, kb = float(mk.group(1)), float(mk.group(2))
assert (ka, kb) == (0.07, 0.085)
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def table(head, body):
    n = len(head)
    assert all(len(r) == n for r in body), (head, body)
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * n] + ["| " + " | ".join(r) + " |" for r in body])


sg = lambda s: "+" if s > 0 else "-"
t1 = table(["lambda", "from", "hybrid sign", "noise signs", "robust", "dln", "float64 sign", "ln\\|det\\|", "seconds (float64 blocks, Rust block 12, logdet)"],
           [[f"{r['lam']:.3f}", "first scan" if r["lam"] in (0.045, 0.05, 0.06, 0.07) else "widened scan", sg(r["sign"]), " ".join(sg(s) for s in r["noise"]), str(r["robust"]),
             f"{r['dln']:.2e}", sg(r["f64_sign"]), f"{r['ln']:.10f}", f"{r['sec']} ({r['sec_parts'][0]}, {r['sec_parts'][1]}, {r['sec_parts'][2]})"] for r in rows])
cum = 0
body = []
for i, r in enumerate(ev):
    cum += r["sec"]
    t = (T0 + datetime.timedelta(seconds=cum)).strftime("%H:%M")
    body.append([str(i + 1), f"{r['lam']:.10f}", "end" if i < 2 else "interior", sg(r["sign"]), " ".join(sg(s) for s in r["noise"]), f"{r['dln']:.2e}", f"{r['ln']:.10f}", str(r["sec"]),
                 f"{r['sec'] / ev[0]['sec']:.2f}", t])
t2 = table(["#", "lambda", "role", "hybrid sign", "noise signs", "dln", "ln\\|det\\|", "seconds", "x the first (2351 s, alone)", "ended about (UTC, start 14:01:09 + cumulative seconds)"], body)
over = [i + 1 for i, r in enumerate(ev) if r["sec"] > 1.5 * ev[0]["sec"]]
lo_d, hi_d = a - ROOT_B, b - ROOT_B
sh = {"R1": R1_ROOT - ROOT_B, "R2": delta}
k_lo, k_hi = ka - ROOT_B, kb - ROOT_B
t3 = table(["", "kappa of the state (and of the mode matrix)", "steps", "root", "shift from state B's own root 0.045968"], [
    ["state B (R0, control)", "0.7", str(STEPS["B"]), "0.045967998", "0"],
    ["R1 (t5, macm3)", "0.5", str(STEPS["R1"]), f"{R1_ROOT}", f"{sh['R1']:+.5f}"],
    ["R2 (this secant)", "0.35", str(STEPS["R2"]), f"{lin:.9f} (bracket {a:.6f} to {b:.6f})", f"{delta:+.5f}"],
    ["Test K: state B, mode matrix at 0.35 (scan pair only, no secant)", "0.7 state, 0.35 mode matrix", f"{STEPS['B']} (state), {STEPS['R2']} (mode matrix)", f"in ({ka}, {kb})", f"{k_lo:+.4f} .. {k_hi:+.4f}"],
])
ratio_k = (k_lo / delta, k_hi / delta)
per_step_r1 = sh["R1"] / (STEPS["R1"] - STEPS["B"])
per_step_r12 = (delta - sh["R1"]) / (STEPS["R2"] - STEPS["R1"])
scan_new = [r["sec"] for r in rows if r["lam"] in (0.035, 0.085, 0.1, 0.13)]
pred = table(["prediction", "result"], [
    ["no robust change in [0.035, 0.130]: 45%; (0.100, 0.130): 25%; (0.085, 0.100): 12%; (0.070, 0.085): 8%; (0.035, 0.045): 7%",
     "(0.100, 0.130) happened (the 25% case, the second most likely): + at 0.035 to 0.100, - at 0.130, all eight robust; the secant root 0.117825 is inside it"],
    ["pole fit (for information): best fit at lambda0 near 0.12, rms 8e-4 in ln", f"the root is {lin:.4f}, near the first of the two registered fits (it does not locate a root, as registered)"],
    ["given a change: |E_root| >= 3e-3 (97%)", f"right: E_root = {e_root:+.5f}, {e_root / 3e-3:.0f} times the bar"],
    ["all four new points robust (80%)", "right: 0.035, 0.085, 0.100, 0.130 all robust (dln 1.33e-05 to 2.03e-05)"],
    ["scan wall: 1800 to 3000 s per point", f"WRONG: {min(scan_new)} to {max(scan_new)} s per point ({scan_wall} s for the four, 12:46:59 to 14:01:09 UTC); the cause was not looked for"],
    ["secant wall: 2 end points and 3 to 6 interior points of 1500 to 2500 s each, 2 to 4 h in all",
     f"WRONG: 2 ends and 8 interior points (10 evaluations), {min(r['sec'] for r in ev)} to {max(r['sec'] for r in ev)} s each, {wall} s = {wall / 3600:.1f} h in all"],
])
sec_txt = f"""
## R2 widened scan and secant result (scan 12:46:59 to 14:01:09 UTC, secant 14:01:09 UTC 27 Nov to {t_end} UTC 28 Nov; unit `i1101r2w`, `run_scan_w.sh`; 1 thread per process, nice 10, `--b12=rust --b12_threads=1`; `results_r2w.md`, `results_r2w_secant.md`, `read_lower_r2w.txt`, `secant_r2w.jsonl`, `secant_r2w.log`, `scan_r2/`, `scan_r2w/`, `scan_r2all/`; written {now} by the clock)
All processes printed the pin check and the record system, and exited 0. The scan read the eight points (the four of `scan_r2/` and the four of `scan_r2w/`) with `read_lower.py`: 1 robust change, (0.100, 0.130), + to -, no non-robust point, no ln|det| local minimum; the secant ran on it (`--pin=25ba3a91,9111bfca`).

{t1}

**The secant** (`d18_secant.py run` 0.1 0.13, tol 5e-5, `maxev 20`; status `tol`, exit 0, 10 evaluations, {wall} s; both bracket ends robust with opposite hybrid signs, inside the scan's pair; the reading rule of the section above is met):

{t2}

**Root and bar.** Final bracket ({a:.9f}, {b:.9f}), width {root['width']:.2e}, signs + and -, both ends robust (dln {ev[-1]['dln']:.2e} at the + end, {ev[-2]['dln']:.2e} at the - end, under 0.1); det-linear root (`lam_lin`) **{lin:.9f}**.
- delta = root - 0.045968 = **{delta:+.6f}** (the bracket gives {lo_d:+.6f} to {hi_d:+.6f}).
- E_root = delta x 16/15 = **{e_root:+.6f}** (bracket {lo_d * 16 / 15:+.6f} to {hi_d * 16 / 15:+.6f}).
- Bar (t5's): |E_root| >= 3e-3 is real, <= 1e-3 refutes #1103's inference, between is mixed. **|E_root| >= 3e-3: the step error is real** (`results_1101.py r2w --secant` exit 0, `results_r2w_secant.md`). The estimator values are at the width of the final bracket, not rigorous enclosures.

**The three roots and Test K side by side** (arithmetic on the numbers above and on the scan pair of `read_lower_k2.txt`; not a fit):

{t3}

- Shift per added step: {per_step_r1:.2e} from 4179 to 5847 steps, {per_step_r12:.2e} from 5847 to 8351 steps. The shift grows with the refinement and by less than the steps do; three points, so no extrapolation is made here.
- Test K's scan pair puts the mode matrix's part of R2's shift at {ratio_k[0]:.2f} to {ratio_k[1]:.2f}; the state's part is the rest, {1 - ratio_k[1]:.2f} to {1 - ratio_k[0]:.2f}. This uses K's pair, not a K root (no secant, t5's order).

**Load and the priority rule.** The first evaluation took {ev[0]['sec']} s alone. Evaluations {", ".join(str(i) for i in over)} took more than 1.5 times that ({1.5 * ev[0]['sec']:.0f} s), up to {max(r['sec'] for r in ev)} s (the third). What ran beside R2's secant, by the clock: Test K's four scans 15:57 to 17:31 UTC, its extension's four scans 17:35 to 19:10, the #1104 re-solve (3 threads, nice 10) from 19:37, the #1104 kappa 0.7 re-root (1 thread, nice 19) 19:39 to 22:40. Evaluation 2 (about 14:41 to 15:46) ran before them, and I did not record here what else was busy then. I did not throttle: the extra jobs ran at nice 19 or were the registered 4 to 5 busy threads, and 4600 s beside five busy threads was the time I had registered for the loaded case (#1104 README, Resources). Evaluations 9 and 10 ran with only the re-solve (3 threads) beside R2 and took {ev[8]['sec']} and {ev[9]['sec']} s ({ev[9]['sec'] / ev[0]['sec']:.2f} times the first).

{pred}

## Status after R2's secant
- {t_end} UTC 28 Nov: R2's secant ended (status `tol`, exit 0, {len(ev)} evaluations, {wall} s): root {lin:.9f}, delta {delta:+.6f}, E_root {e_root:+.6f}, the step error is real; reported to t5 by hc (00:4x UTC). #1101 is not closed and keeps its `running` label (t5 decides).
"""
open(sys.argv[1], "w").write(sec_txt)
post = f"""**dh170: R2's widened scan and secant: root {lin:.6f}, delta {delta:+.5f}, E_root {e_root:+.5f}: the step error is real** ({now} by the clock)

R2's state (kappa 0.35 re-solve, blobs 25ba3a91, 9111bfca), scanner `d18_secant.py` at d4b6b6ce, Rust block 12, 1 thread per process. Scan 12:46:59 to 14:01:09 UTC (0.035, 0.085, 0.100, 0.130; the first scan's 0.045 to 0.070 ended at 12:12), then the secant 14:01:09 UTC to {t_end} UTC 28 Nov.

{t1}

One robust change, (0.100, 0.130), + to -. The secant on it ended with status `tol` (exit 0, 10 evaluations, {wall} s = {wall / 3600:.1f} h):

{t2}

- Final bracket ({a:.9f}, {b:.9f}), width {root['width']:.1e}, signs + and -, both ends robust; det-linear root **{lin:.9f}**.
- delta = root - 0.045968 = **{delta:+.6f}**; E_root = delta x 16/15 = **{e_root:+.6f}**.
- Bar: **|E_root| >= 3e-3, the step error is real** ({e_root / 3e-3:.0f} times the bar); not <= 1e-3 (the refuting case). Values at the width of the bracket, not enclosures.

{t3}

- The shift per added step falls: {per_step_r1:.2e} (4179 to 5847 steps), {per_step_r12:.2e} (5847 to 8351). Three points; no extrapolation here.
- Test K's scan pair puts the mode matrix's part of R2's shift at {ratio_k[0]:.2f} to {ratio_k[1]:.2f}, the state's part at {1 - ratio_k[1]:.2f} to {1 - ratio_k[0]:.2f} (pair arithmetic; no K root).
- Load: evaluations {", ".join(str(i) for i in over)} took more than 1.5 times the first ({ev[0]['sec']} s alone), up to {max(r['sec'] for r in ev)} s, beside Test K's scans (15:57 to 19:10 UTC) and the #1104 jobs from 19:37 (nice 19 for the re-root, 3 threads for the re-solve). I did not throttle (4600 s beside five busy threads was the registered loaded time). The last two ran at {ev[8]['sec']} and {ev[9]['sec']} s.

Predictions scorecard (README): the bucket (0.100, 0.130), |E_root| >= 3e-3 and the robust points right; the scan wall (1800 to 3000 s per point; actual {min(scan_new)} to {max(scan_new)} s) and the secant wall (2 to 4 h; actual {wall / 3600:.1f} h) wrong.

Raw: `I1101-dh170/` of the raw repository. I did not close #1101 and left its `running` label; t5 decides.
"""
open(sys.argv[2], "w").write(post)
