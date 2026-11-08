# I19-win2: chain_fit crawled past D 215 in small octo-double steps

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at origin/main e743608 (octo-double
build, Python only, no rebuild). venv-t126. 18 threads, below normal. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/19

T150 showed the D 215 wall: the octo corrector plateaus near |F| ~3e-20 with "no trial step accepted" (line search
lambda -> 0), far above --tol_od 1e-40, and the octo corrector has no accepted-stall. The only convergence exit past the
wall is --od_junk's junk floor: with the w weakest Delta-free directions frozen, newton_od returns converged when the
projected correction (those directions removed) falls below 1e-45, leaving the residual in the junk. This crawl tries
tiny steps so each prediction is close and the junk subspace is cleanly identified.

## Start state (a reasoned choice)
chain_o/anm_pin3_D215.0000.npz is a chain_fit *extrapolation*; its base polish floors at 6.5e-29 and never converges
(T150), so a crawl cannot start from it. I start from the last truly converged octo state, T138-win2/chain_o/
anm_pin3_D214.5000.npz, and crawl *through* the wall. This maps where the octo step stops being accepted and tests
whether tiny steps + --od_junk carry it past 215.

## Fixed before the run (acceptance item 1)
- h_max = 0.1 (tiny; the chain's own steps were 0.5-1.0). a = min(a_max, h_max, room); a_max from --eps 1e-14.
- Halving floor = 0.0125 = h_max / 8. anm_run has no floor flag; the ladder halves exactly three times
  (0.1 -> 0.05 -> 0.025 -> 0.0125), so the three-halvings stop IS the ladder reaching the floor.
- Stop rules: (a) three halvings without an accepted step -> "stopped: no convergence after three halvings" (reported);
  (b) 24 h wall-clock; (c) hang rule: no log line for 20 min while one core is busy -> one py-spy dump, kill the tree,
  restart from the last state with h_max halved, post.
- Step-acceptance rule (acceptance item 2): a step counts only if the octo corrector returns converged -- either
  max|F| <= --tol_od 1e-40, or (with --od_junk 4) the projected correction with the junk frozen falls below 1e-45.
  There is no other accepted-stall for the octo corrector. Each accepted step's corrected Delta is checked against the
  Taylor prediction: the per-step "moved" (|corrected - predicted|) must sit within the step's truncation (~eps), and the
  "formula diff" against the 1/D formula is recorded. A step whose Delta leaves the predicted truncation is flagged.

## Command (from hp\)
  anm_run.py <raw> <raw>\I19-win2\crawl --state T138-win2/chain_o/anm_pin3_D214.5000.npz --kfreeze 3
    --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 0.1 --steps 40 --D_max 220 --threads 18
    --corrector od --tol_od 1e-40 --qd_it 12 --od_junk 4 --jet_o 1 --reseed 2 --reseed_q 1 --save_pred 1

States land in crawl\, the log in crawl.log. Each can fail; a stall at the wall is a result, reported with the D it
reached, the last accepted step, and the three-halvings ladder.
