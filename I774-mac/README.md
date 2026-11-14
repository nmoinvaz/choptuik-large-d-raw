# I774-mac: the full system's Delta on the exact freeze projector, re-polished from win's pre-#523 states

Machine: the coordinator's Mac (Apple M5), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/774.
Worktree `choptuik-large-d-774` (branch `wip/i774` at main 3e096e26), `/Users/nathan/venv-314` (Python 3.14),
nice 10, 4 threads, `OPENBLAS_NUM_THREADS=1`, one job at a time (`run_774.py`, which logs each job's start, end, exit
code, wall and CPU seconds to `logs/run_774.log`).

## The two builds

| build | hpkernel | `_hpkernel` .so SHA-256 (first 16) | freeze projector |
|---|---|---|---|
| E | main 3c35f0c's build (multishoot 1.2.2, multidouble 4.2.1), session scratchpad `site2`, loaded with `PYTHONPATH` | 13b27ce3f9b60464 | exact (#523) |
| R | venv-314's installed build of 2026-11-09 | 8d271187fc694058 | rounded, as win's venv-t151 of #725-#769 |

Both run the same Python (the worktree's `hp/` at main 3e096e26; its `hp/` differs from #742's 5249c432 only in files
outside the od path, and #752 reproduced #742's lines with it) and the same multidouble Python package (main's pin
f092018d). R reproduced #742's predictions bit for bit and its log lines in #752 (raw `I752-mac/`, 77a5564b). Each
job's log starts with the hpkernel file its interpreter loads, and `run_774.py` refuses a job whose build loads the
other kernel.

## Plan, written before the runs (2026-11-14 15:48 UTC)

Every job is `anm_run.py RAW I774-mac/<job> --state <state> <flags> --steps 0 --save_base 1 --threads 4`, so it is the
base polish only, and the polished state is saved as `<job>/base_pin<k>_D<D>.npz` (eight parts). Flags
(`run_774.py --list`):

- Full system, #727's and #742's: #682's flags with `--corrector od --tol_od 1e-60 --reseed_o 3 --elim_switch 0`.
- Held, T138-win2's chain (`--kfreeze 3 --held_fit data/held_fit.json`, unchanged on main since T138's 31da699) with
  its quad-double corrector swapped for `--corrector od --tol_od 1e-60 --reseed_o 3`, as #727 swapped cont3's, and
  the default switch, which is T138's.

| job | build | state | what it gives |
|---|---|---|---|
| `C_X2c` | R | `I727-win/states/X2_on_cont3plan.npz` | **control, run first**: #727's X2c job from its start (3 Newton steps on win) |
| `E_117` | E | `I742-win/L/anm_pin13_D117.0000.npz` | D 117 on the exact projector; its first lines must equal #752's `I752-mac/logs/AB_main.log` |
| `E_113` | E | `I742-win/P/base_pin13_D113.0000.npz` | D 113 |
| `E_120` | E | `I742-win/M/anm_pin13_D120.0000.npz` | D 120 |
| `E_cont3` | E | `I682-win/cont3/anm_pin13_D99.8750.npz` | cont3 at D 99.875 |
| `E_X2c` | E | `I727-win/X2c/base_pin13_D99.8750.npz` | X2c at D 99.875 (cont3's plan, so it must agree with `E_cont3`) |
| `H_R113`, `H_R117`, `H_R120` | R | `T138-win2/chain/anm_pin3_D<D>.0000.npz` | the held states polished to 1e-60 on the rounded projector (pilot `H_R117` first) |
| `H_E113`, `H_E117`, `H_E120` | E | the same | the held states on the exact projector |

The held jobs are not in #774's list. They are here because #742's Delta_held is T138's quad-double chain (tol_qd
1e-28, pre-#523 build), so Delta_full - Delta_held "on the exact projector" needs the held side polished on it too.

**Delta of a state** is the exact sum of the last entry of its parts (Python `fractions.Fraction`, exact; `cmp_774.py`),
printed to 40 digits. This shares nothing with #739's reading (`I739-win/cmp_739.py`, arb at 600 bits), and
`cmp_774.py` first reproduces #742's 40-digit Delta at D 113, 117 and 120 and X2c's 60 digits from the stored
states, exiting 1 on a mismatch.

**Pass criteria, fixed now (#774's acceptance):**

1. Control: `C_X2c`'s polished Delta equals X2c's stored Delta (`I727-win/X2c/base_pin13_D99.8750.npz`) to 1e-50,
   and its log lines equal #727's `logs/X2c.log`. `cmp_774.py --mutate 1e-48` adds 1e-48 to the control's Delta and
   must fail. If the control fails, nothing on build E is run until the cause is known.
2. Each re-polish on build E converges: the corrector says converged, final octo-double max|F| at most 1e-60.
3. Each shift Delta_E - Delta_stored is reported with its kind: "measured" when both the stored state (on build R) and
   the E polish are converged roots of their systems at most 1e-60; cont3's stored state is quad-double, and #727's
   pilot2 showed its od polish on the rounded build takes no Newton step (Delta unchanged), so its kind says so.
4. Discrepancy bars: a shift above 1e-3 of #742's Delta_full - Delta_held at that D (4.37e-16, 4.95e-16 and
   5.32e-16 at D 113, 117 and 120) flags the notes' statements resting on #742's table, and a shift above 1e-25 at
   D 99.875 flags those resting on #725-#769's D 99.875 values (HELD_HARMONICS 4.4).
5. Table: Delta_full - Delta_held at D 113, 117 and 120 with both sides on the exact projector (E jobs), beside
   #742's (both from the stored states) and beside the rounded pair polished to 1e-60 (stored full, `H_R`).

**Expectation, written now and not a criterion:** #752's `AB_main.log` (build E, D 117) moved Delta by +1.57e-20 in
its first step, so the shifts at D 113-120 are about 1e-20, far below bar 4, and the shift at D 99.875 is probably
above 1e-25 (HELD_HARMONICS 4.4 records -2.76e-23 at D 73 between the builds), which would flag 4.4's D 99.875 values.

**Not done:** states other than these, any continuation step, any flag change beyond the corrector swap of the held
jobs. If a held polish stalls on build R with the default switch, I stop the held jobs and report.

## Addendum to the plan, written before these runs (2026-11-14 16:55 UTC)

The E jobs put the D 99.875 shift at +1.4994e-20, above bar 4's 1e-25, so the D 99.875 statements are flagged. Most of
those statements are differences between roots on different plans (#725, #727, #763, #769: about 1e-25). Whether the
differences survive needs one root on another plan on both builds. So two more jobs, beyond #774's list, with the same
flags as X2c: `R_X2` (build R) and `E_X2` (build E), both from X2 on its own plan (`I725-win/X2/anm_pin13_D99.8750.npz`,
#725). The reading: plan dependence X2 - X2c on each build (#727's -1.6580e-25 on the stored states; `cmp_774.py`
reproduces that first). If exact - rounded is below 1e-30, the differences survive and only the absolute D 99.875
values move. Otherwise both are reported. They run after the held jobs.

## Results (2026-11-14 17:45 UTC)

**Answer.** On main's exact freeze projector the full system's Δ moves by about 1e-19, on both sides of zero:
−9.60e-20 at D 113, +1.57e-20 at D 117, +7.64e-20 at D 120 and +1.4994e-20 at D 99.875. That is at most 2.2e-4 of
the 1e-3 bars at D 113–120, so #742's Δ_full − Δ_held stands to every quoted digit. At D 99.875 it is above the
1e-25 bar, so the absolute Δ of #727's root (and every state of #725–#769 there) is the rounded system's. The
differences between plans survive, though: X2 − X2c changes by −1.2e-31 of its −1.658e-25.

Every number below is from `cmp_774_out.md` (`cmp_774.py`, all checks passed) and `logs/`.

### Every job

| job | build | state | Newton steps | start max\|F\| | final max\|F\| | first-step dDelta | exit | wall s | cpu s |
|---|---|---|---|---|---|---|---|---|---|
| C_X2c | R | `I727-win/states/X2_on_cont3plan.npz` | 3 | 1.76e-35 | 2.71e-93 | +1.66e-25 | 0 | 363 | 1262 |
| E_113 | E | `I742-win/P/base_pin13_D113.0000.npz` | 4 | 2.05e-34 | 9.13e-112 | -9.60e-20 | 0 | 735 | 2601 |
| E_117 | E | `I742-win/L/anm_pin13_D117.0000.npz` | 4 | 2.01e-34 | 1.46e-106 | +1.57e-20 | 0 | 638 | 2323 |
| E_120 | E | `I742-win/M/anm_pin13_D120.0000.npz` | 4 | 1.98e-34 | 1.58e-102 | +7.64e-20 | 0 | 779 | 2804 |
| E_cont3 | E | `I682-win/cont3/anm_pin13_D99.8750.npz` | 3 | 2.20e-34 | 4.45e-69 | +1.50e-20 | 0 | 569 | 1981 |
| E_X2c | E | `I727-win/X2c/base_pin13_D99.8750.npz` | 3 | 2.20e-34 | 4.45e-69 | +1.50e-20 | 0 | 540 | 1874 |
| R_X2 | R | `I725-win/X2/anm_pin13_D99.8750.npz` | 1 | 8.59e-55 | 1.11e-77 | +5.56e-45 | 0 | 306 | 1090 |
| E_X2 | E | `I725-win/X2/anm_pin13_D99.8750.npz` | 3 | 2.20e-34 | 4.45e-69 | +1.50e-20 | 0 | 530 | 1804 |
| H_R113 | R | `T138-win2/chain/anm_pin3_D113.0000.npz` | 2 | 1.09e-35 | 9.26e-92 | -1.07e-31 | 0 | 423 | 1325 |
| H_R117 | R | `T138-win2/chain/anm_pin3_D117.0000.npz` | 2 | 7.03e-36 | 5.55e-93 | -3.33e-32 | 0 | 340 | 1192 |
| H_R120 | R | `T138-win2/chain/anm_pin3_D120.0000.npz` | 2 | 7.00e-36 | 3.22e-93 | -2.92e-34 | 0 | 446 | 1390 |
| H_E113 | E | `T138-win2/chain/anm_pin3_D113.0000.npz` | 2 | 2.43e-34 | 5.70e-73 | -3.62e-27 | 0 | 417 | 1315 |
| H_E117 | E | `T138-win2/chain/anm_pin3_D117.0000.npz` | 2 | 2.39e-34 | 1.07e-71 | -5.82e-27 | 0 | 423 | 1369 |
| H_E120 | E | `T138-win2/chain/anm_pin3_D120.0000.npz` | 2 | 2.35e-34 | 1.21e-70 | -2.48e-27 | 0 | 358 | 1280 |

"Newton steps" counts the steps taken, without the last evaluation. Every polish converged (the corrector's own
"converged", final max|F| at most 1e-60). The largest job took 2804 s of CPU (E_120), and the 14 jobs 23610 s (6.6 CPU
hours). Each start max|F| on build E is 2.0e-34 to 2.4e-34, all in the horizon block's p rows as #752 found at D 117.

### The checks

| check | result | how it can fail |
|---|---|---|
| reading: the stored states give #742's 40 digits (D 113 from `I739-win/B`, 117, 120), X2c's 57 decimals, T138's logged 12 decimals, and #727's X2 − X2c (−1.6580e-25) | all equal | it fired on its first run, when the reader truncated where #742 rounds |
| cross-check: this reading (exact rationals) against #739's (arb, 600 bits), 7 states | difference 0.0 | |
| control: C_X2c on build R against X2c's stored root | Δ difference +0.0000e+00, all eight parts bit for bit equal, the 4 Newton lines equal #727's | `--mutate 1e-48`: NOT MET, exit 1 |
| E_117's Newton lines against #752's run on build E (`I752-mac/logs/AB_main.log`) | 5 of 5 equal | |
| #742's Δ_full − Δ_held reproduced from the stored states at D 113, 117, 120 | equal to its 5 digits | |
| `cmp_774.py --selftest`: a planted eight-part Δ, a planted 1.234e-20 shift, the bars' verdicts | passed | |

### Shifts on the exact projector

| D | state | Δ on the exact projector (40 digits) | shift, exact − rounded | kind | bar | verdict |
|---|---|---|---|---|---|---|
| 113 | #742's (P's base) | 1.733640141567942734310709655625123636920 | −9.6001e-20 | measured, both converged | 4.37e-16 | below |
| 117 | #742's (L) | 1.730635685860038849282734477817859081897 | +1.5675e-20 | measured, both converged | 4.95e-16 | below |
| 120 | #742's (M) | 1.728511242950407985000366909760210225118 | +7.6410e-20 | measured, both converged | 5.32e-16 | below |
| 99.875 | X2c (cont3's plan) | 1.745150028164499252959346891093763008937 | +1.4994e-20 | measured, both converged | 1e-25 | **flag** |
| 99.875 | cont3 (the same plan) | the same, to 7.6e-98 | +1.4994e-20 | against the stored quad-double state, whose od polish on build R takes no Newton step (#727 pilot2) | 1e-25 | **flag** |
| 99.875 | X2 (its own plan) | 1.745150028164499252959346725289547222578 | +1.4994e-20 | measured, both converged (R_X2 is the rounded root) | 1e-25 | **flag** |

"Measured, both converged" means that the rounded root (stored, or R_X2) and the exact root (the E job) are each
converged to at most 1e-60 on their own build, on the same plan.

### Plan dependence at D 99.875 on both projectors

| | rounded | exact | exact − rounded |
|---|---|---|---|
| X2 (own plan) − X2c (cont3's plan) | −1.658041e-25 | −1.658042e-25 | −1.2e-31 |

The projector moves the two plans' roots alike, to 1.2e-31, so the plan dependence of #725–#769 (differences of
1e-48 to 1e-25 between plans) is not what the shift changes. This is one pair of plans. That the node-shifted plans of
#741–#769 behave the same way is inferred from it, not measured.

### Δ_full − Δ_held at D 113, 117 and 120

| D | #742 (stored full − stored held) | exact (E − H_E) | exact − #742 | held: H_E − H_R | held: H_R − stored (its convergence) |
|---|---|---|---|---|---|
| 113 | +4.365506e-13 | +4.365505e-13 | −9.600e-20 | −3.6248e-27 | −1.0744e-31 |
| 117 | +4.945575e-13 | +4.945575e-13 | +1.567e-20 | −5.8163e-27 | −3.3265e-32 |
| 120 | +5.322591e-13 | +5.322592e-13 | +7.641e-20 | −2.4780e-27 | −2.9202e-34 |

The held chain's projector shift is 2.5e-27 to 5.8e-27, eight decades below the full system's. Its smallest pivot
is 1.2e-7, against 2e-20 to 6e-20 in the full system. The T138 states are converged to 1e-31 or better in Δ though
their tolerance was tol_qd 1e-28. So Δ_full − Δ_held on the exact projector differs from #742's by the full system's
shift alone, at most 9.6e-20, a relative 2.2e-7.

### Measured and inferred

- Measured: every number in the tables above, on the two builds named, with the Python and multidouble package of
  main 3e096e26 and f092018d.
- Inferred: that win's venv-t151 kernel (2026-11-07) and venv-314's (2026-11-09) give the same rounded system. The
  control reproduces #727's X2c bit for bit, and #752 reproduced #742's predictions and lines bit for bit.
- Inferred, not explained: the shift does not vary smoothly with D (−9.6e-20, +1.6e-20 and +7.6e-20 at D 113, 117
  and 120; +1.5e-20 at D 99.875). The size fits a residual change of 2e-34 acting through pivots of about 2e-20
  (|dz| 2.7e-13 to 5.8e-13 at step 0). The sign changes would fit a rounding error of the old projector that varies
  erratically with D. Nothing here tests that.
- Not done: A1 and the node-shifted states of #741–#769 on the exact projector, and the chain's held states at other D.

### Discrepancies (reported, not fixed)

1. The absolute D 99.875 Δ quoted in notes/HELD_HARMONICS.md 4.4, 1.745150028164499252944352893640343550633 (#727),
   is the rounded system's root. The exact system's is 1.745150028164499252959346891093763008937, +1.4994e-20 away,
   above #774's 1e-25 bar. The plan differences quoted there (#725, #727, #741, #751, #754, #763, #769) are not
   affected, by the X2 pair.
2. #742's Δ_full − Δ_held at D 113–120 is not affected beyond its quoted digits (largest change 9.6e-20).

### Recommended tasks

1. **Retire or rebuild win's pre-#523 kernel for full-system runs.** What: rebuild venv-t151's hpkernel on win at
   main (or mark it not for use), then run AGENTS.md's bit-identity checks (`highm_check.py ref`, `scaled`, `jets`
   against the stored references). Why: #725–#769 ran on it, and its states solve the rounded system, which this task
   measured as 1e-19 off in Δ. Acceptance: the checks pass, with `--mutate=kappa` failing, and the next full-system run
   on win shows main's kernel in its log. Depends on: #774.
