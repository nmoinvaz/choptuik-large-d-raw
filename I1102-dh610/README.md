# I1102-dh610: the fast solver Jacobian at k_c 127 and the Rust block 12 (ellrs) built and gated on dh610 (#1102)

Machine: dh610-fedora (Fedora, Linux 7.3, i7-12700, 12 cores / 20 threads, AVX2, 62 GB), runner dh610 (account claude-me2), started 2026-11-28 04:04 UTC by the coordinator (hc from t5). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1102. Written 2026-11-28 04:10 UTC by the clock, before the runs.

## Order (the coordinator's, 2026-11-28 04:04 UTC)

Budget: the 8 threads beside t5's unit `i1088a-d6666x` (12 threads, never touched), nice 10, each run its own `systemd-run --user` unit. Code: worktree `~/Source/choptuik-ell1fast` (detached, `wip/i1101-weakdir` at 693a4d79), venv `~/Source/venv-i1058` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble 5.1.0 with `dd_logdet`, maturin 1.16.0), from `solver/matter`.

1. `OPENBLAS_NUM_THREADS=4`, `timeout 7200`:
   `python ell_fastm.py jaccheck <R0 jsonl> <R0 npy> 23.0 --out=I1102-dh610/jac127.json > I1102-dh610/jac127.log 2>&1`
   Report the exit, the times line and block 12's line. Exit 1 is a result: report it, do not rerun. Bars of `jaccheck` (its docstring): the residual equal; per block the state columns within 1e-8 and the Delta column within 1e-12 relative (1e-8 in the horizon block); the phase row equal; exit 0 only on PASS (exit 3: not the record system).
2. ellrs (block 12 in Rust): `ellrs/build.sh` in the venv (about a minute; prints `ellrs <isa> <products>`), then with `OPENBLAS_NUM_THREADS=1` from `solver/matter`:
   - `python ell_b12rs.py selftest` must exit 0;
   - `python ell_b12rs.py selftest --mutate=nolam` must exit 1;
   - `python ell_b12rs.py selftest --mutate=harm` must exit 1;
   - `python ell_b12rs.py check <raw>/I1102-mac/in/l1kc31r1025.jsonl <raw>/I1102-mac/in/sol_l1kc31r1025_D10.5000.npy 10.5 2.87 --threads=2 --controls=1` must exit 0 (15010 of 15010 entries bit for bit, both controls FAIL).
   Any other outcome: stop and report.

## Inputs and code (blobs by `git hash-object --no-filters`, each equal to origin/main's blob of the raw repository)

| what | blob |
|---|---|
| `I1101-dh170/in/sol_l1kc127k070w2_D23.0000.npy` (R0's state) | 90d3e655 |
| `I1101-dh170/in/l1kc127k070w2.jsonl` (R0's record) | d1a3a641 |
| `I1102-mac/in/sol_l1kc31r1025_D10.5000.npy` | f07a8984 |
| `I1102-mac/in/l1kc31r1025.jsonl` | e5a87ec5 |
| `solver/matter/ell_fastm.py` / `ell_b12rs.py` / `d18_secant.py` / `i1101_weakdir.py` / `dss_ell.py` / `ell_ddm.py` at 693a4d79 | 3431e32e / a1fff74f / 9706e506 / c1ecc1e7 / 5d28c19e / 64c4337f |

Inputs were read with `git cat-file blob` from `origin/main` (93f80a38f) of the raw clone into `~/scratch1102/in/` (outside this repository, read only).

## Notes written before the run

- `gh` on this machine reports `The token in default is invalid` (account nmoinvaz), so comments and labels on the issues cannot be posted until it is renewed; reads through the public API and git over SSH work. The results are written here and in the report to the coordinator meanwhile.
- The negative-mass project's four single-thread units (`nm-i246-rec-l0..l3`, nice 10) run on this machine, so with the task's "count their threads against the budget" the budget beside t5's 12 threads is 4, not 8. Step 1 uses 4 threads as ordered.

## Step 2 result (2026-11-28 04:14 UTC)

`run_step2.sh` (unit `i1102-step2`; `exits_1102.txt` has each exit and clock): build exit 0 (68 s; `ellrs avx2 matrixmultiply`), selftest 0, `--mutate=nolam` 1, `--mutate=harm` 1, k_c 31 check 0 (15010 of 15010 bit for bit, both controls FAIL). Logs `build.log`, `selftest*.log`, `check.log`; the post is `post_1102_step2.md`. `ellrs` was installed into `~/Source/venv-i1058` (the only change to that venv).
