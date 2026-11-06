# T132-mac: where the low-D Taylor planner freezes, lowD_plan_probe at the M 320 base on the Mac

Machine: the Mac (Apple M5, NEON), run by the coordinator session, kernel from the octo-double build (Rust identical to
main's), main's Python at b8cde8d (the probe prints its base phases). 7 threads, nice 10, under caffeinate -i. The
laptop's run (T132-win) was stopped after 4 h inside the base's f64 Jacobian and LU, too slow there, not stuck by any
evidence. Procedure and criteria: notes/LOW_D.md 16.

  python3 lowD_plan_probe.py <raw> <raw>/T132-mac/probe --state T106-win2/pilot_M320_p1_N4/anm_lowd_D3.043750_M320.npz
    --targets 3.0425,3.043,3.0434 --N 3 --threads 7 --cap 900

Log probe.log; probe/ holds probe.jsonl, coeffs.npz and each case's plan trace.
