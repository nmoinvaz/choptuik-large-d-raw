# I742-win: the full system from D 113 to 120 with the octo-double corrector (completes #726)

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/742 (the coordinator's message `1794618284752-0` on the `choptuik-large-d` channel; recommended by #739, raw `I739-win/` 51a8e41f). Worktree `choptuik-i710` at main 5249c432, venv-t151 (Python 3.10), `OPENBLAS_NUM_THREADS=1`, BelowNormal, 4 threads. Start state `I739-win/B/anm_pin13_D113.0000.npz` (eight parts, M = 32, octo-double max|F| 7.3e-85, Delta 1.733640141567942734406710993193602081591). Flags as the issue gives them, #739's: #682's plus `--elim_switch 0 --corrector od --tol_od 1e-60 --reseed_o 3`, with `--h_max 1.0 --a0 1.0` (`run_742.py` lists them). Raw output to `I742-win/`.

## Plan, written before the runs (2026-11-14 01:05 UTC)

1. **Pilot `P`**: one step a = 1 from D 113 to D 114 (`--steps 1 --save_base 1`), since a full step may need more Newton steps than a = 1/4 did (5 evaluations at 100 to 120 s there). Its base polish (the octo-double polish of the D 113 start, saved as `P/base_pin13_D113.0000.npz`) is **control (a)**: its Delta must equal B's, 1.733640141567942734406710993193602081591, to 1e-30. The pilot fixes the cost, and I post it before the chain.
2. **Chain `L`**: from the pilot's D 114 state, `--steps 6 --h_max 1.0 --a0 1.0`, to D 120 if every step is taken at a = 1. If the a = 1 step is refused and a halved step is accepted, the states are not on integer D, and I choose a0 so that the next step lands on an integer D and say so on the issue. The stop rule is #726's: anm_run's own, four refused attempts at one D (the first plus three halvings), after which the run ends and its history is posted.
3. **Convergence (b)**: converged means the corrector says converged and its octo-double max|F| is at most 1e-60, for every accepted step.
4. **Table (c)** (`table_742.py`): Delta_full - Delta_held at D 113 and at each integer D from 114 to the last one reached, Delta the exact sum of the eight parts (`I739-win/cmp_739.py`'s reading) against the held states `T138-win2/chain/anm_pin3_D<D>.0000.npz` of the stage checkout, with the ratio to `delta_all.csv`'s err (chain_fit, a spread over fit choices, not an enclosure) as `I726-win/table_726.py` reads it. The script **first reproduces D 113's +4.3655e-13 from `I739-win/B/`** and exits 1 if it does not.

**Expectation, written before the runs and not a criterion**: a = 1 steps converge in 5 to 8 octo-double steps at 10 to 15 min an attempt, so 7 steps take 1.2 to 1.8 h; the shift keeps growing with successive ratios falling slowly from 1.037 toward 1, and its ratio to the err stays near 0.146. A break of that pattern, or a stop, is reported as it is.

**Not done**: any step past D 120, any change of the flags, the quad-double comparison of #740 (closed).

## Decision at D 117 (2026-11-14 02:45 UTC): the own-test attempt crawled, rerun with `--od_accept natural`

D 114 to 117 were accepted at a = 1 (`L`, 603 to 645 s each). The a = 1 attempt D 117 to 118 under the default trial test (`--od_accept own`) **crawled at lam 1/2** (`logs/L.log`): after the first full step (max|F| 1.49e-29, the re-seeded prediction, to 1.39e-15, where the earlier steps left 4.1e-19, 4.4e-19, 5.7e-18 and 2.8e-18) every one of the next eight Newton steps refused lam 1 and was accepted at lam 0.5, so max|F| halved exactly each step (1.39e-15 to 5.42e-18, about 240 s each). The refused lam 1 trial was a very good point (its own max|F| fell by a factor 4 a step, 1.39e-28, 3.48e-29, 8.71e-30, 2.18e-30, 5.44e-31, 1.36e-31, 3.40e-32, 8.50e-33, 2.13e-33), but its own Newton correction stayed at raw |dz_t| 2.977e-15 (2.976e-15 at the last) while |dz| halved from 1.683e-15 to 6.545e-18, so the test |dz_t| < |dz| could never accept it. `--elim_switch 0` was on, so this is not #700's mechanism (the projection switch), and it happens at D 118, not past D 251. The cause is not found.

I stopped that attempt at its Newton step 9 (02:43:59 UTC, 5038 s into `L`, after 8 crawling steps) on the coordinator's word (message `1794624207651-0`, option 2). `L` produced the accepted states D 115, 116 and 117 only. The attempt has no `anm_run.jsonl` record, because anm_run writes a step's record when the step ends.

The rerun is job `N` (`run_742.py N`): from `L/anm_pin13_D117.0000.npz`, `--steps 3 --h_max 1.0 --a0 1.0`, **`--od_accept natural` the only flag changed** (Deuflhard's natural monotonicity test, #644; #603's chain uses it). The acceptance test picks the path, not the root, and each state is still judged by max|F| at most 1e-60, so states from either test are comparable. If lam 1 is accepted, N continues to D 120 under the same stop rule. If natural also crawls, `run_742.py` stops N after its fourth crawling step in a row (its rule has a selftest with planted lines) and I post the per-step |dz_t| and |dz|.

## Result of N (2026-11-14 03:07 UTC): natural also crawls, and stagnates; stopped by the rule

`run_742.py N` (D 117 to 118 at a = 1, `--od_accept natural`, otherwise L's flags) was killed by the driver at 03:05:27 UTC after 1252 s, on the coordinator's rule (four crawling steps in a row), before its attempt ended. The per-step |dz| and the trials' own corrections of both crawling attempts, from the logs (`crawl_742.py`, selftest passed; `crawl_742_out.md`):

- Own test (L): from Newton step 1 on, every lam 1 trial is refused although its own residual is excellent (1.39e-28 down to 2.13e-33), because its own correction stays at raw |dz_t| 2.977e-15 while the iterate's |dz| halves (1.68e-15 to 1.31e-17); lam 0.5 is accepted each time and max|F| halves exactly (1.39e-15 to 5.42e-18).
- Natural (N): the first step's lam 1 trial has a simplified correction 1.015e6 times |dz| (|dz| 1.95e-7, the trial's max|F| 1.39e-15), the ratio falls by about 8 per halving of lam (1.27e5, 1.6e4, 1.98e3, 247, 30.4, 3.27, 0.694) and lam 1/128 is the first accepted, leaving max|F| 8.47e-20 and |dz| 2.45e-9. Steps 1 to 3 then refuse lam 1 (ratios 0.961, 0.986, 1.006 against the bound 0.75) and accept lam 0.5 (ratios 0.5018, 0.5001, 0.4978) **without progress**: max|F| 8.47e-20, 9.55e-20, 1.03e-19, 1.06e-19 and |dz| 2.45e-9, 2.47e-9, 2.46e-9, 2.45e-9, all about constant, about 145 to 165 s a step. So natural is worse here than own (which at least halves max|F| each step).

Both tests fail at the same point, so the acceptance test is not what stops the step: the first full step from the a = 1 prediction at D 117 is large (the iterate's |dz| at the start is 1.95e-7, against 3.38e-9, 3.52e-9, 1.27e-8 and 8.81e-9 for the steps to D 114, 115, 116 and 117, so 22 to 58 times larger), and what follows is a crawl whichever test judges it. That is a reading of the numbers, not a traced cause.

N produced no accepted state. The accepted states of the task are D 114 to 117.

## Result of M and the table (2026-11-14 05:12 UTC): D 120 reached

`run_742.py M` (D 117 at a = 1/2, `--steps 6 --h_max 0.5 --a0 0.5`, the default own test, L's flags, 4 threads) exited 0 after 7373 s with all six steps accepted at their first attempt, lam 1 at every Newton step, no refused attempt: D 117.5, 118, 118.5, 119, 119.5, 120, each 6 evaluations, 897 to 1080 s in the corrector, final octo-double max|F| 8.6e-79, 6.9e-74, 2.2e-70, 2.7e-83, 1.7e-70, 3.1e-65. Tables: `table_742_out.md` (`table_742.py`, which first reproduced #739's D 113 value, +4.3655e-13), `dz_742_out.md`, `crawl_742_out.md`.

| D | Delta_full (octo-double, 40 digits) | Delta_full - Delta_held | err (chain_fit, a spread over fit choices) | ratio to the err | shift ratio to the previous D |
|---|---|---|---|---|---|
| 113 | 1.733640141567942734406710993193602081591 | +4.3655e-13 | 3.0e-12 | 0.146 | |
| 114 | 1.732869663158360015225732667964316431814 | +4.5175e-13 | 3.2e-12 | 0.141 | 1.0348 |
| 115 | 1.732112314608397196279780335037996998181 | +4.6652e-13 | 3.3e-12 | 0.141 | 1.0327 |
| 116 | 1.731367762815444921564320564141065073226 | +4.8080e-13 | 3.5e-12 | 0.137 | 1.0306 |
| 117 | 1.730635685860038849267059677903292989227 | +4.9456e-13 | 3.7e-12 | 0.134 | 1.0286 |
| 118 | 1.729915772540067188606164966063807771721 | +5.0775e-13 | 3.8e-12 | 0.134 | 1.0267 |
| 119 | 1.729207721928085006517252284424691967389 | +5.2033e-13 | 4.0e-12 | 0.130 | 1.0248 |
| 120 | 1.728511242950407984923956924965683176416 | +5.3226e-13 | 4.2e-12 | 0.127 | 1.0229 |

With #726's D 105 to 112 (+3.0518e-13 to +4.2096e-13, shift ratios 1.055 to 1.039) the shift runs smoothly from D 105 to D 120, the successive ratio falling by about 0.002 a step throughout, from 1.055 to 1.0229. The expectation written before the runs, that the ratio to the err stays near 0.146, did not hold: it falls to 0.127 because the err grows (3.0e-12 to 4.2e-12, a factor 1.4) faster than the shift (4.37e-13 to 5.32e-13, a factor 1.22). These are not enclosures. The states at D 118, 119 and 120 come from a = 1/2 steps and D 114 to 117 from a = 1 steps, and the shift is continuous across that change.

**The crawl and what the steps cost.** The a = 1 attempt from D 117 crawls under both trial tests (the previous comments and `crawl_742_out.md`), the cause is not found, and it cost: L, stopped after 8 crawling steps of its attempt (5038 s of L in all), N under `--od_accept natural`, stopped after four crawling steps (1252 s). The a = 1/2 steps that follow start with about the same iterate |dz| (4.5e-8 to 2.6e-7 against 1.95e-7 for the crawling a = 1 step, `dz_742_out.md`), and converge with lam 1 at every step. The series state weakens along the chain (order ratio 5: 5.0 at D 113, 3.3 from D 117 on; z_N from 2.3e-29 to 6.3e-27).

Acceptance of #742: (a) met, trivially (no Newton step in the polish); (b) every accepted step converged to at most 1e-60 (the largest final max|F| is L's D 116 step, 2.3e-62), the a = 1 attempt to D 118 did not converge under either test and was stopped by me (L, on the coordinator's word) and by the driver's crawl rule (N), anm_run's own stop rule (four refused attempts) never fired, and its history is in the logs and posts; (c) the table above, D 113 to 120, with the reading reproduced first.
