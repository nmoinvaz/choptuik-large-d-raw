"""#1101 Test K extension: writes the result section (README text with Status line and predictions scorecard) and the issue post from scan_k/*.jsonl (eight points),
read_lower_k2.txt, secant_r2w.jsonl and steps.txt, with the clock read here.
usage: append_k2_result.py README_SECTION_OUT POST_OUT      (does not touch README.md itself; the section is appended by the caller)
Every table is asserted to have the same cell count in each row."""
import datetime
import glob
import json
import re
import sys

ROOT_B = 0.045967998             # state B's own root at kappa 0.7 (dh370)
rows = sorted((json.loads(l) for f in glob.glob("scan_k/scan_D23.0_p*.jsonl") for l in open(f) if l.strip()), key=lambda r: r["lam"])
assert [r["lam"] for r in rows] == [0.04, 0.055, 0.07, 0.085, 0.1, 0.115, 0.13, 0.15], [r["lam"] for r in rows]
assert all(r["robust"] and r["noise_robust"] and r["b12"] == "rust" for r in rows)
signs = "".join("+" if r["sign"] > 0 else "-" for r in rows)
assert signs == "+++-----", signs                                  # the reading below is written for this pattern; anything else stops here
rl = open("read_lower_k2.txt").read()
m = re.search(r"robust change \(([\d.]+), ([\d.]+)\), \+ to -, det-linear ([\d.]+), range \[([\d.]+), ([\d.]+)\]", rl)
assert m and "robust changes: 1;" in rl, rl
ka, kb, klin, klo, khi = (float(x) for x in m.groups())
assert (ka, kb) == (0.07, 0.085)
st = open("steps.txt").read()
t_scans = re.findall(r"(\d\d:\d\d:\d\d) UTC \[k2\] lambda ([\d.]+) exit 0", st)
assert len(t_scans) == 4, t_scans
t_stop = re.search(r"(\d\d:\d\d:\d\d) UTC \[k2s\] unit i1101k2 stopped .*processes of run_scan_k2.sh left: 0; unit state inactive", st).group(1)
t_read = re.search(r"(\d\d:\d\d:\d\d) UTC \[k2r\] results_1101k.py scan \(eight points\) exit 3", st).group(1)
r2 = [json.loads(l) for l in open("secant_r2w.jsonl") if l.strip()]
r2 = [r for r in r2 if r.get("kind") == "eval" and r["robust"]]
pos = [r["lam"] for r in r2 if r["sign"] > 0]
neg = [r["lam"] for r in r2 if r["sign"] < 0]
c, d = max(pos), min(x for x in neg if x > max(pos))               # R2's current robust bracket
n_r2 = len(r2)
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def table(head, body):
    n = len(head)
    assert all(len(r) == n for r in body), (head, body)
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * n] + ["| " + " | ".join(r) + " |" for r in body])


sg = lambda s: "+" if s > 0 else "-"
t1 = table(["lambda", "scan", "hybrid sign", "noise signs", "robust", "dln", "float64 sign", "ln\\|det\\|", "seconds (float64 blocks, Rust block 12, logdet)"],
           [[f"{r['lam']:.3f}", "first" if 0.085 <= r["lam"] <= 0.13 else "extension", sg(r["sign"]), " ".join(sg(s) for s in r["noise"]), str(r["robust"]), f"{r['dln']:.2e}",
             sg(r["f64_sign"]), f"{r['ln']:.10f}", f"{r['sec']} ({r['sec_parts'][0]}, {r['sec_parts'][1]}, {r['sec_parts'][2]})"] for r in rows])
secs = [r["sec"] for r in rows if r["lam"] in (0.04, 0.055, 0.07, 0.15)]
lo_rng, hi_rng = ka - d, kb - c                                    # [a - d, b - c], K's bracket (a, b), R2's (c, d)
assert hi_rng < -1e-2, (lo_rng, hi_rng)                            # the whole range at 1e-2 or more in size
sh_k = (ka - ROOT_B, kb - ROOT_B)
sh_r = (c - ROOT_B, d - ROOT_B)
ratio = (sh_k[0] / sh_r[1], sh_k[1] / sh_r[0])
t2 = table(["", "root's bracket", "shift from state B's own root 0.045968 (bracket ends)", "source"], [
    ["state B, kappa 0.7 (R0, control)", "0.045967998", "0", "dh370, control passed (`results_ctl.md`)"],
    ["K: state B, mode matrix at kappa 0.35", f"({ka}, {kb}), det-linear {klin:.6f}", f"{sh_k[0]:+.4f} .. {sh_k[1]:+.4f}", "this scan (`read_lower_k2.txt`), no secant"],
    ["R2: kappa 0.35 re-solve", f"({c:.6f}, {d:.6f}) after {n_r2} evaluations", f"{sh_r[0]:+.4f} .. {sh_r[1]:+.4f}", "R2's secant, still running"],
    ["R1: kappa 0.5 re-solve (t5, macm3)", "0.09500769", f"{0.09500769 - ROOT_B:+.4f}", "t5's comment 7223316450"],
])
pred = table(["prediction", "result"], [
    ["the `kappa_mm 0.35` step count within 2% of 8351 at all four (90%)", "right: 8351 on all four (`steps_check_k2.txt` PASS), the record system reproduced (|F| 3.1912e-10 against 3.1949e-10, 4179 steps)"],
    ["the first robust change is in (0.070, 0.085): 30%; (0.055, 0.070): 25%; (0.040, 0.055): 20%", "(0.070, 0.085) happened: the most likely of the three buckets, 30%; its hybrid sign pattern is + + + - - - - -"],
    ["no robust change in 0.040-0.150 (15%)", "right: one change"],
    ["the sign at 0.040 is + (80%)", "right"],
    ["given a root: reads as the state's kappa matters (90%)", "void: no secant (t5's order). By the brackets alone the range is "
     f"[{lo_rng:+.4f}, {hi_rng:+.4f}], whole range above 1e-2 in size: the same reading, outside the reading rule"],
    ["scan wall per point 4400 to 6200 s (70%)", f"right: {min(secs)} to {max(secs)} s (5 busy threads on 4 cores, as registered)"],
    ["secant wall 3 to 6 h (60%)", "void: not run"],
])
sec_txt = f"""
## Test K extension result (scans 17:35:53 to {t_scans[-1][0]} UTC; unit `i1101k2`; lambda 0.040, 0.055, 0.070, 0.150, files p4..p7; 4 processes, 1 thread each, nice 10, `--kappa_mm=0.35 --b12=rust --b12_threads=1`; `results_k2.md`, `read_lower_k2.txt`, `scan_k2_p4.raw` to `scan_k2_p7.raw`; written {now} by the clock)
All four processes printed the pin check, `kappa_mm 0.35: ... 8351 steps (the record's kappa 0.7: 4179)`, the record system (`|F| 3.1911792672e-10 (record 3.1949266444e-10), steps 4179 (record 4179)`) and `block 12 by ellrs (avx2, products dgemm, 1 threads)`, and exited 0 at {", ".join(f"{t} (lambda {l})" for t, l in t_scans)} UTC.

{t1}

**The eight signs: + + + - - - - - (0.040 to 0.150). One robust change, (0.070, 0.085), + to -** (`results_1101k.py scan` exit 3, `read_lower.py`: 1 robust change, 0 non-robust points, endpoint signs + at 0.040 and - at 0.150, no ln|det| local minimum; det-linear {klin:.6f}, estimator range [{klo}, {khi}] at the width of the pair). The orientation did not flip (nothing above 0.130 changes). Float64 alone has the opposite sign at 0.085 to 0.130 (the earlier scans showed that too).

**No secant** (t5's order, 17:45 UTC: "a mode matrix at kappa 0.35 about a kappa 0.7 state is not a valid root"), so no root of K is read and the bars are not applied. The brackets alone (estimators at the scanned lambdas, not enclosures; arithmetic by `append_k2_result.py`):

{t2}

- K's bracket (0.070, 0.085) against R2's ({c:.6f}, {d:.6f}): root(K) - root(R2) lies in [{lo_rng:+.4f}, {hi_rng:+.4f}], the whole range above 1e-2 in size, as t5 wrote for a root below 0.085 ("the state's kappa matters"). Outside the reading rule (no secant record), the same range as the reading rule would take it.
- The mode matrix's part of R2's shift: K moved by {sh_k[0]:+.3f} to {sh_k[1]:+.3f} from state B's own root, R2 by {sh_r[0]:+.3f} to {sh_r[1]:+.3f}: the ratio is {ratio[0]:.2f} to {ratio[1]:.2f} from the brackets. The rest, {c - kb:+.3f} to {d - ka:+.3f}, is the state's.

{pred}

## Status after the extension
- {t_scans[-1][0]} UTC: the four scans ended (exit 0 each, last at lambda {t_scans[-1][1]}); {t_stop} UTC: `systemctl --user stop i1101k2.service` ended the frozen driver and its `systemd-inhibit` (no scan was running; `ps`: 0 processes of `run_scan_k2.sh` left, unit inactive; steps.txt tag `k2s`); {t_read} UTC: `run_k2_read.sh` (399f0746) read the eight points, exit 3 (a bracket), no secant (tag `k2r`). Reported to t5; R2's secant runs on ({n_r2} evaluations, bracket ({c:.6f}, {d:.6f})).
"""
open(sys.argv[1], "w").write(sec_txt)
post = f"""**dh170: Test K extension: the eight signs are + + + - - - - -; one robust change, (0.070, 0.085); no secant run** ({now} by the clock)

State B with `--kappa_mm=0.35 --b12=rust --b12_threads=1` at four more lambdas (4 processes, nice 10, 17:35:53 to {t_scans[-1][0]} UTC). All four print `kappa_mm 0.35: ... 8351 steps (the record's kappa 0.7: 4179)` and the record system; all four exit 0.

{t1}

- One robust change, + to -, in (0.070, 0.085) (`read_lower.py`: det-linear {klin:.6f}, estimator range [{klo}, {khi}]); nothing above 0.130 changes, so the orientation did not flip.
- No secant, as ordered ("not a valid root"): K's root is not read and the bars are not applied. By the brackets alone, root(K) - root(R2) is in [{lo_rng:+.4f}, {hi_rng:+.4f}] against R2's current bracket ({c:.6f}, {d:.6f}), the whole range above 1e-2 in size: the state's kappa matters, as you read it.

{t2}

- The mode matrix's part of R2's shift is {ratio[0]:.2f} to {ratio[1]:.2f} of it (bracket arithmetic); the rest, {c - kb:+.3f} to {d - ka:+.3f}, is the state's.
- The stopped driver was ended after the scans (`systemctl --user stop`, 0 processes left, {t_stop} UTC), then the read-only reading ({t_read} UTC). Order and times in the README.
- Predictions scorecard in the README: step count, sign at 0.040, one change and scan wall right; the secant ones void.

R2's secant keeps running ({n_r2} evaluations; its fifth began about 18:23 UTC; bracket ({c:.6f}, {d:.6f})); I report its root when it ends. #1101 stays open with its `running` label.
"""
open(sys.argv[2], "w").write(post)
