# I504-mac: newton_od's correction test in the equilibrated unknowns, its planted check at D 180.52 and the 0.3-0.8 polish at D 242.36

Machine: the M5 Mac (subagent), 2 threads under nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/504 (depends on #502, #489).

Code: `hp/octo_corrector.py` (newton_od's `scale_c` and `trace`) and `hp/eq_test.py`, branch
`feat/i504-equilibrated-test` of choptuik-large-d (backups `wip/i504-subagent`), interpreter venv-314 (Python 3.14, its
installed `hpkernel`). Each run is `run_eq.sh <worktree>/hp <this raw clone> TAG SUBCOMMAND ARGS...`, which writes
`TAG.log` and appends its exit and wall time to `exits.txt`.

## Criteria, fixed before the runs

Planted state: `T129-win2/chain/anm_pin3_D180.5246.npz`, moved as `octo_corrector.py planted` moves it (rel 1e-12,
seed 1, the last node kept), tol 1e-40, 12 steps, ElimO around the state's own pinned system.

Planted column scaling S: S_j the power of two nearest 10^u_j, u_j uniform in [-20, 20], numpy `default_rng(7)` (#502's
seed). Powers of two make z = S w exact in every part, so with and without S the kernel sees the same points while the
tests decide alike.

Runs: A (raw test, no S), B (equilibrated test, no S), C (equilibrated test, S), D (raw test, S). D_c is near_null_eq's
result scaling (Curtis-Reid then Ruiz, tol 1e-12) of |J| for B and of |J| S for C, with J the f64 leading part of the
octo-double Jacobian at the start.

- The plant shows when D's sequence of accepted lam differs from A's (the control: the raw test changes with the scaling
  of the unknowns). If it does not, nothing is tested (`eq_test.py verdict` exits 2). Then the seed of S is not changed
  by hand: `eq_test.py predict` on A's trace gives the decisions of the raw test under S at A's trials, and S is drawn
  from the first seed of 8..27 whose raw test changes a decision there, which D then runs.
- Pass: C's sequence of accepted lam equals B's step by step, with the same outcome (converged or not).
- Bit identity of the default: `newton_od` with `scale_c` None against the code before it (0cce81e), one step each
  (`--it_max 1`) from A's start. Pass: the iterates' eight parts and the histories without their times are equal.
  Control: `same --mutate_bit 1` (one ulp of one entry) must fail.

### The random S does not show (after run A), and the S used instead (fixed before B, C, D)

Run A (`pA_raw`) converged in 4 full steps (lam 1, 1, 1, 1) to 6.86e-42, Delta 1.700531269818162204386381037834122353007,
the value of notes/OCTO_DOUBLE.md 5.4 (a) to all 40 digits. `predict` on its trace (`predict_A.log`): no seed of 7..27
changes a raw decision. With 500 draws each of u uniform in [-U, U] (`predict_A_unmoved.log`), the raw test's ratio
|dz_t| / |dz| under S is at most 3.0e-3, 2.2e-8 and 4.7e-10 at steps 0, 1 and 2 for U 20, and 6.4e-2 at step 0 for
U 100, never at or above 1. Step 3 is accepted by max|F| <= tol whatever the test. So a random S cannot change the raw
test here, and by the rule above nothing is tested with it.

The raw test can change only where a trial's correction is not much smaller than the step's in some unknown. At step 0
that holds in the unknowns the plant leaves at the truth (j >= 576: the last node, m_h, a_h, Delta), and in a few moved
ones (j 112, ratio 7.7). In the unmoved ones the first step's correction is its own O(p^2) error, which the next
correction undoes (|dz_t,j| / |dz_j| = 1 + O(p^2)). So C and D take S
= `unmoved`, S_j = 2^-66 for j >= 576 and 2^66 for j < 576. That is within [1e-20, 1e20], fixed by the plant alone, and
gives on A's trials (`predict_A_unmoved.log`) raw [refused, accepted, accepted, accepted] and eq [accepted x 4]. The
criteria stay as above, with this S. The random S of seed 7 is kept in `predict_A.log` only.

Real case: #489's base polish (`I489-mac/run_polish.sh`'s anm_run.py options) of `I489-mac/renode_L1_horizon_D242.3642.npz`,
with newton_od given D_c from |J| at the corrector's start and every trial printed. Reported: whether step 0 is accepted,
each trial's lam, max|F| and both sides of the raw and the equilibrated test, and whether it converges below 1e-60.

## Planted check: PASS, the control fires (`verdict.log`, exit 0)

| run | test | S | accepted lam | outcome | max\|F\| | wall |
|---|---|---|---|---|---|---|
| A `pA_raw` | raw | none | 1, 1, 1, 1 | converged | 6.86e-42 | 2641 s |
| B `pB_eq` | eq | none | 1, 1, 1, 1 | converged | 6.86e-42 | 3074 s |
| C `pC_eq_unmoved` | eq | unmoved | 1, 1, 1, 1 | converged | 6.86e-42 | 3998 s |
| D `pD_raw_unmoved` | raw | unmoved | 0.5 (one step, `--it_max 1`) | stopped at it_max | 1.70e-12 | 2481 s |

C's iterate is bit-identical to B's (and A's), Delta 1.700531269818162204386381037834122353007 for all three. D refuses
lam 1 at step 0 (in w, 3.855e+04 vs 3.855e+04) where A accepts it (in z, 7.75e-16 vs 9.96e-13). The two sides of each
test at every trial are in the logs. The equilibrated test accepts step 0 by 1.5e-7 (4.453e-03 vs 4.453e-03 in B), its
max norm on a_h[0] (index 736), whose move step 1 undoes. D_c spans 1.63e-16..1.20e+07 for J and 4.0e-19..5.8e+28 for
J S, and D_c(J S) S / D_c(J) is constant to 5.5e-12 in log10 (`predict_A_unmoved.log`).

The first full run D was stopped after 3 trials (`pD_raw_unmoved_stopped.log`, exit 143). With S unmoved the raw test
refused lam 1 again at step 1 (9.640e+03 vs 9.634e+03), so it would halve every step. `run_all.sh` ran A's
successors until then, and `run_rest.sh` ran the rest.

## Real case: the 0.3-0.8 polish refuses step 0 whatever the test (`polish_eq.log`, exit 0)

`run_polish_eq.sh` (#489's options, D_c from |J| at the corrector's start) ran from 04:18:19 to 08:18:51 UTC (14432 s,
jacobian_o 1477 s of it). D_c spans 3.33e-15..1.86e+06 (45 Ruiz iterations, largest |1 - max-norm| 7.7e-13; saved in
`polish_eq_Dc.npy`). The history is `polish_eq_hist.jsonl`, and the trace with step 0's correction is
`polish_eq_hist_trace1.npz`.

From max|F| 1.62e-34, step 0's correction is 0.168 in the raw max norm and 6.17e+10 in the equilibrated one. All nine
trials, lam 1 to 2^-8, have a non-finite residual at the trial point, and their nine projections failed (ElimO
counts: failed 9, skipped 1). So neither test is ever reached. Each is refused for lack of a residual, newton_od stops
with "no trial step accepted", and the base polish is not adopted.

| lam | max\|F\| at the trial | raw \|dz_t\| vs \|dz\| | eq \|dz_t/D_c\| vs \|dz/D_c\| | s |
|---|---|---|---|---|
| 1 | nan | nan vs 1.683e-01 | nan vs 6.172e+10 | 739 |
| 1/2 | nan | nan vs 1.683e-01 | nan vs 6.172e+10 | 434 |
| 1/4 | nan | nan vs 1.683e-01 | nan vs 6.172e+10 | 1686 |
| 1/8 | nan | nan vs 1.683e-01 | nan vs 6.172e+10 | 1840 |
| 1/16 | nan | nan vs 1.683e-01 | nan vs 6.172e+10 | 726 |
| 1/32 | nan | nan vs 1.683e-01 | nan vs 6.172e+10 | 2084 |
| 1/64 | nan | nan vs 1.683e-01 | nan vs 6.172e+10 | 1251 |
| 1/128 | nan | nan vs 1.683e-01 | nan vs 6.172e+10 | 1275 |
| 1/256 | nan | nan vs 1.683e-01 | nan vs 6.172e+10 | 717 |

Where the correction lives (`eq_test.py step`, `polish_eq_step0.log`): it is O(0.1) in every field. That is p1 0.168,
c0 0.051, the nodes' p and m 0.05 to 0.13, m_h 0.15 and Delta 0.076. Only a and a_h are smaller (1e-4). In the
equilibrated unknowns the horizon data dominate, a_h[0] 6.2e10 and m_h[0] 5.7e10, where D_c is 3e-15 to 1.5e-10. So
even lam 2^-8 moves Delta by 3.0e-4.

D_c here is not #502's D_c at the same state times a constant. log10 of their ratio spans -2.02..+0.99. The scaling
is stable under a relative change of J's entries but not under dropping its smallest ones (`sensitivity_L07.log`,
`sensitivity_D180.log`).

The run used choptuik-large-d 909b1d5 (branch `feat/i504-equilibrated-test`). That branch lacks main's e5bbdcd (the
re-seed's octo-double rung LU refactored after a poor correction), so its projections are #489's.
