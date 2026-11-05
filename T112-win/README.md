# T112-win: hp from main on multidouble 2.1.0, x86 build on win, bit identity checks

Worktree ..\choptuik-t112 at origin/main (612eb2d), venv venv-t112, `bash hp/build.sh`. One log per command, run from hp\ at 4 threads, below normal priority. Cloud task 2026-11-05 13:24 UTC.

Build: 13:26 to 14:18 UTC (52 min), exit 0, peak about 15.9 GB (sum of build-process working sets, the hpkernel rustc). build.log, build_time.txt.
Checks (run.sh, exits.txt): ref exit 0 (72 outputs bit-identical), scaled exit 0 (control fires), jets exit 1 (FAIL: 12 of 28 differ,
all 12 at M = 32; M = 48 and M = 64 outputs bit-identical to the Mac's), jets --mutate=kappa exit 1 (28 of 28 differ, the control).
Logs: highm_ref.log, highm_scaled.log, highm_jets.log, highm_jets_mutate_kappa.log.

Second jets check (cloud 18:55 UTC), the stored-plan reference anm-mac/jets_plans/jets_plans.json, main b1b844c0 highm_check.py, 2 threads:
jets_plans exit 1 (FAIL: 12 of 28 differ, again all at M = 32; M = 48 and 64 bit-identical), jets_plans_kappa exit 1 (28 of 28 differ, control).
Logs: jets_plans.log, jets_plans_kappa.log, run2.sh. With the Mac's plan given, jet_dd_n8_hi at M = 32 is unchanged (409e5906d12cf89d) and jet_dd_n8_lo changed (02e5e6919bf6c081 own plan, 64ad38f32a68762f given plan).

Third jets check (cloud 19:59 UTC), stored-input reference anm-mac/jets_inputs/jets_inputs.json, highm_check.py from main 5cbc0fa5, 2 threads: jets_inputs exit 0, PASS: 28 outputs bit-identical.
Inputs: M 32 DIFFERENT (this machine 21b5b25909166e13, the reference 710ec9904d60d5ac), M 48 same (3ea9b762941f6ae2), M 64 same (b517e36067313555). Log jets_inputs.log, run3.sh.
So the first two jets failures were the M 32 start state, resampled from the M 48 state with numpy; given the reference's input and plan, all 28 outputs are bit-identical.
