# I1098-mm5/fastmul5-build: relaxed-horizon hp kernel with lane-precision reciprocals, build and its checks on the Mac mini M5 Pro (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

A release build of branch `wip/large-d-fastmul5` at f350aa626d4cedd6b161adb876f293dd2c37bb84 (worktree `~/Source/choptuik-fastmul5`) into its own site folder
`~/Source/fastmul5-site`, beside the m48_2000 run (on fastmul4) and the L50000 solve. fastmul5 is fastmul4 plus the jump agent's reciprocal fix (33eeff5c): every 1/k and 1/x0
in the horizon series, the Taylor coefficients and the centre series in lane precision, where they were rounded to double-double before, which put a horizon-block error of 1e-31 into
octo-double residuals (the D 300 "steps" scatter). The installed hpkernel, `~/venv-314`, fastmul3-site and fastmul4-site stay as they are. Runs on this kernel need
`PYTHONPATH=~/Source/fastmul5-site` and `HP_HORIZON_RELAXED=1`.

## Expected results (written 2026-11-26 12:55 UTC, before the build)

| item | expectation |
|---|---|
| build | `maturin build --profile release` exit 0, nice 10, `RUSTFLAGS="-C target-cpu=native"`, `CARGO_PROFILE_RELEASE_STRIP=false`; fastmul4 took 31.8 min and 21.74 GB (swap 0), fastmul3 34.3 min and 23.05 GB, with other jobs beside them |
| relaxed_build_check.py | on the D 2000 step file (blob 392276089bb4a24974e8359adad661a2a0bb72ba): hpkernel under `~/Source/fastmul5-site/`, `|F_relaxed - F_naive| ... (<= 1e-50)`, control `> 1e-40`, PASS, and `M 64: size_s 1153, horizon block 192 values, finite True: PASS`; exit 0 (the numbers may change, since the reciprocals changed) |
| recip_check.py, D 300 | `HP_HORIZON_RELAXED=1 PYTHONPATH=site:hp python hp/recip_check.py <D 300 state>`: the residual change when every Taylor step is halved at most 1e-44 (PASS), and the control in the same run (HP_EXACT_RECIP=0) above 1e-40 (1.7e-36 at D 300 on the old kernel) |
| recip_check.py, D 1000 | the same on the D 1000 state: the change at most 1e-44, the control above 1e-40 |
| inputs | D 300 state: blob e5a3b5f85d19cb7de392261274778920a9ddf448 (I1088-dh610/out/rls300/release_ls_h13_D300.0000.npz); D 1000 state: blob 22bb10b98cd4726c5d0ebd09cbd710423329fa57 (I1088-dh610/rls1000h13q/release_ls_h13_D1000.0000.npz); copies in `../kfree300/input/` and `../kfree1000/input/` |
| stop and report | a build error, a failed line, or swap use past a few GB (swap 0.00M now) |

Reported exactly as printed: both recip_check lines, the build's time and memory. Files: `build.log`, `mem_samples.log`, `check.log`, `recip300.log`, `recip1000.log`, `exit_codes.txt`, `times.txt`.
