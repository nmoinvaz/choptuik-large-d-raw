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
