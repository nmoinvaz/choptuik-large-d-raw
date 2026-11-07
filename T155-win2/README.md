# T155-win2: amplitude coefficients at omega/omega_inf 1.06, 1.09, 1.11, 1.14 (the second zero of S1)

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at origin/main e743608 (Python only
past 79d3e84; no hp build needed). venv-t126, python-flint 0.9.0 (installed for this task; was absent). The four runs at
once, 4 processes each (16 worker processes, 1 thread each), below normal. Comms entry: 2026-11-07 18:04 UTC cloud to win2.

These bracket macm3's T153 nodes (1.08, 1.10, 1.12) around the candidate second zero of the harmonic-1 Stokes
multiplier S1 near omega/omega_inf = 1.10.

From solver\inner_amp\, each to w<wf>.log with its JSON to sigF_w<wf>_K33_J1000.json:
  amp_flint_par.py <wf> 33 1000 960 --procs 4 --fit phys --mf 6:12 --out <raw>\T155-win2\sigF_w<wf>_K33_J1000.json
  wf = 1.06, 1.09, 1.11, 1.14.
About 7 CPU-h each, ~2 h wall. Launched 2026-11-07 18:09:46 UTC. Post per run (wall time and the last order's sigma_err).
