# T97-win: sigma_0..21 (K 43) at wf 1.00, J 1250 at 1280 bits, on win: the second-machine replica of the Mac's pilot (a)

Machine: win, a Surface Laptop 4 (Intel Core i7-1185G7, 4 cores, 8 logical threads, 31.8 GB), Windows 11, Python 3.10.0, python-flint 0.9.0, mpmath 1.3.0 (the system interpreter, not a venv).
The task: the cloud's comms.txt entry of 2026-11-01 21:21 UTC to win ("T97, the second-machine replica of the Mac's pilot (a)"), run from the code
repository at origin/main 1cf2d1a (a worktree beside this clone), from solver/inner_amp at below-normal priority with --procs 2:

    python -u amp_flint_par.py 1.0 43 1250 1280 --procs 2 --fit phys --mf 6:12 --fit-step 1 --out ..\..\..\choptuik-large-d-raw\T97-win\scan43J1250\sigF_w1.0000_K43_J1250_p1280.json >> ..\..\..\choptuik-large-d-raw\T97-win\scan43J1250\w1.0000.log 2>&1

The control is solver/inner_amp/log_compare.py against T94-mac/scan43J1250/w1.0000.log (every common order must be identical). The laptop can sleep, which stretches the wall time;
each post names the awake time since the previous one.
