# I727-win: the three D 99.875 full-system states polished with `--steps 0` to 1e-60

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/727 (the coordinator's message `1794610746892-0` on the `choptuik-large-d` channel; recommended by #725, raw `I725-win/` 9672e70d). Worktree `choptuik-i710` at main 5249c432, venv-t151 (Python 3.10), quad-double, `OPENBLAS_NUM_THREADS=1`, BelowNormal, 4 threads, #682's flags with `--elim_switch 0` as #725 used them (`run_727.py` lists them) and `--tol_qd 1e-60 --qd_it 12 --steps 0`. Raw output to `I727-win/`.

## Plan, written before the run (2026-11-13 23:17 UTC)

States, read from the raw clone and byte-identical (SHA-256) to the copies pushed in the stage checkout: cont3 `I682-win/cont3/anm_pin13_D99.8750.npz`, A1 `I710-win/A1/anm_pin13_D99.8750.npz`, X2 `I725-win/X2/anm_pin13_D99.8750.npz`.

1. **Check first** (job `chk`, cont3): `--steps 0` must stop after the base polish, exit 0, and leave the polished state to compare. **Expectation, written before the run**: reading `hp/anm_run.py`, the loop `for step in range(opt["steps"])` does not run, and a state is saved only inside it (lines 840, 909 to 914) or on the octo-double branch (`--save_base`, line 558). So I expect `chk` to stop after the polish and to fail on "a polished state is saved". If it fails, I stop and tell the coordinator (his instruction), and polish none of the three.
2. **If it passes**: P1 (cont3), P2 (A1), P3 (X2), one after the other, each in its own folder. Delta is the sum of the last entry of the four parts, in arb at 400 bits (`cmp_727.py`), with each state's final qd max|F| from its log and the pairwise differences.
3. **Reading, fixed before the run**: the largest pairwise |Delta difference| at most 1e-30 means the 1.96e-25 spread at D 99.875 was unconverged error; staying near 2e-25 (between 1e-26 and 4e-25) means three distinct near-roots at this precision, with each one's final |F|; anything else is reported as it is.
4. **Control for the comparison**: `cmp_727.py --selftest` plants a pair that must read equal and a pair displaced by 2e-25 that must show 2e-25.
5. **Not done**: any step, any change of the flags, any state at another D.

## Results of the check (2026-11-13 23:22 UTC): `--steps 0` saves no state, and the three states carry three different plans

`run_727.py chk` (cont3, `--steps 0 --tol_qd 1e-60 --qd_it 12`) exited 0 after 95 s and printed "done". Its base polish took 3 quad-double steps, 4.98e-49 to 2.19e-49 to 2.42e-49, and then "no trial step accepted" at |dz| 2.4e-40, not converged (the floor at D 99.875 is a few 1e-49, so 1e-60 is out of reach in quad-double). It changed Delta by +4.30e-47 and +2.03e-46, about 2.5e-46 in all, against a spread of 1.96e-25 between the states. **The folder `chk/` is empty**: the expectation written above held, so the check fails on "a polished state is saved" (a state is saved only in the step loop, `anm_run.py` lines 840 and 909 to 914, or on the octo-double branch, line 558). As the task says, I stopped and polished none of the three (no P1, P2 or P3).

**The three states solve three different discretizations.** `plans_727.py` (its two controls pass: a planted node moved by 1e-3 reads different by 1e-3, and cont3 against itself reads identical) reads the segment plan each state carries in its meta (`plans_727_out.txt`):

| D | pair | plans | max node difference | difference in Delta |
|---|---|---|---|---|
| 99.8125 | A0 and cont3 | identical | 0 | 0 |
| 99.8125 | X1 and cont3 | identical | 0 | 5.670e-34 |
| 99.875 | A1 and cont3 | different | 5.370e-4 | 2.971e-26 |
| 99.875 | X2 and cont3 | different | 9.489e-4 | 1.658e-25 |

Where the plans are equal the states agree to 5.7e-34 or better, and where they differ they disagree by 3e-26 to 2e-25. `notes/OCTO_DOUBLE.md` (d) records that a replanned plan moves Delta by about 1e-28 at D 194, so a plan-dependent root is documented. This is consistent with the 1.96e-25 spread being the plan and not three near-roots, but it is two data points and nothing here tests it. It means that a polish on each state's own plan (`--keep_plan 1`, the default) cannot make the three agree, whatever the corrector.

Files: `chk/` (empty), `logs/chk.log`, `logs/run_727.log`, `baseline_727.txt` (the unpolished starts: largest pairwise difference 1.955e-25), `plans_727_out.txt`, `run_727.py`, `cmp_727.py` (selftest passed), `plans_727.py`.

## Plan for the common-plan polish, fixed before the runs (2026-11-13 23:24 UTC)

The coordinator chose option 1 (message `1794612225861-0`). Points fixed here before any of the runs:

1. **Data edit only.** `make_states_727.py` writes `states/A1_on_cont3plan.npz` and `states/X2_on_cont3plan.npz` beside the originals, which stay untouched. Only the `segs` key of each state's `meta` (a JSON string) is replaced by cont3's; the arrays `zh`, `zl`, `z2`, `z3` are copied bit for bit and every other meta key stays as it was. The script checks that and records the changed keys in `states/edit_log.txt`; its `--selftest` plants one changed array entry and one changed meta key besides `segs`, and both must be flagged.
2. **Pilot and control `pilot`**: cont3's own state, `--corrector od --tol_od 1e-60 --save_base 1 --steps 0`, with #682's flags and `--elim_switch 0` as #725 used them (`run_727.py` lists them; the corrector flags `--corrector od --tol_od 1e-60` replace `--corrector qd --tol_qd`). The plan is unchanged, so its octo-double Delta must equal its quad-double Delta (the stored cont3 state) to 1e-30. If it does not, or the polish does not converge to 1e-60, I stop and tell the coordinator, and run neither A1 nor X2.
3. **Then `A1c` and `X2c`**: the edited copies, the same flags, one after the other, 4 threads, BelowNormal.
4. **Reading**: all three octo-double Delta agree to at most 1e-30, so the plan made the 2e-25 spread; they stay near 2e-25 apart (between 1e-26 and 4e-25), so there are distinct near-roots on one plan; anything between is reported as it is.
5. **Report**: each state's final octo-double max|F|, Delta to 40 digits (the exact sum of all eight parts, `cmp_727.py --od`), the pairwise differences, and each state's |F| on cont3's plan before the polish (the base line of the log, which gives the octo-double max|F| of the stored state under the plan in its meta), which measures how far the plan alone moves the residual.

Not done: any step, any state at another D, any change of the flags other than the corrector pair above.

## Results of the pilot (2026-11-13 23:59 UTC): Delta equal, polish not converged, stopped

`run_727.py pilot` (cont3's own state, plan unchanged, `--corrector od --tol_od 1e-60 --save_base 1 --steps 0`, #682's flags, `--elim_switch 0`, 4 threads) exited 0 after 1990 s and saved `pilot/base_pin13_D99.8750.npz` (eight parts, adopted because the octo-double max|F| fell). Two controls of point 2:

| control | result |
|---|---|
| octo-double Delta equals the quad-double Delta to 1e-30 | **passes**: 1.745150028164499252944352893640343550633 for both, difference +1.1101e-46 (`pilot_cmp_727.txt`) |
| the polish converges to 1e-60 | **fails**: 9 octo-double steps, max\|F\| 3.42e-49 to 2.74e-49 and no further, "not converged" |

The step converges but the residual does not: the first step (|dz| 1.05e-39 to 3.0e-65) moves Delta by +1.11e-46, the second by 9.2e-72, and from the fourth step |dz| sits at 1e-105 to 1e-106 with max|F| unchanged at 2.74e-49. All 13 trial points of the line search report the same 2.74e-49 and are refused ("raw |dz_t| not < |dz|"), so each trial's residual is the projection's, not the step's. The 22 projections of the run are all the quad-double branch (`u0q`). With `--elim_switch 0` every point is projected (`anm_run.py` line 355), and without `--reseed_o` the projection's horizon data is quad-double accurate, which fits a floor of a few 1e-49. notes/CRAWL.md section 8 says the working octo-double configuration projects with `--reseed_q 1 --reseed_o 3` (octo-double corrections, rung residual about 1e-80). **This is the likely cause and it is untested.**

As the coordinator's point 2 says, I stopped: A1c and X2c were not run. The cost: an octo-double Newton step or trial is about 90 s at 4 threads here, so a polish that converges in 2 to 3 steps is about 5 min per state, and this pilot took 33 min because of the refused line search.

Files: `pilot/` (the saved base), `logs/pilot.log`, `logs/run_727.log`, `pilot_cmp_727.txt`, `states/` and `make_states_727.py` (made, not yet used by a run), `cmp_727.py` (selftest passed with the planted eight-part value).

## Decision after the pilot, fixed before pilot2 (2026-11-13 00:01 UTC)

The first pilot (no `--reseed_o`) stalled at octo-double max|F| 2.74e-49 with its Delta equal to the quad-double one to 40 digits. The coordinator's message `1794614449424-0`: repeat it with `--reseed_o 3` added and nothing else changed (job `pilot2`, `run_727.py`), the same two controls, then A1c and X2c, also with `--reseed_o 3`, only if it passes. Their diagnosis matches #713's pilot on the Mac (at D 200 the quad-double projection floored the octo-double residual at 1.2e-33, `--reseed_o 3` brought it to 7.4e-52).

**Pass for pilot2**, written before the run: the polish converges to octo-double max|F| of at most 1e-60 (the corrector's own "converged"), and its Delta equals cont3's stored quad-double Delta to 1e-30. If it still stalls above 1e-60, I stop and post the floor (the coordinator's instruction) and run neither A1c nor X2c. The reading of the three Delta stays as in point 4 above.

## Results of pilot2 (2026-11-14 00:04 UTC): both controls pass, the polish was the projection alone

`run_727.py pilot2` (cont3's own state and plan, `--corrector od --tol_od 1e-60 --save_base 1 --steps 0 --reseed_o 3`, #682's flags, `--elim_switch 0`, 4 threads) exited 0 after 115 s. Base saved in eight parts (`pilot2/base_pin13_D99.8750.npz`).

| control | result |
|---|---|
| the polish converges to at most 1e-60 | **passes**: octo-double max abs F 3.9e-63, "converged" |
| octo-double Delta equals the quad-double Delta to 1e-30 | **passes**: 1.745150028164499252944352893640343550633 for both, difference exactly 0 (`pilot2_cmp_727.txt`) |

The exact 0 needs reading. The polish converged at its first evaluation: the octo-double projection (`--reseed_o 3`) alone took max|F| from the stored state's 3.4e-49 to 3.95e-63, and no Newton step was taken (log line `on 0: |F| 3.95e-63 converged`, "1 steps" counts the evaluation). Against the stored state only 64 of 769 entries differ (max |difference| 4.524e-50, entry 704, the horizon block), the other 705 are bit-identical, and the last entry of all eight parts equals the stored four parts' with z4 to z7 exactly 0. So the stored cont3 state is a root of its own plan's system to better than 1e-62 apart from its horizon data, whose quad-double accuracy was the 2.74e-49 floor of the first pilot (all 769 entries of that run moved, by up to 1.05e-39, along weak directions). The control passes but does not show that the octo-double polish moves Delta when it must: the A1c and X2c runs below do (their plan swap displaces them), with point 5's |F| before the polish.

## Results of A1c and X2c, and the reading (2026-11-14 00:17 UTC)

`run_727.py A1c X2c` (the `states/` copies on cont3's plan, `--corrector od --tol_od 1e-60 --save_base 1 --steps 0 --reseed_o 3`, 4 threads): A1c exit 0 after 5 min, X2c exit 0 after 414 s. Every number below is from `logs/*.log` and `final_cmp_727.txt` (`cmp_727.py --od`, the exact sum of the eight parts).

| state, on cont3's plan | octo max abs F before the polish | Newton steps | final octo max abs F | Delta moved by the first step | Delta, 40 digits | Delta - X2c |
|---|---|---|---|---|---|---|
| cont3 (pilot2) | 3.4e-49 with the quad-double projection (first pilot), 3.95e-63 with `--reseed_o 3` | 0 | 3.9e-63 | none | 1.745150028164499252944352893640343550633 | -1.1101e-46 |
| A1c | 1.67e-35 | 2 | 2.4e-62 | -2.97e-26 | 1.745150028164499252944352893640343550633 | -1.2667e-57 |
| X2c | 1.76e-35 | 3 | 2.7e-93 | +1.66e-25 | 1.745150028164499252944352893640343550633 | 0 |

Pairwise differences: pilot2 - A1c -1.1101e-46, pilot2 - X2c -1.1101e-46, A1c - X2c -1.2667e-57; the largest is 1.1101e-46.

**Reading (point 4, fixed before the runs): all three Delta agree to at most 1e-30 (largest 1.11e-46), so the plan made the 2e-25 spread.** On one plan there is one root, with Delta = 1.745150028164499252944352893640343550633457431631616393443 (X2c, 60 digits).

What backs it, beyond the agreement:
- The plan swap alone moves the residual of A1 and X2 to 1.7e-35 on cont3's plan (X2 was at 4.1e-49 on its own plan, #725's table), and the first Newton step moves Delta by -2.97e-26 and +1.66e-25, which are exactly their offsets from the root on their own plans (A1 on its own plan - X2c = +2.9709e-26, X2 - X2c = -1.6580e-25). So the polish did move Delta, by what the plan explains.
- The first pilot (no `--reseed_o`, stalled at max|F| 2.74e-49) has Delta equal to X2c's to 1.4e-80 (-1.4484e-80) and to A1c's to 1.27e-57: its one effective Newton step already reached the root's Delta, and its horizon floor never touched Delta. Pilot2 (and the stored cont3 state) sit 1.1101e-46 off the root in Delta because pilot2 took no Newton step, which its first-pilot twin shows is the weak direction (pivot 1.2e-18), far below the 1e-30 bar.
- The largest node difference from cont3's plan is 5.4e-4 (A1) and 9.5e-4 (X2), and Delta on their own plans differs by 3.0e-26 and 1.7e-25.

Limits, stated: this is three states at D 99.875 on one plan, and it shows that the spread of #725's three states is the plan, not that every spread elsewhere is. The control of point 2 passed trivially (pilot2 took no Newton step), and the test of the polish is A1c and X2c. The quoted Delta of a state is a root of its own plan's discrete system: two plans 1e-3 apart in a node give Delta differing at 1e-25, whatever the corrector's precision.

Controls run: `make_states_727.py --selftest` (planted array change, second meta key, own plan kept: all flagged), `plans_727.py` (planted node moved, self-comparison), `cmp_727.py --selftest` (planted equal pair, planted 2e-25 displacement, planted eight-part value returned to 40 digits with the two-part sum differing).
