# I1102-win: the Windows gate of the Rust block 12 (ellrs, #1102), built from branch wip/ell1-rust-b12 at d4b6b6ce (winb)

Written before the run, 2026-11-27 05:53:17 UTC (the time the README was staged, 14 s before the driver started; the first push of this folder did not carry it, see the Status; later pushes keep this time). Nothing of the build or the gates had been run for this folder when the order, the expectations and the estimates below were written. Run beforehand, read-only: the toolchain look (cargo 1.95.0, rustc 1.95.0 on host x86_64-pc-windows-msvc, maturin in the scanner's venv), the worktree, the pins. Runner: the winb session (surface-laptop-4, Windows 11, i7-1185G7 4 cores / 8 threads, 32 GB); coordinator t5.

## Order (t5's hc, stamped 2026-11-27 05:47 UTC; winb section, quoted)

"Next for winb, #1102 (https://github.com/nmoinvaz/choptuik-large-d/issues/1102): the Windows gate of the Rust block 12. A worktree of branch wip/ell1-rust-b12 at d4b6b6ce. Follow SPEED_ELL1.md's section "Block 12 in Rust" from Git Bash: solver/matter/ellrs/build.sh into a SITE folder for your scanner's venv, leaving the venv untouched. It needs cargo (rustup) and maturin; if cargo is missing, report it and stop, and do not install toolchains. Gates: ell_b12rs.py selftest exits 0, and 1 with --mutate=nolam and with --mutate=harm. ell_b12rs.py check on raw I1102-mac/in/'s k_c 31 state with --controls=1 prints 15010 of 15010 bit for bit. Use OPENBLAS_NUM_THREADS=1. New raw folder I1102-win/, README first; post the result on #1102."

## What I run

1. **Worktree** `choptuik-i1102` (detached) of the repo `choptuik-large-d`, branch wip/ell1-rust-b12 at **d4b6b6ce** (SPEED_ELL1.md blob 17d70b90, section "Block 12 in Rust"). Pins the driver checks before it builds anything: HEAD d4b6b6cea24f518d38cac17877c9a0da813b05f4 and a clean tree; the `solver/matter/ellrs` tree 47ce5fb8 (`build.sh` e6254c9b, `Cargo.toml` 5bae423e, `Cargo.lock` 2147ed9a, `pyproject.toml` fdc88d51); `ell_b12rs.py` a1fff74f; `ell_ddm.py` 86578fee; `ddnp.py` 9b1fb195; `ell_fastm.py` 93f963f6; `dss_ell.py` 5d28c19e.
2. **Inputs** (raw `I1102-mac/in/`, fetched from origin/main, pinned by blob, checked by the driver): `sol_l1kc31r1025_D10.5000.npy` **f07a8984** (16568 bytes), stub `l1kc31r1025.jsonl` **e5a87ec5** (1946 bytes): the k_c 31 state at D 10.5.
3. **Toolchain** (looked at only, nothing installed): cargo 1.95.0 and rustc 1.95.0 (rustup, `C:\Users\nathan\.cargo\bin`, host x86_64-pc-windows-msvc), maturin in `venv-md510\Scripts` (my scanner's venv: Python 3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 with `dd_logdet`). If the driver finds cargo or maturin missing it stops and I report it.
4. **Build**, from Git Bash (the driver starts Git's `bash.exe`): `ellrs/build.sh SITE` with `VIRTUAL_ENV` set to the scanner's venv (so that `build.sh` picks its python and the wheel tag cp314) and SITE = `i1102_1025/site/` in my stage, outside the venv: `maturin build --release` (RUSTFLAGS `-C target-cpu=native`, `CARGO_PROFILE_RELEASE_STRIP=false`), then `pip install --force-reinstall --no-deps --target SITE`. The first build downloads the crates from crates.io (pyo3 0.30, numpy 0.30, rayon, matrixmultiply, multidouble 6.0.0). **The scanner's venv stays untouched**: `pip freeze` before and after must be equal (logged), and `import ellrs` must not resolve from the venv alone. `build.sh` prints `ellrs <isa> <products>`.
5. **Gates**, with `PYTHONPATH=SITE`, `OPENBLAS_NUM_THREADS=1` and `VECLIB_MAXIMUM_THREADS=1`, in this order, each in its own log:
   - `ell_b12rs.py selftest`: exit 0 wanted;
   - `ell_b12rs.py selftest --mutate=nolam`: exit 1 wanted;
   - `ell_b12rs.py selftest --mutate=harm`: exit 1 wanted;
   - `ell_b12rs.py check l1kc31r1025.jsonl sol_l1kc31r1025_D10.5000.npy 10.5 2.87 --threads=4 --controls=1`: exit 0 wanted, **"15010 of 15010 entries bit for bit"** for the plain block, both controls FAIL (SPEED_ELL1.md: "DDEll's block on the runner itself, about a minute").
6. Everything runs BelowNormal, started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_i1102_1025.cmd` (outside my terminal; the session check, `session_check_i1102.txt`, must report no `claude` in any chain), with a keep-awake helper (`SetThreadExecutionState`, power plan untouched). One driver, `gate_i1102_driver_1025.py`; caps 3600 s per step, killed by the exact pid.

**Stops** (my reading of the order): cargo or maturin missing (report, do not install); the build fails (report the error); a gate not as wanted (report, change nothing on the branch). I run nothing beyond the four gates: not the scanner's `--b12=rust`, not the k_c 87, 127 or 135 states.

## Expectations, written before the run

| item | written |
|---|---|
| `build.sh` | exit 0, prints `ellrs <isa> <products>` (the i7-1185G7 has AVX-512, so I expect an avx512 `isa`, avx2 if the build does not use it) |
| `selftest` | exit 0 (block 12 at k_c 15 lambda 0 and 0.9 bit for bit with scipy's dgemm and with the built-in products) |
| `selftest --mutate=nolam`, `--mutate=harm` | exit 1 and 1 |
| `check` (k_c 31, 15010 entries) | exit 0; plain block 15010 of 15010 at 4 threads, both controls FAIL |
| scanner's venv | untouched: `pip freeze` equal before and after |
| where a failure would come from | the MSVC link or pyo3 0.30 with Python 3.14 in the build; a bit difference only if `numpy.exp` or scipy's LU differed between DDEll's own call and the callback ellrs makes (both are the machine's own, so none is expected) |

## Cost, estimates written before the run

| step | estimate |
|---|---|
| build (first, with the crates downloaded; LTO thin, codegen-units 1, target-cpu native, BelowNormal beside the other project's `convergence.py` jobs) | 2 to 10 min, central 4 min (SPEED_ELL1.md: about a minute on the Mac) |
| each selftest | under 1 min |
| `check` at k_c 31 (the DDEll reference block in Python double-double, then the Rust block at 4 threads and the two controls) | 1 to 6 min (SPEED_ELL1.md: about a minute) |
| the whole driver | 5 to 25 min, central 12 min |
| memory | under 3 GB (no sampler for this short run; the driver logs wall times) |

## Files made here

`README.md`; `gate_driver_w.log` (the driver's log); `build.log`; `gate_selftest.log`, `gate_selftest_nolam.log`, `gate_selftest_harm.log`, `gate_check_kc31.log`, `check_kc31.jsonl`; `gate_summary.txt`; `venv_freeze_before.txt`, `venv_freeze_after.txt`; `session_check_i1102.txt`; `rows/gate_keepawake.log`; the driver `gate_i1102_driver_1025.py`, `go_i1102_1025.cmd`, `keepawake_1025.py`, `session_check_1025.ps1`, `publish_i1102_1025.sh`, `push_1102.sh`. The inputs are not copied (they are raw `I1102-mac/in/`, pinned by blob above).

## Status

README staged 2026-11-27 05:53:17 UTC, before the run. **The README-first push did not carry the folder:** `push_1025.sh` (the script my publish scripts call) adds only `I1025-win` and `INDEX.md`, so raw commit 1d46165d4 (05:53:19 UTC) put only the new line of `INDEX.md` for this folder on raw (the line is made from the README's title; the folder itself did not go). I found it at 05:57 UTC, when the push of this Result stopped on the untracked copy. The folder first reached raw with the push stamped at the end of this Status, after the run; the README text above the run's results is as written at 05:53:17 UTC (the staged file's time; nothing in it was changed after the run except line 3, the file list (it now names `push_1102.sh`), this Status and the Result; checked with diff against the as-staged copy). I copied the script as `push_1102.sh` (adds `I1102-win`; `push_1025.sh` is unchanged). The driver started 05:53:31 UTC (`Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_i1102_1025.cmd`: conhost 26576 <- cmd 22308 <- driver 19648 / 21388, keep-awake helper 21956; `session_check_i1102.txt`: no `claude` in any chain, exit 0) and ended 05:56:48 UTC: **ALL GATES AS WANTED** (`gate_summary.txt`). No stop condition of the order was reached: cargo and maturin were present (nothing was installed), the build exited 0, every gate had the exit code wanted.

Pushed 2026-11-27 05:58:31 UTC.

## Result

**All four gates as wanted, on this machine (Windows 11, i7-1185G7, AVX-512), 3 min 17 s for the whole driver (05:53:31 to 05:56:48 UTC).**

| step | exit | wanted | wall |
|---|---|---|---|
| `ellrs/build.sh SITE` | 0 | 0 | 86 s |
| `ell_b12rs.py selftest` | 0 | 0 | 13 s |
| `ell_b12rs.py selftest --mutate=nolam` | 1 | 1 | 13 s |
| `ell_b12rs.py selftest --mutate=harm` | 1 | 1 | 13 s |
| `ell_b12rs.py check` k_c 31, D 10.5, lambda 2.87, `--threads=4 --controls=1` | 0 | 0 | 70 s |

**Build** (`build.log`): cargo 1.95.0 and rustc 1.95.0 (host x86_64-pc-windows-msvc), maturin 1.16.0, CPython 3.14.10 (the scanner's venv python, wheel `ellrs-0.1.0-cp314-cp314-win_amd64.whl`), 30 crates compiled, `Finished release profile in 1m 22s`, `RUSTFLAGS=-C target-cpu=native`. `build.sh` printed, as is:

```
ellrs avx512 matrixmultiply C:\Users\nathan\Source\i1102_1025\site\ellrs\__init__.py
```

(`ellrs.gemm()` at that point names `matrixmultiply`; the check below ran with `products dgemm`, scipy's.) The crate is installed in `site/` of my stage, outside the venv. **The scanner's venv is untouched**: `pip freeze` before and after are equal (`venv_freeze_before.txt`, `venv_freeze_after.txt`: maturin 1.16.0, mpmath 1.3.0, multidouble @ 8c4360ac, numpy 2.5.4, python-flint 0.9.0, scipy 1.18.1, sympy 1.14.0), and `import ellrs` does not resolve from the venv alone (`find_spec` None). The build left `dist/` and `target/` in the worktree `choptuik-i1102` (mine; not committed).

**Selftest** (`gate_selftest.log`, last lines as printed; the five Ozaki operators, each with scipy's dgemm and with the built-in matrixmultiply, bit for bit in 432, 432, 144, 135 and 432 entries; block 12 at lambda 0 and 0.9, 3666 entries each):

```
block 12 at lambda 0.0: 3666 of 3666 entries bit for bit, max |d|/|entry| 0.00e+00 ok
block 12 at lambda 0.9: 3666 of 3666 entries bit for bit, max |d|/|entry| 0.00e+00 ok
selftest (mutate none): PASS
```

The two controls (`gate_selftest_nolam.log`, `gate_selftest_harm.log`) print `selftest (mutate nolam): FAIL` (block 12 at lambda 0.9: 0 of 3666 entries bit for bit, max |d|/|entry| 1.79e+03; at lambda 0.0 it still matches, as it must without lambda) and `selftest (mutate harm): FAIL` (block 12 0 of 3666 at both lambda, 1.32e+01 and 6.92e+00; Ozaki bodd 0 of 432, sodd 126 of 144), exit 1 each.

**The k_c 31 check** (`gate_check_kc31.log`, as printed; the state f07a8984 and stub e5a87ec5 are raw `I1102-mac/in/`'s, pinned by blob; the records are in `check_kc31.jsonl`):

```
D 10.5 k_c 31: |F| 4.2628798701e-12 (record 4.2644450300e-12), steps 1748 (record 1748): the record system
N 96, n_odd 32, n_even 31, nf 95, horizon steps 384, Ks 30, u0 0.04; operators 0.4 s; ellrs avx512, products dgemm, threads [4], lu scipy, mutate none, controls nolam, harm
lambda 2.87, block (4 threads): 15010 of 15010 entries bit for bit; max |d|/|entry| 0.000e+00, max |d|/max|block| 0.000e+00 (bar 1e-28 per entry): PASS; Rust 5.89 s, DDEll 50.9 s, ratio 8.6
lambda 2.87, control nolam (4 threads): 0 of 15010 entries bit for bit; max |d|/|entry| 1.410e+03, max |d|/max|block| 2.697e-01 (bar 1e-28 per entry): FAIL, as a control must; Rust 5.63 s, DDEll 50.9 s, ratio 9.0
lambda 2.87, control harm (4 threads): 0 of 15010 entries bit for bit; max |d|/|entry| 2.736e+03, max |d|/max|block| 4.142e-01 (bar 1e-28 per entry): FAIL, as a control must; Rust 5.59 s, DDEll 50.9 s, ratio 9.1
check: PASS
```

The plain block: **15010 of 15010 entries bit for bit** (max |d|/|entry| 0, bar 1e-28 per entry), at 4 threads. Both controls FAIL as a control must (0 of 15010; 1.41e+03 and 2.74e+03 per entry).

**Time** (the check's own, one block 12 at k_c 31, lambda 2.87, 4 Rust threads against `DDEll.mode_matrix(only=[12])` in one process): Rust 5.89 s (the controls 5.63 and 5.59 s), DDEll 50.9 s, ratio 8.6. The scanner's evaluation at larger k_c was not run (not in the order).

**Against my estimates:**

| item | written | measured |
|---|---|---|
| build | 2 to 10 min, central 4 min | 86 s (cargo 1 min 22 s): below the range |
| each selftest | under 1 min | 13 s |
| `check` at k_c 31 | 1 to 6 min | 70 s (the DDEll reference block 50.9 s of it) |
| whole driver | 5 to 25 min, central 12 min | 3 min 17 s |
| `isa` | avx512 expected | avx512 |
| scanner's venv | untouched | untouched |
| memory | under 3 GB (not sampled) | not sampled (3 min run) |

Nothing on the branch was changed; no toolchain was installed; the scanner's `--b12=rust` and the k_c 87, 127 and 135 states were not run (not in the order).
