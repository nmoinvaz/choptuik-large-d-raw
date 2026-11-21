# I1025-win/p4_highD: hybrid roots at D 17.5 and 17.75 on winb's own k_c 63 states (winb)

Written before either row runs (2026-11-21 03:38 UTC). Row 4 of P4 (`I1025-win/p4`, D 16.25 k_c 63) still runs; these rows start after it.

## Order

The coordinator (hc, 2026-11-21 about 03:32 UTC), after P4's three clean passes: hybrid roots past D 17 on winb's own k_c 63 states, one row at a time, by `p4_hybrid.py` with the P4 rules (system check against the record, one sign change, the edge rule, noise robust, signtest at lambda -/+ 0.02). Row A: D 17.5, `out/sol_l1kc63Fw1025_D17.5000.npy`, record in `out/l1kc63Fw1025.jsonl`. Row B: D 17.75, `out/sol_l1kc63W1025_D17.750000.npy`, record = its line in `leap_kc63.log`. Each guess and window is written here before its run, taken from the signtested k_c 63 rows' trend (2.0265465 at D 17). xfkappa takes D 18 and 18.5 on the Mac, so those are not run here. A post on #1025 after each row, with cpu and memory.

## Inputs (raw origin/main, taken by `git show`, checked with `git hash-object --no-filters`; `prep_p4hi_inputs_1025.log`)

| item | raw path | blob |
|---|---|---|
| p4_hybrid.py | `I1025-mac/p4_hybrid.py` | a402559b5d37661b49da50f07f877af21fd29b3a (the P4 rows' script) |
| signtest.py | `I1025-mac/signtest.py` | 179ea09681b0a75f7cefdff98984b48051b3f085 (with `around=` and the system check) |
| row A record | `I1025-win/out/l1kc63Fw1025.jsonl` | 7ee33d79eb195a4cbf19c71db799cb93ea92c8d5 |
| row A state | `I1025-win/out/sol_l1kc63Fw1025_D17.5000.npy` | d85f7b71c2c1750ca91d941320b9f2cdf57fe029 |
| row B line | `I1025-win/leap_kc63.log`, line 53 (equal to the D 17.75 line of `I1025-win/out/l1kc63W1025.jsonl`, blob c33039df) | 94ef7a72ed7ac963b42bb01e6b4fbd718c2f70fe |
| row B state | `I1025-win/out/sol_l1kc63W1025_D17.750000.npy` | de9fc3e55aa46bafd4ef62536861f94aed9e3035 |

Code worktree `C:/Users/nathan/Source/choptuik-i1025-lowd` at 505d839940456a3d04321d75cf66cc3b5bc831c4 (the P4 rows'), PY `C:/Users/nathan/Source/venv-md510` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble 5.1.0 at 8c4360ac).

## The two rows, their records and the stubs

| row | D | k_c | record system (what the check compares) | float64 record lambda |
|---|---|---|---|---|
| A | 17.5 | 63 | F 2.2919997574734327e-10, 2649 steps, u0 0.04, Ks 30, kappa 0.7, rk 1 | 1.974481053107075 (n_eval 28): SUSPECT, its signtest failed (raw `I1025-win` 67a15ffb, comment 7033113186), not used |
| B | 17.75 | 63 | F 2.4283364241408305e-10, 2598 steps, u0 0.04, Ks 30, kappa 0.7 (a leap state: `leap_kc63.log` line 53) | none (the leap does not solve for lambda) |

`p4_hybrid.py` reads the guess from the record line's `lam_guess` and needs a `lam` in it. So each row runs on a stub record, made by `make_stubs_p4hi_1025.py` (`make_stubs_p4hi_1025.log`):

- Stub A, `stub_rowA_l1kc63Fw1025_D17.5_trendguess.jsonl`: the D 17.5 line of `l1kc63Fw1025.jsonl` unchanged, except `lam_guess` set to the trend guess below. The record's own `lam_guess` is D 17's lambda, 2.0265465 (kept as `lam_guess_record`). Its `lam` stays the float64 record, so the output's `minus_record` is the hybrid minus that suspect value.
- Stub B, `stub_rowB_l1kc63W1025_D17.75_leapline.jsonl`: `leap_kc63.log`'s D 17.75 line unchanged, plus `lam_guess` and a `lam` equal to the guess. The `lam` is a placeholder: the output's `lam_record` and `minus_record` for row B are the guess and the root minus the guess, not a record.

## Guess and window, fixed here before the runs

The guess is the quadratic through the three signtested k_c 63 rows at equal spacing, D 16.5 (2.1454677042524617, winb, signtest passed), D 16.75 (2.0834870037231608, win2b's signtest passed, winb's record) and D 17 (2.026546497375959, signtest passed), evaluated at the row's D and rounded to 4 decimals.

| row | D | trend value | guess |
|---|---|---|---|
| A | 17.5 | 1.9277860672 | **1.9278** |
| B | 17.75 | 1.8859661434 | **1.8860** |

The search is `ell_refine.lam_root`'s, unchanged in `p4_hybrid.py`: det sign at guess * (1 + w * (-1, 0, 1)) for w = 0.02, 0.06, 0.15, 0.35 in turn, stopping at the first w with a sign change, then `brentq` inside that interval (xtol 2e-8 * guess, rtol 1e-12). Windows:

| row | w 0.02 | w 0.06 | w 0.15 | w 0.35 |
|---|---|---|---|---|
| A, guess 1.9278 | [1.88924, 1.96636] | [1.81213, 2.04347] | [1.63863, 2.21697] | [1.25307, 2.60253] |
| B, guess 1.8860 | [1.84828, 1.92372] | [1.77284, 1.99916] | [1.60310, 2.16890] | [1.22590, 2.54610] |

Other readings of the trend, for scale: linear from the last two rows 1.9127 (A) and 1.8557 (B); linear least squares over the four signtested rows D 16.25 to 17 1.9129 and 1.8558; quadratic least squares over those four 1.8965 and 1.8274; the Mac's k_c 55 value at D 17.5, 1.9522. All of A's lie inside its w 0.02 window; B's lie inside its w 0.02 window except the quadratic least squares 1.8274, which lies in w 0.06. The float64 record 1.9745 of row A lies outside the w 0.02 window and inside w 0.06. The alternative, the record's own guess 2.0265465 for row A, would start at w 0.06 ([1.9049, 2.1481]) with a bracket of 0.12.

## Pass rules (fixed before the runs)

A row PASSES if all hold (rules 5 and 6 are amended after row A: see Amendment 1 at the end):

1. record system true: steps equal and |F| within 1% of the record's or 1e-13 (amendment 5), rebuilt by `p4_hybrid.py` from the stub's `F` and `steps`;
2. one sign change on the search grid, and one over all evaluations in lambda order;
3. every evaluation's sign unchanged under 1e-15 relative noise on blocks 0 to 11 (2 seeds);
4. final bracket at most 1e-7;
5. edge rule (`check_1025.py`'s, 2026-11-20): the root is at least 0.05 grid steps from both edges of the grid interval that holds it (the grid and step are those of the first w with a sign change, read from the row's own evaluations; the distances are printed, so another bar can be read off);
6. signtest at the hybrid lambda -/+ 0.02 (`signtest.py STATE D 63 around=<the row's hybrid jsonl>:D:0.02`, with the record's u0 0.04, Ks 30, kappa 0.7, rk 1): both lines agree (the sign from an LU of M equals the signs from LUs of three random orthogonal rotations of M) and the two signs are opposite; its system line must read same true.

A row failing any of these is reported, not read. The verdict is computed by `verdict_p4hi_1025.py` and logged in `rows/verdict_D<D>.log`. A timeout (21600 s per row) or crash is reported, and the other row still runs.

## Smoke test of the system check (2026-11-21 03:36 UTC, `signtest.py ... syscheck`, 13 s each, `smoke_syscheck_A.log`, `smoke_syscheck_B.log`)

| row | F rebuilt | F in the stub | steps rebuilt | steps in the stub | same |
|---|---|---|---|---|---|
| A | 2.2919997574734327e-10 | 2.2919997574734327e-10 | 2649 | 2649 | true |
| B | 2.4280912473748936e-10 | 2.4283364241408305e-10 (1.0e-4 relative) | 2598 | 2598 | true |

## Run

`p4hi_driver_1025.sh` (a thin driver, no solver code) waits for `p4_driver_w.sh done` in P4's `p4_w.log`, then runs row A and row B one at a time: `p4_hybrid.py` on the stub, then the signtest, then the verdict. Launcher `start_p4hi_1025.cmd` (BelowNormal, 4 BLAS and rayon threads, no `nice`, so no Idle priority). Output: `p4hi_w.log`, `ell_p4_hybrid_1025_w_highD.jsonl`, `rows/D<D>.log`, `rows/signtest_D<D>.log`, `rows/verdict_D<D>.log`.

Timing, estimated from P4's k_c 63 rows (678 to 913 s per evaluation at 4 threads; 12 to 16 evaluations): about 2.3 to 3.5 h per row, plus minutes for the signtest. No RESUME: if the laptop stops, the coordinator decides.

## Status

Row A finished 2026-11-21 06:23:26 UTC (FAIL, below). Row B ran 06:23:26 to 08:46:18 (system check true: |F| 2.4283364241e-10 against 2.4283364241e-10, 2598 steps); its result is in the section "Row B" below, its dd sign check runs (Amendment 2).

### Row A, D 17.5 k_c 63: hybrid root 1.9272222575778963, verdict as first computed FAIL (edge rule and signtest); amended below

| quantity | value |
|---|---|
| guess (fixed before the run) | 1.9278; root minus guess -5.78e-04 |
| search | w 0.02 grid [1.889244, 1.9278, 1.966356], signs -1, +1, +1: one change; 8 evaluations (3 grid + 5 Brent) |
| root, final bracket | 1.9272222575778963, [1.9272222575778963, 1.927222285203896], width 2.76e-08 |
| record system | true (F 2.2935928921e-10 rebuilt against 2.2919997575e-10 in the record, 7e-04 relative, 2649 steps against 2649) |
| sign changes | 1 on the grid, 1 over all 8 evaluations; noise robust True |
| time | 6556 s, 04:18:57 to 06:08:19 UTC |
| hybrid minus the float64 record (1.974481053107075, suspect) | -4.7259e-02 |
| distance to the Mac's k_c 55 value 1.9522 | -2.4978e-02 (-1.279%) |
| edge rule (bar 0.05 grid steps from both edges of the grid interval) | root in [1.889244, 1.9278]: 0.985 steps from the lower edge, **0.015 from the upper**: FAIL |
| signtest at lambda -/+ 0.02 (float64 M, `signtest.py`) | lambda 1.907222258 and 1.947222258: signs from the LU of M and of three rotations Q M are [-1, +1, -1, -1] at both, agree False; 56 singular values below 1e-12 of the largest (44 below 1e-15); 519.5 s and 384.7 s: FAIL |

Verdict by `verdict_p4hi_1025.py` (`rows/verdict_D17.5.log`): FAIL, two checks: edge rule and signtest. The record system, one change, noise robust and the 1e-7 bracket hold. Reported, not read.

Two facts for the reader, not part of the verdict. The edge rule failed because the root lies 5.8e-04 below the guess, which is the grid's middle point and so the upper edge of the interval that holds the root; the root is not float-equal to the guess (the final bracket is 2.8e-08 wide). The signtest is the float64 test used on the records; it does not test the hybrid's double-double block. It fails at 1.907 and 1.947 as it failed at the float64 record's 1.9745 -/+ 0.02 (raw `I1025-win` 67a15ffb): 56 singular values below 1e-12 in both.

CPU and memory: the hybrid phase of row A was not sampled (a miss on my side). The signtest python (7 threads, BelowNormal) at 06:09: 1.62 cores in a 10 s sample, working set 0.09 GB (peak 0.10), private 0.32 GB (peak 0.34). Row B's python (13 threads, BelowNormal) at 06:23:58: 1.73 cores in a 10 s sample, 1.47 cores since its start, working set 0.15 GB (peak 0.17), private 0.47 GB (peak 0.49). Laptop at 06:24: CPU 48 %, 14.28 GB free of 31.83 GB, commit 23.2 GB of limit 41.3 GB, page file 1.6 GB used of 9.7 GB, C: free 43.8 GB; two other sessions' single-thread pythons (4 and 7 GB) run beside.

## Amendment 1, the coordinator's word, stamped 2026-11-21 06:30 UTC (received about 06:26 UTC by my clock), after row A's result (06:23:26) and before row B's

1. Edge rule. The coordinator's ruling of 03:36 meant the window's outer grid points only, where a root could lie outside the window. The text above (both edges of the bracketing grid interval) also catches a root next to the middle point, and the coordinator misread it when approving it at 03:39 (their error). The rule for rows A and B is the 03:36 one: the root is inside the window and at least 0.05 grid steps from its outer grid points guess * (1 -/+ w). Row A under it: grid [1.889244, 1.9278, 1.966356], root 1.9272222576 is 0.985 steps from the lower outer point and 1.015 from the upper: PASS (`rows/verdict_D17.5_amended.log`). The first-written rule's numbers (0.985 and 0.015 steps, fail) stay in that log as information. `verdict_p4hi_1025.py` is now version 2; version 1 (`verdict_p4hi_1025_v1.py`) gave the FAIL at 06:23 (`rows/verdict_D17.5.log`, kept).
2. Sign check. The float64 signtest cannot test this root: the float64 M's sign is noise past D 17, as the D 17.5 record's own failed signtest showed. The sign check moves to the full dd M: win2 runs `ell_ddm` at lambda 1.9072 and 1.9472 on this D 17.5 state (`I1025-win/out/sol_l1kc63Fw1025_D17.5000.npy`, blob d85f7b71). Row A stays pending that check. Row B gets the same treatment, at its root -/+ 0.02. The driver still runs `signtest.py` after each row and the verdict prints it, as information and not as a criterion.

Status after the amendment: row A, checks 1 to 5 and the amended edge rule PASS, dd sign check pending (win2). Row B, running.

## Amendment 2, the coordinator's order (hc, about 06:27 UTC by my clock): row B's dd sign check is mine, after row B ends

Reason: win2 already runs five dd processes at about 1.5 h each, so winb runs row B's check itself. Row A's check stays with win2.

Setup, written before row B's root is known (2026-11-21 06:31 UTC):

| item | value |
|---|---|
| code worktree | `C:/Users/nathan/Source/choptuik-i1025d`, detached at wip/ell1-highD 48c36355d1ba64de4e3112ed968fd6c034384551 (`ell_lam_signtested: winb's k_c 63 record at D 16.75 passed its signtest (#1025)`), made with `core.autocrlf=false`; `solver/matter/ell_ddm.py` |
| python | `C:/Users/nathan/Source/venv-md510` (as P4), BelowNormal |
| commands source | raw `I1025-mac/d18/d18_dd_criteria.log` at commit b2f21b10 (blob 73c6e5ba9f1feb25c2ae964d66e161c9489c8bfb), xfkappa's D 18 (B) criteria, and `I1025-mac/dd_signtest_D17.5_criteria.log` |
| state | `I1025-win/out/sol_l1kc63W1025_D17.750000.npy`, blob de9fc3e55aa46bafd4ef62536861f94aed9e3035 (the hybrid row B's state; k_c 63, Ks 30, u0 0.04, kappa 0.7, rk 1 are `ell_ddm._setup`'s settings, the records') |

The criteria file's commands, quoted (its D 18 state and lambda in place of mine):

- `ell_ddm.py selftest must PASS, and ell_ddm.py selftest --mutate=slices must FAIL; otherwise stop.`
- `ell_ddm.py det STATE 18 63 1.788704083622953,1.8 --noise 1e-24,1e-20,1e-16 (5 exact variants; noise on the dd propagator entries, 2 seeds).`
- `A sign counts: dd, if its 5 variants agree and 1e-24 noise leaves it unchanged (both seeds), as in dd_signtest_D17.5_criteria.log.`
- Stops there: `selftests 1800 s each; ... the dd det 10800 s`. The `--mutate=hionly` information run of that file is not part of this order and is not run.

Selftests, run now (from `solver/matter`, 2 threads, `rows/ddB_selftest_ddm.log`, `rows/ddB_selftest_ddm_mutate_slices.log`, 06:28:43 to 06:28:45 UTC): `ell_ddm.py selftest` PASS (exit 0: operators 4.2e-16, 2.2e-16, 8.7e-18, 5.2e-18, 3.5e-16 against the bar 1e-14; Ozaki product 6.2e-30 against 1e-28; dual derivative 4.4e-32 against 1e-28); `ell_ddm.py selftest --mutate=slices` FAIL (exit 1: Ozaki product 3.0e-14 against 1e-28, BAD), as wanted.

Run, fixed before row B's root is known:

1. When `p4hi_w.log` shows `row B D 17.75: hybrid done`, `ddB_driver_1025.py` reads the root from `ell_p4_hybrid_1025_w_highD.jsonl` and starts two processes in parallel (4 BLAS threads each, BelowNormal): `ell_ddm.py det <state> 17.75 63 <root - 0.02> --noise 1e-24,1e-20,1e-16 --out rows/ell_ddm_B_D17.75_lo.jsonl` and the same at `<root + 0.02>` (`..._hi.jsonl`), logs `rows/ddB_lo.log`, `rows/ddB_hi.log`. If the hybrid row has no root the driver stops and says so.
2. Cap 3 h (10800 s) each. At the cap the driver kills the process it started by its exact pid (`taskkill /PID <pid> /T /F`: the venv launcher and its child, both by pid, never by name). The pids are logged in `ddB_w.log`. Selftest of that runner (a 3 s child ends, a 600 s child is killed at a 6 s cap, 0 left alive): `ddB_driver_selftest.log`.
3. Reading, fixed now (the coordinator's): minus at the lower point and plus at the upper means the root passes; the same sign at both means no root between them. A dd sign counts only if its 5 exact variants agree and 1e-24 noise leaves it unchanged (both seeds); 1e-20 and 1e-16 are information. If a sign does not count at either point, neither reading applies and that is reported. `read_ddB_1025.py` reads the two records (planted cases: root passes, same sign, a disagreeing variant, and a lambda mismatch; `vtest` not published).
4. The float64 `signtest.py` of the main driver still runs after row B and is information only. The hybrid's verdict line says `dd sign check PENDING` until this reading.
5. Post on #1025 with cpu and memory when it ends.

Row B is at its hybrid phase (started 06:23:26). Estimated: hybrid ends about 08:15 to 08:50, the dd runs about 1 to 3 h after that.

## Amendment 3, the coordinator's word, stamped 2026-11-21 07:33 UTC (received about 07:32 by my clock), ruled before any dd result existed

Why it was asked: row B's hybrid grid (w 0.02, guess 1.8860) read +1 at 1.84828, -1 at 1.886 and -1 at 1.92372, one change with plus below and minus above, while row A and the four P4 rows read minus below and plus above. The reading fixed in Amendment 2 (minus at the lower point and plus at the upper means the root passes) covers only the second orientation. I asked at 07:2x UTC, before the dd records existed, and proposed the reading below.

Reading, accepted: the root passes if the two counting dd signs are opposite, in either orientation, and each equals the hybrid's sign at the hybrid evaluation nearest that point (the hybrid's own evaluations, `ell_p4_hybrid_1025_w_highD.jsonl`). The same sign at both means no root between them. A sign that does not count (5 exact variants disagree, or 1e-24 noise changes it) means neither reading applies. Opposite counting signs that differ from the hybrid's nearest ones are reported as the dd disagreeing with the hybrid, not as a pass. The counting rule, the points, the commands and the caps of Amendment 2 are unchanged.

The orientation is reported as information. The coordinator's note: at D 18 win2's dd signs read -, +, - at 1.7529, 1.7887 and 1.8245, so two roots, and the upper one has row B's orientation (plus below, minus above); row A's root at D 17.5 has the usual one; a flip between D 17.5 and D 17.75 would mean a second eigenvalue now lies below this root.

Code: `read_ddB_1025.py` is now version 2 (v1, `read_ddB_1025_v1.py`, had minus-lower/plus-upper only). The running driver calls it with three arguments, unchanged; it reads the hybrid record at the dd records' D from the follow-on's own jsonl. Planted cases (usual and flipped hybrid, dd -/+, +/-, +/+, a disagreeing variant): `read_ddB_selftest_1025.py`, `read_ddB_selftest_1025.log`, all six as wanted.

## Row B, D 17.75 k_c 63: hybrid root 1.8676854883516376; checks 1 to 5, the amended edge rule and the dd sign check all PASS (hybrid 06:23:26 to 08:46:18 UTC, dd 08:46:48 to 10:36:30)

| quantity | value |
|---|---|
| guess (fixed before the run) | 1.8860; root minus guess -1.8315e-02 (stub `lam` is the guess, so this is not a record difference) |
| search | w 0.02 grid [1.84828, 1.886, 1.92372], signs +1, -1, -1: one change, **plus below and minus above**; 11 evaluations (3 grid + 8 Brent) |
| root, final bracket | 1.8676854883516376, [1.8676854575325834, 1.8676854883516376], width 3.08e-08 |
| record system | true (|F| 2.4283364241e-10 against 2.4283364241e-10 in the leap line, 2598 steps against 2598) |
| sign changes | 1 on the grid, 1 over all 11 evaluations; noise robust True |
| time | 8566 s, 06:23:26 to 08:46:18 UTC |
| edge rule (amended: outer grid points) | 0.514 steps from the lower outer point, 1.486 from the upper: pass (as first written, both edges of [1.84828, 1.886]: 0.514 and 0.486: pass) |
| float64 `signtest.py` at lambda -/+ 0.02 (information only) | lambda 1.847685488: signs [+1, +1, -1, +1], lambda 1.887685488: [-1, -1, -1, +1]; agree False at both; 56 singular values below 1e-12; 569.7 s and 545.7 s |
| verdict (`rows/verdict_D17.75.log`, written 09:05 UTC) | checks 1-5 and the amended edge rule PASS; dd sign check PENDING then; PASS by the dd reading below |

The dd sign check (Amendments 2 and 3) started 08:46:48 UTC by itself: `ell_ddm.py det` on `sol_l1kc63W1025_D17.750000.npy` (blob de9fc3e5) at 1.8476854883516376 (launcher pid 16660, python 6788) and 1.8876854883516376 (launcher pid 9440, python 4984), `--noise 1e-24,1e-20,1e-16`, 4 threads each, BelowNormal, 3 h caps by exact pid (11:46:48 UTC). Logs `rows/ddB_lo.log`, `rows/ddB_hi.log`, `ddB_w.log`.

Orientation, as information (Amendment 3): row B's hybrid reads plus below and minus above; row A's root at D 17.5 and the four P4 rows read minus below and plus above. The coordinator's reading: at D 18 win2's dd signs read -, +, - at 1.7529, 1.7887 and 1.8245 (two roots, the upper with row B's orientation), and a flip between D 17.5 and D 17.75 would mean a second eigenvalue now lies below this root. Whether row B's dd signs flip too is decided by the dd check.

CPU and memory (samples; the hybrid phase of row A was not sampled): row B's hybrid python (11 to 13 threads, BelowNormal): 1.73 cores in a 10 s sample at 06:23:58, 1.66 at 06:27:20, 1.15 at 07:01:58; 1.42 to 1.62 cores since start; working set 0.15 to 0.60 GB (peak 0.90 GB), private 0.47 to 1.08 GB (peak 1.38 GB). The dd pythons (7 threads, BelowNormal) at 08:47:09: 1.11 cores each, working set 0.07 GB (peak 0.10), private 0.45 GB (peak 0.47); laptop CPU 83 % (the float64 signtest ran beside), 14.6 GB free of 31.83 GB, commit 26.1 GB of limit 41.3 GB.

### Row B's dd sign check, result (`ddB_w.log`, `rows/ddB_lo.log`, `rows/ddB_hi.log`, `rows/ell_ddm_B_D17.75_{lo,hi}.jsonl`, `rows/ddB_reading.log`)

`ell_ddm.py det` on `sol_l1kc63W1025_D17.750000.npy` (blob de9fc3e5), `--noise 1e-24,1e-20,1e-16`, two processes in parallel, 4 threads each, BelowNormal; both ended with exit 0, neither hit the 3 h cap (6572 s and 6582 s):

| point | dd M built | dd LU signs, 5 exact variants | LU time | noise 1e-24 / 1e-20 / 1e-16 (2 seeds each) | ln\|det\| dd | float64 sign, ln\|det\| (`det`'s own) | counts |
|---|---|---|---|---|---|---|---|
| root - 0.02 = 1.8476854883516376 (pid 16660) | 3616 s | +1, +1, +1, +1, +1 (spread 4.5e-12) | 242.2 s | +1,+1 / +1,+1 / +1,+1 | -1932.9785693733 | +1, -1932.1606009273 | yes |
| root + 0.02 = 1.8876854883516376 (pid 9440) | 3633 s | -1, -1, -1, -1, -1 (spread 1.8e-12) | 242.5 s | -1,-1 / -1,-1 / -1,-1 | -1931.9212584794 | -1, -1932.4451281371 | yes |

Hybrid signs at the evaluations nearest these points: +1 at 1.84828 (5.9e-04 above the lower point) and -1 at 1.886 (1.7e-03 below the upper point).

**Reading (Amendment 3): ROOT PASSES.** The two dd signs are opposite, both count (5 variants agree, 1e-24 noise leaves them unchanged), and each equals the hybrid's nearest sign. Orientation: **plus below, minus above**, the same as the hybrid's grid.

Row B's verdict: checks 1 to 5 and the amended edge rule PASS, and the dd sign check PASSES: **row B PASSES**, root 1.8676854883516376 at D 17.75, k_c 63.

Information. Orientation across D: row A (D 17.5) hybrid grid -1, +1, +1 (minus below, plus above; its dd check is win2's, pending); row B (D 17.75), hybrid and dd both plus below, minus above; D 18, win2's dd signs -, +, - at 1.7529, 1.7887 and 1.8245 (two roots, the upper with row B's orientation). The coordinator's reading: a flip between D 17.5 and D 17.75 would mean a second eigenvalue now lies below this root. The float64 `signtest.py` (rotations of M) disagreed at both points, while `det`'s plain float64 sign matches the dd sign at both, as it did at D 18.

CPU and memory of the dd pythons (7 then 4 to 9 threads, BelowNormal, samples; both are in the matrix build for the first 3600 s): 08:47:09 1.11 cores each, working set 0.07 GB (peak 0.10), private 0.45 GB (peak 0.47); 09:17:51 1.20 and 1.17 cores (1.14 since start), working set 0.13 GB (peak 0.14), private 0.45 GB; 09:48:11 1.15 cores since start (4254 and 4245 cpu s), working set 0.60 GB (peak 0.61), private 0.84 GB (peak 0.87). The laptop: CPU 83 % at 08:47 (the float64 signtest beside), 60 % at 09:17 and 09:48; 14.6, 15.7 and 11.4 GB free of 31.83 GB; commit 26.1 GB of limit 41.3 GB at 08:47; two other sessions' single-thread pythons (6 to 7 GB each) ran beside. The pythons' end-of-run peaks were not sampled.

## Final status (2026-11-21 10:37 UTC)

Row A (D 17.5): hybrid root 1.9272222575778963; checks 1 to 5 and the amended edge rule PASS; its dd sign check is win2's and is pending. Row B (D 17.75): hybrid root 1.8676854883516376; all checks PASS including the dd sign check. D 18 and D 18.5 are xfkappa's on the Mac and were not run here.

## D 18.5 root (the coordinator's order, hc about 10:35 UTC by my clock; written before the run, 2026-11-21 10:42 UTC; the first push, fe704bd5, read 10:43 by a mistyped stamp of mine)

Order: the root at D 18.5. xfkappa's scan there (#1025 comment 7061322463, raw `I1025-mac/d18/`, 36 points at step 0.01 over 1.55 to 1.90 on the leap's D 18.5 state) finds one robust change in (1.67, 1.68), estimator range 1.677016 to 1.677225, usual orientation (minus below, plus above; information, not a bar). Bisect it with `p4_hybrid.py` on xfkappa's leap state with guess 1.6771, so the w 0.02 grid holds only this root. Same rules: system check, P4 rules, the outer-edge rule, and a bracket check that the root lies in (1.67, 1.68). Then the dd M check at root -/+ 0.02 by `ell_ddm.py`, two processes, 6 h caps, with the Amendment 3 reader. Guess, window and readings written here before the run. Post on #1025 with cpu and memory.

| item | value |
|---|---|
| state | raw `I1025-mac/d18/sol_l1kc63Wm1025_D18.500000.npy`, blob 33c1a58b82229d55661cbd5e79d2c1fce0c0717c (raw commit 500b1ed2; k_c 63) |
| record | the leap's D 18.5 line of raw `I1025-mac/d18/l1kc63Wm1025.jsonl`, blob 08f4dbf367edba55814e5cf989ccd32a9a5dbe67: F 2.7672415504278416e-10, 2461 steps, kappa 0.7, u0 0.04, Ks 30 (rk 1 by default); a leap state, so no lambda |
| stub | `stub_d185_l1kc63Wm1025_D18.5_leapline.jsonl` (`make_stub_d185_1025.py`, `make_stub_d185_1025.log`): the leap line unchanged plus `lam_guess` = 1.6771 and `lam` = the guess (placeholder, as for row B: `minus_record` is root minus guess, not a record) |
| system check, smoke test 10:38:59 UTC (`signtest.py ... syscheck`, `smoke_syscheck_d185.log`) | F 2.7712865521590816e-10 rebuilt against 2.7672415504278416e-10 (1.46e-03 relative, inside 1%), 2461 steps against 2461: same true |
| code | hybrid: worktree `choptuik-i1025-lowd` at 505d8399 (rows A and B's), `p4_hybrid.py` a402559b; dd: `choptuik-i1025d` at 48c36355 (row B's), `ell_ddm.py`; PY `venv-md510`; BelowNormal; 4 BLAS and rayon threads per process |

Guess and window (the coordinator's guess, fixed before the run):

| w | 0.02 | 0.06 | 0.15 | 0.35 |
|---|---|---|---|---|
| guess 1.6771 | [1.643558, 1.710642] | [1.576474, 1.777726] | [1.425535, 1.928665] | [1.090115, 2.264085] |

The first grid is 1.643558, 1.6771, 1.710642. xfkappa's scan shows one change in 1.55 to 1.90, in (1.67, 1.68), so the first window should hold only this root; the guess lies inside the estimator range, so the sign at the middle point can read either way, and the change then sits in the lower or the upper interval. The search is `p4_hybrid.py`'s, unchanged (`brentq` inside the grid interval, xtol 2e-8 * guess).

Rules, fixed before the run (`verdict_d185_1025.py`, `rows/verdict_D18.5.log`):

1. record system true (steps equal, |F| within 1% of the record's or 1e-13);
2. one sign change on the search grid, and one over all evaluations;
3. every evaluation's sign unchanged under 1e-15 relative noise on blocks 0 to 11 (2 seeds);
4. final bracket at most 1e-7;
5. outer-edge rule (Amendment 1): the root is inside the window and at least 0.05 grid steps from its outer grid points guess * (1 -/+ w);
6. bracket check: the root and its final bracket lie strictly inside (1.67, 1.68).

The float64 `signtest.py` is not run (Amendment 1: it is information only, and the sign check is the dd M). The orientation (signs at the final bracket's ends) is printed as information; the expected one is the usual (minus below, plus above).

dd check, only if the hybrid's checks all pass (otherwise the driver stops, reports, and the coordinator decides): `ell_ddm.py det <state> 18.5 63 <root -/+ 0.02> --noise 1e-24,1e-20,1e-16 --out rows/ell_ddm_D18.5_{lo,hi}.jsonl`, two processes in parallel, each capped at 6 h (21600 s) and killed at the cap by its exact pid (`taskkill /PID <pid> /T /F`, as tested in `ddB_driver_selftest.log` and `d185_driver_selftest.log`). Reading (Amendment 3, `read_ddB_1025.py` v2): the root passes if the two counting dd signs are opposite, in either orientation, and each equals the hybrid's sign at the evaluation nearest it; the same sign at both means no root between them; a sign that does not count (5 exact variants disagree, or 1e-24 noise changes it) means neither reading applies. A sign counts if its 5 variants agree and 1e-24 noise leaves it unchanged.

Run: `d185_driver_1025.py` (launcher `start_d185_1025.cmd`, BelowNormal, log `d185_w.log`; output `ell_p4_hybrid_1025_w_highD_d185.jsonl`, `rows/D18.5.log`, `rows/dd185_{lo,hi}.log`, `rows/dd185_reading.log`). A sampler thread writes every 60 s each child's cpu seconds, working set, private bytes and their peaks, and the laptop's free memory, cpu load and commit, to `rows/d185_samples.csv`, so the end-of-run peaks are logged this time. Estimate: hybrid about 11 evaluations at 13 to 14 min (about 2.5 h), dd about 1.8 h in parallel; no RESUME.

Status: started 10:42:23 UTC; hybrid done 11:53:13 (section "D 18.5 hybrid result" below); dd check done 13:32:24 (section "D 18.5 dd result" below): ROOT PASSES.

Sampler note (10:57 UTC): the driver's own sampler thread broke at 10:54 UTC. Its PowerShell number format `N1` puts a thousands separator into cpu seconds above 1000, so a CSV line split into one field too many; the exception is caught and logged as `sampler: ValueError(...)` in `d185_w.log` once a minute from then on, and the run itself is untouched. `rows/d185_samples.csv` holds the driver's samples from 10:45 to 10:53 UTC. An external sampler, `sample_d185_1025.ps1` (read-only, BelowNormal, started 10:55 UTC for the driver's python, pid 12848; same columns, invariant number format), writes `rows/d185_samples2.csv` every 60 s for the rest of the run, for the hybrid and the dd stages.

## D 18.5 hybrid result (10:42:23 to 11:53:13 UTC): root 1.6772090983230803, every hybrid check PASSES; dd check pending

| quantity | value |
|---|---|
| search | w 0.02 grid [1.643558, 1.6771, 1.710642], signs -1, -1, +1: one change, in the upper interval [1.6771, 1.710642]; 6 evaluations (3 grid + 3 Brent) |
| root, final bracket | 1.6772090983230803, [1.6772090815512417, 1.6772090983230803], width 1.68e-08 |
| root minus guess | +1.091e-04 (the stub's lam is the guess, so not a record difference); inside xfkappa's estimator range 1.677016 to 1.677225 |
| record system | true (|F| 2.7720397892e-10 against 2.7672415504e-10, 1.7e-03 relative; 2461 steps against 2461) |
| sign changes | 1 on the grid, 1 over all 6 evaluations; noise robust True |
| time | 4236 s in `p4_hybrid.py` (4250 s with the driver) |
| outer-edge rule | 1.003 grid steps from the lower outer point, 0.997 from the upper: pass |
| bracket check | the root and its final bracket lie inside (1.67, 1.68): pass |
| orientation (information) | minus below, plus above (the usual one), as in xfkappa's scan |
| verdict (`rows/verdict_D18.5.log`) | every check PASS; dd sign check PENDING |

The hybrid python's last sample (11:52:12 UTC, `rows/d185_samples2.csv`): 5984 cpu s in 4236 s (1.41 cores on average), working set 0.597 GB (peak 0.919 GB), private bytes 1.081 GB (peak 1.400 GB), 11 threads, BelowNormal.

dd check started 11:53:13 UTC by itself: `ell_ddm.py det` on the same state at 1.6572090983230803 (root - 0.02; launcher pid 7060) and 1.6972090983230803 (root + 0.02; launcher pid 14804), `--noise 1e-24,1e-20,1e-16`, 4 threads each, BelowNormal, caps 21600 s each (17:53:13 UTC) by exact pid. Estimate, from row B's two processes (6572 s and 6582 s): about 13:45 UTC.

## D 18.5 dd result (11:53:13 to 13:32:24 UTC): ROOT PASSES (minus below, plus above); the D 18.5 root 1.6772090983230803 passes every check

`ell_ddm.py det` on `sol_l1kc63Wm1025_D18.500000.npy` (blob 33c1a58b), `--noise 1e-24,1e-20,1e-16`, two processes in parallel, 4 threads each, BelowNormal, caps 6 h not reached (5920 s and 5950 s, both exit 0); `rows/dd185_lo.log`, `rows/dd185_hi.log`, `rows/ell_ddm_D18.5_{lo,hi}.jsonl`, `rows/dd185_reading.log`:

| point | dd M built | dd LU signs, 5 exact variants | LU time | noise 1e-24 / 1e-20 / 1e-16 (2 seeds each) | ln\|det\| dd | float64 (`det`'s own) | counts |
|---|---|---|---|---|---|---|---|
| root - 0.02 = 1.6572090983230803 (pid 7060) | 3058 s | -1 x5 (spread 2.5e-12) | 220.4 s | -1 at all | -1900.8761376389 | **+1**, -1900.3708955721 | yes |
| root + 0.02 = 1.6972090983230803 (pid 14804) | 3082 s | +1 x5 (spread 1.4e-12) | 219.3 s | +1 at all | -1900.4949561074 | +1 | yes |

Hybrid signs at the evaluations nearest these points: -1 at 1.643558 (1.4e-02 below the lower point) and +1 at 1.710642 (1.3e-02 above the upper point). **Reading (Amendment 3): ROOT PASSES**: the counting dd signs are opposite and each equals the hybrid's nearest sign; orientation minus below, plus above (the usual one). Information: `det`'s plain float64 sign is +1 at the lower point where the dd sign is -1 (float64 wrong there), and agrees at the upper point.

The D 18.5 root at k_c 63 is **1.6772090983230803** (hybrid, bracket 1.68e-08, inside (1.67, 1.68), inside xfkappa's estimator range 1.677016 to 1.677225), with its dd sign check passed.

CPU and memory (`rows/d185_samples2.csv`, every 60 s, peaks are the process counters): the dd pythons (BelowNormal, up to 10 and 13 threads): last samples 6652 and 6626 cpu s in about 5920 s (1.12 cores on average); working set peak 1.916 and 1.886 GB; private bytes peak 2.152 and 2.122 GB (the peaks come in the LU phase; working set 0.2 GB at the end). The hybrid python: 5984 cpu s in 4236 s (1.41 cores), working set peak 0.919 GB, private peak 1.400 GB. Laptop during the dd: cpu 46 to 99 %, free memory at least 12.3 GB of 31.83 GB, commit at most 24.2 GB of limit 41.3 GB; during the hybrid: cpu 35 to 79 %, free at least 12.6 GB, commit at most 26.9 GB. Other sessions' single-thread pythons ran beside.

