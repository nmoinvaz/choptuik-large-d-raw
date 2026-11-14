# I375-dh370: the real DSS's imaginary-sector det M in double-double at D 30.07, 45.05, 60.00 (#375)

Machine dh370 (Fedora 45, i7-8700, 6 cores, 12 threads, 31 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/375.

Code: worktree `choptuik-i375` (detached) at origin/wip/xf-checks 38c2fbee, `solver/matter/run_i375.sh` (sha1 ec0ac2c0), the venv of
`choptuik-large-d-614` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0), pure Python, no hp kernel. Started as the user unit
`i375` (`systemd-run --user`, under `systemd-inhibit`) from `solver/matter/`:

    PY=/home/nathan/Source/choptuik-large-d-614/.venv/bin/python bash run_i375.sh /home/nathan/Source/choptuik-large-d-raw/I375-dh370

The script runs the selftests (`selftests.log`), then phase 1 with 12 processes at nice 10 (per D: `tolscan` at tol 1e-12 and 1e-14, and the
box counts B0, U0 and FULL), then phase 2 with 6 processes (the planted pair in FULL and the mutated coupling in B0). One process per thread,
`OPENBLAS_NUM_THREADS=1`. The runner (dh370) runs the commands and does not read the results into a summary, xfchecks does.

## Ended (dh370)

Unit `i375` ran 2026-11-14 10:51:50 to 13:34:39 UTC (2 h 43 min), `Result=success`, `ExecMainStatus=0`, no Traceback in any log. `selftests.log`:
ddnp selftest exit 0, its control (`--mutate=twoprod`) exit 1 (must be 1), complex_imag_dd selftest exit 0, "phase 1 done 13:09:55 UTC",
"phase 2 done 13:34:39 UTC". Phase 1's `tolscan` runs ended about 11:24 to 11:28 UTC, the B0 counts 12:11 to 12:17, the U0 counts 12:36 to
12:37, the FULL counts 13:05 to 13:10. Phase 2 (the planted pair in FULL, the mutated coupling in B0) ended 13:10 to 13:34. Files: one
`tolscan_*` pair per D, `count_*_{B0,U0,FULL}`, `count_*_FULL_plant`, `count_*_B0_coupling` (each `.log` and `.jsonl`), and the evaluation
logs `evals_*` (the plant reuses FULL's). The results are not read here, xfchecks reads them on the Mac.
