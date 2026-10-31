# T94-mac: sigma_0..21 (K 43) at wf 1.00, J 1250 and J 1500 at 1280 bits, then the nodes 0.99 and 1.01 at J 1250: the sigma_21 campaign

Machine: mac (Apple M5), 2 procs per run at nice 10, the choptuik-t83 checkout (origin/main 9e669de), `solver/inner_amp/amp_flint_par.py`.
Comms entry: 2026-10-31 05:27 UTC cloud to mac (follow-on after T93), released by the 11:20 UTC entry. Started 2026-10-31 11:21 UTC.

Settings: `amp_flint_par.py WF 43 J 1280 --procs 2 --fit phys --mf 6:12 --fit-step 1`.
- `scan43J1250`: (a) J 1250 / 1280 bits, wf 1.00, then wf 0.99 and 1.01 if its gate passes.
- `scan43J1500`: (b) J 1500 / 1280 bits, wf 1.00.
Gate for (a): sigma_err_fit.py exit 0 (err21 <= 1e-10 |sigma_21|, --a1-from scan39J1000/sigF_w1.0000_K39_J1000_p960.json) and sigma_0..20 string-equal to T89-mac/scan41J1250/sigF_w1.0000_K41_J1250_p1280.json. Ruling 2 for (b) as in T89.
