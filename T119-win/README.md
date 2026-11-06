# T119-win: plain against elimination corrector at T116's D 149.96 stop

Cloud task 2026-11-06 02:18 UTC. One step each from T116-win2/chain/anm_pin3_D149.9621.npz, h_max 0.5, one after the other, 4 threads, below normal, T112 build (hpkernel multidouble 2.1.0) with anm_run.py, reseed.py and pinning.py from main 48adb33b and the Python multidouble at 78efd7e. plain.log is the plain corrector, elim.log adds --reseed 2 --reseed_q 1. Commands in t119.cmd.

Result (02:20 to 02:58 UTC, both exit 0): plain failed at a = 0.5, 0.25, 0.125, 0.0625 (qd 12, 12, 10, 5 steps, max |F| 1.8e-12, 1.2e-12, 7.0e-13, 3.6e-13, none converged, 667, 551, 368, 182 s), "stopped: no convergence after three halvings". elim converged at a = 0.5 at the first attempt (re-seed ok, ladder 1, failed 0, qd 3 steps, max |F| 2.3e-37, 46 s). No state saved by plain.
