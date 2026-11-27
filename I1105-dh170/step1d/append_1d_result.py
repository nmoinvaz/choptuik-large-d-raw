"""#1105 step 1d: writes the result section (README text) and the issue post from the step1d/ records, with the clock read here and every table asserted to
have the same cell count in each row.  usage: append_1d_result.py README_SECTION_OUT POST_OUT   (run in step1d/)"""
import datetime
import json
import re
import sys

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def last(path, kind=None):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    if kind:
        rows = [r for r in rows if r.get("kind") == kind]
    return rows[-1]


def table(head, body):
    n = len(head)
    assert all(len(r) == n for r in body), (head, body)
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * n] + ["| " + " | ".join(r) + " |" for r in body])


steps = open("steps_1d.txt").read()
src = {D: [json.loads(l) for l in open("in/l1kc55Fb1025.jsonl") if l.strip() and json.loads(l)["D"] == D][-1] for D in (15.0, 16.5)}
rec = {15.0: last("l1kc55r150.jsonl"), 16.5: last("l1kc55r165.jsonl")}
root = {"c150": last("root_c150.jsonl", "root"), "r150": last("root_r150.jsonl", "root"), "c165": last("root_c165.jsonl", "root"),
        "c165w": last("root_c165w.jsonl", "root"), "r165": last("root_r165.jsonl", "root"), "r165w": last("root_r165w.jsonl", "root")}
secs = {k: int(re.search(rf"\[{k}\] root exit \d+.*?, (\d+) s", steps).group(1)) for k in root}
wall = {k: int(re.search(rf"\[{k}\] re-solve exit 0, wall (\d+) s", steps).group(1)) for k in ("r150", "r165")}
assert root["c165"]["status"] == "refused" and root["r165"]["status"] == "refused"

rows = []
for tag, D, role in (("c150", 15.0, "continuation"), ("r150", 15.0, "re-solve"), ("c165", 16.5, "continuation"), ("r165", 16.5, "re-solve")):
    runs = [tag] if D == 15.0 else [tag, tag + "w"]
    for k in runs:
        r = root[k]
        rows.append([str(D), tag, role, "first run" if k == tag else "widened to 2.138-2.172", r["status"], f"({r['bracket'][0]!r}, {r['bracket'][1]!r})",
                     f"{r['width']:.2e}", "-" if r["lam_lin"] is None or r["status"] == "refused" else f"{r['lam_lin']:.9f}", str(r["n_eval"]), str(secs[k])])
t_roots = table(["D", "state", "role", "run", "status", "final bracket", "width", "root (lam_lin)", "evals", "seconds"], rows)
rows = []
for D, tag in ((15.0, "r150"), (16.5, "r165")):
    r, s = rec[D], src[D]
    rows.append([str(D), tag, f"{r['F']:.4e}", f"{s['F']:.4e}", str(r["steps"]), str(s["steps"]), repr(r["Delta"]), repr(s["Delta"]), f"{r['Delta'] - s['Delta']:+.3e}",
                 f"{r['constraint']:.4e}", f"{s['constraint']:.4e}", str(wall[tag])])
t_res = table(["D", "re-solve", "\\|F\\|", "source \\|F\\|", "steps", "source steps", "Delta", "source Delta", "Delta change", "psi-constraint", "source psi-constraint", "re-solve s"], rows)

off = {}
for D, c, r in ((15.0, "c150", "r150"), (16.5, "c165w", "r165w")):
    a, b = root[r]["bracket"]
    cc, d = root[c]["bracket"]
    off[D] = (a - d, b - cc, root[r]["lam_lin"] - root[c]["lam_lin"])
t_off = table(["D", "offset = root(re-solve) - root(continuation)", "range from the brackets", "re-solve's Delta change", "source psi-constraint"], [
    ["15.0", f"{off[15.0][2]:+.4e}", f"{off[15.0][0]:+.4e} .. {off[15.0][1]:+.4e}", f"{rec[15.0]['Delta'] - src[15.0]['Delta']:+.3e}", f"{src[15.0]['constraint']:.3e}"],
    ["16.0 (step 1b, 1c)", "+8.59e-4 (U40; U40b +7.5e-4, U40c +9.2e-4)", "re-solve U40 against the continuation state's root 2.2440424 (step 1b's added control); no bracket ranges formed here", "-8.7e-8 (U40)", "1.846e-4"],
    ["16.5", f"{off[16.5][2]:+.4e}", f"{off[16.5][0]:+.4e} .. {off[16.5][1]:+.4e}", f"{rec[16.5]['Delta'] - src[16.5]['Delta']:+.3e}", f"{src[16.5]['constraint']:.3e}"]])
assert off[15.0][1] < 0 and off[16.5][0] > 5e-4
verdict = ("mixed: both offsets are above 5e-4 in size, but D 15's is negative and D 16's is positive, so the 'both above 5e-4 with D 16's sign' bar fails; "
           "neither is below 2e-4, so the 'one-off' bar fails")
pred = table(["item", "prediction", "result"], [
    ["\\|F\\| <= 1e-8 after each re-solve", "90% each", f"right: r150 {rec[15.0]['F']:.3e}, r165 {rec[16.5]['F']:.3e}"],
    ["the brackets hold", "85% each", "WRONG at D 16.5 for both: c165 and r165 were refused (2.148-2.172, both ends +); right at D 15 for both. After the widening both bracketed (c165w ended `nonrobust` with a robust 3.0e-4 bracket)"],
    ["offsets both above 5e-4 and positive", "40%", "no"],
    ["offsets both below 2e-4", "20%", "no"],
    ["offsets mixed", "40%", "right: -5.3e-4 and +3.25e-3"],
    ["re-solve wall 0.4 to 0.9 h (2 threads, beside R2's scan)", "60%", f"WRONG, slower: {wall['r150']} s and {wall['r165']} s (1.15 to 1.22 h), with 8 busy threads on 4 cores"],
    ["root wall 1000 to 1500 s (1 thread)", "60%", f"WRONG for all four, slower: c150 {secs['c150']}, r150 {secs['r150']}, r165w {secs['r165w']} s; c165w {secs['c165w']} s, only just above; each beside other jobs"],
])
tasks = """1. **A second re-solve of D 16.5** from another start (as step 1c did at D 16, two re-solves from the neighbours' states), rooted on 2.138 to 2.172 (the bracket that now holds): is +3.25e-3 reproduced to within the 1.7e-4 scatter? About 1.2 h for two re-solves at 2 threads and 35 min for the roots.
2. **D 15.5 and D 17.0** (one re-solve each, same recipe, brackets from the three offsets): where offset(D) crosses zero and whether it keeps rising. The three offsets are monotone in D (-5.3e-4, +8.6e-4, +3.25e-3) but each rests on one or three re-solves.
3. Only after 1 and 2: what the offset is for a root used in #1025, since the continuation root at D 16.5 differs from the re-solve's by 3.3e-3, 3.3 times the "order 1e-3" the bars name."""
sec = f"""
## Result (27 Nov 10:33:42 to 12:46:57 UTC; units `i1105r150`, `i1105r165`, `i1105c150`, `i1105c165`, `i1105r165w`, `i1105c165w`; re-solves 2 threads, roots 1 thread, nice 10; `results_1d.md`, `root_*.jsonl`, `root_*.log`, `resolve_*.log`, `l1kc55r150.jsonl`, `l1kc55r165.jsonl`, `sol_l1kc55r150_D15.0000.npy`, `sol_l1kc55r165_D16.5000.npy`, `steps_1d.txt`; written {now} by the clock)
{t_res}

The re-solves reproduce the sources' `|F|` and step counts; Delta moves by -4.3e-7 (D 15) and -2.7e-7 (D 16.5).

First runs of the roots at D 16.5 were refused (same-signed ends, 2.148 to 2.172, `lam_lin` extrapolated to 2.14751 and 2.14779, not read); both were rerun on 2.138 to 2.172, the widening by 0.01 on the low side that the signs give (t5 accepted it for r165, comment 7218045186 and the hc). Roots (`d18_secant.py run`, Rust block 12, `--tol=1e-7 --maxev=20`):

{t_roots}

c165w stopped at status `nonrobust` (an interior point at 2.1426872 had dln 0.186 against the 0.1 limit, next to a deep `ln|det|` dip), with robust ends (2.1426861, 2.1429882) of opposite sign: read by the written rule on its bracket, not as a `tol` root.

**Offsets** (`read_1105d.py`, selftest exit 0 and `--mutate=sign` exit 1, `selftest_read_1105d*.txt`; it prefers `root_*w.jsonl` where the first run was refused):
{t_off}

**Verdict by t5's bars: {verdict}.** Reported as measured.

Beyond the bars (mine, not rules): the three offsets rise with D, the D 16.5 one (3.25e-3) is 19 times the 1.7e-4 re-solve scatter of step 1c, and the D 15 one (5.3e-4) is 3 times it. They do not follow Delta's change (-4.3e-7, -8.7e-8 at D 16, -2.7e-7). The psi-constraint of the sources rises with D as the offsets do (4.4e-5, 1.8e-4, 3.8e-4), but offset over constraint is -12, +4.7 and +8.5, so no proportionality. Three points, one re-solve at D 15 and D 16.5 each.

{pred}

**Recommended next tasks (for t5 to choose):**
{tasks}

## Status
- {now}: step 1d done; offsets -5.26e-4 (D 15) and +3.25e-3 (D 16.5), bars: mixed; posted on #1105, `running` label removed, issue left open for t5.
"""
open(sys.argv[1], "w").write(sec)
post = f"""**dh170, step 1d: the continuation-vs-re-solve offset at D 15.0 and D 16.5 (bars: mixed)** ({now} by the clock)

Re-solves at u0 0.04 of the k_c 55 continuation states of record 5be40af4 (D 15.0, D 16.5), 2 threads each, nice 10; then `d18_secant.py run` (Rust block 12, tol 1e-7) of all four states. D 16.5's first runs were refused (2.148-2.172, both ends +); both were rerun on 2.138-2.172 (widened by 0.01 on the low side).

{t_res}

{t_roots}

{t_off}

- **Bars: {verdict}.**
- Offsets by the brackets: D 15 {off[15.0][0]:+.4e} .. {off[15.0][1]:+.4e}; D 16.5 {off[16.5][0]:+.4e} .. {off[16.5][1]:+.4e}. The D 16.5 continuation run (c165w) stopped at status `nonrobust` (an interior point with dln 0.186) with a robust 3.0e-4 bracket; the offset is read on that bracket, and the bar reading does not depend on where the root sits inside it.
- Beyond the bars (mine): offsets rise with D (-5.3e-4, +8.6e-4, +3.25e-3); the D 16.5 one is 19 times the 1.7e-4 scatter of step 1c; they do not follow Delta's change. One re-solve per D at 15 and 16.5.
- Predictions: |F| and mixed offsets right; the brackets at D 16.5 and both walls wrong (scorecard in the README).
- Recommended next (t5 chooses): (1) a second D 16.5 re-solve from another start, rooted on 2.138-2.172; (2) D 15.5 and D 17.0, one re-solve each; (3) only then what the offset means for #1025's continuation roots.

Raw: `I1105-dh170/step1d/` (`results_1d.md`, `root_*.jsonl`, `resolve_*.log`, `steps_1d.txt`, README "Step 1d" result). Issue left open; `running` label removed.
"""
open(sys.argv[2], "w").write(post)
print("wrote")
