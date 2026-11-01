# T94-win2: sigma_0..21 (K 43) at the nodes wf 0.99 and 1.01, J 1250 at 1280 bits, then the same nodes at J 1500: the sigma_21 campaign's node data

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores: 8 P + 12 E, 20 logical, no SMT; 95.6 GB RAM; always on AC, no battery). venv Python 3.12.8, python-flint 0.9.0, mpmath 1.3.0; shell PowerShell 5.1 (git bash also). Both nodes at once with `--procs 4` each at below-normal priority, checkout origin/main 7fde4a8, `solver/inner_amp/amp_flint_par.py`.
Comms entry: 2026-11-01 18:17 UTC cloud to win2.

Settings: `amp_flint_par.py WF 43 J 1280 --procs 4 --fit phys --mf 6:12 --fit-step 1`.
- `scan43J1250`: wf 0.99 and 1.01 at J 1250 / 1280 bits (K 43), both at once (95.6 GB RAM, the 64 GB+ rule).
- `scan43J1500`: follow-on, the same two nodes at J 1500 / 1280 bits (the hedge: they replace the J 1250 nodes if the wf 1.00 gate fails, otherwise recorded as context).
