# I1025-win2c: the l = 1 DSS solution's growth rate lambda_1 at k_c 63, D 15 and D 15.5, re-solved from the k_c 55 bar states (records, states, logs)

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task: the coordinator's hc of 2026-11-20 ("lambda at k_c 63 at D 15 and D 15.5, from the k_c 55 bar states, so the top-k_c table reaches down to D 15"; commands from xfkappa). Companion folders: `I1025-win2b/` (win2b's k_c 55 re-solves at D 16.25 and 16.75, same machine) and `I1025-win/` (winb's k_c 63 lane at D 17 to 20).

## Setup (written 2026-11-20 08:35 UTC, before any run)

| | |
|---|---|
| code | a new worktree `D:/choptuik-i1025c`, detached at `origin/wip/ell1-highD` **d4f0f854** ("ell_delta: leave out lambda records that failed a check (#1025)"), run from `solver/matter`. Not touched: `D:/choptuik-i1025b` (win2b's), `D:/choptuik-i1003` |
| python | `C:\Users\nathan\Source\venv-i962`'s python (win2b's venv, used read only: the coordinator named it), Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0. 4 BLAS threads per solve (`OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=4`), BelowNormal, the two solves at once |
| inputs | taken by `git show origin/main:I1025-mac/out/...` of choptuik-large-d-raw (fetched, **no pull, no checkout**; origin/main 19d51a61 at the fetch), blob hashes (`git hash-object`, equal to the tree's blob ids and to dh170's list in its #1025 post of 08:32 UTC): `sol_l1kc55Fb1025_D15.0000.npy` **ad055605cb3028c09d1b91ad32c9f2cd361737d1**, `sol_l1kc55Fb1025_D15.5000.npy` **990ccde2b331cf2840e04b8cadeda152aac5f561**, `l1kc55Fb1025.jsonl` **5be40af42cdcf2c1c3751c1b28a03884759fcbd4**; `signtest.py` **a2f53a9001460afb2ffcbe9c13a404ec784a4ce5** (the Mac's `I1025-mac/signtest.py`, the blob the coordinator named, a2f53a90). They sit in `solver/matter/data/` of the worktree |
| commands | `ell_refine.py l1kc55Fb1025 55 l1kc63Fy1025 63 1 15 2.4210058 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60` (D 15, tag `l1kc63Fy1025`) and the same with tag `l1kc63Fz1025`, `15.5`, `2.3387882` (D 15.5). The guesses are the k_c 55 records' lambda at those D: 2.4210057702 and 2.3387882480 (`l1kc55Fb1025.jsonl`) |
| caps | the ordered 12 h (43200 s) per solve, by the exact root pid of its python (the venv launcher stub, found by win2b's `rootpid1025.ps1`, copied here), command line checked, `taskkill /T /F /PID`, nothing else; a cap that fires is logged with the last log line and not retried (the glue is `run1025c.sh`, written after win2b's `run1025.sh`; `timeout` would kill the stub only) |
| outputs | records `data/l1kc63Fy1025.jsonl`, `data/l1kc63Fz1025.jsonl` and states `data/sol_l1kc63F[yz]1025_D*.npy` in the worktree, copied to `out/` here after both solves ended (no live writer is copied). Logs: `kc63_D15.log`, `kc63_D15.5.log`, `exits_1025c.txt`, `signtest.log` |
| load | win2 at 15% CPU at the order. #1003's K 49 (about 22 GiB tree) is still running; **win2's #1034 build restarts when K 49 ends (the coordinator's order, "as planned") and these solves keep running beside it**; win2b's two #1025 solves run on the same machine too. Wall times are therefore not benchmarks. Each solve is about 2-3 GB (the coordinator) |
| not mine | win2b's `mem1025c.sh` and `memalert_win2.sh` alert-only watchers run beside; my own build watches (alert-only) come back with the build |

## Readings fixed before the run (the coordinator's, from the order and win2b's record checks)

1. **Record checks, per solve**: `n_signchanges` is 1, and `lam` is within 2% of its guess (2.4210058 at D 15, 2.3387882 at D 15.5). I also record, as information, the record's `F`, the move of lambda from k_c 55 to k_c 63 at the same D, and the record's other fields (psi-constraint, steps, `n_lam_evals`).
2. **Signtest** (the coordinator: "a signtest on each record at lam -/+ 0.02, with win2b's signtest.py"). First the planted control (`signtest.py planted` must print agree, agree, DISAGREE; if it does not, the signtests are not used). Then for each record `signtest.py data/sol_<tag>_D<D>.npy <D> 63 around=data/<tag>.jsonl:<D>:0.02` (win2b's recipe): the pass reading is that both JSON lines have `agree` true and the two signs are opposite (the root lies between lambda -0.02 and +0.02). A record that fails its signtest is reported with the lines and **not used** (winb's D 17.5 k_c 63 record failed its signtest and was not used, the 07:18 UTC post).
3. A record that fails a check (a second sign change, a lambda outside 2%, a failed signtest), a solve that does not converge, or a cap that fires is a result, reported with its numbers; no threshold is loosened and nothing is rerun to make it pass. The `F` the LM stops at is what it is (win2b's D 16.75 record stopped at 2.2e-10 against the ordered tol 1e-12).
4. What this does not decide: whether lambda at D 15 and 15.5 is converged in k_c (only k_c 55 and 63 exist for these two D, so the 55 -> 63 move is a spread between two resolutions, not a bound), and what the table does with them; that is the coordinator's, with xfkappa's `ell_delta.py`.

## Result (written 2026-11-20 11:26 UTC)

Both solves ended exit 0 (`exits_1025c.txt`: D 15 in 8527 s, D 15.5 in 6921 s, no cap, both started 08:36:09 UTC, 4 BLAS threads each, BelowNormal, beside #1003's K 49 until 10:12 UTC and, from 10:13 UTC, the restarted #1034 build, plus win2b's two #1025 solves: not benchmarks). No Traceback in either log (23 and 21 numpy RuntimeWarning lines, the same kind the k_c 55 solves print). All four readings above hold:

| D | lam (k_c 63) | k_c 55 lam | move 55 -> 63 | guess, error | n_signchanges | F (LM stop), start | steps | psi-constraint (k_c 55) | signtest at lam -0.02 / +0.02 |
|---|---|---|---|---|---|---|---|---|---|
| 15 | **2.4196464502** | 2.4210057702 | -1.359e-3 (-5.6e-4 relative) | 2.4210058, -0.056% | 1 | 2.354e-10, 5.07e-7 | 3113 | 3.60e-6 (4.36e-5) | signs -1 x4 / +1 x4, agree true, true |
| 15.5 | **2.3356825826** | 2.3387882480 | -3.106e-3 (-1.33e-3 relative) | 2.3387882, -0.133% | 1 | 2.162e-10, 1.24e-6 | 3028 | 1.10e-5 (9.16e-5) | signs -1 x4 / +1 x4, agree true, true |

`signtest.py planted` printed agree, agree, DISAGREE (exit 0), then the two signtests (exit 0, 375 s and 366 s per lambda at D 15; 309 s and 304 s at D 15.5; `signtest.log`). Both `agree` true at both lambda with opposite signs, so each record passes its signtest. The smallest-singular-value counts are in `signtest.log` (50 below 1e-12 and 26 below 1e-15 of the largest at D 15; 52 and 32 at D 15.5).

Other fields (information): Delta at k_c 63 0.984130063532 (D 15) and 0.992420536129 (D 15.5), against the k_c 55 states' 0.984130696765 and 0.992420622523 (-6.33e-7 and -8.64e-8); n_eval 22 and 19 (the lambda search's determinant evaluations); the records' `seconds` 8517 and 6906. The LM stopped at F about 2.2e-10 in both, above the ordered tol 1e-12 and below the 1e-8 gate for the lambda search (as in win2b's and winb's records).

**What this does not show.** Only k_c 55 and 63 exist at these two D, so the 55 -> 63 move is a spread between two resolutions, not a bound, and lambda at D 15 and 15.5 is not shown to be converged in k_c. The records are in `out/`; the table is the coordinator's (`ell_delta.py`).

Files: `out/` (the two jsonl and the two states, copied after both solves ended; sha256 prefixes in the post), `kc63_D15.log`, `kc63_D15.5.log`, `signtest.log`, `exits_1025c.txt` (it also records my slip: the first launch at 08:35:25 UTC stopped at once for want of a PATH in a bash started by PowerShell; nothing ran), `run1025c.sh`, `signtest1025c.sh`, `rootpid1025.ps1` (win2b's, copied), `signtest.py` (blob a2f53a90), and the empty stdout/stderr files of the launches (the first signtest chain launch at 10:32:31 UTC also had no PATH and wrote nothing, `signtest_run_z.stderr`).
