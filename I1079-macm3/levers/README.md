# I1079-macm3/levers: the two routes at the excited zeros, a sweep of the certificate's xi1 and Taylor orders (#1079)

Machine: macm3 (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1, arm64; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1079. Written 2026-11-23 15:55 UTC, before any of these runs.
Task from the coordinator (hc of 2026-11-23, after Nathan's word; the plan is #1079's comment of 16:00 UTC, "Both routes, per Nathan"), given as:

"#1079 resumes with both routes (Nathan's word). When your current D 20.78125 lambda scan ends, do this before the next leg point: in a clean worktree of branch `feat/certify-excited` (1addcada; `certify_M.py` reads `CERTIFY_M_XI1` and `CERTIFY_M_NTAY`/`_NJAC` for M >= 3,
defaults unchanged), at x2 first: E1 = `CERTIFY_M_XI1=0.2` (orders 20/12), E2 = xi1 0.3 with `CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16`, E3 = both. Each: `refine 3 --p=<x2 p>` (stop if A or wf moves > 1e-8), a point run (report g's radius), box runs at (h,w) in {1e-11,1e-12} x {1e-13,1e-12},
`krawczyk --point` (no `--hier`), margins and the binding row. Then x1 at the best setting. A passing box: controls and `certify_M_recheck.py` with their mutations, then stop and report. Raw `I1079-macm3/levers/`, README first with these runs. The D 20.8125 leg-point scan can wait or go beside it at 2 procs."

## The routes (the plan comment, in short)

(b) xi1 = 0.2 drops the real leg: Theorem A(M) is stated for a matching radius xi1 >= rho_arc (A_lemmas_M section 8), the price is hypothesis H3 (lemma 6a certified at xi1 = 0.2 for each excited zero; a pilot exists, A_lemmas_M's table at line 712);
the outer signal at 0.2 is about 2e4 times smaller than at 0.3, the real leg's amplification (6.5e5 at x1, 7.5e4 at x2, round 3) disappears. (a) a tighter integration before the leg: the Taylor orders (20 and 12 at M >= 3). The a-priori floor of `lemma6_common.py` only seeds the Picard iteration; containment is still verified.

## Code

A clean detached worktree of branch `feat/certify-excited`, `~/Source/choptuik-large-d-1079e`, at **1addcada42157c197ad1193621b988a978bb96f7** ("certify_M: CERTIFY_M_XI1 and CERTIFY_M_NTAY/_NJAC options for M >= 3 (defaults unchanged)"). Its `solver/proof/certify_M.py` (blob be1c923b) differs from main's a4cd5eaa version (blob 330d3a22) by 7 lines:
`NTAY, NJAC = int(os.environ.get("CERTIFY_M_NTAY", "20")), int(os.environ.get("CERTIFY_M_NJAC", "12"))`, and `path_for(M)` returns the real-leg end `os.environ.get("CERTIFY_M_XI1", "0.3")` for M >= 3 (M = 1 stays 0.3). The rest of `solver/proof` is main's a4cd5eaa (no other change in the folder). python-flint 0.9.0, FLINT 3.6.0, Python 3.14.3, numpy 2.5.4 (`~/Source/venv-macm3-1058b`).

## The sweep (x2 first; `runner/levers.sh SETTING ZERO`)

| run | environment | what changes |
|---|---|---|
| E1 | `CERTIFY_M_XI1=0.2` | the path ends at 0.2: no real leg (zero length) |
| E2 | `CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16` | Taylor orders 28 and 16 (defaults 20 and 12) |
| E3 | both | both |

Each run, from `solver/proof`, `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, `nice -n 10`, own session under caffeinate; the three settings side by side (1 process each):
1. `certify_M.py refine 3 --p=<x2's p> --iters=3 --tag=x2E<k>` with p = (3.526473056695715, 0.211497981391215, 0.9765085451976188, -0.0017633195225818952) (zero_mp's A and w/w_inf, value_mp's F_3: the p of #1079's first round); **stop if A or w/w_inf moves by more than 1e-8** from zero_mp's values.
2. `certify_M.py point 3 --p=<the refine's p_out> --out=data/A_M_point_M3x2E<k>.json`: g(p^)'s radius is reported.
3. `certify_M.py box 3 --centre=data/A_M_refine_M3_x2E<k>.json --use_out --h=H --w=W --out=data/A_M_box_M3x2E<k>_hH_wW.json` for (H, W) in {1e-11, 1e-12} x {1e-13, 1e-12} (4 boxes).
4. `certify_M.py krawczyk --box=<box> --point=data/A_M_point_M3x2E<k>.json` (no `--hier`, which compares with the fundamental zero's stored solves): relative margins (A / w/w_inf / B3 / C3) and the binding row (my read-only `diagnose.py` with the point run).
5. For a passing box: `controls --box=<box> --point=<point>` (exit 0 iff C0 to C8 as expected), `certify_M_recheck.py <box>` (it has no `--point`: its verdict then uses the box run's own g(p^)) and its `--mutate` (must fail); then stop and report.
Then x1 at the best setting (the one with the largest smallest margin, or the smallest g radius if none passes: named when chosen). The round-3 numbers at the defaults (same code, xi1 0.3, 20/12) are the baseline: g radius 1.188e-14 at x2; margins (1e-11, 1e-12): -0.624 / -1.458 / -0.246 / +0.618.

## Not predicted, named before

No numerical prediction was given. What the plan says it measures: E1 the real leg's share of g's radius, E2 the remainder's share before the leg, E3 both. At round 3 the radius at x2 grew from 3e-20 (end of the arc) to 1.188e-14 on the real leg (a factor 7.5e4), so E1 can remove at most that factor.
A caveat of mine: with xi1 = 0.2 the real leg has zero length (the path is ray, arc, "0.2" to "0.2"); whether the integrator accepts it is not known before the run, and an exception is a result.
Hypothesis H3 (lemma 6a at xi1 = 0.2) is not touched here: a passing xi1 = 0.2 box would be a Krawczyk enclosure only for the system at xi1 = 0.2.
