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
