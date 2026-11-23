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


## Results (2026-11-23, 15:56:40 to 16:38:29 UTC; the sweep at x2 took 21 min, x1 at E2 19 min)

**Verdict: at both excited zeros the Krawczyk test passes with the Taylor orders 28 and 16 at xi1 0.3 (E2), at the boxes (h, w) = (1e-12, 1e-13) and (1e-12, 1e-12) at x2 and (1e-12, 1e-13) at x1, with every control as expected and the recheck agreeing; at x1's other passing box (1e-12, 1e-12) control C6 is the one unexpected verdict (below).
xi1 0.2 (E1) and both (E3) do not pass at x2.** Code: `feat/certify-excited` at 1addcada42157c197ad1193621b988a978bb96f7, python-flint 0.9.0, FLINT 3.6.0, Python 3.14.3; every refine moved A and w/w_inf by at most 5.0e-16 (x2) and 3.9e-16 (x1), against the stop of 1e-8.

**g(p^)'s radius** (the point runs; the defaults' values from round 3):

| zero | defaults (xi1 0.3, 20/12) | E1 (xi1 0.2) | E2 (28/16) | E3 (both) |
|---|---|---|---|---|
| x2 | 1.188e-14 | 6.459e-20 | **7.422e-23** | 1.967e-28 |
| x1 | 5.337e-14 | | **1.571e-21** | |

**Relative margins** (A / w/w_inf / B3 / C3; `krawczyk --box --point`, no `--hier`; positive iff inside):

x2:

| (h, w) | E1 | E2 | E3 |
|---|---|---|---|
| (1e-11, 1e-13) | -176 / -237 / -745 / -1.07e+03 | -2.87 / -5.62 / -13.3 / -4.37 | -173 / -233 / -730 / -1.05e+03 |
| (1e-11, 1e-12) | -197 / -265 / -82.3 / -118 | -4.5 / -8.15 / -0.189 / +0.674 | -194 / -261 / -80.9 / -116 |
| (1e-12, 1e-13) | -45.9 / -61.6 / -20.3 / -28.5 | +0.621 / +0.341 / +0.83 / +0.951 | -18.5 / -25.2 / -7.2 / -10.7 |
| (1e-12, 1e-12) | -67.6 / -91 / -2.06 / -3.27 | +0.943 / +0.945 / +0.988 / +0.995 | -40.2 / -54.5 / -0.744 / -1.5 |

x1 at E2 (the best setting):

| (h, w) | E2 |
|---|---|
| (1e-11, 1e-13) | -3.7 / -2.35 / +0.741 / +0.811 |
| (1e-11, 1e-12) | -3.5 / -2.42 / +0.975 / +0.981 |
| (1e-12, 1e-13) | +0.702 / +0.758 / +0.997 / +0.998 |
| (1e-12, 1e-12) | +0.272 / +0.484 / +1 / +1 |

**Passing boxes** (`logs/A_M_krawczyk_pt_*.log`, `A_M_controls_pt_*.log`, `A_M_recheck_pt_*.log`; `steps_levers.txt`):

| box | margins | controls | recheck (no `--point` option) | its `--mutate` |
|---|---|---|---|---|
| x2 (1e-12, 1e-13) | +0.621 / +0.341 / +0.830 / +0.951 | all as expected | exit 0, same verdict and margins | exit 1 |
| x2 (1e-12, 1e-12) | +0.943 / +0.945 / +0.988 / +0.995 | all as expected | exit 0, same | exit 1 |
| x1 (1e-12, 1e-13) | +0.702 / +0.758 / +0.997 / +0.998 | all as expected | exit 0, same | exit 1 |
| x1 (1e-12, 1e-12) | +0.272 / +0.484 / +1.000 / +1.000 | **C6 unexpected**, all others as expected | exit 0, same | exit 1 |

x1 (1e-12, 1e-12): C6 (a zero planted inside, moved by (h/2, -3h/10, w/4, ...), expected to pass) fails with margins -0.228 / +0.184 / +0.750 / +0.750, because the shift h/2 in A exceeds the clean margin 0.272 in A; C6b (moved by half the clean margins) passes (+0.136 / +0.242 / +0.500 / +0.500),
and C0 to C5, C7, C8 are as expected. The same thing is recorded in `proof/A_M.md` section 6.2 for the h = 1e-9 run of the fundamental ("on that sub-box C6 did not give its expected verdict (its planted inner shift w/4 exceeded the clean inner margins); this is recorded, not changed, and is why C6b was added").
It is recorded here, not changed; the x1 certificate to cite is the other box, (1e-12, 1e-13), whose controls are all as expected.

**The certified zero enclosures** (endpoints rounded outward by the script; the zero_mp point and value_mp's F_3 are inside all four coordinates of each, with the box centred on the refine's p):

| zero, box | A | w/w_inf | B3 | C3 |
|---|---|---|---|---|
| x2 (1e-12, 1e-12) | [3.52647305669565, 3.52647305669578] (r 5.66e-14) | [0.211497981391159, 0.211497981391271] (r 5.55e-14) | [0.976508545197566, 0.976508545197672] (r 5.25e-14) | [-0.00176331952260710, -0.00176331952255648] (r 2.53e-14) |
| x1 (1e-12, 1e-13) | [3.44621824636642, 3.44621824636703] (r 2.98e-13) | [0.347606965217164, 0.347606965217650] (r 2.42e-13) | [0.805417586384900, 0.805417586385684] (r 3.91e-13) | [0.0117800438484891, 0.0117800438485225] (r 1.67e-14) |

zero_mp: x2 (3.526473056695715, 0.211497981391215), x1 (3.446218246366727, 0.347606965217407); value_mp's (B3, C3): x2 (0.9765085451976188, -0.0017633195225818952), x1 (0.8054175863852927, 0.011780043848505818).

**Why E1 and E3 fail** (`diagnose.py` with the point run, `logs/I1079_diagnose_pt_*`): at xi1 0.2 the outer rows' Y Dg(X) enclosure radius dominates: E3 (1e-12, 1e-13): row A 19.5 h = 5.3 h (A column) + 13.1 h (w/w_inf column) + 0.6 h + 0.6 h with the (Y g) radius 0.0 h (g radius 1.97e-28); E1 adds a (Y g) radius of 27 h and 36 h (g radius 6.5e-20; the plan comment gives the outer signal at 0.2 as about 2e4 times smaller than at 0.3, which I did not measure here).
At E2 (1e-11, 1e-12), the best failing box: row A 5.5 h and w/w_inf 9.2 h, both from the outer columns' Jacobian enclosure (1.2 h + 4.1 h, 2.0 h + 6.8 h), the (Y g) radius 0.0 h. The Taylor order, not xi1, is the lever: g's radius falls by 8 orders (x2) at 28/16, and the Jacobian enclosure's radius follows (max radius of Dg: 1.972e-05 at the defaults, 1.727e-09 at E2).

## H0: `start_cover_M2.py --box=<passing box> --rerun` does not apply at the excited zeros (16:38 UTC)

Run on all four passing boxes (`CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16`; python-flint 0.9.0, FLINT 3.6.0; `steps_hyp.txt`, `logs/I1079_start_cover_*`): `--rerun` exit 1 ("NOT COVERED"), `--rerun --mutate=overlap` exit 1 (so the control is uninformative), without `--rerun` exit 1.
**Cause:** `start_cover_M2.py` compares the certificate's four start sets with the stored runs of lemma FP(3), which are centred on the fundamental zero x^ = `fixed_point_M.ZEROS[3]` (real boxes x^ +- 1e-6, complex x^ +- 1e-3 (1 + i)). The excited zeros are 0.80 in A, 0.80 in w/w_inf and 0.83 in B3 away from x^
(its log: p^ - x^ = A +0.800, w/w_inf -0.804, B3 +0.832, C3 -0.0129 at x2), so no stored row is around them, and the script's rerun is gated on one (`if "rerun" in opts and (covered or res["around"])`, line 452): it is skipped, and the verdict is NOT COVERED. The configuration test (a) is true (same ray 5pi/16, r0 0.0741, diag splitting, N 94, Cauchy radius 1e-3; `fixed_point_M.py` sha256 589e5a810bc50289),
and (c) holds (M W0 sup|Im w/w_inf| = 0.01147 <= 3/2). What the certificate's own run gives: its start-data call (`certify_M.start_data`, `fixed_point_M.start_data_M`) runs step (i) on its four sets and raises unless the fixed point holds on each, and it did not raise (the box JSON's `start`: eta 6.34e-72 at x2, 1.51e-72 at x1; its derivative part 2.27e-18 and 1.43e-17).
What the script does not give at an excited zero is the second look (a rerun on a set that contains the start sets, compared with stored bounds). That needs stored lemma FP(3) rows at the excited centre (`fixed_point_M.py --table` and `--data-table` at a centre that is not `ZEROS[3]`) or a change of the script: the coordinator's decision. Nothing was changed. I stopped here, as ordered.
