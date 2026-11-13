# I664-win2: natural-test A/B on #603's class B refusals (D 236.13, 238.54, 240.12, 249.87)

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads per run. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/664 (queued by the coordinator on the agent-msg channel, messages 1794557834560-0 and 1794558079369-0, 2026-11-13; after #644).
Code: worktree `D:\choptuik-i664` at origin/main 141d9d48 ("newton_od: |dz| to 3 digits and a line per refused trial at verbose 1", #666; printing only, not the iteration); venv-i600 (the #600 build, hpkernel `_hpkernel.cp314-win_amd64.pyd` sha256 4ede9afe..., the kernel #603 runs on). #603's chain is read in place (the bases `I603-win2/chain/anm_pin3_D<base>.npz`) and left running.
Runs (`run_664.sh`, 8 in all, one after the other, own first for each attempt): `anm_run.py ... --steps 1 --a0 <a> --od_accept own|natural` from the base of the refused attempt, #603's other flags:

| attempt | base state | a0 (full precision: D of the refused attempt's target state minus D of its base, from the states' meta) |
|---|---|---|
| 236.13 -> 237.13 | D236.1312 | 1.0 |
| 238.54 -> 239.51 | D238.5375 | 0.9765625 |
| 240.12 -> 240.89 | D240.1244 | 0.762939453125 |
| 249.87 -> 250.47 | D249.8696 | 0.5960464477539062 |

(`hp/data/corrector_attempts.csv` on main rounds a to 6 digits: 1, 0.976562, 0.762939, 0.596046.) Outputs `<attempt>_own/`, `<attempt>_natural/`, logs `<attempt>_own.log`, `<attempt>_natural.log`, starts and exits in `exits_664.txt`.

Acceptance (#664): each `own` run repeats #603's log lines for that attempt; each `natural` run is reported as converged or refused, with its trial lines; where natural converges, its Delta matches #603's state at the same D_str to 1e-40, or the task fails; with a different D_str, report both.



## Results (2026-11-13 08:43:25 to 12:58:01 UTC)

`exits_664.txt`: eight runs, every exit 0, 4 h 15 min (own 33, 34, 43 and 35 min; natural 26, 24, 25 and 34 min). `compare_664.py TAG BASE_D TARGET_FILE` (output in `compare_<attempt>.txt`) compares each pair with #603 (own against #603's chain.log lines with the seconds, the printed tol and the digits of the `on k:` lines masked; natural's trial lines; where natural converged, its state's D_str and Delta, the eight parts summed exactly, against #603's state at the same D).

| attempt (a, full precision) | own against #603 | natural at that a | natural: Delta against #603's state at the same D_str |
|---|---|---|---|
| 236.13 -> 237.13 (1.0) | refused, 8 of 8 lines identical (3 steps, stall at 2.0e-28, 765 s) | **converged**, 7 Newton steps, 3.8e-75, 461 s | D_str equal, difference 5.3e-59, zh and zl bit for bit |
| 238.54 -> 239.51 (0.9765625) | refused, 8 of 8 (3 steps, 747 s) | **converged**, 7 steps, 1.1e-77, 407 s | D_str equal, 1.2e-55, bit for bit |
| 240.12 -> 240.89 (0.762939453125) | refused, 10 of 10 (4 steps, stall "lam at or below 0.04 twice", 1310 s) | **converged**, 6 steps, 3.6e-94, 390 s | D_str equal, 3.3e-56, bit for bit |
| 249.87 -> 250.47 (0.5960464477539062) | refused, 9 of 9 (4 steps, 6.8e-29, 858 s) | **refused: 12 Newton steps, the `--qd_it 12` cap, printed max\|F\| 2.2e-39, 701 s** | not applicable; its retry at a 0.298 converged (3 steps, 3.0e-61, 182 s) |

**The three converged attempts** share one trial pattern: the first move is accepted at lam 1 (ratio 5e-5 to 2e-8), the next one or two steps are refused at lam 1 (ratio 0.9999 to 2.3) and accepted at lam 0.5 (ratio 0.25 to 0.75, bound 0.875), and from the third or fourth step the iteration is quadratic (ratios 0.2, 4e-17, 2e-12 / 0.2, 1e-17, 3e-13 / 0.46, 9e-31, 6e-19). The default test refuses the same iterates (236.13: every trial on step 2 has raw |dz_t| above |dz|, 5.9e-38 to 7.3e-38 against 5.878e-38; 240.12: a stall with lam down to 0.004).

**The fourth attempt (249.87, a = 0.596)** is different (`249.87_natural.log` lines 8 to 39): the first move needs lam 0.25 (the trials at lam 1 and 0.5 have ratios 21.7 and 2.2), and then the iteration is accepted at every step but converges slowly: max|F| 1.70e-29, 1.22e-29, 7.49e-30, 8.93e-30, 2.48e-30, 5.44e-30, 4.80e-31, 8.37e-31, 8.94e-33, 4.08e-34, 2.16e-39, 2.47e-47 (it rises on three steps, because the test judges |dz|, not |F|), |dz| 1.2e-31 down to 6.0e-51 with the ratios 0.16, 0.85 (refused at lam 1, accepted at 0.5), 0.05, 0.26, 0.30, 0.44, 0.05, 0.15, 2e-3, 1e-4, 6e-10: superlinear only in the last three. The run stops at the cap of 12 steps, refused, with the residual still falling quadratically (2.47e-47 after the 12th step, |dz| 6e-51), so the cap and not the test ended it; the summary line prints "max|F| 2.2e-39", which is the residual of the step before, not the 2.47e-47 of the last step line; I have not traced which iterate the summary belongs to. Two or three more steps would have reached 1e-60. Its retry at a 0.298 is accepted (3 steps, 3.0e-61).

**What this says.** The natural test converges 3 of the 4 class B refusals to #603's own state (the Delta differences are 5e-59, 1.2e-55 and 3.3e-56, against the 1e-40 required) in 6 or 7 steps and 390 to 461 s, where the default test refused after 747 to 1310 s; the fourth is refused by the iteration cap with the residual falling. The class B refusals are therefore artifacts of the test or of the cap, not of the step size. Not shown: a run of `natural` with `--qd_it` above 12 at 249.87; the planted check of the natural test is the Mac's (#644).

Builds as #644 (`../I644-win2/README.md`), with the worktree `D:\choptuik-i664` at origin/main 141d9d48.

