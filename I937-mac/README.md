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
