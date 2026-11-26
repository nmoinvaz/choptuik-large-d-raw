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

`EXTRA="--inner_chord 0" HP=$HOME/Source/choptuik-fastmul7/hp SITE=$HOME/Source/fastmul7-site KSBAR=1e-70 bash tools/ladder_point2_651b.sh 2231 250 6 <ladder>/D2231 <ladder>/inputs/D2000_base6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 31`, detached, 6 threads, from the ladder folder.
`tools/ladder_point2_651b.sh` (raw 12a4068d `I1098-mac-a/tools/ladder_point2.sh`, blob 651bb75f4ee290156c16fb6c6c3ef4bd788d224d, verified; it takes the commit from HP's HEAD) and the D 2000 input `../ladder/inputs/D2000_base6_h13.npz`
(raw `I1098-dh610/fix6/D2000_base6/release_ls_h13_D2000.0000.npz`, blob b897ba43adb46653785b362d2ae6a2f712fdd8db, verified against raw). Its README (`../ladder/D2231/README.md`) carries the bars (D 1291's: the jump converges and the ks gate passes, h5..h13 each released, the tail falls) and the amended stop rule.

### Amendment (2026-11-26 20:08 UTC, coordinator's order): inner_chord 0

fastmul7's Python d40a9c62 also defaults to `inner_chord 1`, which floored D 747's h13 qq inner solve (`../ladder/D747/README.md`); D 2231 therefore starts with `EXTRA="--inner_chord 0"` in front (the script, blob 651bb75f, takes the commit from HP's HEAD, so no `--commit`).
Every later ladder point on this machine also gets `--inner_chord 0` unless the coordinator says otherwise.

## Results (2026-11-26 21:01 UTC)

Build 20:14:37-20:48:32 UTC, maturin exit 0, **2035.12 s real (33.9 min; cargo: 33m 53s)**, peak resident **20,647,624,704 B = 20.65 GB** (`time -l`; max sample 19.59 GB at 20:17:57), swap 0.00M in all 102 samples (`mem_samples.log`), with D 747 and D 1291 running beside it.
hpkernel: `/Users/nathan/Source/fastmul7-site/hpkernel/__init__.py`; the checks ran 20:48:32-20:59:58 UTC. Exit codes (`exit_codes.txt`): build, zipfile, cp, relaxed_build_check, recip_check D 300 and D 1000, dmat_check D 300 and D 1000, taylor_mp_check D 300 (remainders on and off): all 0; **horizon_mp_check: exit 1 (FAIL)**.
Lines exactly as printed:

| check | line | verdict |
|---|---|---|
| 1. relaxed_build_check (D2000 file, blob 392276089bb4a24974e8359adad661a2a0bb72ba) | `D 2000 ks 2618: qd max\|F\| 2.08e-04; \|F_relaxed - F_naive\| 4.50e-57 (<= 1e-50), control \|F_mut56 - F_naive\| 3.69e-05 (> 1e-40); 14.5 s naive, 3.0 s relaxed: PASS` and `M 64: size_s 1153, horizon block 192 values, finite True: PASS` | PASS |
| 2. recip_check D 300 | `the two kinds of reciprocals differ at this state by 7.991e-31; step-plan change 0.00e+00 (bar 1e-44) against the control's 1.72e-36 (must exceed 1e-40): PASS` | PASS |
| 2. recip_check D 1000 | `the two kinds of reciprocals differ at this state by 1.056e-31; step-plan change 0.00e+00 (bar 1e-44) against the control's 5.06e-37 (must exceed 1e-40): PASS` | PASS |
| 3. dmat_check D 300 | `the remainders move F by 4.92e-35; against -(F(D_dd - S c) - F)/S, S = 65536: 2.564e-40 (5.21e-6 of it); the control (2c) 4.92e-35 (1.0)` / `PASS: the two mechanisms agree to 5.21e-6 (bar 1e-3); the control is off by 1.0 (must exceed the bar)` | PASS |
| 3. dmat_check D 1000 (dh610's D1000_base) | `the remainders move F by 2.141e-34; against ...: 5.815e-40 (2.72e-6 of it); the control (2c) 2.141e-34 (1.0)` / `PASS: the two mechanisms agree to 2.72e-6 (bar 1e-3); the control is off by 1.0 (must exceed the bar)` | PASS |
| 4. taylor_mp_check D 300, remainders on | `HP_EXACT_RECIP=1: max \|kernel - mpmath\| 1.096e-124 over 96 values` / `HP_EXACT_RECIP=0: ... 2.356e-31` / `the matrices on both sides: hi + lo + c (the remainders applied)` / `PASS: lane-precision reciprocals 1.1e-124 (bar 1e-60), the control 2.36e-31 (must exceed 1e-40)` | **PASS** (this version of the check applies the remainders on both sides; fastmul6's failed with 3.81e-28) |
| 4b. taylor_mp_check D 300, HP_EXACT_DMAT=0 | `HP_EXACT_RECIP=1: max \|kernel - mpmath\| 1.24e-124 over 96 values` / `the matrices on both sides: hi + lo` / `PASS: lane-precision reciprocals 1.24e-124 (bar 1e-60), the control 2.36e-31 (must exceed 1e-40)` | PASS |
| 5. horizon_mp_check (`../ladder/D300u/tail/release_ls_h21_D300.0000.npz --ks_mp 1100 --ks_mob 800 --bar 1e-100 --ctl_mutate 57 --ctl_bar 1e-80`) | see below | **FAIL** |

**horizon_mp_check, exactly as printed:**

```
mpmath u series to order 1100 at u/sigma = 1.2 (sigma 0.25): last ten terms at most 3.37e-215
kernel u (ks 506) against mpmath at ks 506: 8.772e-120 (the u recurrence's arithmetic)
mpmath at ks 506 against ks 1100: 9.718e-108 (u's truncation)
kernel u (ks 506) against mpmath converged: 9.718e-108 (p, m, c: 9.72e-108, 3.98e-108, 6.58e-111)
kernel Moebius (a 8, ks 800) against mpmath converged: 4.647e-70 (p, m, c: 9.7e-71, 1.7e-70, 4.65e-70)
control (m_h + 1e-30 in the kernel only): 4.619e-28
control (mutate 57, the old split): 1.7e-60 (must exceed 1e-80)
  FAIL: Moebius against mpmath 4.65e-70 (bar 1e-100), the control 4.62e-28 (must exceed it), the split control 1.7e-60 (must exceed 1e-80); 5 nodes, x_l 0.7
```

The Moebius values sit 4.647e-70 from mpmath's converged u sum (bar 1e-100); both controls fire (4.62e-28, and the old split 1.7e-60 against its bar 1e-80), as the coordinator expected from dh610's run (4.65e-70, the same digits).
**D 2231 is not started** (the coordinator's order: if horizon_mp_check fails the same way, wait for the word that follows dh610's ks scan, expected about 21:15-21:30 UTC). Not tested here: that 4.65e-70 is the Moebius series' own truncation at ks 800 against the reference summed to order 1100.

## horizon_mp_check at ks 1600 (2026-11-26 21:12 UTC, coordinator's order after dh610's scan, raw ae3500937)

dh610's scan (`I1098-dh610/fastmul7_build/split300_scan.log`): at a 8 the gap to mpmath falls by about 1e16 per 200 orders (4.65e-70 at ks 800, 1.86e-86, 8.77e-103, 4.31e-119, 9.74e-129 at ks 1600), a 4 agrees (9.96e-129): the 4.65e-70 of the build's check was the Moebius series' truncation at ks 800, not arithmetic.
The same check on this build with `--ks_mob 1600` in place of 800 (`horizon_mp_ks1600.log`, started 21:09:26 UTC, one process beside the running jobs):

```
kernel Moebius (a 8, ks 1600) against mpmath converged: 9.742e-129 (p, m, c: 8.4e-129, 9.74e-129, 1.93e-130)
control (m_h + 1e-30 in the kernel only): 4.619e-28
control (mutate 57, the old split): 1.7e-60 (must exceed 1e-80)
PASS: Moebius against mpmath 9.74e-129 (bar 1e-100), the control 4.62e-28 (must exceed it), the split control 1.7e-60 (must exceed 1e-80); 5 nodes, x_l 0.7
```

**PASS**: 9.742e-129 against the bar 1e-100 (dh610: 9.74e-129), both controls above their bars. The u lines are as at ks 800 (kernel u against mpmath 8.772e-120, u truncation 9.718e-108). **fastmul7 is verified**: all seven checks pass (the ks 800 run's FAIL above is the truncation at ks 800).
