# I1088-mm5/L8000: D 8000 held at L = 20, direct solve (#1088)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1088

Order of coordinator t5 (2026-11-26): D 8000 by a direct solve, last node at L = 20 (x_l 0.706222, ks 10418, 1099 Taylor
steps), held system (harmonics 5-13 at the guess's values), with the precision ladder.

- `guess_D8000.0000.npz`: the guess, git blob 2c59ff47d694728c930b92f94578f1faf06936c2 (verified with `git hash-object`),
  from `I1088-mac-a/form_s/g8000L20/` of this repository (commit 7c2b9983, the same blob in main at 53a0c75f). Built from the L = 20 states at D 2828, 4000 and 5657. `guess.log` (blob ce215c8c) is its log: max |F| per
  block (double-double) 2.9e-12 3.5e-12 6.2e-12 1.0e-11 1.9e-11 7.1e-11 1.7e-18, the horizon block 3.8x the largest other.
- Code: `~/Source/choptuik-formsq`, wip/large-d-form-s 1ccd32ab; hp built there (I1088-mm5/build/).
- Command, from `~/Source/choptuik-formsq/hp` with `~/venv-314`'s python, OPENBLAS_NUM_THREADS=2, nice 10, detached, under
  `timeout 8h`:

      python -u form_s_lastnode.py solvestate <this folder> --state <the guess here> --threads 14 --ladder dd,qd \
        --it_max 2 --it_hi 2 --chord 1 --step_est 3000,600 --delta_tol 1e-15 \
        --tc 1.64519021245138076:1.66e-9 --commit 1ccd32ab

  Its log is `lastnode.log`; the per-step jsonl is `lastnode_solvestate.jsonl`; each accepted step's state is
  `lastnode_D8000.0000_step.npz`; the Jacobian is kept in `lastnode_D8000.0000_J.npz`.

## The bar and what to expect (written 2026-11-26 02:53 UTC, before the run)

| item | bar or expectation |
|---|---|
| stop rules (built in) | at most 2 dd steps, then at most 2 qd chord steps with the last dd Jacobian; a step that cuts max \|F\| by less than 10x ends its stage (floor); then the octo-double check, the discretization tails, the Hamiltonian check; `direct_s.jsonl` only if converged |
| bar | Delta's first-order bound (gain x octo-double max \|F\|) **<= 1e-15** |
| expected path | dd step 0 from the guess's 7.1e-11 down to about 1e-17 to 1e-20, dd step 1 to the dd floor (about 5e-21); the qd chord step to about 1e-25 or lower. At D 4000 one qd step took 6.0e-20 to 7.6e-26 (gain 1.7e7); here the gain is expected near 2e8, so max \|F\| must reach about 4e-24 (gain interpolated in log-log from D 5657's 6.2e7 and D 10^4's 5.25e8) |
| timing | the `--step_est` guess: 3000 s for a fresh dd step, 600 s for a chord step (the log prints each step's start and predicted end) |
| Delta against Track C | 1.64519021245138076 +- 1.66e-9 is printed as "Delta - reference". The earlier L = 20 solves sit -5.2e-10 (D 2000) and -6.7e-10 (D 4000) from Track C, inside its bar, so |Delta - reference| of about 1e-9 or below is expected. This is a comparison with a series fit, not an enclosure; the "+-" is Track C's own error estimate |
| checks | ks + 200 and kc + 20 tails below 1e-25; halved Taylor steps below 1e-25; the Hamiltonian check's a rows below about 1e-24 |
| not met | if the bar is missed, the run ends at its stop rules and the record is not written; nothing is loosened |
