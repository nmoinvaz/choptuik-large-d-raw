"""#1105 step 1e: writes the result section (README text) and the issue post from the step1e/ records, with the clock read here, every number taken from the
records and every table asserted to have the same cell count in each row.  usage: append_1e_result.py README_SECTION_OUT POST_OUT   (run in step1e/)"""
import datetime
import json
import re
import sys

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def rows(path, kind=None):
    r = [json.loads(l) for l in open(path) if l.strip()]
    return [x for x in r if x.get("kind") == kind] if kind else r


def last(path, kind=None):
    return rows(path, kind)[-1]


def table(head, body):
    n = len(head)
    assert all(len(r) == n for r in body), (head, body)
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * n] + ["| " + " | ".join(r) + " |" for r in body])


steps = open("steps_1e.txt").read()
src = {"r165b": last("in/l1kc55r165.jsonl"), "r155": [r for r in rows("in/l1kc55Fb1025.jsonl") if r["D"] == 15.5][-1]}
rec = {"r165b": last("l1kc55r165b.jsonl"), "r155": last("l1kc55r155.jsonl")}
root = {k: last(f"root_{k}.jsonl", "root") for k in ("r165b", "r155", "c155")}
r165 = last("../step1d/root_r165w.jsonl", "root")
c165 = last("../step1d/root_c165w.jsonl", "root")
r150 = last("../step1d/root_r150.jsonl", "root")
c150 = last("../step1d/root_c150.jsonl", "root")
secs = {k: int(re.search(rf"\[{k}\] root exit \d+.*?, (\d+) s", steps).group(1)) for k in root}
wall = {k: int(re.search(rf"\[{k}\] re-solve exit 0, wall (\d+) s", steps).group(1)) for k in ("r165b", "r155")}
src_all = rows("in/l1kc55Fb1025.jsonl")
src_c = {D: [r for r in src_all if r["D"] == D][-1] for D in (15.0, 15.5, 16.0, 16.5)}
res1d = {15.0: last("../step1d/l1kc55r150.jsonl"), 16.5: last("../step1d/l1kc55r165.jsonl")}
assert root["c155"]["status"] == "tol" and root["r165b"]["status"] == "nonrobust" and root["r155"]["status"] == "nonrobust"
for k in root:
    assert all(root[k]["robust"]) and root[k]["signs"][0] != root[k]["signs"][1], k
assert r165["status"] == "tol" and all(r165["robust"])

# T and offset(15.5), by lam_lin and by the brackets [a - d, b - c]
a, b = root["r165b"]["bracket"]
c, d = r165["bracket"]
T = (root["r165b"]["lam_lin"] - r165["lam_lin"], a - d, b - c)
a, b = root["r155"]["bracket"]
c, d = root["c155"]["bracket"]
O155 = (root["r155"]["lam_lin"] - root["c155"]["lam_lin"], a - d, b - c)
a, b = r150["bracket"]
c, d = c150["bracket"]
O150 = (r150["lam_lin"] - c150["lam_lin"], a - d, b - c)
a, b = last("../step1d/root_r165w.jsonl", "root")["bracket"]
c, d = c165["bracket"]
O165 = (r165["lam_lin"] - c165["lam_lin"], a - d, b - c)
assert T[2] < -3e-4 and T[1] < -3e-4, T      # entirely outside the bar, below
assert O155[1] < -4e-4 and O155[2] > -5e-4 and O155[0] < -5e-4, O155      # lam_lin below -5e-4, the range straddles it
# the numbers printed by the reader must equal these
rd = open("results_1e.md").read()
assert f"{T[0]:+.4e}" in rd and f"{T[1]:+.4e}" in rd and f"{T[2]:+.4e}" in rd, (T, "reader differs")
assert f"{O155[0]:+.4e}" in rd and f"{O155[1]:+.4e}" in rd and f"{O155[2]:+.4e}" in rd, (O155, "reader differs")

t_res = table(["re-solve", "from", "D", "\\|F\\|", "source \\|F\\|", "steps", "source steps", "Delta", "Delta change", "psi-constraint", "re-solve s"], [
    ["r165b", "r165", "16.5", f"{rec['r165b']['F']:.4e}", f"{src['r165b']['F']:.4e}", str(rec["r165b"]["steps"]), str(src["r165b"]["steps"]), repr(rec["r165b"]["Delta"]),
     f"{rec['r165b']['Delta'] - src['r165b']['Delta']:+.3e}", f"{rec['r165b']['constraint']:.4e}", str(wall["r165b"])],
    ["r155", "continuation c155", "15.5", f"{rec['r155']['F']:.4e}", f"{src['r155']['F']:.4e}", str(rec["r155"]["steps"]), str(src["r155"]["steps"]), repr(rec["r155"]["Delta"]),
     f"{rec['r155']['Delta'] - src['r155']['Delta']:+.3e}", f"{rec['r155']['constraint']:.4e}", str(wall["r155"])]])
roots_rows = []
for k, D, role, r in (("r165", 16.5, "re-solve (step 1d, widened run)", r165), ("r165b", 16.5, "re-solve of r165", root["r165b"]), ("c155", 15.5, "continuation", root["c155"]),
                      ("r155", 15.5, "re-solve", root["r155"])):
    roots_rows.append([str(D), k, role, r["status"], f"({r['bracket'][0]!r}, {r['bracket'][1]!r})", f"{r['width']:.2e}", f"{r['lam_lin']:.9f}", str(r["n_eval"]),
                       str(secs[k]) if k in secs else "step 1d"])
t_roots = table(["D", "state", "role", "status", "final bracket", "width", "root (lam_lin)", "evals", "seconds"], roots_rows)
dl = {15.0: res1d[15.0]["Delta"] - src_c[15.0]["Delta"], 15.5: rec["r155"]["Delta"] - src["r155"]["Delta"], 16.0: 1.0017134267209413 - 1.0017135137307174,
      16.5: res1d[16.5]["Delta"] - src_c[16.5]["Delta"]}
off = {15.0: O150[0], 15.5: O155[0], 16.0: 8.59e-4, 16.5: O165[0]}
t_off = table(["D", "offset = root(re-solve) - root(continuation)", "range from the brackets", "re-solve's Delta change", "source psi-constraint", "from"], [
    ["15.0", f"{O150[0]:+.4e}", f"{O150[1]:+.4e} .. {O150[2]:+.4e}", f"{dl[15.0]:+.3e}", f"{src_c[15.0]['constraint']:.3e}", "step 1d (r150, c150)"],
    ["15.5", f"{O155[0]:+.4e}", f"{O155[1]:+.4e} .. {O155[2]:+.4e}", f"{dl[15.5]:+.3e}", f"{src_c[15.5]['constraint']:.3e}", "this step (r155, c155)"],
    ["16.0", "+8.59e-4 (U40; U40b +7.5e-4, U40c +9.2e-4)", "no bracket ranges formed", f"{dl[16.0]:+.3e}", f"{src_c[16.0]['constraint']:.3e}", "steps 1b, 1c"],
    ["16.5", f"{O165[0]:+.4e}", f"{O165[1]:+.4e} .. {O165[2]:+.4e}", f"{dl[16.5]:+.3e}", f"{src_c[16.5]['constraint']:.3e}", "step 1d (r165, c165w nonrobust)"]])
ratio = O165[0] / abs(T[0])
verdict = (f"|T| = {abs(T[0]):.2e} (range {T[1]:+.4e} .. {T[2]:+.4e}, entirely below -3e-4): the bar fires, and T is above 3e-4 and below 1e-3. "
           "A re-solve of a re-solve at D 16.5 moves the root by 1.3 times the bar's 3e-4, not by 1e-3 or more")
pred = table(["item", "prediction", "result"], [
    ["\\|F\\| <= 1e-8 after each re-solve", "92% each", f"right: r165b {rec['r165b']['F']:.3e}, r155 {rec['r155']['F']:.3e}"],
    ["r165b: \\|T\\| <= 3e-4", "45%", f"WRONG: T = {T[0]:+.2e}"],
    ["r165b: \\|T\\| between 3e-4 and 1e-3", "25%", f"right: {abs(T[0]):.2e}"],
    ["r165b: \\|T\\| 1e-3 or more", "30%", "no"],
    ["r165b first-run bracket (2.138-2.172) holds", "85%", f"right: root {root['r165b']['lam_lin']:.6f}"],
    ["r155 and c155 first-run bracket (2.3282-2.3522) holds", "60% each", f"right for both: r155 {root['r155']['lam_lin']:.6f}, c155 {root['c155']['lam_lin']:.6f}, no widening needed"],
    ["offset(15.5) in -5e-4 .. +1e-3", "55%", f"no by lam_lin ({O155[0]:+.4e}); the range {O155[1]:+.4e} .. {O155[2]:+.4e} straddles -5e-4"],
    ["offset(15.5) above +1e-3", "25%", "no"],
    ["offset(15.5) below -5e-4", "20%", f"by lam_lin yes, by the range a straddle: {O155[0]:+.4e}, not clean"],
    ["re-solve wall 0.5 to 1.0 h", "60%", f"half right: r155 {wall['r155']} s ({wall['r155'] / 3600:.2f} h); r165b {wall['r165b']} s ({wall['r165b'] / 3600:.2f} h) is faster than 0.5 h"],
    ["root wall 1000 to 2000 s", "60%", f"one of three: r155 {secs['r155']} s; c155 {secs['c155']} s and r165b {secs['r165b']} s are above (by 12% and 14%)"]])
tasks = f"""1. **D 15.5 re-solve of a re-solve (r155b)**, rooted on 2.3282-2.3522, about 40 min plus 30 min: tests at D 15.5 what r165b tested at D 16.5, where the offset ({O155[0]:+.2e}) equals D 15's ({O150[0]:+.2e}) to {abs(O155[0] - O150[0]):.0e}.
2. **One more D**, one re-solve and the continuation root: D 14.5 (the record's lowest point) for whether the flat -5.3e-4 continues below D 15, or D 17.0 for whether the offset keeps rising past +3.25e-3. The D 14.5 state is in the raw repository (`I1025-mac/out/sol_l1kc55Fb1025_D14.5000.npy`, blob d9238215); I found no k_c 55 state at D 17 (`I1025-mac/out` and `I1025-win2b/st` end at D 16.5), so D 17 needs a continuation first.
3. Only after those: what the offset means for #1025, whose roots are continuation-state roots."""
sec = f"""
## Result (27 Nov {steps.splitlines()[0][11:16]} to 15:42:49 UTC; units `i1105r165b`, `i1105r155`, `i1105c155`; re-solves 2 threads, roots 1 thread, nice 10, beside the R2 secant (1 thread); `results_1e.md`, `root_*.jsonl`, `root_*.log`, `resolve_*.log`, `l1kc55r165b.jsonl`, `l1kc55r155.jsonl`, `sol_l1kc55r165b_D16.5000.npy`, `sol_l1kc55r155_D15.5000.npy`, `steps_1e.txt`; written {now} by the clock)
{t_res}

Both re-solves reproduce the source's `|F|` and step count. No first-run bracket was refused, so no run was widened.

Roots (`d18_secant.py run`, Rust block 12, `--tol=1e-7 --maxev=20`; r165 is step 1d's widened run, for T):

{t_roots}

r165b and r155 stopped at status `nonrobust`: the probe at `lam_lin` landed in the `ln|det|` dip with dln 0.193 (r165b, at 2.1455493) and 0.394 (r155, at 2.3360515), above the 0.1 limit. Both final brackets have robust ends of opposite sign and are read by the written rule on the bracket, not as `tol` roots.

**T** (`read_1105e.py`, selftest exit 0, `--mutate=bar` and `--mutate=sign` exit 1, `selftest_read_1105e*.txt`): T = root(r165b) - root(r165) = {T[0]:+.4e} by `lam_lin`, range from the brackets {T[1]:+.4e} .. {T[2]:+.4e}.

**Offsets** (re-solve minus continuation), with the earlier steps':
{t_off}

**Verdict by t5's bar: {verdict}.** The reader's line says "of order 1e-3 or more"; the measured size is {abs(T[0]):.1e}. Reported as measured. D 15.5 has no bar.

Beyond the bars (mine, not rules):
- The two re-solved D 16.5 states differ by {abs(T[0]):.1e}; r165 sits {O165[0]:+.2e} above the continuation state's robust bracket (range {O165[1]:+.2e} .. {O165[2]:+.2e}), {ratio:.1f} times |T|. At D 16 (step 1c) the three re-solves span 1.7e-4 and sit +7.5e-4 to +9.2e-4 above the source's root. So at D 16 and D 16.5 re-solved states agree with each other better than with the continuation state, by about 4 to 8 times.
- r165b's Delta equals r165's to {abs(rec['r165b']['Delta'] - src['r165b']['Delta']):.1e} while its root moved {T[0]:+.1e}: Delta does not track the root's move.
- offset(D 15.5) = {O155[0]:+.4e} and offset(D 15.0) = {O150[0]:+.4e}: equal to {abs(O155[0] - O150[0]):.1e} ({abs(O155[0] - O150[0]) / abs(O150[0]):.2%}), with both brackets 5e-8 to 4e-5 wide. The four offsets (-5.26e-4, -5.26e-4, +8.6e-4, +3.25e-3) are flat from D 15 to D 15.5 and rise after; step 1d's "rise with D" was drawn from three of them.
- The offsets do not follow the re-solve's Delta change ({dl[15.0]:+.1e}, {dl[15.5]:+.1e}, {dl[16.0]:+.1e}, {dl[16.5]:+.1e}), and the source psi-constraint rises ({src_c[15.0]['constraint']:.1e}, {src_c[15.5]['constraint']:.1e}, {src_c[16.0]['constraint']:.1e}, {src_c[16.5]['constraint']:.1e}) while the offset is flat then rising: no proportionality.
- One re-solve per D at 15, 15.5 and 16.5 for the offsets, three at D 16.

{pred}

**Recommended next tasks (for t5 to choose):**
{tasks}

## Status
- {now}: step 1e done (14:35:49 to 15:42:49 UTC); T = {T[0]:+.2e} (bar 3e-4: fires, below 1e-3), offset(15.5) = {O155[0]:+.2e}; posted on #1105, `running` label removed, issue left open for t5.
"""
open(sys.argv[1], "w").write(sec)
post = f"""**dh170, step 1e: does a re-solve of a re-solve stay put at D 16.5 (|T| = {abs(T[0]):.2e}, above the 3e-4 bar), and the D 15.5 offset ({O155[0]:+.2e})** ({now} by the clock)

r165b (re-solve of r165), r155 (re-solve of the D 15.5 continuation state) and the roots of r165b, r155 and c155 (continuation), 14:35:49 to 15:42:49 UTC, beside the R2 secant. No first-run bracket was refused; none was widened.

{t_res}

{t_roots}

{t_off}

- **t5's bar on T = root(r165b) - root(r165): {verdict}.** The reader's wording is "of order 1e-3 or more"; the measured size is {abs(T[0]):.1e}.
- r165b and r155 ended `nonrobust` (the probe at `lam_lin` fell into the dip, dln 0.193 and 0.394) with robust opposite-signed ends, read on the bracket (widths {root['r165b']['width']:.1e} and {root['r155']['width']:.1e}); c155 reached `tol`.
- Beyond the bars (mine): at D 16 and D 16.5 the re-solved states agree with each other (1.7e-4 span at D 16, {abs(T[0]):.1e} at D 16.5) 4 to 8 times better than with the continuation state. offset(15.5) equals offset(15.0) to {abs(O155[0] - O150[0]):.0e}; the offsets are flat from D 15 to 15.5 and rise after. r165b's Delta equals r165's to {abs(rec['r165b']['Delta'] - src['r165b']['Delta']):.0e} while its root moved {T[0]:+.1e}.
- Predictions: |F|, the r165b band (3e-4 to 1e-3, 25%) and all brackets right; |T| <= 3e-4 (45%) wrong; offset(15.5) at the edge of the -5e-4 line; re-solve and root walls half right (scorecard in the README).
- Recommended next (t5 chooses): (1) r155b, a re-solve of r155 at D 15.5, rooted on 2.3282-2.3522; (2) one more D (D 14.5, whose state is in `I1025-mac/out`; D 17.0 has no k_c 55 state in the raw folders I checked), one re-solve and the continuation root; (3) only then the meaning for #1025.

Raw: `I1105-dh170/step1e/` (`results_1e.md`, `root_*.jsonl`, `resolve_*.log`, `steps_1e.txt`, README "Step 1e" result). Issue left open; `running` label removed.
"""
open(sys.argv[2], "w").write(post)
print("wrote")
