# I1009-dh610: cache-ordered f64 Jacobian fill, x86 checks and timings on one Linux build (hp perf/cauchy-cache-chunks 76fdcbc9)

Machine: dh610 (Fedora desktop, Linux 7.3, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1009 (moved here from dh170, whose 31 GB could not hold the build).

New worktree `~/Source/choptuik-large-d-ccc` at 76fdcbc9 (detached) and new venv `~/Source/venv-ccc` (uv, Python 3.14, seeded with pip), so that nothing the #1003 K 49 run imports
(`~/Source/choptuik-large-d-1003`, `~/Source/choptuik-large-d-967/.venv`) is touched. The K 49 run shares the machine (12 procs), so absolute seconds below are loaded;
only the two forms' ratio within one binary is reported.

Build: low-memory recipe (`CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`), `CARGO_BUILD_JOBS=6`, nice 10, as a user unit with `MemoryMax=30G` (raised to 36G at 07:11 UTC)
(a cgroup OOM kills only the build) and a watchdog that stops that unit when MemAvailable falls below 4 GB (the coordinator's rule; the issue says 2 GB).

| file | what |
|---|---|
| `common1009.sh`, `build1009.sh`, `watch1009.sh` | paths, the build, the watchdog and the per-minute memory sample (including the K 49 run's total RSS) |
| `checks1009.sh`, `cols_native1009.sh`, `summary_checks.txt` and the logs `cols_test.log` (no RUSTFLAGS: multidouble's Sse2 backend), `cols_test_native.log` (target-cpu=native: Avx2), `highm_ref.log`, `highm_scaled.log`, `highm_jets.log`, `highm_jets_kappa.log` | step 4, the bit checks |
| `timings1009.sh`, `summary_timings.txt`, `dump_ctx.log`, `bench_compile.log`, `bench_fill_T1.log`, `bench_fill_T4.log` | step 5 (`ctx320.bin`, the 2.1 MB input, is not committed) |
| `multidouble1009.sh`, `multidouble_bench1009.sh`, `summary_multidouble.txt`, `md_f64_matrix_{native,portable}.log`, `md_bench_dmat_f64*.log` | step 6, with the failed bench attempts' logs |
