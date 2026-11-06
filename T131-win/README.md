# T131-win: quad-double second path over D 162.8-175.6 on win, for the error column of T127's rows

Cloud task 2026-11-06 08:23 UTC. Two segments in turn, both on T127's points so the 0.25 steps land on its D values: A from T127-win2/chain/anm_pin3_D162.8059.npz to D_max 169.9 (chainA, chainA.log), B from T127-win2/chain/anm_pin3_D170.2746.npz to D_max 175.6 (chainB, chainB.log). Flags of T124: --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.25 --steps 300 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1, below normal. Command in t131.cmd. Stop a segment at its D_max, on a degenerate series, or after 4 h.

Build: T125 (hpkernel on multidouble 3.2.0, quad-double only), choptuik-t125 checked out at origin/main 266a4108 (reseed.py with the 5423d2b polish and the ba1637c guard, anm_run.py from main), venv-t125. No rebuild.

Segment B not run, for T132 (cloud 2026-11-06 13:59 UTC): I killed the batch parent while segment A was at D 169.31 so B did not start; segment A (python) ran on to its D_max.
