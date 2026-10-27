# T83-mac: sigma_16, the 16th inner amplitude coefficient, K 33

Machine: mac (Apple M5), python-flint 0.9.0, 2 worker processes per run at nice 10.
Task: T83, comms entry "cloud to mac" of 2026-10-27 14:25 UTC. Source: `solver/inner_amp/` of origin/main ef124c0 (worktree `choptuik-t83`).

Command (from `solver/inner_amp`, wf 1.00 pilot):

    amp_flint_par.py 1.0 33 J BITS --procs 2 --fit phys --mf 6:12 --fit-step 1 --out <file>

- `scan33J1000/`: J 1000 at 960 bits. The wf 1.00 pilot (a), wf 0.99 and wf 1.01. Logs `w<wf>.log`.
- `scan33J1250/`: J 1250 at 1280 bits, wf 1.00 pilot (b) only. Its sigma_err is inf (family 1_1 fit error inf at Mf 12), so it fails the err16 gate; its sigma agrees with (a) to 2.7e-26.

wf 0.99 and 1.01 (variant (a), same command with the wf in the first argument) finished 2026-10-27 22:02 UTC, rc 0, 160 min each, so this folder is complete.
