# I961-dh370: #955's rounds, #956's tangent_from and the split series on the merged head 40f4b4a5, one Linux build, one chain step

Machine dh370 (Fedora 45, i7-8700, 12 threads, 31 GB, avx2). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/961

Worktree `~/Source/choptuik-large-d-961` at branch `perf/series-par-at` 40f4b4a5 (main add322ff plus #955), fresh venv. Build: `hp/build.sh`
with `CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`, `CARGO_BUILD_JOBS=6`, nice 10. T = 10 threads at nice 10.
The memory watcher only logs and alerts, it never stops anything.

Files are added as the run goes (build961.sh, build.log, run961.sh, exits_961.txt, mem961.log, one log per line of the issue).

## Results (finished 2026-11-18 18:12 UTC, one unit `run961`, every stage exit 0)

Build: exit 0, 32 min 44 s (12:27:29 to 13:00:13 UTC), peak RSS 24.08 GB, system used peak 27 437 MB, `hpkernel avx2 multidouble avx2`,
multidouble 4.9.0, multishoot 3.3.0, multisolver 0.1.1 (Cargo.lock), Python package multidouble 482c6835, .so sha1 d8cafd682ed3
(`build961.txt`, `build.log`, `mem961_build.log`).

| line | verdict | numbers |
|---|---|---|
| 1 `cargo test --release --lib oseries_` | pass, 3 passed, 1 ignored (the bench) | 8 min 37 s compile, tests 919 s; controls: 9600 rows, horizon round 3200, centre round 4224, kept series not moved 1.001e0. Compiled without `-C target-cpu=native` (the command as written), so it ran multidouble's portable path (`simd.rs` selects avx2 and fma by `cfg(target_feature)`), not the avx2 build |
| 2 by-order, 10 threads, `--save` | PASS | by order 316.9 s (#957 on 954eadcb: 721.3 s, `jbo_default2.json`), jets 1650.5 s, ratio 5.21; 24 of 24 orders the same bits, 6 of 6 with the hook; four controls fired |
| 2 by-order, 4 threads, N 12, `--compare` | PASS | 12 of 12 the same bits, 12 of 12 as saved by the 10-thread run; the round control's series differs from the saved one at orders 2 to 6 |
| 3 `--tangent_from 1` at ST | PASS | formed twice 316.3 s, moved 196.9 s (1.61); agreement max 1.0e-46 (bound 1e-40); rho 6.55e-35 (bound 6.71e-32); control rho 1.2e29, agreement 1.0e-30 |
| 3 `--tangent_from 1` at ST2 | PASS | 316.4 s and 197.0 s (1.61); agreement 6.7e-46; rho 1.38e-36 (bound 1.41e-33); control rho 2.7e29 |
| 3 `--tangent_from 3` at ST | PASS | 316.4 s and 198.8 s (1.59); agreement 3.2e-48; rho 6.55e-35; control rho 3.5e29 |
| 4 `series_split_check.py` | PASS | default 317.1 s, split 304.5 s (ratio 1.04); d_split 0 at every order; control 1.1e84 times the threshold |
| 5 (a), (b) | PASS | both accepted at a 0.5 (third attempt, 2.0 and 1.0 refused by the re-seed); \|Delta(b) - Delta(a)\| 2.96e-69 (bound 1e-40); (b)'s series 191.0 s against (a)'s 316.5 s, ratio 1.657 (bar 1.5, `base_lu` kept in both, so `t_coef` is the series alone) |
| 5 (c) control | fires | (c) accepted at a 0.5; \|Delta(c) - Delta(a)\| 1.10e-17, above 1e-40 |
| 5 (d) reported | not judged | a 1.2899 accepted at the first attempt, see below |

`summary961.py` (log `summary961.log`) gives the step verdicts, its control `--mutate series` (a's series seconds in b's place) exits 1
(`summary961_mutate.log`); `delta_cmp961.py` has a planted `selftest` (`selftest_delta961.log`).

(d) against (b), on this machine (stage wall includes the base polish and setup):

| | (b) N 24, default rule | (d) N 31, a_rule reseed 0.0715 |
|---|---|---|
| accepted a, attempts | 0.5, 3 | 1.2899, 1 |
| series s (per unit D) | 191.0 (382.1) | 288.3 (223.5) |
| accepted attempt s, re-seed plus corrector (per unit D) | 468.6 (937.2) | 781.3 (605.7) |
| all attempts s (per unit D) | 1203.7 (2407.3) | 781.3 (605.7) |
| whole step s, stage wall (per unit D) | 2273 (4546) | 1953 (1514) |

Discrepancy with #960's P1 (same state, flags, N 31, rule 0.0715, build 954eadcb): the same a 1.289888489590666 is accepted and Delta
agrees to 8.58e-51 (`delta_d_vs_960.log`), but #960's corrector took 3 steps (287 s) and (d)'s took 7 (628 s). #960's first step has
its trial at lam 1 with simplified correction / |dz| 1.012 (above the 0.75 bound) accepted because max|F| 9.12e-61 was under tol_od
1e-60, leaving |dz| 8.58e-51 in its last step, equal to the Delta difference; (d)'s trial had max|F| 2.36e-56, was refused (1.010),
and it iterated to |dz| 1.65e-92. That reading is from the two logs, not tested by a rerun.

Files: `build961.sh`, `run961.sh`, `exits_961.txt`, `mem961.log`, `mem961_build.log`, one `.log` and `.json` per check line, `step_off/`
`step_on/` `step_ks250/` `step_n31/` (anm_run.jsonl, states, jets, predictions), `s10.npz` (the 10-thread series `--compare` reads),
`delta_*.log`, `summary961.*`, `push961.sh`. Scripts: `delta_cmp961.py`, `summary961.py`.
