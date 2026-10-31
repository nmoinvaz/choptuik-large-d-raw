# T93-mac: sigma_0..19 (K 39) at wf 0.995 and 1.005, J 1250 / 960 bits, the P5 type-bound test between the nodes

Machine: mac (Apple M5), 2 procs per run at nice 10, the choptuik-t83 checkout (origin/main 9e669de), `solver/inner_amp/amp_flint_par.py`.
Comms entry: 2026-10-29 02:16 UTC cloud to mac (follow-on after T89's nodes). Started 2026-10-31 04:31 UTC.

Settings: `amp_flint_par.py WF 39 1250 960 --procs 2 --fit phys --mf 6:12 --fit-step 1`, files `scan39J1250p960/sigF_w0.9950_K39_J1250_p960.json` and `sigF_w1.0050_K39_J1250_p960.json`.
No gate (finite errs, no companion needed; the bound test needs 1e-6).
