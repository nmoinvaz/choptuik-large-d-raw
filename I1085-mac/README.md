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
