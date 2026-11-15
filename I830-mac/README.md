# I830-mac: Newton's Delta-step spread under 1e-65 horizon perturbations against D (240 to 252.6)

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/830.

Code: branch `wip/i830` at 01c5df20 (`hp/step_spread.py`, on main 365d1bca), worktree
/Users/nathan/Source/choptuik-large-d-830. Build: main 3c35f0c's hpkernel (i599/site2), as #823 and #827. 3 threads,
nice 10, one job at a time (queue.sh).

Inputs: #603's states `I603-win2/chain/anm_pin3_D{240.1244,245.6366,250.1676}.npz`; D 252.6135 is #827's run
(`I827-mac/spread.json`, raw 504238d3); #805's p_min from `I805-mac/table.json` at raw fe89a58a, copied here as
`table805.json`.

## Plan and criteria (written by 2026-11-15 07:49 UTC, before the runs)

At each D, step_spread as #827: the plain pinned Newton step unperturbed, then again (`--repeat 1`), with m_h and a_h
perturbed by 1e-65 relative over seeds 1-4, and with the centre and each node (and Delta) perturbed alone (seed 1).

- **Checks at each D** (exit 1 on failure): the unperturbed step taken again has the same eight parts of its Delta
  part and the same smallest pivot; the centre's and every node's Delta step equal the unperturbed one as a double.
  The repeat check's control, `--mutate repeat` (the second step's centre perturbed by 1e-65), runs first at D 240
  and must fail. D 252.6 has #827's check against the recorded step (exact) instead of the repeat.
- **The spread** at each D is the largest |dDelta(seed) - dDelta(unperturbed)| over the four seeds, exact from the
  steps' eight parts (the seeds' standard deviation is reported beside it). It was fixed before the runs.
- **The fit** (`step_spread.py sum`): the slope of log(spread) against D over the four D by least squares, compared
  with #805's 1.44, and with the slope of log(2.2e-37/p_min) at the same four D (1.29 from the table).
- **The ratio** spread / (2.2e-37/p_min) at each D, with p_min from #805's table, in #808's bands: within a factor 3
  (1/3 <= ratio <= 3), below 1e-2, or between.
- The rules' self-test passes, and `--mutate=bar` and `--mutate=band` fail: selftest*.log, run before the queue
  (exit 0, 1, 1).

The ratios the plan expects to compare against: 2.2e-37/p_min is 3.0e-14 at 240.1244, 5.0e-11 at 245.6366, 2.1e-8 at
250.1676 and 3.0e-7 at 252.6135. #827's spread at 252.6135 is 4.18e-8, a ratio of 0.138 (between).

Estimate: the control 2 steps, then 13 steps per D at 3-4 min, about 2.4 h in all.

## Runs

| run | result | exit |
|---|---|---|
| `selftest`, `selftest_bar`, `selftest_band` | PASS, FAIL, FAIL | 0, 1, 1 |
| `repeat_control` (D 240.1244, `--mutate repeat`) | the second step's parts NOT the same: FAIL, as required | 1 |
| `spread_D240.1244` (07:56–08:59 UTC) | repeat pass, controls 6 of 6 pass; determined | 0 |
| `spread_D245.6366` (08:59–09:43 UTC) | repeat pass, controls 6 of 6 pass; not determined | 0 |
| `spread_D250.1676` (09:43–10:24 UTC) | repeat pass, controls 6 of 6 pass; not determined | 0 |
| `sum` | below | 0 |
| `diag_parts` (10:26–10:37 UTC, post hoc) | below | 0 |

## Results (2026-11-15 10:40 UTC)

**First, post hoc: the four-part read.** The I603-win2 chain states store eight parts (parts 4-7 up to 1.9e-65), and
`planted`, `proj_shift` and `step_spread` read them with `load_q`, four parts. `diag_parts.py` compares the two reads
in planted's own system (`diag_parts.log`):

| D | max part dropped | pinned max\|F\|, four-part | pinned max\|F\|, eight-part | step's dDelta, four-part | step's dDelta, eight-part | smallest pivot, four / eight |
|---|---|---|---|---|---|---|
| 252.6135 | 1.887e-65 | 3.5827e-20 | 3.5827e-20 | +3.311084859e-8 | **+1.100878052e-5** | 7.095e-29 / **7.287e-31** |
| 240.1244 | 1.875e-65 | 2.2158e-20 | 2.2158e-20 | +1.182305177e-12 | +1.182296448e-12 | 7.303e-24 / 7.306e-24 |

- The residual is the same in both reads, so planted's 3.58e-20 is its rebuilt system's (held values as floats, the
  plan made at the state) and not the truncation's. #805's table has these states at 1.7e-66 and 5.6e-92 in the
  chain's own systems. Which of the two (plan or held values) makes the difference is not measured.
- The step is not the same. At 252.6135 the eight-part state's step is #816's "projected" step, +1.100878e-5, and
  its smallest pivot is #805's p_min, 7.287e-31. So #823's 332-fold change between the "unprojected" and "projected"
  steps is the four-part read's. The switch-0 projection with `refine_o` moved the horizon data by 1.7e-65 and put
  them back near their eight-part values. At 240.1244 the two reads' steps agree to 7.4e-6 relative.

**The spread against D** (`sum.log`; the spread is the largest |dDelta(seed) - dDelta(unperturbed)| over four seeds,
exact; E = 2.2e-37/p_min with #805's p_min):

| D | unperturbed dDelta | spread | seeds' sd | smallest pivot here | #805's p_min | E | spread / E | band | verdict (1e-3) |
|---|---|---|---|---|---|---|---|---|---|
| 240.1244 | +1.1823e-12 | 5.609e-16 | 3.13e-16 | 7.303e-24 | 7.306e-24 | 3.011e-14 | 0.0186 | between | determined |
| 245.6366 | -3.0437e-11 | 3.651e-10 | 2.38e-10 | 3.263e-27 | 4.374e-27 | 5.029e-11 | 7.26 | between | not determined |
| 250.1676 | -1.1079e-7 | 4.228e-7 | 1.71e-7 | 6.015e-29 | 1.069e-29 | 2.059e-8 | 20.5 | between | not determined |
| 252.6135 (#827) | +3.3111e-8 | 4.179e-8 | 1.33e-8 | 7.095e-29 | 7.287e-31 | 3.019e-7 | 0.138 | between | not determined |

The slope of log(spread) against D over the four points is 1.5585, against #805's 1.44 (ratio 1.08) and against
1.3015 for log(E) at the same four D (ratio 1.20). Every ratio is in neither registered band.

## Reading (inferred, not shown)

- The spread grows with D at about the rate of 1/p_min, but scatters about it by a factor of 1100 (0.019 to 20.5).
  With four seeds per D, a spread is the largest of four draws, not an error bar. The bands cannot settle the
  question, and nor can this data.
- The steps were taken at the four-part reads, whose smallest pivots exceed #805's p_min by 1.3x at 245.6, 5.6x at
  250.2 and 97x at 252.6. So above 245 these spreads are of a different point's step than the chain's own. A rerun at
  the eight-part states is the like-for-like test.
- At 252.6135 the eight-part state's step (+1.10e-5) lies 260 times farther from the four-part one than any of the
  four seeds' steps. Restoring the dropped parts is not a random-sign perturbation of the same size. It moves the
  point back onto the chain's own state, where the pivot is 97 times smaller.

## Discrepancies

1. Every "truth" of #713's s0_D252, #777, #816, #817, #823, #826, #827 and #830 is a four-part read of an eight-part
   state. Their residual (3.58e-20 at 252.6135) is unaffected, but their first step's Delta part and pivot are not.
   #823's "projection effect" is this read's effect. Runs on four-part states are unaffected: #468, #504, #523, #555,
   #644, #674, #709, od-corrector-mac, and #713's D 200 runs (raw logs searched at f1dc6ff3).
2. planted's pinned system leaves the chain's converged states at 2.2e-20 (D 240) and 3.6e-20 (D 252.6), against
   1.7e-66 and 5.6e-92 in the chain's systems (#805). So "the truth" has never been a root of planted's system at
   these D.

## Recommended tasks

1. **Read eight parts where the file has them.**
   - What: `planted`, `wall` (for eight-part predictions), `proj_shift` and `step_spread` read states with `load_o`.
     A check fails when an eight-part file is read in four parts.
   - Why: the four-part read moves the horizon data by 1.9e-65, and at D 252.6 that changes Newton's Delta step
     332-fold (discrepancy 1).
   - Acceptance (can fail): at 252.6135 planted's step from the eight-part read is +1.100878052e-5 (this folder), and
     a forced four-part read of the same file fails the new check.
   - Estimate: the code, then minutes. Depends on #830.
2. **planted's system against the chain's.**
   - What: rebuild planted's pinned system as the chain's attempt built it (its stored plan, held values carried in
     eight parts as anm_run.py --held_o 1). Measure the eight-part state's residual there, and which of plan and held
     values moves it from 5.6e-92 to 3.6e-20.
   - Why: discrepancy 2. No Newton test "from the truth" is one while the truth is 3.6e-20 off its system's root.
   - Acceptance (can fail): the rebuilt system's residual at the state is within 1e3 of #805's od_F at 240.1244 and
     252.6135, or the cause is named.
   - Estimate: under 1 h at 3 threads. Depends on #830.
3. **#830 again at the eight-part states**, once task 1 is in. Same seeds, same bands, step_spread's own repeat check.
   About 2.5 h.
