# T153-macm3: amplitude coefficients at omega/omega_inf 1.08, 1.10, 1.12 (the second zero of S1)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0). Comms entry: 2026-11-07 16:37 UTC cloud to win2, macm3 (T153).

From solver/inner_amp/ with venv-macm3, the three at once, each 2 processes (6 threads in all), nice 10 under
caffeinate -i, each to w<wf>.log and sigF_w<wf>_K33_J1000.json (w<wf>.cmd has the exact line; exits.txt how each ended):
  amp_flint_par.py <wf> 33 1000 960 --procs 2 --fit phys --mf 6:12 --out <raw>/T153-macm3/sigF_w<wf>_K33_J1000.json
for wf = 1.08, 1.10, 1.12.

All three ended with exit 0 at k 33, started 17:11:11 UTC: 1.10 at 20:41:08 (12597 s), 1.12 at 20:41:12 (12601 s), 1.08
at 20:46:12 (12901 s). Last order's sigma_err (a spread over fit choices): 1.08 1.11e-26, 1.10 1.32e-26, 1.12 1.58e-26.
Comms 2026-11-07 20:35 UTC made this task issue #3 (https://github.com/nmoinvaz/choptuik-large-d/issues/3).
