# I944-dh170: `--od_junk 4` on the failing first steps of the order-150 and order-160 chains

Machine dh170 (Fedora 45, i7-7700, 4 cores / 8 threads, AVX2, 31 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/944
(follow-up of #937). Depends on #935 (the 4.8.2 build, I935-dh170/) and #936 (its bits equal the chain's build at one state).

## Setup

- Code: worktree ~/Source/choptuik-large-d-935 at origin/main 043834d9. Its hpkernel is #935's build (multidouble 4.8.2,
  multishoot 3.2.0, multisolver 0.1.1, has `series_o`; hp/src, hp/python and the Cargo files are the same at 043834d9 as at
  the built cdb5a6bc). Venv ~/Source/choptuik-large-d-935/.venv.
- The chains ran on 7f88c5bb and on 423bd22d with multidouble 4.7.0 (dh170) and #911's build (dh610). The only Python change in
  anm_run.py, octo_corrector.py and reseed.py since 7f88c5bb is `--od_tangents` (default 2, the same bits as one tangent, #921).
- The command is `run944.sh`: the chain's flags (run903.sh of I903-dh170, run903c.sh of I903-dh610) with `--od_junk` set
  by the argument, `--steps 1`, `--threads 10`, `nice -n 10`, a 3 h limit by `timeout` (a run past it is killed and reported).
- Input states are copies of the committed raw files (cmp-equal to the live ones) in ~/scratch944/ with the same relative paths:
  I903-dh170/chain_k150/anm_pin3_D233.0000.npz (and D225, D226), I903-dh610/chain_k160/anm_pin3_D234.0000.npz.

## Runs, in order, one at a time

| name | state | ks | `--od_junk` | what |
|---|---|---|---|---|
| k150_junk0_ctl | chain_k150 D 233 | 150 | 0 | control on this build: stopped after the a = 1 attempt (it failed at its start in the chain) |
| k150_junk4 | chain_k150 D 233 | 150 | 4 | run 1 |
| k160_junk0_ctl | chain_k160 D 234 | 160 | 0 | control on this build: stopped after the a = 1 attempt |
| k160_junk4 | chain_k160 D 234 | 160 | 4 | run 2 |
| k150_D225_junk4 | chain_k150 D 225 | 150 | 4 | run 3, only if runs 1 and 2 converge |

## Pass criteria, written before the first run

- **Controls** (junk 0): the a = 1 attempt's start fails to project exactly as the chain's log has it (k150: predicted |F|
  1.11e+08, rung u 0.3000 not converged at |R| 1.28e+05 after 8 steps; k160: predicted |F| 1.10e+11, |R| 1.82e-05 after 8
  steps). A control that converges is a discrepancy and stops the work until the cause is known.
- **Runs 1 and 2:** with `--od_junk 4` the start of an attempt projects and the octo-double corrector ends with max|F| <= 1e-60
  ("converged" and the printed max|F|) at a = 1 or at a trial with a >= 1/64 (the step halves three times at most, so a >= 1/8)
  where the default failed. The corrector can also report converged through the junk floor (projected correction below 1e-45,
  `junk_floor`), which leaves max|F| at the junk's residual; that is not a pass of the 1e-60 criterion and is reported with its
  max|F|.
- **Run 3:** the next state (D 226) has its Delta, the eight parts summed exactly, within 1e-40 of the chain's stored
  I903-dh170/chain_k150/anm_pin3_D226.0000.npz, and max|F| <= 1e-60.

## Result of the junk probes (k150, D 233.0 toward D 234; 13:17 to 15:41 UTC, 2026-11-17)

`--od_junk 4` does not carry the step: it is empty or absent at a = 1, 0.5 and 0.25 and makes a = 0.125 worse. Default = I903-dh170's
chain_k150.log (multidouble 4.7.0); the a = 1 default is also re-run here (k150_junk0_ctl, this build).

| a (D) | default | `--od_junk 4` (this build) |
|---|---|---|
| 1 (234.0) | the start's projection fails (rung u 0.3000 stalls at \|R\| 1.28e+05 after 8 steps; predicted \|F\| 1.11e+08). The control here reproduces it: same numbers, 108 s | the same failure, 106 s (k150_junk4.log). It is raised before `newton_od` runs, so no junk freeze acts |
| 0.5 (233.5) | the start projects; first step's trials fail down to lam 1/16 (max\|F\| 7.32e-27); stalled after 3 steps, 3223 s | `0 junk directions frozen, 4 weak ones with Delta content kept`: the same first iteration as the default to every printed digit (chord max\|F\| 6.86e+06, \|dw\| 8.149e+10, lam 1/16 at 7.32e-27); stopped after 31 min (its path is the default's) |
| 0.25 (233.25) | stalled after 2 steps, 3708 s | `0 junk directions frozen`; stopped at that line (k150_junk4_a0p25, 12 min) |
| 0.125 (233.125) | **converged**: 16 steps, max\|F\| 2.1e-71, 4470 s (lam 1/4, 1/4, 1/4, 1/2, 1, ...) | `1 junk directions frozen (sigma 4e-24), 3 weak ones with Delta content kept`; lam 1/2, 1/8, 1/32, 1/64, then the stall rule (lam <= 0.04 twice) ended it after 4 steps at max\|F\| 8.1e-25, **not converged**, 4625 s |

At the base D 233.0 the polish with `--od_junk 4` finds 1 junk direction (sigma 5e-24), 3 with Delta content kept. The stall rule
`--lam_stall 0.04` is the chain's. Whether the a = 0.125 junk attempt would have converged without it is not known.

Verdict on the issue's first acceptance line: not met at a = 1 (fails before the corrector), not at a = 0.5 and 0.25 (the junk
subspace is empty, the attempt is the default's), and at a = 0.125 the default converges and the junk freeze does not.
The k160 junk probes were dropped by the coordinator's order.
