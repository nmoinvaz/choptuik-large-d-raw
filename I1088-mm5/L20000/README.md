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
  The value used is recorded in `pid.txt`: **11416** (the run started at 04:27:04 UTC on the coordinator's word).
  Coordinator's verdict, relayed by hc at 2026-11-26 04:54 UTC: the D 10^4 ks check passed (the formula's ks 5912 equals
  ks 13018 to 2e-46 in quad-double; its control at ks 5100 fires), so ks 11416 stands for D 2x10^4. The run's own ks + 200
  tail check stays the safeguard. The check's own output is in the coordinator's raw folder, not here.

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

## Results (2026-11-26 06:27 UTC)

Started 04:27:04 UTC, ended 06:27 UTC (7197 s in all; timeout pid 12148, python 12149; 14 threads, nice 10, ks 11416).
The job's exit code was not captured (it ran detached); its log ends with `converged` and the record is in
`direct_s.jsonl`. Delta - Track C below comes from `diff_trackc.py` on the log's digits (mpmath, 50 digits).

| quantity | value | bar | verdict |
|---|---|---|---|
| dd step 0 (fresh J) | max \|F\| 4.021e-11 -> 5.837e-20, \|dz\| 5.24e-10, dDelta -5.238e-10, lam 1, 877.8 s | | OK |
| dd step 1 (fresh J) | 5.837e-20 -> 1.575e-21, \|dz\| 3.79e-13, dDelta +3.786e-13, lam 1, 858.9 s (a 37x cut: the 2-step cap, not the floor) | | OK |
| qd chord step 0 (last dd J) | 6.759e-21 -> 9.796e-25, \|dz\| 1.06e-14, dDelta +1.058e-14, lam 1, 444.3 s; bound 6.73e-15, above the bar | | OK |
| qd chord step 1 | 9.796e-25 -> 1.333e-28, \|dz\| 3.35e-18, dDelta -3.351e-18, lam 1, 455.1 s | | OK |
| octo-double check, max \|F\| | 1.333e-28 (the qd value; about 31 min serial) | | OK |
| Delta's first-order bound (gain 6.87e9) | 9.16e-19 | 1e-15 | **OK** (1090x margin) |
| Delta | 1.644412437784434198116472157953837612412 | | |
| Delta - Track C | -7.96868e-10 (the log's line; Track C 1.64441243858130260, +- 1.77e-9 is Track C's own error estimate) | | inside |
| kc + 20, ks + 200 (the ks 11416 safeguard) | \|dF\| 0 and 0 | 1e-25 | OK |
| halved Taylor steps | \|dF\| 7.3e-39 (gain-weighted 5.0e-29) | 1e-25 | OK |
| Hamiltonian code check | a rows up to 1.3e-29 | | OK |
| top theta harmonic (M 32), relative | 9.2e-19 (field mh) | 1e-25 | **WATCH**: a size, not a residual change |

Delta - Track C per step (diff_trackc.py): dd 0 -7.9726e-10, dd 1 -7.9688e-10, qd 0 -7.9687e-10, qd 1 -7.9687e-10.

- Two qd chord steps were needed, as expected (one would have left a bound of 6.7e-15); both used the last dd Jacobian
  (2 formed in all). The qd residual of the dd state reads 6.759e-21 where the dd residual read 1.575e-21.
- The gain, 6.87e9, is the extrapolation's 7e9. The Delta - Track C offsets of the L = 20 solves are -5.2e-10 (D 2000),
  -6.7e-10 (D 4000), -7.5e-10 (D 8000) and -8.0e-10 (D 20000).
- ks 11416 is below the formula's 1.3 n (26018) and the D 10^4 ks check passed (above); the run's own ks + 200 tail is 0.
- Layout: last node x_l 0.706753 (L = 20), a 49.995 (hmob), ks 11416, kc 250, 2659 Taylor steps, held harmonics 5-13 at
  the guess's values (a held solve). Delta is of the held system.
- Memory: 0.4 to 2.7 GB resident.
- Files: `lastnode.log`, `lastnode_solvestate.jsonl` (one record per step), `direct_s.jsonl` (the record, state blob
  0ec5aba9), `lastnode_D20000.0000.npz` (the solved state), `lastnode_D20000.0000_step.npz` (last accepted step),
  `lastnode_D20000.0000_J.npz` (the last dd Jacobian), `diff_trackc.py`, `pid.txt`.
