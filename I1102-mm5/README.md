# I1102-mm5: ellrs (block 12 of the l = 1 mode matrix in Rust) built and checked on the Mac mini M5 Pro (#1102)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1102. Written 2026-11-28 03:30 UTC by the clock, before the build and the checks, on the coordinator's order of 03:27 UTC.

## Order (the coordinator's, 2026-11-28 03:27 UTC)

1. New worktree, nothing running uses it: `git -C ~/Source/choptuik-large-d fetch origin wip/i1101-weakdir`, then `git -C ~/Source/choptuik-large-d worktree add --detach ~/Source/choptuik-ellrs 44ef3c82` (the weak-direction tools plus ellrs; the same `i1101_weakdir.py` and `dss_ell.py` as 49664990).
2. Build into the venv the roots use (`~/venv-314`): `cd ~/Source/choptuik-ellrs/solver/matter && VIRTUAL_ENV=~/venv-314 ellrs/build.sh` (about a minute; prints `ellrs <isa> <products>`, expect accelerate). The script was read before it ran: it runs `maturin build --release` (features accelerate on macOS) with `RUSTFLAGS="-C target-cpu=native"` and installs the wheel with `pip install --force-reinstall --no-deps`, touching no other package of the venv; crates are fetched from crates.io on the first build (`Cargo.toml`: pyo3 0.30, numpy 0.30, rayon 1.10, matrixmultiply 0.3.11, multidouble =6.0.0).
3. Checks, `OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`, from that folder:
   - `python ell_b12rs.py selftest` (must exit 0);
   - `python ell_b12rs.py selftest --mutate=nolam` (must exit 1);
   - `python ell_b12rs.py selftest --mutate=harm` (must exit 1);
   - `python ell_b12rs.py check <raw>/I1102-mac/in/l1kc31r1025.jsonl <raw>/I1102-mac/in/sol_l1kc31r1025_D10.5000.npy 10.5 2.87 --threads=2 --controls=1` (must exit 0: 15010 of 15010 entries bit for bit, both controls FAIL).
   Any other outcome: stop and report; nothing switches.
4. If all pass: #1110's root (when dh170's chord state lands) runs from `~/Source/choptuik-ellrs/solver/matter` with `--b12=rust --b12_threads=2` in place of `--b12=fast`, the rest as before; the block-12 choice is noted in I1110-mm5's README.

Reported: the build line and the four check exits, in one line. The logs are in this folder.

## Inputs and code (blobs by `git hash-object --no-filters`)

| what | blob |
|---|---|
| worktree `~/Source/choptuik-ellrs` at 44ef3c82 | `solver/matter/i1101_weakdir.py` 8709abbd and `dss_ell.py` 5d28c19e (equal to the 49664990 worktree's), `d18_secant.py` 9706e506 (49664990's is eb1396ad; this one adds `--b12=rust` and `--b12_threads`) |
| `in/l1kc31r1025.jsonl` (from `origin/main:I1102-mac/in/`) | e5a87ec573c6e53c36c2ef3b2598850f44e8d68d |
| `in/sol_l1kc31r1025_D10.5000.npy` (same) | f07a8984e9b13be834a171a44f05f8bd979735b0 |

`~/venv-314`: Python 3.14.10, maturin 1.16.0, Rust through `source ~/.cargo/env`. The build touches only the new `ellrs` package of the venv; the running jobs (stage 1c's roots, which use `d18_secant.py` eb1396ad and do not import ellrs) are not affected.

## Notes written before the run

- `i1101_weakdir.py root` (8709abbd) reads only `--tol`, `--maxev`, `--dln` and `--b12`, and builds `RealEval` without a thread count, so `--b12_threads=2` is ignored there and the rust block would use rayon's default pool. The root step of step 4 is therefore run with `RAYON_NUM_THREADS=2` as well, and the threads `ellrs` reports are checked in its log.

## Results (2026-11-28 03:31 UTC)

The build and the four checks of the order, all as required (logs `build.log`, `selftest.log`, `selftest_nolam.log`, `selftest_harm.log`, `check.log`, `checks.txt`; `run_checks.sh`):

| step | result |
|---|---|
| build (`ellrs/build.sh`, 03:30:24 UTC, about 11 s of compiling) | `ellrs neon accelerate` (isa neon, products by Accelerate's dgemm), installed into `~/venv-314` |
| `selftest` | exit 0 (3666 of 3666 entries bit for bit at lambda 0 and 0.9) |
| `selftest --mutate=nolam` | exit 1 (as required) |
| `selftest --mutate=harm` | exit 1 (as required) |
| `check` (k_c 31, D 10.5, lambda 2.87, 2 threads, `--controls=1`) | exit 0: the record system (|F| 4.2644450300e-12, 1748 steps, equal to the record's), **15010 of 15010 entries bit for bit**, both controls FAIL (nolam 0 of 15010, harm 0 of 15010), Rust 1.64 s against DDEll 16.2 s (ratio 9.9) |

One line: `ellrs neon accelerate`; exits 0, 1, 1, 0.

## Amendment: the fast solver Jacobian at k_c 127 (2026-11-28 03:43 UTC, coordinator's order of 03:43 UTC; written before the run)

One check of the new fast solver Jacobian (`ell_fastm.jacobian_fast`, #1102) at k_c 127, queued for when part A of the ladder (D 4628's k* stage, `I1098-mm5/ladder/D4628m/tail/run.log`) ends and frees its 4 threads: the run starts when that log has a `job rc` line. Code: `wip/i1101-weakdir` at **693a4d79** (detached worktree `~/Source/choptuik-jac127`; `ell_fastm.py` blob 3431e32e, `i1101_weakdir.py` c1ecc1e7, `dss_ell.py` 5d28c19e), `~/venv-314/bin/python`, from `solver/matter`, `OPENBLAS_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4`, `nice -n 10`, `timeout 7200`. Inputs: R0's state and record, the blob-checked copies in `I1109-mm5/c/in/` (90d3e655, d1a3a641).

```
python ell_fastm.py jaccheck REC STATE 23.0 --out=I1102-mm5/jac127.json > I1102-mm5/jac127.log 2>&1
```

It builds both Jacobians (the solver's `DSSEll.jacobian` and `jacobian_fast`; about 0.6 GB each) and compares them: the residual equal; per block the state columns within 1e-8 and the Delta column within 1e-12 relative (1e-8 in the horizon block); the phase row equal; exit 0 only on PASS (exit 1 is a result, not a reason to rerun; exit 3 not the record system). Reported: the exit, the times line and block 12's line. The two files are pushed here. Driver: `run_jac127.sh`, log `jac127_run.log`.

## The k_c 127 Jacobian check is dropped (coordinator's order of 04:04 UTC, noted 2026-11-28 04:05 UTC)

dh610 (back at full speed) runs the k_c 127 `jaccheck` with the Rust block; the check queued above on this machine was never started. Its driver (`run_jac127.sh`, waiting for part A's `job rc`) was stopped at 04:05 UTC (`jac127_run.log`). No `jac127.log` or `jac127.json` exists here. The detached worktree `~/Source/choptuik-jac127` (693a4d79) stays unused.
