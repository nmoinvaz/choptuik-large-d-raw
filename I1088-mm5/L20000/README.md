# I1088-mm5/L20000: D 20000 held at L = 20, direct solve (#1088)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1088

Order of coordinator t5 (2026-11-26, after D 8000's checks): D 2x10^4 by a direct solve, last node at L = 20
(x_l 0.706753, held system with harmonics 5-13 at the guess's values), with the precision ladder.

- `guess_D20000.0000.npz`: the guess, git blob 1f63b72bbfb3d3fde0d94450031af328064b3aec (verified with
  `git hash-object`), from `I1088-mac-a/form_s/g20000L20/` of this repository (commit f922c922; the same blob in main at
  3873dc27). Built from the L = 20 states at D 4000, 5657 and 10^4; saved with ks 11416 and 2659 Taylor steps. `guess.log`
  (blob 837bac72) is its log: max |F| per block (double-double) 1.6e-12 1.9e-12 3.4e-12 5.7e-12 1.0e-11 4.0e-11 5.1e-18,
  the horizon block 3.84x the largest other.
- Command, from `~/Source/choptuik-formsq/hp` with `~/venv-314`'s python, OPENBLAS_NUM_THREADS=2, nice 10, detached, under
  `timeout 12h`:

      python -u form_s_lastnode.py solvestate <this folder> --state <the guess here> --ks KS --threads 14 --ladder dd,qd \
        --it_max 2 --it_hi 2 --chord 1 --step_est 2800,900 --delta_tol 1e-15 \
        --tc 1.64441243858130260:1.77e-9 --commit <the code's commit>

  KS is the coordinator's word: 11416 (the guess's own, if the D 10^4 ks check passed) or 26018 (1.3 n, otherwise).
  The value used is recorded in `pid.txt`.

## Bars and what to expect (written 2026-11-26 03:38 UTC, before the run)

| item | bar or expectation |
|---|---|
| bar | Delta's first-order bound (gain x octo-double max \|F\|) **<= 1e-15**; discretization tails (ks + 200, kc + 20, halved Taylor steps) **<= 1e-25** |
| stop rules (built in) | at most 2 dd steps, then at most 2 qd chord steps with the last dd Jacobian; a step that cuts max \|F\| by less than 10x ends its stage (floor); then the octo-double check, the tails, the Hamiltonian check; `direct_s.jsonl` only if converged |
| gain | about 7e9, extrapolated by D^3.75 from D 8000's 2.28e8 (this machine) and D 10^4's 5.25e8; so max \|F\| must reach about 1.4e-25 |
| path | D 8000 took dd 7.08e-11 -> 2.66e-19 -> 7.1e-21 (dd floor) and one qd chord step 2.2e-20 -> 3.3e-25 (bound 7.5e-17). Here 3e-25 would give a bound of about 2e-15, so a second qd chord step may be needed |
| timing | the `--step_est` guess is 2800 s for a fresh dd step and 900 s for a chord step; at D 8000 they took 700 s and 358 s, and this system has 2.4x the Taylor steps |
| Delta against Track C | 1.64441243858130260 +- 1.77e-9 is printed as "Delta - reference". The L = 20 solves sit -5.2e-10 (D 2000), -6.7e-10 (D 4000) and -7.5e-10 (D 8000) from Track C, so about -8e-10 is expected, inside the bar. This is a comparison with a series fit, not an enclosure; the "+-" is Track C's own error estimate |
| not met | if a bar is missed, the run ends at its stop rules, the record is not written and nothing is loosened |
