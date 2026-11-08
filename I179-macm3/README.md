# I179-macm3: macm3 moved to Python 3.14 (venv, hp build, checks)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/179. Main 9286b05b.

Interpreter: uv is not installed on macm3, so the coordinator's fallback (b) applies: Homebrew's existing python@3.14 3.14.3_1 (/opt/homebrew/bin/python3.14, Python 3.14.3, Clang 17.0.0,
not free-threaded), which is a dependency of llvm, mlx, mlx-c and ollama. Brew is not upgraded and nothing in it is changed (coordinator, 2026-11-08). So the patch level is 3.14.3 where win2's venv-t177 is
3.14.10, and "newest 3.14.x" is not met; recorded in the posts. The environment is ~/Source/venv-macm3-314 beside ~/Source/venv-macm3 (3.13.3).

`run_i179.sh` (plain steps): venv, pins, pip freeze of both venvs, `pip uninstall multidouble`, hp/build.sh with the venv active (CARGO_PROFILE_RELEASE_LTO=false and CODEGEN_UNITS=16 for 24 GB, as in T133), then the checks.
Each exit and wall time is in exits.txt, each command in its own log's first line.

Written before the run. Pass criteria (any miss stops the switch and is reported, not fixed):
  1. The pins equal the 3.13 venv's: python-flint 0.9.0, mpmath 1.3.0, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, maturin 1.16.0 (freeze_*.txt, diff_freeze.txt shows only the hpkernel wheel's cp tag).
  2. hp/build.sh exits 0 and the final line prints hpkernel neon and multidouble neon (the isa of T133's build).
  3. python3 check_numbers.py --selftest exits 0 (its mutation controls fire inside it).
  4. The amplitude copy (amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12) hashes fd6b5ef2f90d4f559a1a1ab68a7e85fe7c9b8538cc7e50ac41d2fb5510eb47d8 (#161's compare_amp.py rule, adapted), and its changed-digit control differs.
  5. highm_check.py ref --compare=T81/ref_main.json --Ms=48,64,80 exits 0 (72 outputs bit-identical, T133); scaled --compare=T81/scaled_main.json exits 0 with its control firing; jets
     --compare=anm-mac/jets_inputs/jets_inputs.json exits 0 (28 outputs bit-identical); jets --mutate=kappa exits 1 (28 of 28 differ, the control). Commands as T133's, from hp/, --threads=4.

Attempt 1 (20:53 to 21:29 UTC; logs kept as attempt1_*): venv, pins and the amplitude copy ran. hp/build.sh compiled the cp314 wheel (cargo 15m09s, peak 10.9 GB) and then failed:
`pip install ... dist/hpkernel-0.1.0-*.whl` also matched the stale cp313 wheel of the 3.13 build in hp/dist ("not a supported wheel on this platform"), so hpkernel was not installed and
check_numbers --selftest and the three highm_check runs failed on `No module named 'hpkernel'` (exit 1). The amplitude copy does not use hpkernel: exit 0, hash equal (compare_amp.txt).
Attempt 2 (run_i179_b.sh): the stale wheel is moved (not deleted) from the ignored hp/dist to ~/Source/hp-dist-stale-cp313/, then hp/build.sh again as written and the checks. No code changed.

Results (macm3, main 9286b05b, Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0; awake.log: attempt 2 awake = wall (1159 s); attempt 1 had 870 s asleep (a clamshell sleep and maintenance sleeps from 12:54 to 13:11 PST, inside its hp/build.sh), 1293 s awake. run_i179.sh and run_i179_b.sh did not use caffeinate (my omission, the earlier tasks' scripts did), so the lid closing slept the Mac. Sleep changes no result, only wall times: cargo's own "15m 09s" is awake time and the build's wall 1774 s includes the sleep).
  Attempt 2 (21:31:48 to 21:51:07 UTC): hp/build.sh exit 0 in 18 s (cargo reused attempt 1's 15m09s compile; maturin built the cp314 wheel, multidouble 0.1.0 at git f092018 built as cp314), last line
  "hpkernel neon multidouble neon" (as T133's build). freeze_venv-macm3-314_after_build.txt has the two added packages. build_time.txt is attempt 2's; attempt1_build_time.txt: peak 10.9 GB.
  amplitude copy (attempt 1, exit 0, 343 s): hash fd6b5ef2f90d4f559a1a1ab68a7e85fe7c9b8538cc7e50ac41d2fb5510eb47d8 EQUAL to win2's six copies and macm3's 3.13 run (#161); changed-digit control differs (compare_amp.txt).
  highm_check ref --compare=T81/ref_main.json --Ms=48,64,80: exit 0, PASS 72 outputs bit-identical (74 s).
  scaled --compare=T81/scaled_main.json: exit 0, PASS, control (scale wrong at order 7, M 192) fires (818 s).
  jets --compare=anm-mac/jets_inputs/jets_inputs.json: exit 0, PASS 28 outputs bit-identical (118 s); with --mutate=kappa: exit 1, FAIL 28 of 28 differ, the control (118 s).
  check_numbers.py --selftest: exit 1, 1040 of 1043 checks pass, and all 1043 reject a value shifted by one unit. The three failures are formula_refit (README "The formula"): refit within 1e-9 of the stored Delta
  on 4-30.2, within 1e-8 of the stored gamma, and Delta(80) moved between 0.5e-7 and 2e-7. The same three fail on Python 3.13.3 (check_numbers_selftest_py313.log, venv-macm3), and formula_all.refit_distance() returns the same
  values to every digit on both (formula_refit_values.txt): delta_fit_range 9.29e-09 (limit 1e-9), gamma_fit_range 1.72e-08 (limit 1e-8), delta_80 3.21e-07 (limit 2e-7). So not caused by 3.14; a failure of the check at
  this main (9286b05b) on this machine, reported not fixed.
