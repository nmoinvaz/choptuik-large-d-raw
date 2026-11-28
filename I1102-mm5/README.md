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
