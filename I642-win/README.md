# I642-win: where the full release stops converging, D 74 to 79 (hp/release_held.py, --kfreeze=13)

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/642 (the coordinator's message `1794551624089-0` on the `choptuik-large-d` channel and the commands in the issue's comment; follows #640, raw `I640-macm3/` at 725ecb92). Worktree `choptuik-i642` at main efe05840 (`hp/release_held.py`, main 9839474 or later), venv-t151 (Python 3.10, hpkernel from before #523, multidouble 0.1.0), quad-double, `OPENBLAS_NUM_THREADS=1`, `--threads=4`, BelowNormal, one run at a time (4 busy threads). The coordinator's note: below D 215 the exact and rounded freeze projectors agree to far better than these tests resolve, so win's build is fine. Nothing is built.

## Plan, written before the runs (the issue's acceptance)

1. **The planted control** (#640's), on `T81/conv_pin5_D73.0000_D73.000000.npz` (read in place from the raw repository's origin/main checkout), each with `--kfreeze=13 --threads=4`:
   - `--perturb=0` (the unperturbed release),
   - `--perturb=1e-10` (the cos and sin coefficients of p1's harmonics 5, 7, 9, 11, 13 moved by 1e-10 each, as a wrong fit would),
   - `--perturb=1e-10 --it_max=0` (no Newton step, nothing released).
   Pass: the perturbed release equals the unperturbed one, Delta_full within 1e-25 and every coefficient of harmonics 5, 7, 9, 11, 13 at the end within 1e-20; and the no-release run does **not** (its coefficients stay 1e-10 off). Each control goes in its own subfolder, because the second and third write the same state file name.
2. **The six chain states** `T138-win2/chain/anm_pin3_D7X.0000.npz`, X = 4 to 9 (D 74 to 79), `release_held.py <raw>/I642-win/release.jsonl STATE --kfreeze=13 --threads=4`, in order, one at a time.
3. **Pass.** The control as in 1. Per D: converged (max|F| <= 1e-50, or the accepted stall max|F| <= 1e-44) or not; the start's and the end's max|F|; the number of Newton steps; Delta_released - Delta_held (the record's `diff`, Delta_full - Delta_start) where it converges. The last D that converges is named, and so is the first that does not; a missing D in between (converges at 75, not at 74) is reported as it is.
4. **What a stop is.** A run that does not converge stops at `--it_max=12` or at a stalled Newton step, and its record carries the |F| it stopped at; that |F| is reported and nothing is tuned (no other `--tol`, `--it_max` or start).
5. `compare_control.py` (written before the runs) reads the three control records and prints the two comparisons and a verdict; `compare_control.py --selftest` plants records whose answer is known, including one that must fail.

## Summary

The planted control passes. **The full release converges at D 74, 75, 76 and 77 (max|F| 3.7e-53 to 1.1e-52, 6 to 8 Newton steps) and does not converge at D 78 and 79** (a stall at max|F| = 1.05e-20 and 1.71e-19 after 4 steps, "no trial step accepted"). The last D that converges is **77**, the first that does not is **78**. Delta_released - Delta_held, where it converges, is +4.62e-16 (D 74), +1.252e-15 (75), +2.432e-15 (76) and +4.062e-15 (77), growing by factors 2.71, 1.94 and 1.67.

## What ran

`run_642.py` (logs/run_642.log), BelowNormal, one run at a time, `--threads=4`, `OPENBLAS_NUM_THREADS=1`, `--kfreeze=13`, quad-double, defaults for `--tol 1e-50`, `--tol_accept 1e-44`, `--it_max 12`; venv-t151 (Python 3.10, hpkernel from before #523), worktree `choptuik-i642` at main efe05840. The three control runs took 24 s, 32 s and 1 s (06:35:39 to 06:36:35 UTC), the six states 46 s to 100 s each (06:36:52 to 06:43:49 UTC). Inputs are read in place from the raw repository's origin/main: `T81/conv_pin5_D73.0000_D73.000000.npz` and `T138-win2/chain/anm_pin3_D7X.0000.npz` (M 32, kt 36, kc 146, ks 130; the chain states are held, `kfreeze` 3 and `pin_held` 5, 7, 9, 11, 13 in their metadata). The records are `release.jsonl` (the six states) and `control_*/release.jsonl`; the released states `released_kf13_D*.npz` of the four converged D are kept here.

## The planted control (`python compare_control.py`)

| run | max abs F at start | Newton steps | max abs F at end | Delta_full | Delta_full - Delta_start |
|---|---|---|---|---|---|
| unperturbed (`--perturb=0`) | 1.18e-35 | 3 | 2.59e-53 | 1.781239681930926192607359939054672495841 | -8.387e-28 |
| perturbed by 1e-10 | 9.85e-11 | 4 | 2.95e-53 | 1.781239681930926192607359939054672495841 | -8.387e-28 |
| perturbed by 1e-10, `--it_max=0` | 9.85e-11 | 0 | 9.85e-11 | 1.78123968193092619260735993989335692491 | 0 |

The perturbed release equals the unperturbed one: |dDelta| = 0 to the 40 digits of the records (limit 1e-25) and the largest difference of the end coefficients of harmonics 5, 7, 9, 11, 13 is 0.0 (limit 1e-20). The no-release run has the same Delta to 8.39e-28 (it is below the 1e-25 limit) but its coefficients are 1.00e-10 off (limit 1e-20), so it fails the coefficient test, as it must. The control fails the right run: the Delta test alone would not see the unreleased state, the coefficient test does. **CONTROL PASSED.** `compare_control.py --selftest` plants an equal pair (passes), a pair 1e-12 off in Delta and a pair 1e-10 off in one coefficient (both fail).

The unperturbed release moves Delta by -8.387e-28 here; the docstring of `release_held.py` gives -2.8e-23 for the same state on the Mac. The Taylor steps are planned afresh at each run, and AGENTS.md notes that hp's computed plans depend on libm's `pow`, which differs between macOS and Windows; I did not test whether that is the cause, but the floor of the comparison with the state's own Delta is evidently platform dependent. Here it is 8.4e-28, far below every Delta_released - Delta_held in the table (4.6e-16 and up).

## Results (`table_642.txt`)

| D | converged | max abs F at start | max abs F at end | Newton steps | seconds | Delta_released - Delta_held | max change of held coefficients | harmonic |
|---|---|---|---|---|---|---|---|---|
| 74 | yes | 2.41e-25 | 3.69e-53 | 6 | 45.8 | +4.623e-16 | 1.81e-10 | 13 |
| 75 | yes | 6.16e-25 | 5.19e-53 | 7 | 53.8 | +1.252e-15 | 3.78e-10 | 13 |
| 76 | yes | 1.13e-24 | 5.00e-53 | 7 | 53.8 | +2.432e-15 | 5.92e-10 | 13 |
| 77 | yes | 1.79e-24 | 1.11e-52 | 8 | 61.1 | +4.062e-15 | 8.21e-10 | 13 |
| 78 | no | 2.56e-24 | 1.05e-20 | 4 | 99.5 | not a value (stalled iterate +6.198e-15) | (stalled iterate 1.06e-09) | 13 |
| 79 | no | 3.49e-24 | 1.71e-19 | 4 | 99.3 | not a value (stalled iterate +8.885e-15) | (stalled iterate 1.32e-09) | 13 |

last D that converges: 77.0; first D that does not: 78.0

The coefficient column is how far p1's held harmonics (5, 7, 9, 11, 13; cos and sin) move from the fitted values to the full solution, largest at harmonic 13 throughout: 1.8e-10 at D 74 growing to 8.2e-10 at D 77. At D 78 and 79 the stalled iterate has moved by 1.06e-9 and 1.32e-9, and its Delta difference (+6.2e-15, +8.9e-15) continues the sequence of the converged ones, but it is not a value of a converged system.

How a stop looks (`logs/D78.log`, `logs/D79.log`): the first Newton step takes max|F| from 2.6e-24 to 1.8e-14 (D 78) and from 3.5e-24 to 6.1e-14 (D 79), the second brings it to 1.15e-20 and 2.1e-19, the third changes it by 9% (1.05e-20) and 18% (1.71e-19), and the fourth finds no trial step it accepts. At D 74 to 77 the third and fourth steps keep reducing |F| (5.9e-29 to 4.4e-29 to 5.1e-46 at D 74). The smallest pivot of the Newton matrix is 3.3e-16 at D 78 and 1.4e-15 at D 79 after the first step, against 3.5e-16 at D 74 and 1.0e-16 at D 75 and 76: it does not mark the frontier.

## Controls

- The planted control as above, passed, with the run that must fail failing the coefficient test.
- **Not run:** a second implementation of the release, the rounded projector (win's kernel is from before #523; the coordinator states the projectors agree below D 215), any D between the integers, and any start other than the chain's.

## Discrepancies

`notes/HELD_HARMONICS.md` 13.19 placed the frontier near 79 on the rounded projector (the issue text). Here the first D that does not converge is 78 and D 79 does not converge either; win's kernel is from before #523, so these runs use the rounded freeze projector (the coordinator states that the exact and the rounded projectors agree below D 215, so the issue's "exact projector" is not tested separately here). The frontier is therefore 77 to 78 against "near 79", a difference of one or two in D that I cannot explain, from one run per D and one start. The unperturbed D 73 release moves Delta by -8.4e-28 here against -2.8e-23 on the Mac (above).

## Recommended tasks (for the coordinator)

1. **Is the frontier between 77 and 78 a property of the system or of the start?** What: at D 77.5, then 77.25 and 77.75, from the chain's held state (or a state interpolated between the D 77 released state and the D 78 held one), the same release; and the D 78 release from the D 77 released state `I642-win/released_kf13_D77.0000.npz` (a continuation start, not the held one). Why: the chain's held fit starts the release 1e-9 away in the harmonics it holds; a better start may converge at D 78. Acceptance: converged or the stall's |F| at each, the control repeated. Depends on #642.
