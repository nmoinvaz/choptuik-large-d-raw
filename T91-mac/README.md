# T91-mac: sigma_19 (K 39) at wf 1.00 with J 1250 / 960 bits, the J-or-bits attribution of T88's pilot (b) gate failure

Machine: mac (Apple M5), python-flint 0.9.0, 2 worker processes at nice 10.
Task: T91, comms entry "cloud to mac" of 2026-10-28 21:06 UTC. Source: `solver/inner_amp/` of origin/main 9e669de (worktree `choptuik-t83`).

Command (from `solver/inner_amp`), pilot (d): (a)'s bits with (b)'s J. A measurement, no gate:

    amp_flint_par.py 1.0 39 1250 960 --procs 2 --fit phys --mf 6:12 --fit-step 1 --out scan39J1250p960/sigF_w1.0000_K39_J1250_p960.json
