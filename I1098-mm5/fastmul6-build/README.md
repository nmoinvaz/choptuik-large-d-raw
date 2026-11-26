# I1098-mm5/fastmul6-build: hp kernel with f64 remainders on the d/dtheta matrices, build and its checks on the Mac mini M5 Pro (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

A release build of branch `wip/large-d-fastmul6` at d368a0c02352461986c6a03acb40f397c6d27b26 (worktree `~/Source/choptuik-fastmul6`) into its own site folder `~/Source/fastmul6-site`, beside horizon300 (fastmul5).
fastmul6 is fastmul5 plus an f64 remainder per d/dtheta matrix entry (c = D - D_dd), so that the operator is good to about 1e-48 in the quad- and octo-double lanes; the jump agent found the dd-stored matrices
move Delta by -1.2e-24 at D 1000 (-2.2e-32 at D 300), growing roughly as D^15. The installed hpkernel, `~/venv-314`, fastmul3/4/5-site stay as they are.
If the compile fails at the hpkernel crate, the jump agent sends a fixed commit (dh610 builds the same commit).

## Expected results (written 2026-11-26 14:31 UTC, before the build)

| item | expectation |
|---|---|
| build | `maturin build --profile release` exit 0, nice 10, `RUSTFLAGS="-C target-cpu=native"`, `CARGO_PROFILE_RELEASE_STRIP=false`; fastmul5 took 33.0 min and 21.46 GB (swap 0), with other jobs beside it |
| 1. relaxed_build_check.py on the D2000 file (blob 392276089bb4a24974e8359adad661a2a0bb72ba) | exit 0, hpkernel under fastmul6-site, relaxed vs naive <= 1e-50, control > 1e-40, `M 64 ... PASS` |
| 2. recip_check.py on the D 300 state (blob e5a3b5f8, kfree300/input) and the D 1000 state (blob 22bb10b9, kfree1000/input) | exit 0, PASS: the step-plan change at most 1e-44, control above 1e-40 |
| 3. dmat_check.py on the D 300 state and on dh610's D1000_base state (`inputs/D1000_base_h13_dh610.npz`, blob from raw 261a4bef) | exit 0, PASS: "the remainders move F by X" with **X > 1e-45** (about 5e-35 expected at D 300), the two mechanisms' difference at most **1e-3** of X, the 2c control's fraction **above 1e-3** (about 1) |
| 4. taylor_mp_check.py on the D 300 state | exit 0, PASS: bar 1e-60, control above 1e-40 (fastmul5: 1.2e-124 and 2.4e-31) |
| kernel_info | one log line from a form_s run (dump_residual.py on D300_u_base, `inputs` of ../fix) showing kernel_info with **exact_dmat 1** |
| stop and report | a build error (at the hpkernel crate: wait for the jump agent's fixed commit), a failed check, or swap use past a few GB (swap 0.00M now) |

Reported exactly as printed: every check line, the build's time and memory. Files: `build.log`, `mem_samples.log`, `check.log`, `recip300.log`, `recip1000.log`, `dmat300.log`, `dmat1000.log`, `taylor300.log`, `dump_residual.log`, `exit_codes.txt`, `times.txt`.

## Results (2026-11-26 14:57 UTC)

Build 14:31:09-14:55:07 UTC, maturin exit 0, **1437.84 s real (24.0 min)**, peak resident **25,062,637,568 B = 25.06 GB** (`time -l`; 23.20 GB in the 20-s samples, 14:33:30), swap 0.00M throughout. hpkernel:
`/Users/nathan/Source/fastmul6-site/hpkernel/__init__.py`. Exit codes (`exit_codes.txt`): build, zipfile, cp, relaxed_build_check, recip_check D 300 and D 1000, dmat_check D 300 and D 1000, dump_residual all 0;
**taylor_mp_check D 300: exit 1 (FAIL)**. Lines exactly as printed:

| check | line | verdict |
|---|---|---|
| 1. relaxed_build_check (D2000 file) | `D 2000 ks 2618: qd max\|F\| 2.08e-04; \|F_relaxed - F_naive\| 4.53e-57 (<= 1e-50), control \|F_mut56 - F_naive\| 3.69e-05 (> 1e-40); 10.5 s naive, 2.4 s relaxed: PASS` and `M 64: size_s 1153, horizon block 192 values, finite True: PASS` | PASS |
| 2. recip_check D 300 | `the two kinds of reciprocals differ at this state by 7.991e-31; step-plan change 0.00e+00 (bar 1e-44) against the control's 1.72e-36 (must exceed 1e-40): PASS` | PASS |
| 2. recip_check D 1000 | `the two kinds of reciprocals differ at this state by 1.056e-31; step-plan change 0.00e+00 (bar 1e-44) against the control's 5.06e-37 (must exceed 1e-40): PASS` | PASS |
| 3. dmat_check D 300 | `max \|F\| without the remainders 7.991e-31; the remainders move F by 4.92e-35; against -(F(D_dd - S c) - F)/S, S = 65536: 2.564e-40 (5.21e-6 of it); the control (2c) 4.92e-35 (1.0)` / `PASS: the two mechanisms agree to 5.21e-6 (bar 1e-3); the control is off by 1.0 (must exceed the bar)` | PASS (X 4.92e-35 > 1e-45; 5.21e-6 <= 1e-3; control 1.0) |
| 3. dmat_check D 1000 (dh610's D1000_base, blob 57af5b81) | `max \|F\| without the remainders 1.621e-71; the remainders move F by 2.141e-34; against -(F(D_dd - S c) - F)/S, S = 65536: 5.815e-40 (2.72e-6 of it); the control (2c) 2.141e-34 (1.0)` / `PASS: the two mechanisms agree to 2.72e-6 (bar 1e-3); the control is off by 1.0 (must exceed the bar)` | PASS |
| 4. taylor_mp_check D 300 | `HP_EXACT_RECIP=1: max \|kernel - mpmath\| 3.807e-28 over 96 values` / `HP_EXACT_RECIP=0: max \|kernel - mpmath\| 3.807e-28 over 96 values` / `FAIL: lane-precision reciprocals 3.81e-28 (bar 1e-60), the control 3.81e-28 (must exceed 1e-40)` | **FAIL** |
| kernel_info (dump_residual on D300_u_base, fix/inputs) | `D 300: od max \|F\| 7.991724e-31 ({'file': '/Users/nathan/Source/fastmul6-site/hpkernel/__init__.py', 'relaxed': '1', 'exact_recip': 1, 'exact_dmat': 1, 'version': '0.1.0'})` | exact_dmat 1 |

**The taylor_mp_check failure.** Its mpmath recursion reads the double-double d/dtheta matrices only ("Both use the same double-double d/dtheta matrices ... the matrices' own rounding is dmat_perturb's term"), while fastmul6's kernel now adds the f64
remainders (HP_EXACT_DMAT on by default), so the kernel and the check differ by 3.8e-28 with either reciprocal setting, instead of 1.2e-124 and 2.4e-31 (fastmul5). Diagnostic, same check on the same state with the remainders off
(`taylor300_dmat0.log`: `HP_EXACT_DMAT=0`): `HP_EXACT_RECIP=1: max |kernel - mpmath| 1.24e-124`, `HP_EXACT_RECIP=0: ... 2.356e-31`, `PASS: lane-precision reciprocals 1.24e-124 (bar 1e-60), the control 2.36e-31 (must exceed 1e-40)`, exit 0.
So the Taylor arithmetic is unchanged; the check (as written) does not know about the remainders. It was not edited.
