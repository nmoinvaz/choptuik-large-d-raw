# T153-macm3: amplitude coefficients at omega/omega_inf 1.08, 1.10, 1.12 (the second zero of S1)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0). Comms entry: 2026-11-07 16:37 UTC cloud to win2, macm3 (T153).

From solver/inner_amp/ with venv-macm3, the three at once, each 2 processes (6 threads in all), nice 10 under
caffeinate -i, each to w<wf>.log and sigF_w<wf>_K33_J1000.json (w<wf>.cmd has the exact line; exits.txt how each ended):
  amp_flint_par.py <wf> 33 1000 960 --procs 2 --fit phys --mf 6:12 --out <raw>/T153-macm3/sigF_w<wf>_K33_J1000.json
for wf = 1.08, 1.10, 1.12.
