# T123-win: the fixed chain from T118's 152.93 state, cross-check against win2's T122

Cloud task 2026-11-06 03:48 UTC. 4 steps from T118-win2/chain/anm_pin3_D152.9309.npz, --reseed 2 --reseed_q 1, h_max 0.5, 4 threads, below normal, T112 build (hpkernel multidouble 2.1.0), anm_run.py, reseed.py and pinning.py from main 23d94488, Python multidouble 78efd7e. Command in t123.cmd, log chain.log, states and anm_run.jsonl in chain/.

Result (03:50 to 04:12 UTC, exit 0, 4 steps D 152.9309 to 154.9309, all at a = 0.5, re-seed ok at every step, qd 2 steps each, 22 min). States chain/anm_pin3_D153.4309 to D154.9309. Against win2's T122 (multidouble 3.2.0 build) the same four states differ: max |zh,zl,z2,z3 difference| 1.3e-27, 1.6e-26, 4.8e-26, 2.8e-20; Delta difference (formula of the 1e-20 check) 1.3e-27, 6.3e-27, 3.8e-26, 2.2e-22; not bit-identical.
