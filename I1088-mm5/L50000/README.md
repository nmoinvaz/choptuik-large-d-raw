# I1088-mm5/L50000: D 50000 held at L = 20, direct solve (#1088)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1088

Order of coordinator t5 (relayed unchanged from the jump agent): D 50000 by a direct solve, last node at L = 20 (x_l
0.706965340034678, hmob 124.995, ks 27918), held system (harmonics 5-13 at the guess's values), with the precision
ladder. Code: `~/Source/choptuik-formsq` at 1ccd32ab (the build of I1088-mm5/build/ and of L8000 and L20000).

- `inputs/`: the guess's three source states, copied here and pinned by git blob (verified with `git hash-object`):
  `lastnode_D5656.8542_step_chord0.npz` (blob 61f776a24e1165643ab21ac44662fcaaddd68831, from
  `I1088-dh370/L5657c/`; D 5656.85, ks 7372), `D10000_converged_step.npz` (blob f4cd82c0e85b9873f16be13739fc0c3b0742c8d7,
  from `I1088-mac-a/form_s/ks_scan/`; D 10000, ks 13018) and `lastnode_D20000.0000.npz` (blob
  0ec5aba927a9475f7d13e96e9c736a923f5c9051, this machine's `I1088-mm5/L20000/`; D 20000, ks 11416).
- Guess, from `~/Source/choptuik-formsq/hp`, `~/venv-314`'s python:

      python -u form_s_lastnode.py guess <this folder> --D 50000 --states_s "<inputs>/lastnode_D5656.8542_step_chord0.npz,<inputs>/D10000_converged_step.npz,<inputs>/lastnode_D20000.0000.npz" \
        --xl 0.706965340034678 --mob 124.995 --ks 27918 --threads 9 > guess.log

- Solve, with OPENBLAS_NUM_THREADS=2, nice 10, detached (a new session under `timeout 30h`, a safeguard that the pilot stop
  below makes moot):

      python -u form_s_lastnode.py solvestate <this folder> --state <the guess here> --ks 27918 --threads 9 --ladder dd,qd \
        --it_max 2 --it_hi 3 --chord 1 --step_est 7500,2700 --delta_tol 1e-15 \
        --tc 1.64410123966582504:1.82e-9 --commit 1ccd32ab > lastnode.log

## Bars (written 2026-11-26 06:31 UTC, before the guess and the run)

| item | bar |
|---|---|
| guess | the horizon block's max \|F\| at most **1e-9**. If it is over, the report goes to the coordinator and the solve is not started |
| stop | Delta's first-order bound (gain x octo-double max \|F\|) at most **1e-15**. The gain is about 2.5e11, so max \|F\| must reach about 4e-27; two qd chord steps should give that. The ladder's floor stop: a step that cuts max \|F\| by less than 10x ends its stage |
| stop rules (built in) | at most 2 dd steps, then at most 3 qd chord steps with the last dd Jacobian; then the octo-double check, the discretization tails and the Hamiltonian check; `direct_s.jsonl` only if converged |
| tails | gain x \|dF\| at most **1e-15** for each tail (kc + 20, ks + 200, halved Taylor steps). The gain \|dF\| column is read, not the printed 1e-25 bar |
| Track C | 1.64410123966582504 +- 1.82e-9, expected near -8e-10: reported, not a bar. The "+-" is Track C's own error estimate; this compares a held solve with a series fit and is not an enclosure |
| pilot stop | dd step 0 still running 16 h after it starts: the run is stopped and reported |
| not met | if a bar is missed the run ends at its stop rules, the record is not written and nothing is loosened |

Predicted times (the coordinator's):

| phase | estimate |
|---|---|
| guess | 1 to 5 min |
| dd steps 0 and 1 | about 2 h each (`--step_est` 7500 s) |
| qd start residual | about 45 min |
| each chord step | about 45 min (`--step_est` 2700 s) |
| od end check | about 4 to 5 h |
| tails | about 2 h |
| total | about 12 to 14 h |

A step more than 50% past its predicted end is reported with the log's last lines. The folder is pushed at each step.
The Delta - Track C differences below come from `diff_trackc.py` (copied from L20000) on the log's digits, never by hand.

## Results (2026-11-26 13:16 UTC)

The solve: started 06:36:14 UTC, stopped by hand at 13:04:45 UTC (SIGTERM to the `timeout` pid 14770, python 14771) once chord step 1 met the bound, on the coordinator's order; the
end checks were run by `form_s_lastnode.py checkstate` (checked_by "checkstate") on the saved step state, on the relaxed kernel. Delta - Track C below is by script
(`diff_trackc.py`, mpmath) from the digits.

| step | max \|F\| | \|dz\| | dDelta | gain | gain x \|F\| (the bound) | time | Delta - Track C |
|---|---|---|---|---|---|---|---|
| guess | 7.854e-12 (dd) | | | | | | |
| dd 0 (fresh J) | 7.854e-12 -> 5.694e-21 | 1.49e-10 | -1.493e-10 | 2.12e11 | 1.21e-9 | 6421.6 s | -8.1731e-10 |
| dd 1 (fresh J) | 5.694e-21 -> 5.097e-22 (11.2x, the 2-step cap) | 6.11e-13 | -6.112e-13 | 2.14e11 | 1.09e-10 | 6522.1 s | -8.1792e-10 |
| qd chord 0 (last dd J) | 1.572e-21 (the qd residual of the dd state; start 55 min) -> 1.617e-24 (972x) | 1.59e-14 | +1.590e-14 | 2.14e11 | 3.46e-13 | 3177.2 s | -8.179e-10 |
| qd chord 1 | 1.617e-24 -> 1.674e-27 (966x) | 9.47e-18 | -9.466e-18 | 2.14e11 | **3.58e-16** | 3166.3 s | **-8.179e-10** |

- Delta: **1.644101238847922219139403432362086469533**; Delta - Track C (1.64410123966582504 +- 1.82e-9, Track C's own error estimate; a held solve against a series fit, not an enclosure): **-8.17903e-10**.
- The saved step state `lastnode_D50000.0000_step.npz` (step_it 1, qd, step_F 1.674253245297557e-27; gain 213815129674.55933) is the record's state.

End checks (checkstate, 13:04:48-13:15 UTC; `checkstate.log`; `hpkernel` `~/Source/fastmul4-site` (relaxed kernel, kernel recorded in `direct_s.jsonl`), code `~/Source/choptuik-check` = a3888ffe + 9bcfe8ba):

| check | value | bar | verdict |
|---|---|---|---|
| octo-double max \|F\| | 1.674e-27 (191 s; the qd value) | | OK |
| Delta's first-order bound (gain 2.14e11) | 3.58e-16 | 1e-15 | **OK** |
| kc + 20 | \|dF\| 0, gain \|dF\| 0 | gain \|dF\| <= 1e-15 | OK |
| ks + 200 | \|dF\| 3.3e-57, gain \|dF\| 7.1e-46 | gain \|dF\| <= 1e-15 | OK |
| halved Taylor steps | \|dF\| 3.9e-40, gain \|dF\| 8.4e-29 | gain \|dF\| <= 1e-15 | OK |
| Hamiltonian code check | a rows up to 3.3e-31 | | OK |
| top theta harmonic (M 32), relative | 3.6e-19 (field mh) | | a size at M 32, not a residual change (D 1000's M 48 test: harmonics beyond h17 move by up to 1e-19) |

- ks 27918 (about 1.4 n at n = 49998... at n/2 = 24999 the fast mode enters the horizon series; ks 27918 is 1.12 n/2): the `ks + 200` tail changes max \|F\| by 3.3e-57 only.
- The record (`direct_s.jsonl`, checked_by "checkstate", commit 9bcfe8ba, kernel fastmul4) is for the **held** system (harmonics 5-13 at the guess's values), as the earlier L = 20 solves.
- The kernel was the 1ccd32ab build for the solve (dd and qd residuals, the old reciprocals in dd) and fastmul4 (relaxed horizon) for the end checks; the 1e-15 bound holds at this gain either way (coordinator).
- The stop of the solve was by hand after chord step 1's line, so the process never ran its own od check: the exit code of the solve is not meaningful.
- Files: `lastnode.log`, `lastnode_solvestate.jsonl`, `direct_s.jsonl`, `checkstate.log`, `lastnode_checkstate.jsonl`, `lastnode_D50000.0000_step.npz`, `lastnode_D50000.0000_J.npz`, `guess_D50000.0000.npz`, `inputs/`.
