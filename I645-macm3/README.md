# I645-macm3: does a continuation start carry the full system past D 78?

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (hpkernel cp314 neon of 2026-11-09, the kernel win used for #642; quad double), worktree ~/Source/choptuik-large-d-b640 at main 9839474. R is a worktree of the raw repository, ~/Source/choptuik-large-d-raw-641 (up to date, holds I642-win and T138-win2; this folder is pushed from it). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/645 (recommended by #642; queued for macm3 by the coordinator's message of 2026-11-13 06:54 UTC, after #641). Started 11:19 UTC.

Command (run_to78.sh), from hp/, OPENBLAS_NUM_THREADS=1, nice 10, caffeinate -is: python3 -u scan_qd.py R/I645-macm3/to78/scan.jsonl R/I642-win/released_kf13_D77.0000.npz 78 --history R/I642-win/released_kf13_D74.0000.npz,R/I642-win/released_kf13_D75.0000.npz,R/I642-win/released_kf13_D76.0000.npz --kfreeze 13 --dD 0.05 --threads 4 --tag full. If it reaches 78: the same to 79 with the last four converged states of step 1 (start = the D 78 state, history the three before it), then to 80 from step 2's last four.

Written before the run (the issue's). Control: scan_qd re-converges each input state at its own D first and writes it to OUT; those four Delta must equal I642-win/release.jsonl's Delta_full at 74-77 within 1e-25, and the comparison must fail against Delta_start (the held Delta, 4.6e-16 to 4.1e-15 off); both verdicts recorded. Stop when step 1 stops short of 78 (scan_qd stops by itself below --dD_min 1e-4): report the last converged D, its |F|, the attempts file's last ten rows and what the Newton steps did (the first step's |F|). Report: a table of D, converged, |F|, Newton steps, Delta_full - Delta_held at each integer D reached (Delta_held the held chain state's Delta, the sum of the last entries of its parts as release_held.py's delta_of); the control's two verdicts; the last D reached. Acceptance: the two control verdicts; every reported Delta_full from a point with |F| <= 1e-44; the frontier stated as the last converged D. About 1 h.

## Results (11:32 UTC; exits.txt: to78 exit 1 at 11:31:19 UTC, 11:25 start)

Control (the four re-converged inputs the scan wrote, to78/full_D7x.000000.npz, against I642-win/release.jsonl): Delta equals Delta_full to 3.2e-40, 3.9e-40, 1.8e-40, 2.1e-40 at D 74 to 77 (limit 1e-25: pass) and differs from Delta_start by 4.62e-16, 1.25e-15, 2.43e-15, 4.06e-15 (the comparison fails against the held Delta, as it must).

Step 1 stopped at D 77.0 (scan_qd: dD below 1e-4), last converged D = 77.0 (the re-converged input, |F| 1.33e-52). The attempts file's last ten rows (to78/attempts_last10.md):

| D | converged | Newton steps | first Newton step: \|F\| (after the predictor) | first step's \|dz\| | trial accepted | \|F\| at the end | seconds |
|---|---|---|---|---|---|---|---|
| 77.000000 | True | 2 | 6.90e-36 | 6.9e-36 | yes | 1.33e-52 | 14.4 |
| 77.050000 | False | 1 | 2.20e+08 | 4.5e+08 | no (no trial step accepted) | 2.20e+08 | 72.9 |
| 77.025000 | False | 1 | 7.74e+06 | 6.4e+05 | no (no trial step accepted) | 7.74e+06 | 74.3 |
| 77.012500 | False | 1 | 2.39e+05 | 4.8e+03 | no (no trial step accepted) | 2.39e+05 | 75.0 |
| 77.006250 | False | 1 | 6.95e+03 | 1.3e+03 | no (no trial step accepted) | 6.95e+03 | 75.6 |
| 77.003125 | False | 1 | 2.09e+02 | 4.6e+05 | no (no trial step accepted) | 2.09e+02 | 74.7 |
| 77.001563 | False | 1 | 6.83e+00 | 9.8e+02 | no (no trial step accepted) | 6.83e+00 | 75.5 |
| 77.000781 | False | 1 | 5.20e-01 | 1.7e+02 | no (no trial step accepted) | 5.20e-01 | 76.1 |
| 77.000391 | False | 1 | 1.65e-01 | 8.0e+01 | no (no trial step accepted) | 1.65e-01 | 76.5 |
| 77.000195 | False | 1 | 8.24e-02 | 5.2e+01 | no (no trial step accepted) | 8.24e-02 | 76.3 |

Every attempt from D 77: one Newton step, no trial step accepted, so |F| at the end is the predictor's. Steps 2 (to 79) and 3 (to 80) were not run: step 1 stopped short of 78.
