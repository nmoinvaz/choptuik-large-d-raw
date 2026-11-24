# I1085-mac: is the falling regular Jacobian mode of the l = 1 legs the lambda_1 eigenmode? Overlaps on stored states

Machine: Nathan's Mac (macOS, Apple silicon), one process at nice 10, 2 BLAS threads (Accelerate).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1085 (from #1025).
Plan and predictions, written before any overlap was computed: issue comment 7138890561 (17:14 UTC 2026-11-24).

## Code

`solver/matter/ell_overlap.py` on branch `wip/l1-branch-overlap` of choptuik-large-d. It was first committed at
04b0bbe6 (parent 48c36355 = wip/ell1-highD, the legs' code). The docstring gives the method, the checks and the reading.

## Amendment before real data (17:22 UTC)

The planted P1 case (H true by construction) did not reach the reading "consistent with H" under the first rule. The
reason is the residual rho = |J (P_e v1, 0)|. The computed v1 is mostly junk (88% of its weight lies in J's numerical
null space), and its rounding in J's large directions floors rho near 1e-9: rho / sigma_m came out 12, against the bar
of 3. O was 0.983, with the controls at most 0.155.

rho / sigma_m was therefore replaced in the reading by W_far: the junk-free weight of (P_e v1, 0) on J's right singular
vectors with sigma >= 100 sigma_m. The new reading:
- consistent with H if O >= 0.9, W_far <= 0.01 and every control <= 0.3;
- refuted if O <= 0.3 or W_far >= 0.5;
- otherwise no verdict.

The planted lambda_1 bar became 1e-4. A weak mode's lambda_1 is conditioned like eps |M| / slope, which is 1e-5 at
slope 1e-10; P1 found 0.7999972. This was done before any state was run.

`planted.log` (exit 0):

| case | O | W_far | reading |
|---|---|---|---|
| P1 | 0.983 | 7.5e-19 | consistent with H |
| P2 | 0.054 | 0.992 | refuted |
| P1b (spacing as k_c 87) | 0.949 | 2.3e-16 | consistent with H |

The three mutations each make the planted test exit 1: `planted_mutate_border.log`, `planted_mutate_trans.log` and
`planted_mutate_vec.log`.

## States (pinned by blob)

| k_c | D | state (blob) | record (blob) | lambda_r, bracket | falling mode |
|---|---|---|---|---|---|
| 87 | 21.125 | `I1025-dh370/kc87_leg/sol_l1kc87Ldh370_D21.125000.npy` (078ab7d8) | `l1kc87Ldh370.jsonl` (07eef60f) | 0.8771076154 (`I1025-macm3/kc87_leg_lambda/21.125`), (0.875, 0.880) | sv_reg_small[1] |
| 87 | 21.75 | `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.750000.npy` (f99f513b) | `l1kc87Lmacm3b.jsonl` (4cac8c31) | 0.646846 (`I1025-macm3/kc87_leg_lambda/21.75`), (0.645, 0.650) | sv_reg_small[1] |
| 79 | 21.375 | `I1025-win2/kc79_leap/states/sol_l1kc79Lw1025g_D21.375000.npy` (f7b6d0b5) | `l1kc79Lw1025g.jsonl` (e52b6afd) | 0.787758 (`I1025-dh610/kc79_leg/D21.375`), (0.785, 0.790) | sv_reg_small[1] |

The falling mode is the mode tracker's m1 (`I1025-win2/kc71_leap/mode_tracker.py`). At k_c 79 it is sv_reg_small[2]
up to D 21.34375. At D 21.375 it is sv_reg_small[1], after n_null went 71 -> 72.

The command per state, from `solver/matter`:
`ell_overlap.py run REC STATE D LAM_R LO HI --mode 1 --out I1085-mac/runs.jsonl`.
Its log is `run_kc<kc>_D<D>.log`.

## What ran, in order (all at nice 10 with 2 BLAS threads, one process at a time)

| file | code | what |
|---|---|---|
| `run_kc87_D21.125.log`, `runs.jsonl` | 04b0bbe6 | the posted test. Reads "no verdict"; the controls fired (wrong-lambda 0.651, 0.723 > 0.3); R1 (matvec) and the sv bar missed their first bars; 614 s, peak RSS 3.71 GB |
| `run_kc87_D21.75.log` | 9fda3676 | started, then stopped by the agent after 31 s, when D 21.125's controls fired |
| `diag_kc87_D21.125.log`, `diag.jsonl` | 04e20728 | \|M(lam) x\| along lambda. Its positive control failed: J's vectors carry Delta components |
| `floor_kc87_D21.125.log`, `floor.jsonl` | 04e20728 | R1's rounding floor 1.25e-10 (R1 7.76e-11); the full M(0) equals J[:n, :n] bitwise |
| `floor_kc87_D21.125_mutate_r1.log` | 41f9194e | under the 10 x floor bar alone the mutation passed (exit 0), so the bar now also requires the full matrices to agree (d91193d2) |
| `floor_kc87_D21.125_mutate_r1_bar2.log` | after d91193d2 | the same mutation under the new bar |
| `geom_first_kc87_D21.125.log` (first line of `geom.jsonl`) | 41f9194e | removed M(lambda_1)'s null space, which holds the lambda_1 mode itself, so its v1c lines are invalid. Its s(lam) lines are valid |
| `geom_kc87_D21.75.log`, `geom_kc79_D21.375.log`, `geom_kc87_D21.125.log`, `geom.jsonl` | 540a20aa onward | the lambda_1 mode's J vector with its Delta component; v1 cleaned of M's null space at lambda_1 - 0.05; s(lam) on span{x_m0..x_m3, t} |
| `refit_kc87.log`, `refit_kc79.log`, `refit.jsonl` | a8023dd4 onward | the falling mode's sigma against lambda_1, from the records and the scans' readings |

The planted logs above ran at 04b0bbe6.

`shares.sh` and `shares.log` give the falling mode's share of dDelta_dF^2, from the geom logs' J mode lines and the
records.

## Results (the note is `notes/L1_BRANCH_OVERLAP.md` of the code repository, branch `wip/l1-branch-overlap`)

- R1-R4 hold at k_c 87, D 21.125: the full M(0) equals J[:n, :n] bitwise, R3 2.0e-8, R4 4.6e-9.
- The posted overlap test reads no verdict, and its controls fired (0.651, 0.723, 0.925 > 0.3). The cause:
  - J's weak vectors carry Delta components;
  - the lambda_1 eigenvector lies 0.999999-1.000000 in M's numerical null space at every state (80-81 vectors at k_c
    87, 72 at k_c 79), and that space turns with lambda. So the eigenvector cannot be separated from it in float64.
- The falling mode is not a null vector of M at lambda_1: |M(lambda) x| for its unit spectral part runs from 6.1e-2 to
  9.4e-2 over lambda in [0, 1.2], with 8.1e-2 at lambda_1 (`diag_kc87_D21.125.log`).
- At none of the three states does sigma_min(M(lambda) Q) dip at lambda_1 on span{J's four weakest modes, t}
  (`geom_*.log`).
- The falling mode is J's period mode:
  - |delta| = 0.137, 0.145 and 0.138, against 0.002-0.010 for the other weak modes (except the k_c 79 cutoff mode,
    0.075 at sigma 1.44e-11);
  - it carries 0.967, 0.989 and 0.948 of dDelta_dF^2.
- At k_c 79, D 21.375 this Mac has n_null 71 (win2's record: 72), so the falling mode is index 2 here. The geom run's
  `--mode 1` statistics there refer to the record's m0. The J mode rows are complete and do not depend on the index.
- The floor control exits 1 under the bar with the Frobenius condition (`floor_kc87_D21.125_mutate_r1_bar2.log`). Its
  label "R1 <= 10 x floor: BAD" reports the combined check; the label names both bars from 9748f9fa on.
- Refit (`refit_kc87.log`, `refit_kc79.log`):
  - k_c 87, D 21.125-21.375 (7 points): p = 1.145, rms 0.58%, as the runners reported. Over 21.125-21.75: p = 1.792,
    rms 2.30%. The local exponent rises to 2.28.
  - k_c 79, D 21.125-21.375 (9 points): p = 1.207, rms 0.69%.
  - sigma x dDelta_dF is 0.134-0.153 at all 17 k_c 87 points, and 0.139-0.141 at k_c 79 from D 21.25.
  - lambda_1 = 0 extrapolated, not a result: k_c 87 at D 23.205 (parabola) or 23.390 (line); k_c 79 at D 22.861 or
    23.611.
- Peak RSS (`/usr/bin/time -l`): the k_c 87 run 3.71 GB. The largest of all runs was 4.28 GB
  (`geom_first_kc87_D21.125.log`, two SVDs of M besides J's).
