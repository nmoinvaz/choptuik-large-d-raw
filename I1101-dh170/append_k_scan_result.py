"""#1101 Test K: writes the scan's result section (README text with Status line and predictions scorecard) and the issue post from scan_k/*.jsonl,
secant_r2w.jsonl and steps_check_k.txt, with the clock read here.
usage: append_k_scan_result.py README_SECTION_OUT POST_OUT      (does not touch README.md itself; the section is appended by the caller)
Every table is asserted to have the same cell count in each row."""
import datetime
import glob
import json
import sys

ROOT_B = 0.045967998             # state B's own root at kappa 0.7 (dh370)
R1_ROOT = 0.09500769             # t5's R1 (kappa 0.5) root, comment 7223316450 (macm3)
rows = sorted((json.loads(l) for f in glob.glob("scan_k/scan_D23.0_p*.jsonl") for l in open(f) if l.strip()), key=lambda r: r["lam"])
assert [r["lam"] for r in rows] == [0.085, 0.1, 0.115, 0.13], [r["lam"] for r in rows]
assert all(r["sign"] < 0 and r["robust"] and r["noise_robust"] and r["b12"] == "rust" for r in rows)
r2 = [json.loads(l) for l in open("secant_r2w.jsonl") if l.strip()]
r2 = [r for r in r2 if r.get("kind") == "eval"]
r2pt = {r["lam"]: r for r in r2}
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def table(head, body):
    n = len(head)
    assert all(len(r) == n for r in body), (head, body)
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * n] + ["| " + " | ".join(r) + " |" for r in body])


sg = lambda s: "+" if s > 0 else "-"
t1 = table(["lambda", "hybrid sign", "noise signs", "robust", "dln", "float64 sign", "ln\\|det\\|", "seconds (float64 blocks, Rust block 12, logdet)"],
           [[f"{r['lam']:.3f}", sg(r["sign"]), " ".join(sg(s) for s in r["noise"]), str(r["robust"]), f"{r['dln']:.2e}", sg(r["f64_sign"]), f"{r['ln']:.10f}",
             f"{r['sec']} ({r['sec_parts'][0]}, {r['sec_parts'][1]}, {r['sec_parts'][2]})"] for r in rows])
slopes = [(rows[i + 1]["ln"] - rows[i]["ln"]) / (rows[i + 1]["lam"] - rows[i]["lam"]) for i in range(3)]
by = {r["lam"]: r for r in rows}
shared = [lam for lam in (0.1, 0.13) if lam in r2pt]
t2 = table(["lambda", "K: sign, ln\\|det\\|", "R2: sign, ln\\|det\\|", "K - R2 in ln\\|det\\|"],
           [[f"{lam:.3f}", f"{sg(by[lam]['sign'])} {by[lam]['ln']:.6f}", f"{sg(r2pt[lam]['sign'])} {r2pt[lam]['ln']:.6f}", f"{by[lam]['ln'] - r2pt[lam]['ln']:+.4f}"] for lam in shared])
neg = sorted(r["lam"] for r in r2 if r["sign"] < 0 and r["robust"])
pos = sorted(r["lam"] for r in r2 if r["sign"] > 0 and r["robust"])
lo_r2, hi_r2 = max(pos), min(neg)          # R2's current robust bracket
assert lo_r2 < hi_r2
hi_s = f"{hi_r2:.6f}"
gap = lo_r2 - 0.085
secs = [r["sec"] for r in rows]
pred = table(["prediction", "result"], [
    ["the `kappa_mm 0.35` step count within 2% of 8351 (90%)", "right: 8351 on all four (`steps_check_k.txt` PASS), with the record system reproduced (|F| 3.1912e-10 against 3.1949e-10, 4179 steps)"],
    ["k_c 31 control: 0.7 bit for bit equal to plain (90%); 0.35 moves ln\\|det\\| by more than 1e-3 (97%)", "right: -430.2952244423991 for both, and +0.6949 at 0.35"],
    ["the scan has a robust change in 0.085-0.130 (65%; no change 35%)", "WRONG: no change; the registered 35% outcome happened (all four hybrid signs -, all robust)"],
    ["given a root: within 3e-3 of r2 (40%), between (30%), 1e-2 or more (30%)", "not formed: no root. The inference below (outside the bars) puts the difference above 1e-2 if its assumptions hold"],
    ["scan wall per point 4400 to 6000 s (60%)", f"right: {min(secs)} to {max(secs)} s (5 busy threads on 4 cores, as registered)"],
    ["secant wall 4 to 6 h (60%)", "not run (no bracket)"],
])
sec_txt = f"""
## Test K scan result (15:57:43 to about 17:31 UTC; unit `i1101k`; 4 processes, 1 thread each, nice 10, `--kappa_mm=0.35 --b12=rust --b12_threads=1`; `results_k.md`, `read_lower_k.txt`, `scan_k/`, `scan_k_p0.raw` to `scan_k_p3.raw`; written {now} by the clock)
All four processes printed the pin check, `kappa_mm 0.35: ... 8351 steps (the record's kappa 0.7: 4179)`, the record system (`|F| 3.1911792672e-10 (record 3.1949266444e-10), steps 4179 (record 4179)`) and `block 12 by ellrs (avx2, products dgemm, 1 threads)`, and exited 0.

{t1}

**No robust change in 0.085-0.130: report and wait** (`results_1101k.py scan` exit 2; `read_lower.py`: 0 robust changes, endpoint signs - and -, no ln|det| local minimum, float64 alone has the opposite sign (+) at all four, which the earlier scans showed too). Nothing widened by me, no secant: the reading rule needs a robust change. The bars are not applied (no root).

What the four points do and do not say (mine, outside the bars; the estimators are values at the scanned lambdas, not enclosures):
- `ln|det|` falls smoothly, by {-slopes[0]:.0f}, {-slopes[1]:.0f} and {-slopes[2]:.0f} per unit lambda over the three intervals, with no dip.
- Assuming the orientation (sign + below the root, - above it: measured at state B's own root, + at 0.045 and - at 0.050 in the control, and at R2's bracket, + at 0.100 and - at 0.130; assumed for K) and a single sign change: state B's root with the mode matrix at kappa 0.35 lies **below 0.085**. R2's secant (`secant_r2w.jsonl`, as of {now}) has + at {lo_r2} and - at {hi_s} (its third evaluation, the interior point), so r2 lies in ({lo_r2}, {hi_s}) and **|root - r2| > {gap:.3f}**, above the 1e-2 bar: the state's kappa matters too. This is an inference from signs under the stated assumptions, not a measured root; the scan below 0.085 would measure it.
- Against t5's R1 (kappa 0.5 state and steps, root {R1_ROOT}, comment 7223316450): if the step error were the mode matrix's alone, the root would depend on the mode matrix's steps only, and with the root rising monotonically as they are refined (0.046 at 0.7, {R1_ROOT} at 0.5) the 0.35 root on state B would be at or above R1's. It lies below 0.085 < {R1_ROOT} under the assumptions above. In shifts from state B's own root {ROOT_B}: R2's is more than {lo_r2 - ROOT_B:.3f}, Test K's is less than {0.085 - ROOT_B:.3f} (and negative if K's root lies below {ROOT_B}).
- Alternatives not excluded by four minus signs: an even number of sign changes inside the scanned range (spacing 0.015 would miss two close ones), or the root above 0.130 with the opposite orientation.

R2's ln|det| and K's at the lambdas both have (K's mode matrix on kappa 0.35 steps, R2's solved at kappa 0.35):

{t2}

{pred}
"""
status = (f"- {now}: Test K's scan done (about 5300 s per point, 17:31 UTC): hybrid sign - at 0.085, 0.100, 0.115, 0.130, all robust; no robust change, so no secant: reported to t5, "
          f"waiting for t5's order (nothing widened). R2's secant is still running (bracket ({lo_r2}, {hi_s}))." )
open(sys.argv[1], "w").write(sec_txt + "\n## Status after the scan\n" + status + "\n")
post = f"""**dh170: Test K's scan: no robust change in 0.085-0.130, all four points -; no secant, nothing widened** ({now} by the clock)

State B (R0's kappa 0.7 re-solve, blobs 90d3e655, d1a3a641) scanned with `--kappa_mm=0.35 --b12=rust --b12_threads=1` (wip/ell1-kappa-mm f56f91d2, 4 processes, nice 10, 15:57:43 to about 17:31 UTC). All four printed `kappa_mm 0.35: ... 8351 steps (the record's kappa 0.7: 4179)` and the record system.

{t1}

No robust change: the reading rule (a root from a `run` ending `tol`) does not apply, so the bars are not applied. Outside the bars, assuming the orientation (+ below the root, - above) and one sign change:
- K's root is **below 0.085** (the orientation is measured at state B and at R2, assumed for K). R2's secant has + at {lo_r2} and - at {hi_s} (its third evaluation), so r2 is in ({lo_r2}, {hi_s}) and |root - r2| > {gap:.3f}, above the 1e-2 bar: **the state's kappa matters too** (an inference from signs, not a measured root).
- Against R1 (kappa 0.5, root {R1_ROOT}): the mode matrix at 0.35 on state B gives a root below 0.085, below R1's. If the step error were the mode matrix's alone, the root would depend on its steps only and (rising monotonically as they are refined) be at or above R1's.
- Not excluded: two sign changes closer than the 0.015 spacing, or the root above 0.130 with the opposite orientation.

{t2}

Predictions scorecard (README): step count, controls and wall time right; the 65% "robust change" prediction wrong (the 35% case). R2's secant keeps running (1 thread; its fourth evaluation started 17:06 UTC).

**Proposal, not started:** scan K below 0.085 at lambda 0.045, 0.055, 0.065, 0.075 (4 processes, about 1.5 h), then `run` at tol 5e-5 on the change (about 4-6 h). This measures K's root and the bars apply. I wait for t5's order. #1101 stays open with its `running` label.
"""
open(sys.argv[2], "w").write(post)
