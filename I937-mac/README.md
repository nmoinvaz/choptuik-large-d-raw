# I937-mac: the corrector's projection from the point's own quad-double data (--project_start pred) at order 160, D 234

Machine: the Mac (M5), 3 threads at nice 10, one process. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/937.
Code: worktree `choptuik-large-d-937` at fe489b42 (branch `fix/project-start-pred`), unchanged. hpkernel: site2 (main
3c35f0c's build, xfkappa's chain build). It has no `Solver.series_o` and no `set_octo_tangents`, so anm_run.py forms the
series by jets and the Jacobian one tangent per evaluation: the same bits (#914, #921) and slower.

## Runs

`run.sh NAME [ARGS]` runs `run937.py` from dh610's order-160 base at D 234 (`I903-dh610/chain_k160/anm_pin3_D234.0000.npz`,
blob 3af3f49e) with chain_k160's flags from `run903c.sh` (raw I903-dh610), `--threads 3` instead of 10, `--ks 160
--keep_plan 1 --steps 1`, at most 4 h each. `run937.py` runs anm_run.py's `main()` unchanged, with two logging wrappers
that change no result. `[937] project:` prints every projection's outcome and stages (the `pred_q` stage of
`--project_start pred` included, which `why_failed` does not print). `[937] with_horizon:` prints `rs.last_o`, the
rung max|R| of each `refine_o`, whenever `with_horizon` runs with `rs.od > 0`.

- `c1_pred`: `--project_start pred` (the test)
- `c1_ctl`: the default `u0` (the control), only if `c1_pred` changes the outcome of a trial

On dh610 (the default code, the same flags) the step from D 234 failed as follows. At a = 1 the re-seed failed (the
quad-double polish from the prediction's own data, |R| 1.82e-5 after 8 steps) and the start's projection failed. At
a = 0.5 every trial projection at λ ≥ 1/64 failed, and the trials at λ 1/128 were accepted (`chain_k160.log`).

## Criteria (written before the runs)

- **A1, the test:** with `--project_start pred`, at the a = 0.5 attempt (D 234.5), the projections of trials at λ ≥ 1/64
  converge (outcome not `failed` in `[937] project:`), and the attempt converges, octo-double max|F| (F − c) ≤ 1e-60.
  It fails if those projections fail as in the control. A converged attempt with λ ≤ 1/128 only is also a fail.
- **A2, the control:** with the default, the same trials fail as dh610 logged. Without a `c1_ctl` run, dh610's log is
  the control, on another machine and build (#911's, bit-identical to site2 by #911's checks).
- **A3:** where both runs converge an attempt, the two states agree to Δ within 1e-40.
- **A4, refine_o:** whether `[937] with_horizon:` lines appear inside the corrector's projections, and with what
  residuals.

Prior expectation (not a criterion): at a = 1 the flag's first stage is the same quad-double polish from the same
data as the re-seed's `--reseed_start pred`, which failed there, so a = 1 likely fails again. The test is at a = 0.5.

## The refine_o question, from the code (before the runs)

The coordinator is right, and my #903 statement was wrong for successful projections. `octo_corrector.ElimO.project`
returns `z if how == "failed" else with_horizon(z, zp, self.rs)`, and `with_horizon` runs `rs.refine_o` whenever
`rs.od > 0`, which `--reseed_o 3` sets. So `refine_o` runs in every projection that does not fail, and never in a failed
one. At D 235 on dh610 every projection at λ ≥ 1/64 failed, so none of those ran it. The ones that converged (λ 1/128,
and the `ladder` 5 counted at D 233 and 234) did. anm_run.py prints `rs.last_o` only at the start's re-seed, so
dh610's log cannot show the others. `run937.py`'s wrapper prints them.

## Decisions (the coordinator, by hc, after the criteria post)

Case 2 (win2b's ks 230 leg at D 215) is skipped. Its re-seed already polishes from the point's own data, so
`--project_start pred` would repeat that failure. dh610's log is c1's control unless `c1_pred` changes an outcome. 2 to 3
h per order-160 run on site2 is accepted as the estimate.

## Results (c1_pred, 06:47 to the 4 h cap at 10:47 UTC)

The run reproduces dh610's step to every printed digit up to the attempts. The base polish at D 234 gave |F| 3.42e-78.
The series line matches: pivots 7.7e-21..2.9e+33, ratios 2-5 300.0 270.3 257.8 250.8, a_max 3.114 (5105 s by jets
here). `compare937.py c1_pred.log <dh610's chain_k160.log>` (`compare937.log`) compares the a = 0.5 attempt's Newton
iteration 0, trial by trial. All 8 trials print the same max|F|, correction ratio and verdict in both runs, so the
flag changed no outcome. λ 1 to 1/64 are refused in both and λ 1/128 is accepted at 2.00e-27 in both. The iteration
ends identically, |F| 1.79e-33 -> 2.00e-27, |dz| 1.18e-14, dDelta +4.64e-15. The first two trials of iteration 1, at
λ 1 and 1/2, also match dh610's (7.78e9 and 3.368e37, 2.14e9 and 2.105e36). At a = 1 the re-seed fails in both runs,
at |R| 1.82e-5 after 8 steps, and the start's projection fails in both.

The new first stage, `pred_q`, fails where the double-double-started polish `u0q` fails, at about the same level:

| λ | `pred_q` \|R\| | `u0q` \|R\| (the same in dh610's log) | `u0` (double-double) |
|---|---|---|---|
| 1 | 8.24e8 -> 8.24e8 | 8.26e8 -> 8.26e8 | 1.87e10 floor |
| 1/2 | 2.04e8 -> 2.04e8 | 2.03e8 -> 2.03e8 | 2.39e10 |
| 1/4 | 5.35e7 -> 2.83e4 | 5.83e7 -> 2.70e4 | 3.48e9 |
| 1/8 | 1.36e7 -> 1.15e3 | 1.21e7 -> 9.31e2 | 5.60e8 |
| 1/16 | 3.41e6 -> 4.82e1 | 2.21e6 -> 1.37e2 | 2.26e8 |
| 1/32 | 8.55e5 -> 9.74e0 | 2.68e6 -> 8.72e1 | 1.74e9 |
| 1/64 | 2.14e5 -> 1.95e1 | 1.54e6 -> 7.80e1 | 2.25e8 |
| 1/128 | 5.34e4 -> 5.37e-29, converged (23 its) | (dh610: converged) | – |

Every failed polish reports 8 its. In the code (`invert_q` reruns `polish_q` with the block steps "am" up to 3 times),
the last run's history then holds its 6 block steps and one Newton step. The take-all rule stops that step when |R|
rises above 1e12 times the best, or turns non-finite, and keeps the best iterate. So at λ ≥ 1/64 the Newton step on
the horizon data leaves its basin from the block steps' iterate, whether the data start from the point's own four
parts or from the double-double rung. The double-double first stage is dead weight there (|R| 1.7e9 to 2.4e10 at
its floor), and removing it does not make the projection converge.

The refine_o question (A4), from the log: the wrapper printed `[937] with_horizon:` twice. Once at the a = 0.5 start's
re-seed: 2.53e-26 -> 2.44e-39 (anm_run.py's own line has the same). Once inside the corrector, after the λ 1/128 trial's
successful projection: 8.52e-26 -> 4.12e-28 -> 5.26e-32, then flat. It ran after no failed projection. So `refine_o`
runs in the corrector's successful projections, as the coordinator said. There it stalls at 5.26e-32, against 2.44e-39
at the start.

The run stopped at the 4 h cap at 10:47:49 UTC (exit 124), in Newton iteration 1 of the a = 0.5 attempt. Its saved
predictions, `c1_pred/pred_pin3_D234.5000.npz` and `pred_pin3_D235.0000.npz`, are bit for bit dh610's (raw I903-dh610
at ff5dd9f6, `pred_compare.log`: zh, zl, z2 and z3 equal in both). So the step reproduces exactly, and its trial points
can be regenerated from the stored base.

## Acceptance

| criterion | verdict | number |
|---|---|---|
| A1: with `pred` the projections at λ ≥ 1/64 converge and the attempt reaches 1e-60 | FAIL | 7 of 7 projections at λ 1 to 1/64 failed, `pred_q` best \|R\| 8.24e8 (λ 1) to 9.74 (λ 1/32); the first converged at λ 1/128 (5.37e-29), as without the flag |
| A2: the default fails at the same trials (control: dh610's log) | pass | `compare937.log`: 8 of 8 trials the same, check pass; predictions bit for bit |
| A3: Δ within 1e-40 where both converge | not reached | no attempt converged before the cap; neither did dh610's |
| A4: refine_o in the projections | answered | it ran after the λ 1/128 successful projection, 8.52e-26 -> 4.12e-28 -> 5.26e-32 then flat, and after no failed one |

## Recommended tasks

1. **The corrector's first step at D 234.5, limited in the weak subspace.** What: the a = 0.5 start is at pinned |F|
   1.79e-33. The full Newton step (|dz| 1.18e-14, Δ +4.64e-15) lands at 7.89e9, and only λ 1/128 is accepted. Test a
   step that drops or bounds its components on the four weak directions `--od_strong 4` finds (a trust region there),
   on this start, regenerated bit for bit from `I903-dh610/chain_k160/anm_pin3_D234.0000.npz`. Why: no projection can
   repair the λ ≥ 1/64 points, and the step decides where they land. Acceptance: the attempt converges to ≤ 1e-60
   with every accepted λ ≥ 1/64, while the unlimited step (control) still needs λ 1/128. Depends on: #937.
2. **polish_q's basin at these D.** What: at λ 1/4 to 1/64 the quad-double polish's first Newton step on the horizon
   data leaves the basin after the block steps, whether it starts from the point's own data or the double-double rung
   (`invert_q`, `pre` "am", take-all rise rule 1e12). Test more block sweeps, or a damped Newton with a line search, on
   the regenerated trial points. Why: the projection fails from |R| 1e2 to 1e8 there. Acceptance: it converges below
   1e-24 at λ 1/64 where the current polish fails, and the current one still fails there (control). Depends on: #937.

## Discrepancies

- `reseed.why_failed` does not print the `pred_q` stage, so `--project_start pred`'s own "projection failed" lines
  omit the stage it adds (`run937.py`'s `[937] project:` lines show it).
- Inside the projection `refine_o` stalls at 5.26e-32, above the 2.44e-39 it reaches at the start's re-seed.
- My #903 statement that `refine_o` runs only at the start was wrong (corrected in `I903-mac-grip/README.md`).
- The estimate: 4 h did not finish one attempt on site2. The series took 5105 s by jets, and Newton iteration 0 took
  5926 s here against 1338 s on dh610.
