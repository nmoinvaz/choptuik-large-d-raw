# I944-dh170: `--od_junk 4` on the failing first steps of the order-150 and order-160 chains

Machine dh170 (Fedora 45, i7-7700, 4 cores / 8 threads, AVX2, 31 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/944
(follow-up of #937). Depends on #935 (the 4.8.2 build, I935-dh170/) and #936 (its bits equal the chain's build at one state).

## Setup

- Code: worktree ~/Source/choptuik-large-d-935 at origin/main 043834d9. Its hpkernel is #935's build (multidouble 4.8.2,
  multishoot 3.2.0, multisolver 0.1.1, has `series_o`; hp/src, hp/python and the Cargo files are the same at 043834d9 as at
  the built cdb5a6bc). Venv ~/Source/choptuik-large-d-935/.venv.
- The chains ran on 7f88c5bb and on 423bd22d with multidouble 4.7.0 (dh170) and #911's build (dh610). The only Python change in
  anm_run.py, octo_corrector.py and reseed.py since 7f88c5bb is `--od_tangents` (default 2, the same bits as one tangent, #921).
- The command is `run944.sh`: the chain's flags (run903.sh of I903-dh170, run903c.sh of I903-dh610) with `--od_junk` set
  by the argument, `--steps 1`, `--threads 10`, `nice -n 10`, a 3 h limit by `timeout` (a run past it is killed and reported).
- Input states are copies of the committed raw files (cmp-equal to the live ones) in ~/scratch944/ with the same relative paths:
  I903-dh170/chain_k150/anm_pin3_D233.0000.npz (and D225, D226), I903-dh610/chain_k160/anm_pin3_D234.0000.npz.

## Runs, in order, one at a time (the plan; what ran, with the later runs, is in the sections below)

| name | state | ks | `--od_junk` | what |
|---|---|---|---|---|
| k150_junk0_ctl | chain_k150 D 233 | 150 | 0 | control on this build: stopped after the a = 1 attempt (it failed at its start in the chain) |
| k150_junk4 | chain_k150 D 233 | 150 | 4 | run 1 |
| k160_junk0_ctl | chain_k160 D 234 | 160 | 0 | control on this build: stopped after the a = 1 attempt |
| k160_junk4 | chain_k160 D 234 | 160 | 4 | run 2 |
| k150_D225_junk4 | chain_k150 D 225 | 150 | 4 | run 3, only if runs 1 and 2 converge |

## Pass criteria, written before the first run

- **Controls** (junk 0): the a = 1 attempt's start fails to project exactly as the chain's log has it (k150: predicted |F|
  1.11e+08, rung u 0.3000 not converged at |R| 1.28e+05 after 8 steps; k160: predicted |F| 1.10e+11, |R| 1.82e-05 after 8
  steps). A control that converges is a discrepancy and stops the work until the cause is known.
- **Runs 1 and 2:** with `--od_junk 4` the start of an attempt projects and the octo-double corrector ends with max|F| <= 1e-60
  ("converged" and the printed max|F|) at a = 1 or at a trial with a >= 1/64 (the step halves three times at most, so a >= 1/8)
  where the default failed. The corrector can also report converged through the junk floor (projected correction below 1e-45,
  `junk_floor`), which leaves max|F| at the junk's residual; that is not a pass of the 1e-60 criterion and is reported with its
  max|F|.
- **Run 3:** the next state (D 226) has its Delta, the eight parts summed exactly, within 1e-40 of the chain's stored
  I903-dh170/chain_k150/anm_pin3_D226.0000.npz, and max|F| <= 1e-60.

## Result of the junk probes (k150, D 233.0 toward D 234; 13:17 to 15:41 UTC, 2026-11-17)

`--od_junk 4` does not carry the step: it is empty or absent at a = 1, 0.5 and 0.25 and makes a = 0.125 worse. Default = I903-dh170's
chain_k150.log (multidouble 4.7.0); the a = 1 default is also re-run here (k150_junk0_ctl, this build).

| a (D) | default | `--od_junk 4` (this build) |
|---|---|---|
| 1 (234.0) | the start's projection fails (rung u 0.3000 stalls at \|R\| 1.28e+05 after 8 steps; predicted \|F\| 1.11e+08). The control here reproduces it: same numbers, 108 s | the same failure, 106 s (k150_junk4.log). It is raised before `newton_od` runs, so no junk freeze acts |
| 0.5 (233.5) | the start projects; first step's trials fail down to lam 1/16 (max\|F\| 7.32e-27); stalled after 3 steps, 3223 s | `0 junk directions frozen, 4 weak ones with Delta content kept`: the same first iteration as the default to every printed digit (chord max\|F\| 6.86e+06, \|dw\| 8.149e+10, lam 1/16 at 7.32e-27); stopped after 31 min (its path is the default's) |
| 0.25 (233.25) | stalled after 2 steps, 3708 s | `0 junk directions frozen`; stopped at that line (k150_junk4_a0p25, 12 min) |
| 0.125 (233.125) | **converged**: 16 steps, max\|F\| 2.1e-71, 4470 s (lam 1/4, 1/4, 1/4, 1/2, 1, ...) | `1 junk directions frozen (sigma 4e-24), 3 weak ones with Delta content kept`; lam 1/2, 1/8, 1/32, 1/64, then the stall rule (lam <= 0.04 twice) ended it after 4 steps at max\|F\| 8.1e-25, **not converged**, 4625 s |

At the base D 233.0 the polish with `--od_junk 4` finds 1 junk direction (sigma 5e-24), 3 with Delta content kept. The stall rule
`--lam_stall 0.04` is the chain's. Whether the a = 0.125 junk attempt would have converged without it is not known.

Verdict on the issue's first acceptance line: not met at a = 1 (fails before the corrector), not at a = 0.5 and 0.25 (the junk
subspace is empty, the attempt is the default's), and at a = 0.125 the default converges and the junk freeze does not.
The k160 junk probes were dropped by the coordinator's order.

## `--od_weak_first 1`, old code d93f5b1b (k150, D 233.0; 15:42 to 16:51 UTC; logs k150_weakfirst_d93f5b1b*)

Stopped on the coordinator's order in its second attempt. a = 1 failed in the start's projection as in every run above (106 s). a = 0.5:
the weak components were dropped (|d| 2.0e-27, the default's first step 5.3e-15), the chord left max|F| 3.66e+04 (default 6.86e+06) and
was refused, and no trial was accepted. The trials, all refused:

| lam | max\|F\| | theta (bound) |
|---|---|---|
| 1, 1/2 | 3.66e+04, 1.81e+04 | 8.6e+31, 2.2e+31 (0.750, 0.875) |
| 1/4, 1/8, 1/16, 1/32, 1/64, 1/128, 1/256 | 3.4e-24, 1.7e-24, 7.7e-23, 4.3e-25, 2.1e-25, 1.1e-25, 5.4e-26 | 1.000 at each (0.938 up to 0.999) |

The attempt ended `no trial step accepted` at max|F| 9.3e-32 (the start's), 2112 s, with the printed |dz| 5.28e-15 equal to the default's full
first step. Cause (the coordinator's, from this log): the test judged each trial by the full correction, whose weak part a step that
holds the weak coordinates cannot change, so theta was 1.000 by construction. The a = 0.25 attempt's trials down to lam 1/8 (max|F|
5.2e+05 to 2.4e+04, theta 1e31 to 1e33) were refused before the stop.

## `--od_weak_first 1`, fixed test (main c714694a, multidouble Python package 482c6835), k150, D 233.0 (16:54 to 20:26 UTC)

Runs: `k150_weakfirst` (a = 1, 0.5, 0.25; stopped on my order after the a = 0.25 attempt so that the a = 0.125 attempt gets its own 3 h
limit, 7628 s) and `k150_weakfirst_a0p125` (`--a0 0.125`, exit 0, 5086 s). Chain flags with `--od_junk 0 --od_strong 4`.

| a | default (I903-dh170 chain_k150.log, 4.7.0) | `--od_weak_first 1` |
|---|---|---|
| 1 | the start's projection fails | the same failure, 106 s (before the corrector, so no corrector option acts) |
| 0.5 | stalled after 3 steps, 3223 s | it 0: chord refused, lam 1/4 accepted (theta 0.750), max\|F\| 9.3e-32 to 3.4e-24. It 1: lam 1/32 (theta 0.969), \|dz\| 5.28e-15 to 5.11e-15. It 2: lam 1/2 to 1/32 refused, lam 1/64 accepted, \|dz\| 5.03e-15. Stall rule (lam <= 0.04 twice). 3 steps, max\|F\| 3.3e-24, **not converged**, 3353 s |
| 0.25 | stalled after 2 steps, 3708 s | it 0: lam 1/32 accepted (theta 0.969), 1.0e-35 to 2.3e-24. It 1: no trial accepted (lam 1 to 1/256), \|dz\| 6.2e-14. 2 steps, max\|F\| 2.3e-24, **not converged**, 3284 s |
| 0.125 | converged, 16 steps, max\|F\| 2.1e-71, 4470 s | **converged**, 11 steps, max\|F\| 5.4e-61, 4443 s. Lam 1/2 (theta 0.500), 1/4, 1/4, 1/4, 1/2, 1, 1, 1, 1/2, 1 |

The old-code runs (d93f5b1b, 8c1857ce) are in `k150_weakfirst_d93f5b1b*` and `k150_weakfirst_8c1857ce_old_pkg*`; the
section above this one has the d93f5b1b trials.

| code | multidouble Python package | runs |
|---|---|---|
| 043834d9 | a93e0896 (4.6.0, pre-fix) | k150_junk0_ctl, k150_junk4*, k150_junk4_a0p25, k150_junk4_a0p125 |
| d93f5b1b | a93e0896 | k150_weakfirst_d93f5b1b |
| 8c1857ce | a93e0896 | k150_weakfirst_8c1857ce_old_pkg (killed at 90 s) |
| c714694a | 482c6835 | k150_weakfirst, k150_weakfirst_a0p125, k150_D225_weakfirst |

All runs: hpkernel 4.8.2 (the #935 build), 10 threads, nice 10.

## Agreement with the chain's stored states (compare_states.py)

`compare_states.py HP_DIR A B` sums each component's eight parts exactly and exits 0 only when |Delta_A - Delta_B| <= 1e-40. Controls:
chain D 226 against chain D 225 (2.0e-4, exit 1), a planted 1e-39 (exit 1) and a planted 1e-41 (exit 0) on the compared pair.

| compared | \|dDelta\| | max \|diff\| over the 769 components | verdict |
|---|---|---|---|
| k150_weakfirst_a0p125's D 233.125 against chain_k150's | 3.7e-48 | 3.7e-48 | pass |
| k150_D225_weakfirst's D 226 (a = 1 from D 225, 5 steps, max\|F\| 1.5e-95, 1392 s) against chain_k150's | 5.4e-91 | 9.9e-91 | pass |
| control: chain D 233.125 against chain D 233.0 | 2.3e-5 | 4.8e-5 | fail, as it must |

## Verdict

- `--od_junk 4`: the first acceptance line (the start projects and the corrector converges where the default failed) is not met.
- `--od_weak_first 1` (fixed): not met either. The start of a = 0.5 and 0.25 projects, the first iteration passes, and the later
  iterations that move the weak coordinates stall as the default's do (max\|F\| 3.3e-24 and 2.3e-24). a = 1 fails before the
  corrector. At a = 0.125, where the default converges, it converges too, in 11 steps instead of 16 and about the same time.
- Agreement: both checks pass.

## Recommended tasks (for the coordinator to file; full text)

1. **Trust region on the weak components in every iteration, not only the first.**
   What: `--od_weak_first 1` holds the 4 weakest directions in iteration 0 only. At a = 0.5 and 0.25 the later iterations, which move
   them, are accepted only at lam 1/32 to 1/64 with \|dz\| falling 3% per step (5.28e-15, 5.11e-15, 5.03e-15) until the stall rule ends the
   attempt. Limit the step's component along those directions to their basin radius in every iteration (or deflate it as
   `deflated_newton` does in double-double).
   Why: this log shows the first iteration is fixed and the crawl comes back at the first step that moves them.
   Acceptance (each can fail): from chain_k150 D 233.0 the a = 0.5 and a = 0.25 attempts end with octo-double max\|F\| <= 1e-60 inside the
   3 h limit; the controls (default and the current `--od_weak_first 1`) stall at 3.3e-24 and 2.3e-24 as recorded here; from D 225
   the step to D 226 keeps its Delta within 1e-40 of the stored state (compare_states.py, controls included).
   Depends on: this issue's option and #944's coordinator code.
2. **The a = 1 start's re-seed and projection.**
   What: at k150 D 233.0 and k160 D 234.0 the a = 1 attempt fails in the start's projection (rung u 0.3000 stalls at \|R\| 1.28e+05 after
   8 steps at k150; predicted \|F\| 1.11e+08), before the corrector, so no corrector option acts. Widen `Reseeder.polish_q`'s basin or
   re-seed from a smaller-a prediction.
   Why: every run here fails identically at a = 1 (106 s), with the default, `--od_junk 4` and `--od_weak_first 1`.
   Acceptance: the a = 1 start projects at D 233.0 (all rungs converge) and the corrector converges or reaches a stated max\|F\|;
   the control (the current code) reproduces \|R\| 1.28e+05. Depends on: #937.
3. **The stall rule at a = 0.5 and 0.25.**
   What: rerun the weak_first a = 0.5 attempt with `--lam_stall 0` to see whether the crawl converges given time.
   Why: the default's a = 0.125 attempt crawled at lam 1/4 for three iterations and then converged (16 steps); the stall rule would
   have ended a crawl at lam <= 0.04. At a = 0.5 the \|dz\| fall (3% per step) makes this unlikely, so this is the cheapest test of the
   guess, not a forecast.
   Acceptance: the attempt converges to 1e-60 or hits the 3 h limit with its \|F\| history; control: the same command with
   `--lam_stall 0.04` stalls at 3.3e-24 as recorded. Depends on: nothing.
