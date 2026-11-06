# T124-win: a second path past 153, steps of 0.25, for the error column of the new chain rows

Cloud task 2026-11-06 04:18 UTC. From T118-win2/chain/anm_pin3_D152.9309.npz, --reseed 2 --reseed_q 1, h_max 0.25, steps 300, D_max 200, 4 threads, below normal, same build as T123 (T112 hpkernel multidouble 2.1.0, anm_run.py, reseed.py, pinning.py from main 23d94488, Python multidouble 78efd7e). Command in t124.cmd, log chain.log, states and anm_run.jsonl in chain/. Stop after 6 h (about 10:25 UTC) or when T122 is past 200 and T124 past 170, or on a degenerate series.

Stopped at D 153.4309 (last saved state chain/anm_pin3_D153.4309.npz; step 1 at D 153.18 was running) for the T125 rebuild, cloud 04:27 UTC entry. Process tree killed 04:3x UTC.

Resumed 2026-11-06 05:55 UTC on the T125 build (t124b.cmd) from chain/anm_pin3_D153.4309.npz. Reached D 161.9309 (step 35, last saved state chain/anm_pin3_D161.9309.npz), stopped by win at 10:15 UTC for T131: from D 161.4 the steps took 16-29 min each (qd steps 9, then halvings 0.25 -> 0.125, failed re-seeds with the old polish), the 162.3 wall T122 hit.
