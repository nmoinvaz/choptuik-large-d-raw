# I935-win2: hp on multidouble 4.8.2 on win2, the build and the reference checks

Machine: win2 (Windows desktop, 20 threads, 95 GB), session "win2 build session" beside win2b's #903 chain.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/935 (win2's row; #936 has its own folder `I936-win2/`).

| | |
|---|---|
| code | worktree `D:\choptuik-i935` of choptuik-large-d, detached at origin/main d7b59668 |
| venv | `C:\Users\nathan\Source\venv-md482`, Python 3.14.10, `requirements.txt` (venv + pip, uv is not installed here) |
| raw clone | worktree `D:\choptuik-i935-raw` of `D:\choptuik-large-d-raw` (that clone is 1301 commits behind and dirty), branch `i935-win2` |
| build | `run_build.sh`: `bash hp/build.sh`, BelowNormal, `CARGO_BUILD_JOBS=8`, `RUSTFLAGS="-C target-cpu=native"` (build.sh) |

Files: `run_build.sh`, `mem_sampler.ps1` and `mem.log` (30 s samples), `build.times`, `build.log`.

## Result (2026-11-17)

The build exited 0 and the import prints `hpkernel avx2 multidouble avx2`. `ref`, `scaled` and `jets` exit 0 with every
compared entry bit-identical, and `jets --mutate=kappa` exits 1.

| criterion | verdict | number | log |
|---|---|---|---|
| `hp/build.sh` exit | 0 | 11:48:27 to 15:58:30 UTC, 250 min (cargo: `Finished release in 248m 26s`), `hpkernel avx2 multidouble avx2` | `build.log`, `build.times` |
| build peak memory | | 34.68 GB working set, 35.61 GB private (rustc, 30 s samples, 501 of them), free memory never below 28.1 GB | `mem.log` |
| `ref --compare=T45-win/.../ref_new.json --Ms=48,64,80` | exit 0 | 72 of 72 outputs bit-identical | `ref.log` |
| `scaled --compare=T81/scaled_main.json` | exit 0 | 22 of 22 outputs bit-identical (M 192, 256), control fires (step differs) | `scaled.log` |
| `jets --compare=anm-mac/jets_inputs/jets_inputs.json` | exit 0 | 28 of 28 outputs bit-identical, on the stored plans and inputs | `jets.log` |
| `jets ... --mutate=kappa` | exit 1 (must be non-zero) | 28 of 28 outputs differ | `jets_mutate_kappa.log` |

`run_checks.sh` ran the three checks in parallel at BelowNormal with one BLAS thread, 15:58:55 to 16:15:27 UTC, exit 0
(`checks_done.txt`).

The M 32 line of `jets.log` says `input: this machine's 21b5b259..., the reference's 710ec990... (DIFFERENT)`. That is the
resample difference AGENTS.md describes (M 32's input is the M 48 state resampled by numpy, whose rounding differs on
Windows): the run's own line says `input given`, so the 28 hashes are on the stored plans and inputs. dh610's `jets.log` shows
the same line with its own hash.

## Deviations from the task's text

- The estimate was 150 min and 29-31 GB. The build took 250 min and peaked at 34.7 GB: win2b's chain and its other jobs
  kept the CPU near 100% for part of the time, and the build ran at BelowNormal.
- uv is not installed on win2. The venv is `python -m venv` on Python 3.14.10 (the interpreter `venv-i600` uses) with
  `pip install -r requirements.txt`: numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0, maturin 1.16.0.

## The Python package is still at multidouble 4.6.0

`hp/pyproject.toml` at d7b59668 names the multidouble Python package at commit a93e0896, the commit of tag 4.6.0, so
`hp/build.sh` installs a package whose `od_axpy`, `od_add_dd` and `ODLu` use `multidouble::od::OD` of 4.6.0, which has the
renormalization bug of PR #56. Tag 4.8.2 is 482c6835. The bit-identity checks above and #936's compare call the Rust kernel
(`residual_o`, `newton_o`), not these helpers, so they do not cover them. `od_axpy_gap_test.py` checks `od_axpy` against
exact rational arithmetic on 20000 seeded trials per class, and `od_axpy_pin_vs_482.py` compares the two packages bit for bit
on the same inputs (the 4.8.2 package built from tag 4.8.2 into a scratch directory with
`pip install --no-deps --target`, venv-md482 untouched). Run both from this folder, the second with
`PYTHONPATH=<that directory>` for the 4.8.2 side.

| input class (normalized inputs) | worst relative error, pin a93e0896 (4.6.0) | worst relative error, tag 4.8.2 | results that differ in any bit |
|---|---|---|---|
| dense, 8 parts | 2^-423.6 | 2^-423.6 | 0 of 20000 |
| zero parts between nonzero ones, gaps 53-60 bits | 2^-160.9 | 2^-213.3 | 1787 of 15112 |
| same, gaps 53-150 bits | 2^-167.8 | 2^-219.1 | 862 of 19548 |
| same, gaps 53-250 bits | 2^-174.8 | 2^-234.1 | 735 of 19800 |
| same, gaps 53-400 bits | 2^-183.1 | 2^-228.7 | 846 of 19871 |

Dense inputs give the same bits under both packages. On inputs with zero parts between nonzero ones the 4.8.2 package is
much more accurate, and still about 2^-213 off, which is not cancellation (the worst results are as large as the larger
operand). The gap class is mine (up to 12 terms into 8 parts), not PR #56's, so this does not say 4.8.2 violates its bounds.
Logs: `od_axpy_gap_pin_a93e0896.log`, `od_axpy_gap_tag_4.8.2.log`, `od_axpy_pin_vs_482.log`. The 20000-trial output arrays
are regenerable (seeded) and not stored.
