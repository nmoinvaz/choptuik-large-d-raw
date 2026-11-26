# I1098-mm5/fastmul7-build: hp kernel with the Moebius split fix (horizon_mob solves with q_0 - omega (D_e + c) 1), build and its checks on the Mac mini M5 Pro (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

A release build of `wip/large-d-fastmul6` at d40a9c62 (worktree `~/Source/choptuik-fastmul7`, from `~/Source/choptuik-fastmul6`'s repository; c21ba40d "form_s.rs horizon_mob: B_0's split exact for the matrix applied" is the kernel change over f398e829) into its own site folder `~/Source/fastmul7-site`.
fastmul7 is fastmul6 plus a corrected split of B_0 = 1 + X in the Moebius series: the right side is q_0 - omega D_e 1 with D_e the matrix as applied (with its f64 remainder), whose rows sum to its own rounding, not 0; without that term the Moebius values sat 1.7e-60 off the u series at D 300 (`I1098-dh610/mpcheck`).
`FS_MUT_SPLIT` (mutate 57) leaves the term out again, the control. Coordinator's order (2026-11-26 19:26 UTC), started when D 622 ended and was reported. `~/Source/fastmul6-site`, `~/venv-314` and the other sites stay as they are.

## Expected results (written 2026-11-26 19:27 UTC, before the build)

| item | expectation |
|---|---|
| build | `maturin build --profile release` exit 0, nice 10, `RUSTFLAGS="-C target-cpu=native"`, `CARGO_PROFILE_RELEASE_STRIP=false`, its own `CARGO_TARGET_DIR`; fastmul6 took 24.0 min and 25.06 GB peak resident (swap 0) with other jobs beside it; here three jobs run beside it |
| 1. relaxed_build_check.py on the D2000 file (blob 392276089bb4a24974e8359adad661a2a0bb72ba) | exit 0, relaxed vs naive <= 1e-50, control > 1e-40, `M 64 ... PASS` |
| 2. recip_check.py D 300 and D 1000 (`kfree300/input`, `kfree1000/input`) | exit 0, PASS: step-plan change at most 1e-44, control above 1e-40 |
| 3. dmat_check.py D 300 and D 1000 (`../fastmul6-build/inputs/D1000_base_h13_dh610.npz`) | exit 0, PASS: remainders move F by X > 1e-45 (about 5e-35 at D 300), mechanisms agree to 1e-3 of X, the 2c control's fraction above 1e-3 |
| 4. taylor_mp_check.py D 300 | **expected FAIL as on fastmul6** (the check reads the dd matrices only; kernel against mpmath 3.8e-28 with either reciprocal setting); rerun with HP_EXACT_DMAT=0, expected PASS (1.24e-124 against the bar 1e-60, control 2.36e-31); both reported |
| 5. `horizon_mp_check.py ../ladder/D300u/tail/release_ls_h21_D300.0000.npz --ks_mp 1100 --ks_mob 800 --bar 1e-100 --ctl_mutate 57 --ctl_bar 1e-80` | **Moebius against mpmath at most 1e-100**; the split control (mutate 57) above 1e-80 (about 1.7e-60 expected) |
| D 2231 | if every check passes, started at once (below) |
| stop and report | a build error, any failed check (the taylor_mp_check failure with the remainders on is the known one: report both runs), or swap use past a few GB |

Run from `~/Source/choptuik-fastmul7/hp` with HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 PYTHONPATH=`~/Source/fastmul7-site`, the same inputs as `../fastmul6-build`. Reported exactly as printed: every check line, the build's time and memory.
Files: `build.log`, `mem_samples.log`, `check.log`, `recip300.log`, `recip1000.log`, `dmat300.log`, `dmat1000.log`, `taylor300.log`, `taylor300_dmat0.log`, `horizon_mp.log`, `exit_codes.txt`, `times.txt`.

## D 2231, if every check passes

`HP=$HOME/Source/choptuik-fastmul7/hp SITE=$HOME/Source/fastmul7-site KSBAR=1e-70 bash tools/ladder_point2_651b.sh 2231 250 6 <ladder>/D2231 <ladder>/inputs/D2000_base6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 31`, detached, 6 threads, from the ladder folder.
`tools/ladder_point2_651b.sh` (raw 12a4068d `I1098-mac-a/tools/ladder_point2.sh`, blob 651bb75f4ee290156c16fb6c6c3ef4bd788d224d, verified; it takes the commit from HP's HEAD) and the D 2000 input `../ladder/inputs/D2000_base6_h13.npz`
(raw `I1098-dh610/fix6/D2000_base6/release_ls_h13_D2000.0000.npz`, blob b897ba43adb46653785b362d2ae6a2f712fdd8db, verified against raw). Its README (`../ladder/D2231/README.md`) carries the bars (D 1291's: the jump converges and the ks gate passes, h5..h13 each released, the tail falls) and the amended stop rule.
