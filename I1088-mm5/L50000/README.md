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
