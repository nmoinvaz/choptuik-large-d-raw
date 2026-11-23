# I1079-macm3: Theorem A(M = 3)'s certificate tried at the two excited M = 3 zeros (#1079)

Machine: macm3 (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1, arm64; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1079
(from #1076 https://github.com/nmoinvaz/choptuik-large-d/issues/1076 and #1021). Task from the coordinator (hc of 2026-11-23, after the zero0_cert acceptance).
Written 2026-11-23 13:36 UTC, before any step ran. The steps, stops and acceptance are the issue's; the choices below are mine and are named.

## The question

Do the two excited zeros of the M = 3 multiplier, located in extended precision in #1076 (`zero_mp.py`, orientation +1 each), have a Krawczyk certificate of the kind of
Theorem A(M = 3) (`proof/A_M.md` section 6.2: K(X) in int X on a box h = 1e-10, w = 4e-16 around the zero)?

| zero | A | w/w_inf | source |
|---|---|---|---|
| x1 | 3.446218246366727 | 0.347606965217407 | #1076 zero1 run (raw c31b5d24), last row; `zero_mp.py` at 2dada6c4 |
| x2 | 3.526473056695715 | 0.211497981391215 | #1076 zero2 run (comment 7099358732), the point after the unapplied step |

## Code and versions

- Certificate code: a clean detached worktree of main, `~/Source/choptuik-large-d-1079`, at **a4cd5eaa7b297ffc6f171551fa15ba054e970e21** (`solver/proof`: `certify_M.py` blob 330d3a22,
  `certify_M_sys.py` 62ad5c15, `certify_M_lohner.py` 100c2cb9, `certify_M_recheck.py` 8ac746c6, `fixed_point_M.py` 71cee337 with sha256 prefix 589e5a810bc50289, the lemma's file as `proof/A_M.md` section 6.2 names it,
  `validated_int.py` 39794d0c). Python 3.14.3 (`~/Source/venv-macm3-1058b`), **python-flint 0.9.0, FLINT 3.6.0**, numpy 2.5.4, mpmath 1.3.0. Nothing in the worktree's tracked files is changed; the runs add new files named with the tags x1 and x2.
- Step 1 (F_3): `~/Source/choptuik-inner-mp` at **79d4af3b47ea39310ab5263f63ff3b8f1609f6eb** (feat/inner-mp; against 90d914e9 only `zero_mp.py` changed, 1 line; `value_mp.py` is the one of pass 3 and the zero runs).

## Plan (the issue's work list; `proof/A_M.md` section 8 commands, with the excited zeros as centres)

All certify commands from `solver/proof`, `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, `nice -n 10`, own session under caffeinate, one process each.

1. **F_3 at each zero**: `value_mp.py point A WF F3RE F3IM` with the F_3 of the nearest valued cache record (the cache of #1076 after pass 3, `I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl`, 3605 lines, sha256 8d7cb732...;
   "valued" as `zero_mp.py` reads it: `info` below 1e-8 and a finite F_3; the records are named in the results), 2 processes. Then p = (A, w/w_inf, B3 = -2 Im F3, C3 = 2 Re F3).
2. **Checks and centre** (`solver/proof`): `certify_M.py startcheck 3` (contains) and `--mutate` (must fail); `crosscheck 3` (agree) and `--mutate` (must DISAGREE);
   `refine 3 --p=<p> --iters=3 --tag=x1` and `--tag=x2`. **Stop if refine moves A or w/w_inf by more than 1e-8 from the zero_mp values above** (the models would differ). Extra, seconds each and named in `proof/A_M.md` section 8 as the first checks:
   `certify_M_sys.py selftest` (PASS) and `--mutate=coupling` (must FAIL).
3. **Certificate** for each zero: `certify_M.py plan --centre=data/A_M_refine_M3_x1.json`; `box 3 --centre=data/A_M_refine_M3_x1.json --use_out --h=1e-10 --w=4e-16 --out=data/A_M_box_M3x1_1e-10.json --log=logs/A_M_box_M3x1_1e-10.log`;
   `krawczyk --box=data/A_M_box_M3x1_1e-10.json --hier`; `controls --box=...` (C0 to C8, exit 0 iff all as expected); `krawczyk ... --hier --mutate=hier`; `certify_M_recheck.py data/A_M_box_M3x1_1e-10.json` and its `--mutate` (must fail).
   Same for x2 (files `..._M3x2_...`).

## Stops and acceptance (the issue's)

Stops: any failing check; refine not converging; the box run failing (path, start data or a singularity); refine moving A or w/w_inf by more than 1e-8 from the zero_mp values. On any of these: report the cause and change nothing.
A Krawczyk test that fails at h = 1e-10 is reported with its margins; a smaller box needs the coordinator's word.
Acceptance: for each zero, the Krawczyk test passes with every control as documented and the recheck agreeing, or the obstacle is named precisely (which step, which quantity) with the logs. The result is a Krawczyk enclosure
(rigorous given the start-value lemma `fixed_point_M.start_data_M` and Braaksma's theorem, with the trusted code named in `proof/A_M.md`), or it is numerical evidence with the obstacle named.

## Known before the run (read from `certify_M.py`, not a result)

- `krawczyk --hier` compares the box with `HIER[3]`, the stored double-precision solves of the **fundamental** zero (A 2.7265, w/w_inf 1.0156). If the Krawczyk test passes, the exit code is that of `hier_check`
  (`certify_M.py` lines 875-877), so at an excited zero `--hier` can only fail (its containment (a) is false by 0.7 in A), and `--hier --mutate=hier` fails trivially. I run the test **without `--hier`** as well, so that the
  Krawczyk verdict is read on its own, and report the `--hier` runs as run, with this reason; I do not edit the script.
- `start_data_M` raises unless the fixed point holds on the set and on its Cauchy box; at these parameters (far from the fundamental zero) the start data may not exist: that would be the obstacle named (box step).
- `startcheck 3` and `crosscheck 3` check the system, start data and path at fixed points near the fundamental zero (`XCHECK[3]` p = (2.7, 1.0, 0.14, 0.01)), not at the excited zeros.

## Output

Live files are written by the scripts into `~/Source/choptuik-large-d-1079/solver/proof/{data,logs}` (new names only) and copied here at each milestone (not the `.ckpt` files): `data/`, `logs/`, `runner/` (my wrappers, launcher outputs,
session checks), `steps.txt`. Memory and disk: alerts only to the coordinator (available memory under 2 GiB, free memory under 8%, disk under 3 GiB); nothing is stopped for memory.


## Results (2026-11-23, 13:36 to 14:12 UTC; every step ran on macm3 in a few minutes)

**Verdict: the Krawczyk test does not pass at h = 1e-10, w = 4e-16 at either zero. The obstacle is named below; nothing else was changed or run (a smaller box needs the coordinator's word).**

| step | x1 (3.446218..., 0.347607...) | x2 (3.526473..., 0.211498...) |
|---|---|---|
| step 1: F_3 (`value_mp.py point`, valued, 1550 to 1790 s) | 0.005890021924252909 - 0.40270879319264635i | -0.0008816597612909476 - 0.4882542725988094i |
| p = (A, w/w_inf, B3, C3) | (3.446218246366727, 0.347606965217407, 0.8054175863852927, 0.011780043848505818) | (3.526473056695715, 0.211497981391215, 0.9765085451976188, -0.0017633195225818952) |
| step 2: checks (selftest, startcheck, crosscheck, each with its mutation) | all as required (`steps.txt`, `logs/I1079_*.log`) | same |
| refine 3 --iters=3: \|g\| at it 0, 1, 2 | 7.06e-17, 1.66e-18, 6.09e-32 | 7.72e-18, 4.16e-18, 2.25e-32 |
| refine: largest move of A or w/w_inf from the zero_mp values (the stop was 1e-8) | 3.9e-16 | 5.0e-16 |
| plan: Schur complement singular values; inner block singular values; cond Dg | 7.8e-3, 3.6e-5; 1.88, 1.48; 1.2e5 | 2.0e-2, 2.7e-5; 0.105, 0.023; 7.5e3 |
| box run (`--h=1e-10 --w=4e-16`), steps (ray, arc, real); time | 726, 397, 57; 118 s | 718, 394, 64; 117 s |
| start data: `fixed_point_M.start_data_M` | no exception (rigorous given the lemma) | no exception |
| derivative radius at real-leg step 50 (the fundamental's h = 1e-10 run: 2.78) | 2.51e-02 | 6.00e-03 |

For Theorem A(M = 3) at the fundamental zero: Schur singular values 0.443 and 0.238, inner block 1.05e7 (twice), cond Dg 4.7e7 (`logs/A_M_plan_M3.log`).

**Krawczyk test** (`certify_M.py krawczyk --box=data/A_M_box_M3x{1,2}_1e-10.json`, no `--hier`; `logs/A_M_krawczyk_M3x*_1e-10.log`), exit 1: K(X) is not in int X. Relative margins (A, w/w_inf, B3, C3; positive iff inside):

| zero | A | w/w_inf | B3 | C3 | radius of g(p^) | max radius of Y Dg(X) |
|---|---|---|---|---|---|---|
| x1 | -80.2 | -59.0 | -6786.9 | -4688.2 | 5.4e-14 | 6.4e+01 |
| x2 | -79.9 | -131.3 | -220056.7 | -94318.7 | 1.2e-14 | 1.0e+02 |

(Theorem A(M = 3)'s fundamental zero, same box: +0.994, +0.997, +0.778, +0.778; g(p^) radius 1.7e-16; max radius of Y Dg(X) 0.23.)

**Recheck** (`certify_M_recheck.py`, mpmath intervals): the same verdict and the same margins (x1 to every printed digit; x2 within 9e-3 of the 2.2e5 and 4e-3 of the 9.4e4): exit 1 each. Its `--mutate` (jump sign flipped): exit 1 each, as it must.
**Controls**: not run: C0 (the clean run) must pass, and the test does not. **`--hier`**: not applicable (the stored solves are the fundamental zero's) and not run, as the coordinator ordered.

**Where K leaves X** (`diagnose.py`, my own read-only script that repeats `krawczyk_test`'s arithmetic row by row and reproduces the margins; `logs/I1079_diagnose_M3x*_1e-10.log`): K_i = -(Y g)_i + sum_j (I - Y Dg(X))_ij X_j, in units of the half-width w_i:

| zero | row | \|K_i\| / w_i | (Y g)_i radius | column A term | column w/w_inf term | columns B3, C3 terms |
|---|---|---|---|---|---|---|
| x1 | A | 81.2 | 0.7 | 16.8 | 63.7 | 0 |
| x1 | w/w_inf | 60.0 | 0.5 | 12.4 | 47.1 | 0 |
| x1 | B3 | 6787.9 | 100.0 | 1435.6 | 5252.2 | 0 |
| x1 | C3 | 4689.2 | 77.2 | 988.6 | 3623.3 | 0 |
| x2 | A | 80.9 | 0.1 | 18.0 | 62.8 | 0 |
| x2 | w/w_inf | 132.3 | 0.1 | 29.5 | 102.6 | 0 |
| x2 | B3 | 220057.7 | 750.8 | 50258.4 | 169048.1 | 0.2 |
| x2 | C3 | 94319.7 | 314.9 | 21669.7 | 72334.9 | 0.1 |

The midpoints of all terms are zero (Y is the midpoint's inverse). So, per row:
- **Outer rows**: K leaves X through the radius of the enclosure of Y Dg(X) in the two outer columns, 17 to 64 (x1) and 18 to 103 (x2) times h, against the required below 1; the radius of (Y g) is below 1 w.
- **Inner rows (B3, C3)**: K leaves X because the outer columns' entries of Y Dg(X) have radius 5.7e-3 and 2.1e-2 in the B3 row (x1; 0.20 and 0.68 at x2) and times h = 1e-10 they are 1400 to 5300 w (x1), 5e4 to 1.7e5 w (x2) with w = 4e-16; and the radius of g(p^) itself, 5.4e-14 (x1) and 1.2e-14 (x2), already gives (Y g) radii of 100 w and 77 w (x1), 751 w and 315 w (x2).

So the obstacle is a scale mismatch of the box, not a failure of the path, the start data or a singularity: h = 1e-10 and w = 4e-16 are Theorem A(M = 3)'s, where the inner block has singular values 1e7; at these zeros the inner block is 0.02 to 1.9, the Schur complement has a singular value of 3e-5, and the enclosure radius of Dg over the box and of g(p^) (5e-14 to 1e-14) are far above what the inner width w = 4e-16 and outer width h can absorb. I have not tested any other box: whether a smaller h and a larger w pass is not known. A box run takes 2 minutes here (1 process), the test seconds.


## Round 2 (the coordinator's order after the diagnosis, raw 38e524a4; written 2026-11-23 14:15 UTC, before the runs)

The coordinator's words: "an exact diagnosis; the box scale it is. Go on both: (a) `krawczyk --best` on the two existing runs; (b) box reruns at each zero for h in {1e-11, 1e-12, 1e-13} x w in {1e-15, 1e-14, 1e-13, 1e-12}
(12 runs per zero, 2 at a time, about 2 min each), each followed by `krawczyk` (no `--hier`) and its relative margins. Report the margins table per zero. For any box that passes: controls (C0-C8, exit 0 iff all as expected) and
`certify_M_recheck.py` with its `--mutate` (must fail), as the issue says; then stop and report. If none passes, name the binding row and quantity at the best box (as you did) and stop."

**Prediction (the coordinator's, written before):** the best box lies near h about 1e-12 with w about 1e-14 to 1e-13 (the outer columns' radius scales with the box; g(p^)'s radius, about 5e-14, floors h near 1e-13).

**What I run** (`runner/scan.sh`, own session under caffeinate, `nice -n 10`, 1 thread per BLAS; the two zeros side by side, so 2 processes at a time; code unchanged: main at a4cd5eaa, python-flint 0.9.0, FLINT 3.6.0):
- (a) `certify_M.py krawczyk --box=data/A_M_box_M3x{1,2}_1e-10.json --best` (outer sub-boxes h' = 0.9^k h with the run's inner widths kept; seconds).
- (b) for each zero N in {1, 2}, h in {1e-11, 1e-12, 1e-13}, w in {1e-15, 1e-14, 1e-13, 1e-12}: `certify_M.py box 3 --centre=data/A_M_refine_M3_xN.json --use_out --h=H --w=W --out=data/A_M_box_M3xN_hH_wW.json --log=logs/A_M_box_M3xN_hH_wW.log`,
  then `certify_M.py krawczyk --box=data/A_M_box_M3xN_hH_wW.json > logs/A_M_krawczyk_M3xN_hH_wW.log` (no `--hier`); its exit and relative margins (A, w/w_inf, B3, C3) go to `steps.txt` and into the margins table. A box run that ends with an exception is recorded and not
  repeated (`proof/A_M.md` section 7).
- For every box whose test passes (exit 0): `controls --box=...` (exit 0 iff C0 to C8 are as expected), `certify_M_recheck.py <box>` (exit 0, the same verdict) and `certify_M_recheck.py <box> --mutate` (must exit nonzero); a result that is not as expected is a STOP line.
- If no box passes: the binding row and quantity at the best box (the one with the largest smallest margin), by the same row-by-row breakdown as before (`diagnose.py`, read-only), and I stop. `--hier` stays not applicable and is not run.
- Output names: `data/A_M_box_M3xN_hH_wW.json` (not the `.ckpt` files), `logs/A_M_*M3xN_hH_wW*.log`, the same copying into this folder as before.
