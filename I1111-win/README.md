# I1111-win: which band of the R2 to chord035 difference moves det M, l = 1, k_c 127, D 23.0, lambda 0.122 (#1111's k_c 127 follow-up of #1110; winb)

Written before the run, 2026-11-28 11:05:43 UTC (the time of the README-first push; later pushes keep it). Nothing of this order had been run when the order, the bars and the estimates below were written. Run beforehand, read-only: the pins, the inputs' blobs, the selftests of the tools (dry run of the driver, `selftest_*_dry` files are the `.dry` ones), the driver's fake-mode tests of its checks. Runner: the winb session (surface-laptop-4, Windows 11, i7-1185G7 4 cores / 8 threads, 32 GB, 42 GB free on C:); coordinator t5.

## Order (t5, quoted)

**t5's hc of 2026-11-28 10:58 UTC (the next task for winb):** "Next task: #1111 (read its body and comment 7231937181), the k_c 127 follow-up of #1110 (closed: a chord state on R2's 8351-step map has lambda_1 9.8e-3 above R2's own; the two states differ by 1.0e-6, 97% in the weak band, which at k_c 127 also holds the top-harmonic horizon pair at s/s_max 2.7e-8, and 23% null). Question: which band of that difference moves det M? Budget 4 threads beside the negative-mass jobs, BelowNormal, every run outside your terminal (WMI), raw folder I1111-win/, README first.
Code: a new worktree of wip/i1101-weakdir at 0ee1d95d (detparts now takes --b12 and --b12_threads); your venv-md510 with its Rust ellrs. In it, from solver/matter, set D18_DIR to that folder (detparts imports d18_secant from D18_DIR).
Inputs from raw origin, blob-checked: R2 = I1101-dh170/in/sol_l1kc127k035w2_D23.0000.npy (25ba3a91), I1101-dh170/in/l1kc127k035w2.jsonl (9111bfca); chord035 = I1110-macm3/sol_chord035_D23.0000.npy (205b6a90) with its .map.json (3bed6d4d).
  python i1101_weakdir.py jac <R2 jsonl> <R2 npy> 23.0 jac_r2.npz --pin=25ba3a91,9111bfca      (OPENBLAS_NUM_THREADS=4; R2's 8351 steps, so about twice R0's J)
  python i1101_weakdir.py svd jac_r2.npz svd_r2.npz
  python i1101_weakdir.py detparts svd_r2.npz <R2 jsonl> <R2 npy> <chord035 npy> 23.0 0.122 --b12=rust --b12_threads=4     (OPENBLAS_NUM_THREADS=1, RAYON_NUM_THREADS=4)
Bars: jac prints the record system (else stop); detparts prints the hybrid sign and ln|det| for A (R2), A + P_null, A + P_weak, A + P_strong and B (chord035), each with dln and robust. Report that table and which part carries B - A. jac/svd npz stay local (0.6 and 2 GB); push the logs. Caps: jac 14400 s, svd 7200 s, detparts 28800 s. Post files as before, or post yourself if gh works there."

**The issue (#1111 body and t5's comment 7231937181, stage 1):** at k_c 55, D 16 the double-double determinant confirmed that the discrete mode matrix carries a sensitivity of ln|det M| of 0.81 per 6.8e-12 of the inner strong band; float64 alone cannot give that root. #1110 measured the same scatter at k_c 127, D 23: a chord state on R2's step map has lambda_1 9.8e-3 above R2's own (macm3's secant: root 0.12759 against R2's 0.117825). This run asks which band of the difference z_B - z_A (|dz| 1.014e-6 in macm3's coords, bands of R0's SVD: null 0.231, weak 0.97286, strong 6.55e-5 of it) moves det M at lambda 0.122, a point between the two roots.

Stop rules (t5's, as in my earlier lanes): stop and report on a refusal (record system, pins, selftests), an exception, or a step over its cap (jac 14400 s, svd 7200 s, detparts 28800 s). No other stop is written in the order.

## Registered before the run

**Bars (t5's, and the checks I add):**

| step | bar |
|---|---|
| start | the worktree is `wip/i1101-weakdir` at 0ee1d95d; the solver files, my `ellrs` build and the four raw inputs equal their blobs (table below); the chord035 map has R2's 8351 steps; `d18_secant.py` selftest 0 and its controls `--mutate=half`, `--mutate=norobust`, `--mutate=nosigncheck` 1 1 1; `ell_b12rs.py` selftest 0 and its controls `--mutate=nolam`, `--mutate=harm` 1 1 |
| jac (t5's) | exit 0 within 14400 s; it prints "the record system" (exit 3 and a stop if not; the `--pin` is R2's state and record). Mine, also: 8351 steps, J square |
| svd (t5's cap; my checks) | exit 0 within 7200 s; the tool's `planted` check on the SVD exits 0 and its `--mutate=basis` control exits 1; `coords` of chord035 on R2's own SVD (extra, seconds), for comparison with macm3's numbers (R0's SVD) |
| detparts (t5's) | exit 0 within 28800 s; it prints the hybrid sign, ln|det|, dln and robust for A (R2), A + P_null, A + P_weak, A + P_strong, B (chord035), at lambda 0.122, `--b12=rust --b12_threads=4`, and the three parts' norms. Mine, also: the three norms squared add up to |z_B - z_A|^2 (checked to 1e-9 from my own V^T on the stored SVD); every dln against the limit 0.1 reported as printed (a non-robust case is reported, not a stop) |
| the question (t5 reads it) | "which part carries B - A". My reading rule, written before the run: a part carries B - A if its hybrid sign equals B's and its ln|det| lies within 0.1 of B's; if none does I report that and the numbers (ln - ln(A) of each case). t5 rules |

**My own estimates (not predictions of the order):**

- **jac:** macm3's jac at R0 took 521 s (M3, 6 threads); R2's 8351 steps are about twice R0's, so about 1050 s there. Here, 4 OpenBLAS threads on a laptop with a negative-mass job beside: **about 3000 s (2000 to 4500 s)**; J is 8300 x 8300 doubles (about 0.55 GB).
- **svd:** macm3 110 s (R0, 6 threads). Here **about 500 s (300 to 1000 s)**, peak about 5 GB; `svd_r2.npz` about 1.1 to 2 GB (t5: 2 GB). C: has 42 GB free.
- **detparts:** five hybrid evaluations in one process, one after the other. At k_c 143 and 4 threads an evaluation took 1572 to 1601 s at 4705 steps (kappa 0.7) and 1917 to 1929 s at 6582 steps (kappa 0.5, with the negative-mass job beside); about 0.29 to 0.34 s a step. At k_c 127 and 8351 steps: **about 2400 s (2000 to 2900 s) an evaluation, 12000 s (10000 to 15000 s) for the five**, plus the loading of the SVD. Peak private memory about 5.6 to 7 GB.
- **The whole run:** about 15500 s (**4.3 h**, 3.5 to 6.5 h), so the table at about 15:30 UTC if it starts at 11:10 UTC. The caps add up to 50400 s.
- **Threads:** jac and svd 4 (OpenBLAS), detparts: the float64 part single-threaded and block 12 on 4 Rust threads (RAYON 4). A negative-mass job (`convergence.py 6`, not mine) holds about 3 of the 8 threads (laptop 32 % CPU alone; 21 GB free memory at 11:00 UTC); 4 threads fit (see my handover note in auto-memory: laptop mean 47 to 60 % with 4 of mine).

## Code and inputs (blobs)

| item | blob |
|---|---|
| worktree `choptuik-i1111` (detached) | `wip/i1101-weakdir` 0ee1d95d |
| `solver/matter/i1101_weakdir.py` | 472e820d |
| `d18_secant.py` (D18_DIR is the worktree's `solver/matter`) | 9706e506 (the file my k_c 143 lane used) |
| `ell_b12rs.py` | a1fff74f (as mine) |
| `ell_fastm.py`, `ell_ddm.py` | 3431e32e, 64c4337f (the worktree's, newer than my regrid-era ones 93f963f6, 86578fee) |
| `dss_ell.py`, `ell_dd.py`, `ddnp.py`, `ell_fastdd.py` | 5d28c19e, 7e58fcbc, 9b1fb195, 237ebfdd |
| `ellrs` (my #1102 build, `i1102_1025/site`, on PYTHONPATH) | pyd ddd5a082, `__init__` 76c7cfbc |
| R2 state `sol_l1kc127k035w2_D23.0000.npy` (66488 B) | 25ba3a91 (raw `I1101-dh170/in/`, here `inputs/r2_state.npy`) |
| R2 record `l1kc127k035w2.jsonl` (kappa 0.35, 8351 steps, \|F\| 3.1242e-10, Delta 1.1743229234) | 9111bfca (`inputs/r2_record.jsonl`) |
| chord035 state `sol_chord035_D23.0000.npy` | 205b6a90 (raw `I1110-macm3/`, `inputs/chord035_state.npy`) |
| chord035 map `sol_chord035_D23.0000.map.json` (R2's 8351 steps, \|F\| 3.1190e-10, Delta 1.1743225027) | 3bed6d4d (`inputs/chord035_state.map.json`) |

The inputs were copied with `git cat-file blob` from raw origin/main (85ccc6df7 and later, 50d3aa1d0 at the copy); their blobs were checked with `git hash-object --no-filters` and are the ones named above, byte for byte.

## The run

One driver, `w127_1111_driver.py`, started by `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_w127_1111.cmd` (BelowNormal, no window, nothing in my terminal), with a sampler (60 s), an alert-only memory watcher (hc below 1 GB, kills nothing) and a keep-awake helper (`SetThreadExecutionState`, power plan untouched); the session check must report no `claude` in the chain.

1. **Step 0** (the driver): pins and the four checks of the table above.
2. **jac:** `i1101_weakdir.py jac inputs/r2_record.jsonl inputs/r2_state.npy 23.0 I1111-local/jac_r2.npz --pin=25ba3a91,9111bfca` (log `jac_r2.log`).
3. **svd:** `i1101_weakdir.py svd I1111-local/jac_r2.npz I1111-local/svd_r2.npz` (`svd_r2.log`), then `planted` (`planted_r2.log`), `planted --mutate=basis` (`planted_basis_r2.log`) and `coords svd_r2.npz inputs/r2_state.npy chord035=inputs/chord035_state.npy` (`coords_r2.log`).
4. **detparts:** `i1101_weakdir.py detparts I1111-local/svd_r2.npz inputs/r2_record.jsonl inputs/r2_state.npy inputs/chord035_state.npy 23.0 0.122 --b12=rust --b12_threads=4` with `OPENBLAS_NUM_THREADS=1 RAYON_NUM_THREADS=4 D18_DIR=<worktree>/solver/matter PYTHONPATH=<ellrs site>` (`detparts_r2.log`), then `detparts_table.txt` and `summary_1111.txt`.
5. **Reports:** an hc to t5 at the end of each step and at half a cap if a step runs that long; at the end I push `I1111-win` and post the table (on #1111 myself if gh works, as in #1025; else a post file). The npz files stay in `C:/Users/nathan/Source/I1111-local/` (outside the raw clones); the logs are pushed.
6. `cap_seconds.txt` in this folder (lines `jac=N`, `svd=N`, `detparts=N`), if present, overrides a cap at every poll; only on t5's word.

## Files made here

`README.md`; the driver `w127_1111_driver.py`, `k127_watch_alert_1111.py`, `sample_driver_1111.ps1`, `keepawake_1111.py`, `session_check_1111.ps1`, `go_w127_1111.cmd`, `publish_1111.sh`, `push_1111.sh`; `inputs/` (not pushed: the four raw files are in raw already); the dry-run and fake-test evidence `selftest_driver_dry_1111.txt`; later the logs named above, `rows/` (sampler, watcher and keep-awake logs), `detparts_table.txt`, `summary_1111.txt`.

## Status

Driver built and dry-tested before the start (2026-11-28 11:03 to 11:10 UTC): the real dry run (pins, the four blob checks, the selftests of `d18_secant.py` and `ell_b12rs.py` with their controls) exit 0; the fake-mode tests of the driver's checks (a stand-in for each step): ok, jac exit 3 (stop), parts that do not add up (stop).

Pushed 2026-11-28 11:05:43 UTC.

## Result

Not yet run.
