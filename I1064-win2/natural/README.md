# I1064-win2/natural: base polishes from the chain's front on win2 with --od_accept natural: ks_chain3b's leg 14 state at D 261.6229 at ks 293 (control), 315 and 316

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1064. Task: the coordinator's hc of 2026-11-21 (~09:30 UTC), after the
first #1064 run on win2 (folder `../`, post 7060623893): the same two rungs with `--od_accept natural` in place of `own`, because the trials at lam 1 cut max|F| from 1.15e-08 to 9.6e-10 (ks 315) and
9.4e-11 (ks 316) and the own test (`|dz_t| < |dz|`) refused them.

## Setup (written 2026-11-21 09:32 UTC, before any run)

| | |
|---|---|
| state | `I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D261.6229.npz` (blob e0737904cb19..., read only from `D:/choptuik-large-d-raw-push`), as in `../` |
| code | worktree `D:/choptuik-i1060` at main **8179068d** (clean), `hp/anm_run.py`, `hp/exact_recip_check.py`; venv `C:\Users\nathan\Source\venv-i1058b`; as in `../` |
| command | `../run1064w.sh`'s line (dh610's leg 13 line with `--steps 0 --keep_plan 0 --save_base 1 --ks K --D_max 270.8483`, 10 threads) with **only `--od_accept own` changed to `--od_accept natural`**. `flags_natural.txt` is `../flags_leg13.txt` with that one word changed; `run1064n.sh` checks this before any run (it stops otherwise) |
| rungs | 1. **control ks 293** (natural), 10 threads; must converge. 2. **ks 315 and ks 316 side by side**, 10 threads each, caps 7200 s each by the exact root pid (`taskkill /T /F /PID` after the command line is checked) |
| controls first | `../gate1064.py --selftest` (exit 0) and `--selftest --break` (exit 1); `../xcheck1064.py --planted STATE ctl_test` (exit 0) and `--mutate` (exit 1); the flags check (passes on `flags_natural.txt`; fails on the own flags and on an eps change, tested before the launch). The run stops if one is wrong |
| files | the gate, the delta check, the table script and `cmp_lib/` are the parent folder's (`../gate1064.py`, `../xcheck1064.py`, `../table1064.py`, `../cmp_lib/`), unchanged; `run1064n.sh`, `lib_1064.sh` (OUT changed), `mem_watch.ps1`, `commit_watch.ps1` (alert-only, 30 s samples, kill nothing) are copies |
| memory | as in `../`: I tell the coordinator at commit over 99 GB, a page file up by 2 GB, or available under 1 GB for 5 min. win2b's jobs share the machine |

## Readings fixed before the runs (the coordinator's)

1. **A rung that converges under natural** (the gate: the last octo-double Newton line says converged and the base is saved) means the own test, not the polish, blocked the raise. Then Delta(K) - Delta(293) is reported, with both states at the same D to 50 digits (`exact_recip_check.py delta`, then `xcheck1064.py`); 293 here is this folder's natural control base.
2. **Both rungs failing under natural** means the acceptance test is not the cause.
3. **The control (ks 293 under natural) must converge.** If it fails: stop and report; the rungs are not started.
4. If one rung converges and the other fails, both are reported as they are; reading 1 holds for the K that converged. A cap that fires is a result (the gate then reads "no octo-double Newton line"). Nothing is rerun or loosened.

Reported for each rung: the gate verdict, the iteration lines with seconds, the wall time, and, as information, the same K's own-test log in `../` (ks315.log, ks316.log). Information (not in the readings): this control's base against the stored state and against the own-test control's base (`../ks293`).

## Result (run 2026-11-21 09:33:10 to 11:28:40 UTC)

Reading 3: the control converged under natural. Reading 2: **neither ks 315 nor ks 316 converged under natural** (the gate: the last octo-double Newton
line says "not converged"), so the acceptance test is not the cause, in the coordinator's reading. Reading 1 does not apply: no rung converged, so no
Delta(K) - Delta(293) is reported as a reading. Nothing was rerun or loosened. Both rungs stopped on their own, inside the 7200 s caps (no cap fired).

| K | arm | exit | wall s | octo-double Newton steps | final max\|F\| | how it stopped | base saved |
|---|---|---|---|---|---|---|---|
| 293 (control) | natural | 0 | 91 | 1 | 2.0e-36, converged | converged | yes |
| 315 | natural | 0 | 6796 | 10 | 5.7e-11, not converged | step 9: no trial step accepted, stopping | yes |
| 316 | natural | 0 | 4057 | 6 | 2.1e-12, not converged | step 5: lam at or below 0.04 twice in a row, stopping (stalled) | yes |
| 315 | own (`../`) | 0 | 2781 | 2 | 1.9e-08, not converged | step 1: no trial step accepted | no (not adopted) |
| 316 | own (`../`) | 0 | 1918 | 1 | 1.1e-08, not converged | step 0: no trial step accepted | no (not adopted) |

The walls are each run's own (30 s polls). The saved bases are the last iterates of stalled polishes, not converged bases: the gate fails them, as the verdict
lines in `summary_1064.txt` and `gate_ks*.txt` say. The tolerance is `--tol_od 2e-34`.

Per-step lines are in `ks315.log` and `ks316.log` (each step's trials with the simplified-correction ratio and its bound, and the step line with seconds). What they show:

- Step 0 is the same start as under own: the strong chord is refused (ks 315 407.36 s, ks 316 393.68 s; chord 1 max\|F\| 8.59e+11 and 1.72e+12) and the first trial at lam 1 is the one the own test refused.
  Under natural it is accepted: max\|F\| 1.15e-08 -> 9.63e-10 (ks 315; ratio 3.68e-02, bound 0.750) and 1.15e-08 -> 9.38e-11 (ks 316; ratio 0.189).
- Then the polish keeps stepping, after step 0 mostly at small lam (0.0039 to 0.5; lam 1 only at ks 315 step 7), and max\|F\| stays between 1e-9 and 2e-12 over 6 and 10 steps. The lowest max\|F\| of ks 315 is 5.53e-12 (step 7); its last
  iterate is 5.66e-11. ks 316 ends at its lowest, 2.11e-12.
- A trial at lam 1 at ks 316 step 1 gave max\|F\| 3.34e+11 (ratio 2.0e+38, refused, projection failed); the next trials were fine.
- The gap from the tolerance is about 1e22 (ks 316, 2.1e-12 against 2e-34) and 3e23 (ks 315).
- The double-double \|F\| in the 'base ...' lines (1.5e+32 to 3.7e+32) is not a residual (AGENTS.md, #903) and is not quoted as one.

Information (not in the readings):

| comparison | Delta(b) - Delta(a) | check |
|---|---|---|
| natural ks 293 base against the stored state (`delta1064_ctl_vs_state.json`) | 0.0 | exact sums difference below 1e-30: ok |
| natural ks 293 base against the own-test ks 293 base (`delta1064_natctl_vs_ownctl.json`) | 0.0 | ok |
| natural ks 315 base (not converged) against natural ks 293 (`delta1064_info_K315.json`) | 5.75337e-19 | exact sums difference -7.89e-45 (bound 1e-30): ok |
| natural ks 316 base (not converged) against natural ks 293 (`delta1064_info_K316.json`) | 4.20168e-19 | exact sums difference -8.08e-45 (bound 1e-30): ok |

D is equal to 50 digits in all four (261.62291163319045732282841498772540944628417491913). The last two are for bases that failed the gate and are not a result of reading 1; the
driver did not run them, I ran them by hand after `all.done` with `exact_recip_check.py delta` and `xcheck1064.py` (`xcheck PASS` each).

`table_1064.md` is written by `../table1064.py` unchanged; its closing note ('ks293 to ks318 ... exits_1064b.txt') is the script's fixed text for dh610's run and does not apply here.
Its Delta column is empty for the two failed rungs (the driver runs the delta check for converged rungs only).

Memory: lowest available 51.54 GB, peak commit 49.05 GB of 101.47 GB, page file peak 2610 MB (as at the start); no alert fired (no `alerts.log`). win2b's jobs were on the machine throughout.
