# T89-mac: sigma_20 (K 41) at wf 1.00 with J 1250 and J 1500 at 1280 bits, then wf 0.99 and 1.01 with J 1250

Machine: mac (Apple M5), 2 procs per run at nice 10, the choptuik-t83 checkout (origin/main 9e669de), `solver/inner_amp/amp_flint_par.py`.
Comms entry: 2026-10-28 21:06 UTC cloud to mac (follow-on after T91). Started 2026-10-29 02:01 UTC.

Settings: `amp_flint_par.py WF 41 J BITS --procs 2 --fit phys --mf 6:12 --fit-step 1`.
- `scan41J1250`: (a) J 1250 / 1280 bits (|sigma_19(d) - sigma_19(b)| = 1.94e-27 > 1e-27 in T91, so 1280 bits), wf 1.00, then wf 0.99 and 1.01 if its gate passes.
- `scan41J1500`: (b) J 1500 / 1280 bits, wf 1.00.
Gate for (a): err20 <= 1e-10 |sigma_20| and sigma_0..19 string-equal to T88-mac/scan39J1250/sigF_w1.0000_K39_J1250_p1280.json. Gate for (b): sigma_20 within (a)'s err20.

Restarted 2026-10-29 14:42 UTC after the Mac slept at 1% battery on 2026-10-29 09:51 UTC and booted at 14:24 UTC; each log keeps the killed attempt above a marker line.

Gate for (a) passed 2026-10-30 03:38 UTC (sigma_err_fit.py exit 0, err20 1.335e-29 = 7.18e-13 |sigma_20|; sigma_0..19 string-equal to T88-mac). Nodes wf 0.99 and 1.01 (J 1250 / 1280 bits, K 41) started 2026-10-30 03:38 UTC, files sigF_w0.9900_K41_J1250_p1280.json and sigF_w1.0100_K41_J1250_p1280.json.

(b) J 1500 / 1280 bits finished 2026-10-30 07:16 UTC (46758 s = 12.99 h). Gate (b) per ruling 2: sigma_20(b) - sigma_20(a) = 1.524e-31, within (a) err20 1.335e-29. Raw files in scan41J1500.

Nodes wf 0.99 and 1.01 (J 1250 / 1280 bits, K 41) done 2026-10-31 ~04:2x UTC (1460 min of the script clock each); err20 1.224e-29 and 1.455e-29.
