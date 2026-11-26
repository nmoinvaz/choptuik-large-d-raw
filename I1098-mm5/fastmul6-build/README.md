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
