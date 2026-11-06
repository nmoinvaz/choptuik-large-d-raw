# T125-win: hp from main on multidouble 3.2.0, x86 build on win, bit identity checks

Worktree ..\choptuik-t125 at origin/main (7db6e118), venv venv-t125 (pip 26.3, numpy 2.2.6, scipy 1.15.3, mpmath 1.4.1, maturin 1.16.0), `bash hp/build.sh`, detached, below normal, 4 cargo jobs. Cloud task 2026-11-06 04:27 UTC; replaces the T112 build (multidouble 2.1.0), which stays in ..\choptuik-t112. One log per command, run from hp\ at 4 threads, below normal.

Results (2026-11-06): build exit 0, 04:30:10 to 05:29:11 UTC (59 min), sum of peak working sets 16.84 GB (build_peak.txt), min free physical 2.1 GB. Checks (run.sh, exits.txt): highm_ref 0, highm_scaled 0, highm_jets (jets_inputs.json) 0, highm_jets --mutate=kappa 1, all as expected. T124 resumed on this build from T124-win/chain/anm_pin3_D153.4309.npz at 05:55 UTC (T124-win/t124b.cmd).
