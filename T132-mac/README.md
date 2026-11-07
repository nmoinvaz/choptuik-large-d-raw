# T132-mac: where the low-D Taylor planner freezes, lowD_plan_probe at the M 320 base on the Mac

Machine: the Mac (Apple M5, NEON), run by the coordinator session, kernel from the octo-double build (Rust identical to
main's), main's Python at b8cde8d (the probe prints its base phases). 7 threads, nice 10, under caffeinate -i. The
laptop's run (T132-win) was stopped after 4 h inside the base's f64 Jacobian and LU, too slow there, not stuck by any
evidence. Procedure and criteria: notes/LOW_D.md 16.

  python3 lowD_plan_probe.py <raw> <raw>/T132-mac/probe --state T106-win2/pilot_M320_p1_N4/anm_lowd_D3.043750_M320.npz
    --targets 3.0425,3.043,3.0434 --N 3 --threads 7 --cap 900

Log probe.log; probe/ holds probe.jsonl, coeffs.npz and each case's plan trace.

Stopped 2026-11-07 01:20 UTC. The base's Jacobian and LU took 15989 s (pivots 4.3e-05..4.9e+01, as T115's on win2), but
z_1's GMRES diverged: |z_1| nan after 40 products (960 + 7515 s), with overflow warnings in multidouble's Python
double-double helpers. On win2 (T115) the same base gave |z_1| 1.410e+04 in 5 products. A discrepancy between this
Mac's build (the octo-double venv, NEON) and win2's at M 320, not yet explained; T135 on the laptop (x86) runs the same
probe at M 384.
