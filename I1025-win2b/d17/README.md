# I1025-win2b/d17: #1025 the k_c 71 hybrid root at D 17, and the k_c error there

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, Windows 11), runner `win2b`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025
Written before the run (2026-11-21 04:01 UTC).

## Order

The coordinator (hc 2026-11-21 about 03:57 UTC): the delta trend past D 17 rests on k_c 63 alone. At D 16.5 the k_c 71 hybrid root (win2b, 2.1459968362025212) and the Mac's k_c 63 hybrid root (2.1466599631271923, `l1kc63Fw1025b`) differ by -6.631e-4. Is that still the size at D 17? The first order was a leap of k_c 71 from my D 16.5 state to D 17 and then the hybrid root. **Changed by the coordinator before any run** (second hc, about 04:01 UTC), after I pointed out that `ell_leap.py` needs two k_c 71 states and I hold one: skip the leap; the state for the root is the Mac's float64 k_c 71 state at D 17, `I1025-mac/out/sol_l1kc71Fm1025_D17.0000.npy` (the regrid of winb's k_c 63 D 17 state), and its line in `I1025-mac/out/l1kc71Fm1025.jsonl` is the record for `p4_hybrid.py`'s system check. Nothing of the leap was run.

The reading, fixed now: **k_c error at D 17 = lambda_71(17) - 2.0399399392** (xfkappa's k_c 63 hybrid root at D 17, `I1025-mac/lane_p4a.log`), to be reported beside D 16.5's -6.6e-4.

## Inputs (raw origin/main dfdfc984, taken by `git show`, checked with `git hash-object --no-filters`)

| item | raw path | blob |
|---|---|---|
| state | `I1025-mac/out/sol_l1kc71Fm1025_D17.0000.npy` (k_c 71, D 17, 4655 unknowns, Delta 1.022439103213245) | 9e9f007ec5f5e1a038ff119b82d576e8748dd8a5 |
| record | `I1025-mac/out/l1kc71Fm1025.jsonl` (one line: F 2.2606164643635036e-10, 3092 steps, u0 0.04, Ks 30, kappa 0.7, rk 1, float64 lam 2.0379024670520076 from its own guess 2.026546497375959, n_signchanges 1, 4846 s) | d786d48948f75caef60f6b9163b9d80270041148 |
| `p4_hybrid.py` | `I1025-mac/p4_hybrid.py` | a402559b5d37661b49da50f07f877af21fd29b3a |
| `signtest.py` | `I1025-mac/signtest.py` (with `around=` and the system check) | 179ea09681b0a75f7cefdff98984b48051b3f085 |
| edge/pass rules | `I1025-mac/d18/d18_check.py` (the P4 rules plus the outer-grid-point edge rule, amendment 1 of 2026-11-21 03:36 UTC; its selftest passes here, `d18_check_selftest.log`) | 08969ea28fbd6cb0d83e17c2d4ded1901ce6b209 |

Code worktree `D:/choptuik-1025p4` at 505d839940456a3d04321d75cf66cc3b5bc831c4 (the P4 rows' worktree), PY `C:/Users/nathan/Source/venv-md510` (python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble 5.1.0). 4 BLAS threads, BelowNormal. The Mac's state was made on another machine and build: the system check (steps equal, |F| within 1% or 1e-13) decides whether it is the record system here.

## Guess and window, fixed here before the run

Guess = the k_c 63 hybrid root at D 17 plus D 16.5's offset = 2.0399399392 - 6.6e-4 = **2.0392799** (the coordinator's change: the float64 2.0265465 is the noisier centre, and the guess only centres the window; the offset actually measured at D 16.5 is -6.631e-4). The stub record is the Mac's D 17 line with `lam_guess` set to 2.0392799 (the record's own, 2.026546497375959, kept as `lam_guess_record`); its `lam` stays the Mac's float64 record 2.0379024670520076, so `minus_record` is the hybrid root minus that float64 value.

The search is `ell_refine.lam_root`'s, unchanged in `p4_hybrid.py`: the sign of the hybrid det at guess * (1 + w * (-1, 0, 1)) for w = 0.02, 0.06, 0.15, 0.35 in turn, stopping at the first w with a sign change, then `brentq` inside that interval.

| w | lower | guess | upper | step |
|---|---|---|---|---|
| 0.02 | 1.998494 | 2.0392799 | 2.080065 | 0.040786 |
| 0.06 | 1.916923 | 2.0392799 | 2.161637 | 0.122357 |
| 0.15 | 1.733388 | 2.0392799 | 2.345172 | 0.305892 |
| 0.35 | 1.325532 | 2.0392799 | 2.753028 | 0.713748 |

Written down before the run: if the offset of D 16.5 persists, lambda_71(17) = 2.0392799 + (0 to a few e-4), i.e. a root at the middle grid point (not flagged by the outer-edge rule). The k_c 63 hybrid root 2.0399399392 lies 0.16 grid steps above the guess in the w 0.02 window.

## Pass rules (fixed before the run)

All of: (1) record system true (steps equal to 3092 and |F| within 1% of 2.2606e-10 or 1e-13); (2) one sign change on the search grid and one over all evaluations in lambda order; (3) every evaluation's sign unchanged under 1e-15 relative noise on blocks 0-11 (2 seeds); (4) final bracket at most 1e-7; (5) the edge rule of `d18_check.py`: the root at least 0.05 grid steps from the window's outer grid point on its side; (6) signtest at the hybrid lambda -/+ 0.02 (`signtest.py STATE 17 71 around=<hybrid jsonl>:17:0.02`): both lines agree (the sign from an LU of M equals the signs from LUs of three random orthogonal rotations of M), the two signs are opposite, and its system line reads same true. A row failing any is reported, not read. The verdict is `d17_verdict.py`'s (its selftest has planted failing cases).

## Run

`d17_hybrid.sh` (launched by `launch_d17.ps1` at BelowNormal): the checks above, the stub (`make_stub_d17.py`), `p4_hybrid.py` (cap 43200 s by exact pid after a command-line check), the signtest (cap 10800 s), the verdict. One line per event in `../exits_1025.txt`. Progress posts on #1025 every 3 h, and at the end, with cpu and memory. win2-build's #1060 `anm_run` (20 threads, BelowNormal, started 03:57 UTC) shares the machine.

## Log

(appended below as the run goes)
- 2026-11-21 04:02:53 UTC: README with the guess 2.0392799 and the windows, inputs by blob, rules, stub (blob 80b7ffde), d17_verdict.py (selftest and a planted-path run, both able to fail) and d18_check.py's selftest written and pushed before the run.
- 2026-11-21 04:04:22 UTC: the chain started 04:03:03 UTC (root pid 16508 and its child, BelowNormal, cap 43200 s). System check: |F| 2.2637712819e-10 against 2.2606164644e-10 (+0.14%), steps 3092 = 3092, the record system. Start post on #1025: comment 7057011122.
- 2026-11-21 06:22:44 UTC: hybrid row done (exit 0, 8381 s, cap not reached): lam 2.0400263140919073, bracket [2.0400263140919073, 2.040026337903978] (width 2.38e-8), 9 evaluations, 1 sign change on the grid and 1 over all, noise-robust. Grid (w 0.02): -1 at 1.998494, -1 at the guess 2.0392799, +1 at 2.080065 (both noise draws agree at every point). The root is 0.018 grid steps above the guess (the middle point; 0.982 steps from the outer upper point, so the outer-edge rule passes; the older both-edges rule would have flagged it).
- 2026-11-21 06:44:29 UTC: signtest (1304 s, exit 0) at lam 2.0200263140919072 and 2.0600263140919073: **FAIL**. The four signs (LU of M, then LU of three random orthogonal rotations of M) are [-1, -1, -1, +1] and [+1, +1, -1, +1], agree false at both; 64 singular values below 1e-12 at both (D 16.5's signtest: 63 and 62, all agree). Verdict `VERDICT D 17.0 k_c 71: FAIL (rules pass, signtest FAIL)`: the row is reported, not read. If it were read: k_c error lam71(17) - 2.0399399392 = +8.637e-5 (D 16.5: -6.631e-4); hybrid minus the Mac's float64 record 2.0379024670520076: +2.124e-3.
- Output blobs (git hash-object --no-filters): `ell_p4_hybrid_1025_w_d17.jsonl` 9746d6dd, `hybrid_D17.log` da640286, `signtest_D17.log` e91eec88, `verdict_D17.log` a9b67268. Chain done 06:44:29 UTC; nothing of mine runs.

## The dd M sign check at D 17 (the coordinator's hc ~06:46 UTC; written before the run, 2026-11-21 06:48 UTC)

The row above failed its float64 signtest by the letter. The coordinator: the float64 M's sign is unreliable from D 17 on (the D 17.5 record failed the same way), so the sign check moves to the full double-double M. Neither the hybrid's own signs at lambda -/+ 0.02 nor a smaller-offset signtest: run `ell_ddm.py det` as win2 does (raw `I1025-win2/d18/run_d18.sh`, which I model `dd/d17_dd.sh` on).

- Code: win2's worktree `D:/choptuik-i1025d` (wip/ell1-highD 48c36355; read only, nothing is written into it), PY `C:/Users/nathan/Source/venv-md510`. `dss_ell.py`, `ell_ddm.py`, `ddnp.py` and `ell_dd.py` are the same files at 48c36355 and at 505d8399 (the hybrid's worktree), so the hybrid row's system check (|F| 2.2638e-10, steps 3092 = 3092) is the system `ell_ddm.py` builds (`_setup`: Ks 30, u0 0.04, kappa 0.7).
- State: `in/sol_l1kc71Fm1025_D17.0000.npy` (blob 9e9f007e, the Mac's k_c 71 D 17 state the root used), by absolute path.
- First `ell_ddm.py selftest` (must PASS, exit 0) and `selftest --mutate=slices` (must FAIL, exit 1), 1800 s caps; if either is wrong, nothing else runs.
- Then `ell_ddm.py det STATE 17 71 LAMBDA --noise 1e-24,1e-20,1e-16 --out ...` at **2.0200263141** and **2.0600263141** (the hybrid root 2.0400263141 -/+ 0.02), two processes in parallel, 20 BLAS threads each as win2's driver (the order gives no count), BelowNormal, caps 10800 s (3 h) each by exact pid after a command-line check.
- A sign counts if its 5 dd variants agree and 1e-24 relative noise (both seeds) leaves it unchanged (xfkappa's rule as win2 reads it; the 1e-20 and 1e-16 noise are information).
- **Reading, fixed now:** minus at the lower point and plus at the upper means the root passes, and the k_c error at D 17 is +8.637e-5 (2.0400263141 - 2.0399399392). The same counted sign at both means no root between them. A point whose sign does not count gives no reading. `read_d17_dd.py` (selftest with planted records for each case) prints this.
- win2-build's own `ell_ddm.py det` processes (D 17.5 and D 18, 20 threads each, BelowNormal) share the machine; cpu and memory go into the post.
- 2026-11-21 06:48:28 UTC: dd section, `dd/d17_dd.sh`, `dd/read_d17_dd.py` (selftest passes, 7 planted cases) written and pushed before the run.
- 2026-11-21 09:49 UTC, the cap ended both processes: det_lo killed at 10800 s (pid 34904), det_hi at 10800 s (pid 35576), exit 1 (the driver's MISMATCH lines), **no jsonl record exists**. `ell_ddm.py det` writes the record after the noise loop and after the float64 `slogdet(S.mode_matrix(z, lam))` (detcmd, `open(o.out, "a")` at the end); both logs end with the 1e-16 noise line, so the kill came during the float64 step. The driver's reader failed (`FileNotFoundError` for `ell_ddm_d17_lo.jsonl`, `dd/d17_dd_read.log`), so no record-based reading was made.
- The signs are in the logs. `dd/det_log_to_jsonl.py` turns a det log into a record of the same keys (`source: "log"`, `f64_sign` NaN since the float64 step did not finish) and nothing else; its selftest (`dd/det_log_to_jsonl_selftest.log`, 7 planted logs through the unchanged `read_d17_dd.py`: a flipped variant, a flipped 1e-24 noise sign, a missing 1e-24 line, same sign at both, swapped order) passes. Run on the two logs it gives `dd/ell_ddm_d17_lo_fromlog.jsonl`, `ell_ddm_d17_hi_fromlog.jsonl` and `dd/d17_dd_read_fromlog.log`. This reading is from the logs, not from records; the coordinator decides whether it stands.
