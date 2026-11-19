# I1003-dh610: the amplitude series at omega_inf to sigma_24 (K 49): the K 25 pilot at J 1250 (#638's follow-up)

Machine: dh610 (Fedora desktop, Linux 7.3, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1003

Code: worktree `~/Source/choptuik-large-d-1003` at origin/main ceba4ae9 (`solver/inner_amp/amp_flint_par.py`), Python 3.14.10 with python-flint 0.9.0 and mpmath 1.3.0 from
#967's `.venv` (`~/Source/choptuik-large-d-967/.venv`). The pilot: `python amp_flint_par.py 1.0 25 1250 1280 --procs 8 --fit phys --mf 6:12 --phys-prec 3840 --out I1003-dh610/pilot_K25_J1250.json`
(the coordinator's hc order of 2026-11-19 02:3x UTC, --procs 8 in place of 10 to leave room for #997's step 2), nice 10, 1 h cap (`timeout -s TERM 3600`).
Reference: `solver/inner_amp/scan45J1250/sigF_w1.0000_K45_J1250_p1280.json` (K 45, J 1250, prec 1280, `--fit phys --mf 6:12`, fit step 1, phys prec 3840).

| file | what |
|---|---|
| `run1003_pilot.sh`, `common1003.sh` | the pilot |
| `pilot_K25_J1250.log`, `pilot_K25_J1250.json` | its output |
| `pilot_K25_J1250_capped.log` | the K 25 pilot (first run, `run1003_pilot.sh`): capped at 3600 s at order 19, no JSON |
| `run1003_pilot_k17.sh`, `pilot_K17_J1250.log`, `.json` | the K 17 rerun (sigma_0..sigma_8), 1 h cap, --procs 8 |
| `compare1003.py` | the check against the K 45 file's `sigma_str` (1e-19), with its controls |
| `compare_K17.txt`, `compare_K17_controls.txt` | the K 17 pilot against the K 45 file (sigma_0..sigma_8, worst relative difference 0.0 over the 20-digit strings) and its two controls |
| `run1003_k49.sh`, `K49_J1250.log`, `sigF_w1.0000_K49_J1250_p1280.json` | the main run, K 49 at J 1250, --procs 12, 48 h cap (started 06:55:10 UTC); the JSON appears only at the end |
| `K49_J1250_procs12_stopped.log`, `memlog_k49_j1250_procs12.log` | the first K 49 J 1250 run at --procs 12 (06:55:10 to 07:42:35 UTC), stopped at order 23 by me for memory (see the issue) |
| `K49_J1250.log`, `memlog_k49_j1250.log` | the restart at --procs 5, 72 h cap (started 07:42:44 UTC) |
