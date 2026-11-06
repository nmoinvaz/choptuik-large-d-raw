# T129-win2: the chain to D 200 in octo-double

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2; 95.6 GB RAM). Worktree `..\choptuik-t126` at origin/main
4eac02b (the T126 octo-double build, multidouble 4.0.0; 4eac02b has the ba1637c re-seed guard; no pull or rebuild).
venv-t126. 18 threads, below normal. Comms entry: 2026-11-06 08:23 UTC cloud to win2 (the switch to octo-double).

The switch decision: T128 showed the octo-double series stays healthy where quad-double collapses, and at D 171.77 /
172.27 the octo pilot's Delta matched chain2's in all 21 printed digits while its prediction moved ~1e-20 vs quad's
~1e-9. The octo a_max ~2.07 puts the truncation term at a step of 1.0 near 1e-21 of |z_1|, so the octo chain takes
h_max 1.0 (half the series cost per unit of D vs h_max 0.5).

Start from T127-win2/chain2/anm_pin3_D175.5246.npz as written (not chain2's last state D 176.7746), because the Mac's
second path T130 (h_max 0.5) starts there too and every other of its points lands on T129's D values.

  anm_run.py <raw> T129-win2\chain --state T127-win2/chain2/anm_pin3_D175.5246.npz --kfreeze 3 --N 24 --eps 1e-14
    --h_max 1.0 --steps 300 --D_max 200 --threads 18 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_o 1
    --reseed 2 --reseed_q 1
Log T129-win2\chain.log. Post after the first two steps (series seconds at 18 threads vs T128's 694 s at 6, accepted a,
re-seed, qd steps, max |F|, Delta), then hourly. Stop at D_max 200, on a degenerate series, when two steps in a row
need a of 0.125 or less, or after 10 h. Push T129-win2/ at each post.

chain reached D 188.0246 cleanly in 13 full a=1.0 steps (series healthy, a_max ~2.06, re-seed 12 ok / 3 failed), then
the step above it hung: the a 1.0 re-seed failed at rung u 0.15 (double-double floor now ~1e-19), the kept prediction's
horizon was off by the mass-mode gain (~1.8e26), and each corrector projection ran a full single-core quad-double
polish (py-spy: Reseeder.integrate via ElimQ.newton_q inside newton_qd), ~1 h per a=1.0 attempt. hung above D 188.0246,
killed at 2026-11-06 11:21 UTC for chain2.

chain2/ restarts from chain/anm_pin3_D188.0246.npz with h_max 0.5 (a=1.0 overshoots here; a=0.5 lets the warm
projection work) plus --save_pred 1. 18 threads. Steps of 0.5 from 188.0246 land on the Mac's T130 points. Stop at
D_max 200, after 3 restarts, or after 8 h. New hang rule: if the log gains no line for 20 min while one core is busy,
take one py-spy dump, kill the tree, restart from the last state with h_max halved (0.25, then 0.125), and post.

chain2 climbed cleanly to D 193.7746 (no hang), then self-stopped at three halvings: the next step failed at a 0.5,
0.25, 0.125, 0.0625, each "no trial step accepted", the kept prediction's double-double |F| ~3.4e-02 (the octo wall at
condition ~1.4e27). Last clean Delta 1.69752838546306850.

chain3/ is the next restart (restart 2 of the 3-restart budget) from chain2/anm_pin3_D193.7746.npz with h_max 0.25
(0.03125 floor), the rest as chain2 (--save_pred 1, 18 threads). Per the coordinator's restart ladder (0.25, then
0.125). chain3 broke through to D 194.2746 at a=0.25, but was superseded: the coordinator diagnosed the D 193.77 stop
as the quad-double corrector stalling at max|F| ~1.0-1.1e-28 against tol_qd 1e-28 (a precision floor that rises with D),
not a step-size problem. stopped at 2026-11-06 13:36 UTC for chain4.

chain4/ restarts from chain2/anm_pin3_D193.7746.npz (realigned to the Mac T130 grid) on fc636e7 (Python-only past
4eac02b, no rebuild) with --accept_stall_qd 1e-24 (d898c15: accepts a quad-double stall below the given level, so the
~1e-28 floor no longer blocks), h_max back to 0.5, D_max 1000 (Nathan wants the chain as far as it can go). 18 threads,
--save_pred 1. Stop on its own three-halvings stop, a degenerate series, or after 12 h; the hang rule stands with a
fresh 3-restart budget. Per post: D, steps, halvings, re-seed ok/failed, stalls accepted ("quad-double stall at max|F|
... accepted") with the largest accepted max|F|, and Delta; flag if the largest accepted max|F| passes 1e-26 (floor
then two orders from the 1e-24 level, octo-double corrector takes over).
