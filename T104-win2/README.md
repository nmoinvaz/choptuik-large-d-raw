# T104-win2: the K = 22 stages of the sigma_22 campaign, planted_k22.py on win2

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores: 8 P + 12 E, no SMT, AVX2; 95.6 GB RAM; on AC). venv choptuik-venv: Python 3.12.8, python-flint 0.9.0, mpmath 1.3.0. Single-process mpmath, normal priority, all cores. Run from `solver\inner_amp` of the main checkout (origin/main), with the J 1500 wf 1.00 pilot `sigF_w1.0000_K45_J1500_p1280.json` copied into `solver\inner_amp\scan45J1500`.
Comms entry: 2026-11-04 00:15 UTC cloud to win2.

Stages, each run to completion before the next (logs here): converge, plants, real, ring, calib, recomplete, project, combine, table. Stop if a stage exits non-zero (post the stage, exit code, last 40 lines; no rerun/edit) or the process exceeds 10 GB. The stage records `planted_results_k22.jsonl` and `planted_checks_k22.json` (written into solver\inner_amp) and the copied pilot go to the code repo on branch `wip/k22-win2`, never main.
