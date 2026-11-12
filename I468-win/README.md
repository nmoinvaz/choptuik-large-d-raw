# I468-win: #218's remaining acceptance runs

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/468 (follows #218; the coordinator's message `choptuik-large-d/2026-11-12/021602Z-coordinator-40e6.md`). Worktree `choptuik-i513` at main 14dc3863 (Python only; the venv-t151 build of hpkernel, the one of #462), 3 threads per command at BelowNormal, two commands at a time. Every command runs under `I462-win/run_capped.py` with a cap of 10800 s (the issue's stop condition, a run past 3 h); the exit code of each is in `<name>.exit`, its log in `<name>.log`.

| name | command (from `choptuik-i513/hp`, RAW = the raw clone) | inputs |
|---|---|---|
| polish | `anm_run.py` of #218's `d10_D191.5_od.cmd` (`--steps 0 --corrector od --tol_od 1e-40`), output `chain_d10/` | I13-win/chain_d10/anm_pin3_D191.5000.npz |
| planted | `octo_corrector.py planted RAW STATE --threads 3 --out planted` | I13-win/chain_d6/anm_pin3_D192.0000.npz |
| planted_ctrl | the same with `--qd 0 --mutate_offset qd --Delta_ref <the quad-double Delta of planted>` (notes/OCTO_DOUBLE.md 5.3 (c)) | the same |
| wall | `octo_corrector.py wall RAW PRED --threads 3 --out wall` | I215-win/chain_d10/pred_pin3_D194.5000.npz |
| wall_ctrl | the same with `--mutate 10` | the same |

The inputs are read from the raw clone; their sha256 (first 16) equal origin's: D191.5000 state f38111880b8196c0, D192.0000 state b47fc73eee665e70, D194.5000 prediction 45c548db289ec8a3. Lane 1 runs polish and then planted, lane 2 runs wall and then wall_ctrl; planted_ctrl follows planted.

**Criteria, as the code judges them, fixed before the runs.** polish: octo-double max|F| below 1e-40, and the table of its Delta minus the quad-double Delta (the qd run is line 2 of `I215-win/chain_d10.log`, max|F| 6.37e-29) beside #218's two rows (+4.48e-19 at d6 D 192.0, -2.07e-18 at d10 D 193.5). planted: the octo-double corrector converges with pinned max|F| below 1e-40 and its Delta agrees with the quad-double corrector's from the same start to 1e-30 (`octo_corrector.py planted` judges exactly this, notes 5.3 (a)). wall: pinned max|F| below 1e-36 (5.3 (b)). Each control must exit 1.

**A reading to settle.** The issue says the planted Delta must agree "with the planted value" to 1e-30. `planted` also prints the octo-double Delta against the truth state's own Delta ("od against the truth: dDelta") but does not judge it. The truth state is a quad-double result (max|F| 7e-29 at D 192.0), so its Delta is not an exact solution of the octo-double system, and #218's log comparison puts the octo-double shift of this very state at +4.48e-19. I expect that line to read about 4.5e-19, which is above 1e-30; the results report both numbers.

## Commands added after the coordinator's messages

The coordinator's message 022020Z settled the planted criterion (notes/OCTO_DOUBLE.md 5.3 (a): the octo-double pinned max|F| below 1e-40 and the octo-double Delta equal to the quad-double corrector's from the same start to 1e-30; the printed distance to the truth state's Delta is information). After planted failed that check, the message 031023Z asked for a valid reference, and 031232Z agreed to take its Delta as the exact eight-part sum of a saved base (`--save_base 1`) and asked for a check of that saved base. These followed, with `i468_<name>.cmd` and `<name>.log/.exit`:

| name | command |
|---|---|
| polish_d6 | `anm_run.py` as polish with chain_d6's options (`--held_fit data/held_fit_d6.json`) on I13-win/chain_d6/anm_pin3_D192.0000.npz, `--steps 0 --tol_od 1e-40 --save_base 1`; saves `chain_d6/base_pin3_D192.0000.npz` |
| check_base | `check_base.py RAW chain_d6/base_pin3_D192.0000.npz polish_d6.log` with the options `--held_exact`, `--stored_plan`, `--mutate` (the `_he0`, `_he1`, `_sp1` logs; `_v1` are the first version of the script) |
| reload_d6 | `anm_run.py --steps 0` from the saved base with the same options (the real consumer) |
| planted_ref | `octo_corrector.py planted RAW I13-win/chain_d6/anm_pin3_D192.0000.npz --qd 0 --Delta_ref 1.697193549538995551413179773802307928375` (`delta_ref_d6_D192.txt`) |
| planted_ref_ctrl | the same with `--mutate_offset qd` |

## Results (2026-11-12)

| command | exit | verdict | last line |
|---|---|---|---|
| polish (d10 D 191.5 od polish, `--steps 0`) | 0 | pass | `octo-double Newton: 3 steps, max\|F\| 2.7e-44, converged` |
| wall | 0 | pass | `(b) PASS: od max\|F\| 5.09e-53 < 1e-36` |
| wall_ctrl (`--mutate 10`) | 1 | fails as it must | `(b) FAIL: od max\|F\| 1.72e-35 < 1e-36` |
| planted | 1 | **fails (a)** | `(a) FAIL: od max\|F\| 1.10e-44 < 1e-40, \|Delta_od - Delta_qd\| <= 1e-30` |
| planted_ctrl (5.3 (c), `--Delta_ref` the stalled quad-double Delta) | 1 | stopped by hand | superseded, see below |
| polish_d6 (`--save_base 1`) | 0 | pass | `octo-double Newton: 3 steps, max\|F\| 1.5e-44, converged` |
| reload_d6 | 0 | pass | `on 0: \|F\| 1.53e-44 converged` |
| planted_ref | 0 | **pass** | `(a) PASS: od max\|F\| 1.10e-44 < 1e-40, \|Delta_od - Delta_qd\| <= 1e-30` (the distance is 8.7647e-41) |
| planted_ref_ctrl (`--mutate_offset qd`) | 1 | fails as it must | `(a) FAIL: od max\|F\| 3.39e-12 < 1e-40, \|Delta_od - Delta_qd\| <= 1e-30` (the distance is 4.4791e-19) |

**polish.** Delta(od) - Delta(qd) at d10 D 191.5 is +4.540e-19 (qd max|F| 6.37e-29, od 2.69e-44), within the 1e-18 bound. `compare_qd_od.out` tables it with #218's two rows (+4.480e-19 at d6 D 192.0, -2.068e-18 at d10 D 193.5, which fails the bound); its input `d10_D191.5_qd_od.log` is lines 1 and 2 of `I215-win/chain_d10.log` (the quad-double run) followed by `polish.log`, because the script reads a qd run and the od run that follows it in one file. The script's control `--mutate=shift=5e-18` trips all three rows and its selftest passes.

**wall** (`I215-win/chain_d10/pred_pin3_D194.5000.npz`): re-seed ok in 60 s, od 3 steps converged, pinned max|F| 5.09e-53, Delta 1.696517437744296120575177615628097346557, 515 s. Its control stops with `no trial step accepted` after 5 steps, max|F| 1.72e-35, 3693 s (one solve took 1427 s at lam 0.0078).

**planted (5.3 (a) as written): FAIL, a discrepancy.** On `I13-win/chain_d6/anm_pin3_D192.0000.npz`, start 3.39e-12:

| corrector | steps | end | Delta |
|---|---|---|---|
| octo-double | 5, converged | pinned max\|F\| 1.10e-44 | 1.697193549538995551413179773802307928375 |
| quad-double | 5, **stopped**: `qn 4: no trial step accepted` | max\|F\| 7.87e-24 | 1.697193549539037351952678242883515155388 |

|Delta_od - Delta_qd| is 4.1801e-14 against 1e-30. 5.3 (a)'s quad-double reference does not converge at D 192.0. The distance of the octo-double Delta from the truth state's Delta is 4.4791e-19, the shift #218 found for this state (information, not judged). The bound is not loosened.

**planted_ctrl** was the 5.3 (c) control with that stalled Delta as `--Delta_ref`. I stopped it by hand at 03:43:22 UTC after 35 minutes with no solve printed (its worker had used 5321 s of CPU; the exit file 1 is the kill's), because the coordinator then ruled that reference invalid and its octo-double run is the same as planted_ref_ctrl's, which differs only in `--Delta_ref`.

**A valid reference (the coordinator's steps 1 to 3).** polish_d6 polishes the same state with anm_run.py to max|F| 1.53e-44 (the value #215's od run reached) and saves the base. Its Delta is the exact sum of the eight parts of the last entry, 1.697193549538995551413179773802307928375 (`delta_ref_d6_D192.txt`), which equals the planted run's octo-double Delta to all 40 digits printed. The log prints Delta as `1.69719354953899559 -4.2493e-17`: the first number is a double printed to 17 decimals and the second its lower part, so the log fixes Delta to about 1e-21 once the first is read as `float(...)`, not to 32 digits. planted_ref converges to the same 1.10e-44 and the same Delta, 8.7647e-41 from the reference.

**What the reference shares with the test.** The polish and the planted run use the same octo-double kernel and corrector. So planted_ref tests whether the corrector returns to the known root from 1e-12 away, not whether the kernel is right; the independent cross-check is notes/OCTO_DOUBLE.md 5.4 (a) at D 180.5, where quad-double converges.

**The saved base** (`--save_base 1`, de63a118; this is its first real run). `check_base.py`:

| variant | Delta, exact sum against float(hi) + lo | reload pinned max\|F\| (the polish's last 1.530e-44) |
|---|---|---|
| v1 (hi read as a decimal, plan again at 1e-32) | 3.9e-18, FAIL (the script's bug: hi is off by up to 5e-18) | 4.715e-36, FAIL |
| plan again at 1e-32, `--held_exact 0` or `1` | 1.142e-22, PASS | 4.715e-36, FAIL (identical for both) |
| **stored plan (18 steps), as anm_run.py's reload** | **1.142e-22, PASS** | **1.527e-44, ratio 0.998, PASS** |

Controls (must fail): `--mutate dd` (drop parts 2 to 7) gives 2.322e-3, `--mutate shift` (Delta + 1e-15) gives a Delta difference of 1.11e-15; `--mutate qd` (drop parts 4 to 7) gives 5.5e-36 with the replanned system, hidden by that system's 4.7e-36 floor, which is why dd was added. The 4.7e-36 of the replanned system is what the comment in `anm_run.py` (#461) says a new plan leaves; with the stored plan the base reloads to the polish's value. reload_d6 loads the base in anm_run.py ("the base keeps its stored plan (18 steps)") and starts at |F| 1.53e-44, converged in one step, Delta unchanged. The saved base is right.

**planted_ref_ctrl (the control) fails, and for the right reason.** With `--mutate_offset qd` (PinnedO's J^-1 c taken through the quad-double LU) the first Newton step has |dz| 1.1e-2 where the unmutated one has 1.0e-12, no trial step is accepted (`on 0: |F| 3.39e-12, |dz| 1.1e-02: no trial step accepted, stopping`, 9 failed projections), and the run ends at the start, pinned max|F| 3.39e-12, 2683 s. So it fails both criteria: max|F| 3.39e-12 against 1e-40, and |Delta_od - Delta_ref| = 4.4791e-19 against 1e-30. The Delta failure is only the distance between the truth state's Delta (the start's, "od against the truth: dDelta 0.0") and the polished root, because no step was taken; the informative failure is the broken Newton step. The earlier mutated run (planted_ctrl) was stopped at 35 minutes; this run's first solve took 45 minutes (2683 s) to end the same way.

## Summary of verdicts

| check | criterion | verdict |
|---|---|---|
| od polish of d10 D 191.5 | max\|F\| below 1e-40, table with #218's rows | pass: 2.69e-44; Delta(od) - Delta(qd) +4.540e-19 |
| wall | pinned max\|F\| below 1e-36 | pass: 5.09e-53 |
| wall control `--mutate 10` | must fail | fails: 1.72e-35 |
| planted, 5.3 (a) as written (quad-double reference) | od below 1e-40 and \|Delta_od - Delta_qd\| below 1e-30 | **fails**: 1.10e-44, but the quad-double reference stalls at 7.87e-24 (4.18e-14) |
| planted against an octo-double polish of the same state | od below 1e-40 and \|Delta_od - Delta_ref\| below 1e-30 | pass: 1.10e-44, 8.7647e-41 |
| its control `--mutate_offset qd` | must fail by its Delta | fails: no step accepted, 3.39e-12, 4.4791e-19 |
| saved base (`--save_base 1`) | loads, Delta within the log's digits, reload \|F\| within a factor 2 | pass: 1.1e-22, 1.527e-44 against 1.530e-44 |
