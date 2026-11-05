# T112-win: hp from main on multidouble 2.1.0, x86 build on win, bit identity checks

Worktree ..\choptuik-t112 at origin/main (612eb2d), venv venv-t112, `bash hp/build.sh`. One log per command, run from hp\ at 4 threads, below normal priority. Cloud task 2026-11-05 13:24 UTC.

Build: 13:26 to 14:18 UTC (52 min), exit 0, peak about 15.9 GB (sum of build-process working sets, the hpkernel rustc). build.log, build_time.txt.
Checks (run.sh, exits.txt): ref exit 0 (72 outputs bit-identical), scaled exit 0 (control fires), jets exit 1 (FAIL: 12 of 28 differ,
all 12 at M = 32; M = 48 and M = 64 outputs bit-identical to the Mac's), jets --mutate=kappa exit 1 (28 of 28 differ, the control).
Logs: highm_ref.log, highm_scaled.log, highm_jets.log, highm_jets_mutate_kappa.log.
