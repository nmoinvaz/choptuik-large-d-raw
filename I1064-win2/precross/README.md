# I1064-win2/precross: base polishes to ks 315 on win2 from two states before the crossing: ks_chain3b's leg 10 states at D 260.0073 and D 259.4568, each with its ks 293 control

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1064. Task: the coordinator's hc of 2026-11-21 (~11:31 UTC), moved
from dh610's queue after the first two arms on win2 (folder `../`: own test, post 7060623893; `../natural/`: natural test, post 7061935318), where ks 315 and 316 from D 261.6229 failed under both tests.

## Setup (written 2026-11-21 11:32 UTC, before any run)

| | |
|---|---|
| states | `I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_pin3_D260.0073.npz` (blob 7d45e683..., Delta share 0.991 per the hc) and `.../anm_pin3_D259.4568.npz` (blob 7e2452f7...), ks 293, read only from `D:/choptuik-large-d-raw-push` (raw main c6248595); `run1064p.sh` checks both blobs before any run |
| code | worktree `D:/choptuik-i1060` at main **8179068d** (clean), `hp/anm_run.py`, `hp/exact_recip_check.py`; venv `C:\Users\nathan\Source\venv-i1058b`; as in `../` |
| command | the first arm's line (`../flags_leg13.txt`, blob 583db2d4, dh610's leg 13 line with `--od_accept own`, 10 threads) with only `--state`, an absolute OUT and `--steps 0 --keep_plan 0 --save_base 1 --ks K --D_max 270.8483` changed (the command is in the issue comment before the run and in each log's first line) |
| rungs | 1. **the two ks 293 controls**, one per state, side by side, 10 threads each; 2. **ks 315 from each state whose control converged**, side by side, 10 threads each. Caps 7200 s each by the exact root pid (`taskkill /T /F /PID` after the command line is checked) |
| controls first | `../gate1064.py --selftest` (exit 0) and `--selftest --break` (exit 1); `../xcheck1064.py --planted STATE ctl_test` (exit 0) and `--mutate` (exit 1); the report script `report_precross.py` was run on planted logs before the launch and fired both readings (a converging 315, and no 315 run). The run stops if a control is wrong |
| files | `../gate1064.py`, `../xcheck1064.py`, `../cmp_lib/`, `../flags_leg13.txt` are the parent folder's, unchanged; `run1064p.sh`, `lib_1064.sh` (OUT changed), `report_precross.py` (new, replaces the table script, which has one state's names), `mem_watch.ps1`, `commit_watch.ps1` (alert-only, 30 s samples, kill nothing) |
| memory | as in `../`: I tell the coordinator at commit over 99 GB, a page file up by 2 GB, or available under 1 GB for 5 min. win2b's jobs share the machine |
| start max\|F\| | the first \|F\| of the log's `on 0:` step line (the octo-double max\|F\| of the base at that order, as in the first two arms), given beside each rung's verdict. For the comparison: D 261.0721's, read from `I1064-dh610/ks315.log`, and D 261.6229's, read from `../ks315.log` |

## Readings fixed before the runs (the coordinator's)

1. **A ks 315 that converges** (the gate: the last octo-double Newton line says converged and the base is saved) means the chain can rerun from that state at order 315.
2. **Both ks 315 failing**: compare their start max|F| with D 261.0721's (1.35e-11 in the hc) and D 261.6229's (1.15e-8).
3. **A state's ks 293 control must converge** (the gate); if it does not, that state's 315 is not started and it is reported (the issue's reading). A cap that fires is a result (the gate then reads "no octo-double Newton line"). Nothing is rerun or loosened.

A note on the comparison figure, read from the files before the runs: dh610's `ks315.log` at D 261.0721 starts at max\|F\| **1.36e-11** (step 0 line); the hc's 1.35e-11 is the start of dh610's `ks295.log` (order 295). The report prints both.

Information (not in the readings): each converged 315 base against its own control's base, and each control's base against its stored state, by `exact_recip_check.py delta` and `xcheck1064.py`.

## Result (run 2026-11-21 11:32:48 to 12:22:36 UTC)

Reading 3: both ks 293 controls converged (62 s each). Reading 1 does not apply: **neither ks 315 converged**. Reading 2 applies: the start max|F| at order 315 is compared with
D 261.0721's and D 261.6229's below. Nothing was rerun or loosened. Both rungs stopped on their own ('no trial step accepted'), at 2625 s and 2883 s, inside the 7200 s caps (no cap fired).

| state | order | exit, wall | gate | start max\|F\| (step 0 line) | od steps | last od line max\|F\| | how it stopped |
|---|---|---|---|---|---|---|---|
| D 260.0073 | 293 (control) | 0, 62 s | converged, base saved | 3.97e-36 | 1 | 4.0e-36, converged | converged |
| D 260.0073 | 315 | 0, 2883 s | failed, base not saved | **9.54e-12** | 3 | 5.7e-11, not converged | step 2: no trial step accepted |
| D 259.4568 | 293 (control) | 0, 62 s | converged, base saved | 2.51e-36 | 1 | 2.5e-36, converged | converged |
| D 259.4568 | 315 | 0, 2625 s | failed, base not saved | **1.57e-11** | 2 | 2.7e-11, not converged | step 1: no trial step accepted |

Start max|F| at order 315 across the states tried (the first |F| of each ks 315 log's step 0 line; all with the own test):

| state D | start max\|F\| at order 315 | verdict | source |
|---|---|---|---|
| 259.4568 | 1.57e-11 | failed | this folder |
| 260.0073 | 9.54e-12 | failed | this folder |
| 261.0721 | 1.36e-11 | failed (dh610's ks 315) | `I1064-dh610/ks315.log`; the hc's 1.35e-11 is the start of `ks295.log` (order 295) |
| 261.6229 | 1.15e-08 | failed (own and natural) | `../ks315.log`, `../natural/ks315.log` |

What the table and the logs show, no cause claimed:

- The start max|F| at order 315 is 9.5e-12 to 1.6e-11 at the three states from D 259.4568 to D 261.0721, and 1.15e-08 at D 261.6229, three orders higher. The three at about 1e-11 all failed, so a start of about 1e-11 is not low enough for this polish to converge. At order 293 the same states start at 2.5e-36 to 4.0e-36.
- Both polishes ended above their start: the accepted steps raised max|F| (D 260.0073: 9.54e-12 -> 3.44e-11 -> 5.67e-11, lam 0.25 twice; D 259.4568: 1.57e-11 -> 2.71e-11, lam 0.125). Each log ends 'base polish not adopted' (9.5e-12 -> 5.7e-11 and 1.6e-11 -> 2.7e-11): the stored state stays the base.
- The own test (|dz_t| < |dz|) refused trials with a lower max|F| than the iterate's, as at D 261.6229. D 260.0073: step 1 lam 1 reached 2.92e-14 (iterate 3.44e-11), step 2 lam 1 4.07e-15, lam 0.125 9.11e-13, lam 0.03125 6.31e-13 (iterate 5.67e-11). D 259.4568: step 1 lam 0.25 reached 1.55e-12, lam 0.0625 3.05e-12, lam 0.0039 5.10e-12 (iterate 2.71e-11). Each was refused ('not <'). The natural test was not run at these states (not ordered); at D 261.6229 it accepted such trials and still stalled at 2.1e-12 (ks 316) and 5.7e-11 (ks 315).
- The strong chord is refused at step 0 in both (chord 0 max|F| 2.91e+10 and 4.41e+10; 174.43 s and 149.79 s).
- The double-double |F| in the 'base ...' lines (2.5e+31, 3.7e+31) is not a residual (AGENTS.md, #903) and is not quoted as one.

Information (not in the readings): each control's base against its stored state (`delta1064_D260.0073_ctl_vs_state.json`, `delta1064_D259.4568_ctl_vs_state.json`): D equal to 50 digits (260.0072663205446736 and 259.4567664040657674 to the digits printed), Delta(b) - Delta(a) = 0.0 in both, `xcheck PASS`.
No 315 converged, so no Delta(315) - Delta(293) was computed.

`table_precross.md` is written by `report_precross.py` (planted-log tested before the launch). Per-step and per-trial lines are in `D<D>_ks315.log`.

Memory: lowest available 52.19 GB, peak commit 46.98 GB of 101.47 GB, page file peak 2610 MB (as at the start); no alert fired (no `alerts.log`). win2b's jobs were on the machine throughout.
