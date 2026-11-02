# T99-win2: sigma_0..22 (K 45) at wf 0.99, 1.00, 1.01, J 1250 at 1280 bits, with the pilot (b) and the nodes at J 1500: the sigma_22 campaign

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores: 8 P + 12 E, no SMT, AVX2; 95.6 GB RAM; on AC). venv choptuik-venv: Python 3.12.8, python-flint 0.9.0, mpmath 1.3.0. Below-normal priority, run beside T100 (6 threads). `solver/inner_amp/amp_flint_par.py`, main checkout origin/main 87099ba.
Comms entry: 2026-11-02 22:34 UTC cloud to win2.

Settings: `amp_flint_par.py WF 45 J 1280 --procs P --fit phys --mf 6:12 --fit-step 1`.
- Stage 1, four runs at once at `--procs 3`: wf 1.00, 0.99, 1.01 at J 1250 (`scan45J1250`), and the pilot (b) wf 1.00 at J 1500 (`scan45J1500`). Memory guard on (b) only (`util_report.py --guard 10`, log `scan45J1500/mem_guard.log`).
- Stage 2, when stage 1 ends: the wf 0.99 and 1.01 nodes at J 1500, `--procs 4`, into `scan45J1500`.
- Machine control (K does not enter below the top order, so every common order up to 43 must be identical): J 1250 wf 1.00 vs T94-mac/scan43J1250/w1.0000.log, wf 0.99 and 1.01 vs T94-win2/scan43J1250, J 1500 wf 1.00 vs T94-mac/scan43J1500/w1.0000.log.
