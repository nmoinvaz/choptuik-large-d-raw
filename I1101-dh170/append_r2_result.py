"""#1101: writes R2's result section (README text, Status line) and the issue post from scan_r2/*.jsonl and steps.txt, with the clock read here.
usage: append_r2_result.py README_SECTION_OUT POST_OUT      (does not touch README.md itself; the section is appended by the caller)
Every table is asserted to have the same cell count in each row."""
import datetime
import glob
import json
import sys

ROOT_B = 0.045967998
rows = sorted((json.loads(l) for f in glob.glob("scan_r2/scan_D23.0_p*.jsonl") for l in open(f) if l.strip()), key=lambda r: r["lam"])
assert [r["lam"] for r in rows] == [0.045, 0.05, 0.06, 0.07], [r["lam"] for r in rows]
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def table(head, body):
    n = len(head)
    assert all(len(r) == n for r in body), (head, body)
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * n] + ["| " + " | ".join(r) + " |" for r in body])


sg = lambda s: "+" if s > 0 else "-"
t1 = table(["lambda", "hybrid sign", "noise signs", "robust", "dln", "float64 sign", "ln\\|det\\|", "seconds (float64 blocks, Rust block 12, logdet)"],
           [[f"{r['lam']:.3f}", sg(r["sign"]), " ".join(sg(s) for s in r["noise"]), str(r["robust"]), f"{r['dln']:.2e}", sg(r["f64_sign"]), f"{r['ln']:.10f}",
             f"{r['sec']} ({r['sec_parts'][0]}, {r['sec_parts'][1]}, {r['sec_parts'][2]})"] for r in rows])
assert all(r["sign"] > 0 and r["robust"] and r["b12"] == "rust" for r in rows)
slopes = [(rows[i + 1]["ln"] - rows[i]["ln"]) / (rows[i + 1]["lam"] - rows[i]["lam"]) for i in range(3)]
d_hi = 0.070 - ROOT_B
d_lo = 0.045 - ROOT_B
sec = [r["sec"] for r in rows]
ctl = 1521
pred = table(["prediction", "result"], [
    ["R2, which pair brackets: none (20%; 0.045/0.050 30%, 0.050/0.060 20%, 0.060/0.070 30%)", "none: the registered 20% outcome happened; the three pairs (30%, 20%, 30%) did not bracket"],
    ["R2, E_root >= 3e-3 (40%), <= 1e-3 (30%), between (30%)", "not formed: no pair brackets"],
    ["R2 reproduces its record's system, `|F|` and steps (95%)", f"right: all four processes print `|F| 3.1258555149e-10 (record 3.1242366894e-10), steps 8351 (record 8351): the record system`"],
    ["all four points robust (75%)", "right: noise signs equal the hybrid sign at all four, dln 1.35e-05 to 1.38e-05"],
    ["R2 wall 3000 to 4800 s per point on a free machine; the pins section said 26 to 30 min in all",
     f"WRONG, slower: {min(sec)} to {max(sec)} s per point, 6650 s in all (1 h 51 min), {min(sec) / ctl:.1f} to {max(sec) / ctl:.1f} times the control's 1521 s per point at the same k_c. "
     "The machine was not free: step 1d (#1105) started two re-solves of 2 threads each at 10:33:42 UTC, 12 min after this scan, and they ran to 11:42 and 11:47 UTC; "
     "a root run of step 1d ran beside the scan to its end. The cause of the 4.3 times is not separated by these runs (4 processes against the control's 2 is the other difference)"],
])
sec_txt = f"""
## R2 result (27 Nov 10:21:28 to 12:12:18 UTC = 6650 s; unit `i1101r2`; 4 processes, 1 thread each, nice 10; `results_r2.md`, `read_lower_r2.txt`, `scan_r2/`, `scan_r2_p0.raw` to `scan_r2_p3.raw`; written {now} by the clock)
All four processes printed the pin check, `D 23.0 k_c 127: |F| 3.1258555149e-10 (record 3.1242366894e-10), steps 8351 (record 8351): the record system` and `block 12 by ellrs (avx2, products dgemm, 1 threads)`, and exited 0; peak RSS 4.51 to 4.64 GiB (4733404 to 4863912 kB). The selftests ran in the control's step; `results_1101.py r2` exit 2 (no pair brackets).

{t1}

**No pair brackets: report and wait** (`results_1101.py r2` exit 2; nothing widened, no extra lambda). Hybrid sign is + at all four points, all noise-robust; `read_lower.py`: 0 robust changes in 0.045 to 0.070, endpoint signs + and +, no `ln|det|` local minimum without a sign change, no repeated point. The float64 sign differs from the hybrid sign at 0.045, 0.060 and 0.070, as it did at 0.045 in the control. Bars not applied: delta, E_root and the verdict are not formed.

What the four points do and do not say (mine, outside the bars):
- `ln|det|` falls smoothly with lambda, by {-slopes[0]:.0f}, {-slopes[1]:.0f} and {-slopes[2]:.0f} per unit lambda over the three intervals, with no dip. In the control `ln|det|` changed by +1.4268 between 0.045 and 0.050 (its root lies 9.7e-4 above 0.045 and 4.0e-3 below 0.050, and ln(0.00403/0.00097) = 1.43). A root 3e-3 above 0.070 would steepen the 0.060 to 0.070 slope by about 150 per unit lambda (-ln(0.013/0.003)/0.01 is -147); it steepens by 3. A root within about 3e-3 of 0.070, or of 0.045, would show as a dip; none does.
- Assuming the control's orientation (the sign is + below the root and - above it) and a single sign change: the root lies above 0.070, delta > {d_hi:+.6f}, E_root > {d_hi * 16 / 15:+.4f}, which is above #1103's estimate of +0.02. This is an assumption, not a reading under the bars: the orientation of the hybrid sign across two different states is not established, and an even number of roots in the window would also give four equal signs.
- With the other orientation the root lies below 0.045: delta < {d_lo:+.6f}, |E_root| > {-d_lo * 16 / 15:.2e}, so the bar's "<= 1e-3" case fails either way for a single sign change, but 3e-3 is not decided there.

{pred}
"""
status = f"- {now}: R2's scan done (6650 s): hybrid sign + at 0.045, 0.050, 0.060, 0.070, all robust; no pair brackets: reported to t5, waiting for t5's order (nothing widened)."
open(sys.argv[1], "w").write(sec_txt + "\n## Status\n" + status + "\n")
post = f"""**dh170: R2's scan on the Rust block 12 (the bars are not applied: no pair brackets)** ({now} by the clock)

State R2 (win2's kappa 0.35 re-solve at k_c 127, D 23.0; blobs 25ba3a91, 9111bfca; |F| 3.1258555149e-10 against the record's 3.1242366894e-10, 8351 steps = the record's) scanned by `d18_secant.py scan --b12=rust --b12_threads=1` at four lambdas, one process each, from 10:21:28 to 12:12:18 UTC (6650 s, 1 h 51 min).

{t1}

- **No pair brackets**: hybrid sign + at 0.045, 0.050, 0.060 and 0.070, all noise-robust (dln 1.35e-05 to 1.38e-05). `read_lower.py`: 0 robust changes, endpoint signs + and +. `results_1101.py r2` exit 2: report and wait. delta and E_root are not formed, and no bar is applied. Nothing widened, no extra lambda.
- `ln|det|` falls smoothly with lambda (by {-slopes[0]:.0f}, {-slopes[1]:.0f}, {-slopes[2]:.0f} per unit lambda) with no dip, whereas the control's moved by +1.43 between 0.045 and 0.050 beside its root at 0.045968. A root within about 3e-3 of 0.045 or 0.070 would show; none does.
- My reading outside the bars, with its assumption: if the sign is + below the root and - above it as in the control, and the window holds one sign change at most, the root is above 0.070: delta > {d_hi:+.4f}, E_root > {d_hi * 16 / 15:+.4f}, above #1103's +0.02. With the opposite orientation the root is below 0.045 and |E_root| > {-d_lo * 16 / 15:.2e}. Either way the "|E_root| <= 1e-3" case does not hold for a single sign change. The orientation across two states is not established, and an even number of roots in the window would also give four equal signs.
- Time: {min(sec)} to {max(sec)} s per point, {min(sec) / ctl:.1f} to {max(sec) / ctl:.1f} times the control's 1521 s per point at the same k_c. I started #1105 step 1d's two re-solves (2 threads each) 12 minutes into the scan, so the machine was not free; the scan's ETA of 10:50 UTC was wrong. The runs do not separate that cause from the 4-against-2 process count.
- The control passes (comment 7212966539); the Rust block 12 is bit for bit the stored Python block.

Raw: `I1101-dh170/` (`results_r2.md`, `read_lower_r2.txt`, `scan_r2/`, `scan_r2_p*.raw`, `steps.txt`; README "R2 result"). #1101 stays open and keeps its `running` label (win2 and dh370 also use it). Waiting for t5.
"""
open(sys.argv[2], "w").write(post)
print("wrote", sys.argv[1], sys.argv[2])
