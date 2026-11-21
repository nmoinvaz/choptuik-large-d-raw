# I1064-win2/precross_natural: base polishes to ks 315 on win2 from two states before the crossing with --od_accept natural: ks_chain3b's leg 10 states at D 260.0073 and D 259.4568, each with its ks 293 control

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1064. Task: the coordinator's hc of 2026-11-21 (~12:24 UTC), after
`../precross/` (own test: both ks 315 failed, post 7062537228). The lead the hc names: the own test refused trials with far lower max|F| (4.07e-15 against an iterate at 5.67e-11 at D 260.0073). dh170 is meanwhile testing whether the start
residual has a large step component along the weak direction (not part of this folder).

## Setup (written 2026-11-21 12:25 UTC, before any run)

| | |
|---|---|
| states | as in `../precross/`: `I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_pin3_D260.0073.npz` (blob 7d45e683...) and `.../anm_pin3_D259.4568.npz` (blob 7e2452f7...), ks 293, read only from `D:/choptuik-large-d-raw-push`; `run1064n2.sh` checks both blobs before any run |
| code | worktree `D:/choptuik-i1060` at main **8179068d** (clean), venv `C:\Users\nathan\Source\venv-i1058b`; as in `../` |
| command | `../precross/`'s line with **only `--od_accept own` changed to `--od_accept natural`**: `../natural/flags_natural.txt` (blob e8dbadce), which is `../flags_leg13.txt` with that one word changed; `run1064n2.sh` checks this before any run (it stops otherwise) |
| rungs | 1. **the two ks 293 controls** (natural), one per state, side by side, 10 threads each; 2. **ks 315 from each state whose control converged**, side by side, 10 threads each. Caps 7200 s each by the exact root pid (`taskkill /T /F /PID` after the command line is checked) |
| controls first | `../gate1064.py --selftest` (exit 0) and `--selftest --break` (exit 1); `../xcheck1064.py --planted STATE ctl_test` (exit 0) and `--mutate` (exit 1); the flags check (passes on the natural flags; fails on the own flags and on an eps change, tested in the natural arm); `report_precross_natural.py` was run on planted logs before the launch and fired the converged reading (the failing reading is the sibling script's, which ran on real logs in `../precross/`). The run stops if a control is wrong |
| files | the gate, `xcheck1064.py`, `cmp_lib/`, `flags_leg13.txt`, `natural/flags_natural.txt` are the parent folder's, unchanged; `run1064n2.sh` (from `../precross/run1064p.sh`), `lib_1064.sh` (OUT changed), `report_precross_natural.py` (from `../precross/report_precross.py`, strings and the own-test lines changed), `mem_watch.ps1`, `commit_watch.ps1` (alert-only, kill nothing) |
| memory | as in `../`: I tell the coordinator at commit over 99 GB, a page file up by 2 GB, or available under 1 GB for 5 min. win2b's jobs share the machine |
| start max\|F\| | the first \|F\| of the log's `on 0:` step line, as in `../precross/` |

## Readings fixed before the runs (the coordinator's)

1. **A ks 315 that converges under natural** (the gate: the last octo-double Newton line says converged and the base is saved) means the chain can rerun from that state at order 315 with the natural test for the raise. Delta(315) - Delta(293) is then reported (same D to 50 digits, `exact_recip_check.py delta` then `xcheck1064.py`; 293 = this folder's control of the same state).
2. **Both ks 315 failing** means neither test carries the raise from a start of about 1e-11.
3. **A state's ks 293 control must converge** (the gate); if it does not, that state's 315 is not started and it is reported. A cap that fires is a result. Nothing is rerun or loosened.

Reported beside each verdict: start max|F|, od steps, last od line, seconds, how it stopped, and the own test's run of the same state from `../precross/`.

## Result (run 2026-11-21 12:25:17 to 14:27:15 UTC)

Reading 3: both ks 293 controls converged under natural (60 s and 76 s). Reading 1 does not apply: **neither ks 315 converged under natural**. Reading 2 applies: neither test carries the raise from a start of about 1e-11.
No Delta(315) - Delta(293) is reported, since none converged. Nothing was rerun or loosened. D 259.4568 stopped on its own inside the cap; **D 260.0073 reached the 7200 s cap** (killed by the exact root pid at 14:26:41 UTC, in step 8),
so its gate reads "no octo-double Newton line", as the README fixed for a cap.

| state | arm | order | exit, wall | gate | start max\|F\| | od steps | last od line max\|F\| | how it ended |
|---|---|---|---|---|---|---|---|---|
| D 260.0073 | natural | 293 (control) | 0, 60 s | converged | 3.97e-36 | 1 | 4.0e-36, converged | converged |
| D 260.0073 | natural | 315 | 1, 7201 s, **CAPPED** | failed (no od Newton line) | **9.54e-12** | 8 accepted steps, step 8 unfinished | none (killed); the last accepted iterate 9.05e-12 | cap |
| D 260.0073 | own (`../precross/`) | 315 | 0, 2883 s | failed | 9.54e-12 | 3 | 5.7e-11, not converged | no trial step accepted |
| D 259.4568 | natural | 293 (control) | 0, 75 s | converged | 2.51e-36 | 1 | 2.5e-36, converged | converged |
| D 259.4568 | natural | 315 | 0, 4908 s | failed | **1.57e-11** | 4 | 2.3e-11, not converged | step 3: no trial step accepted; base not adopted |
| D 259.4568 | own (`../precross/`) | 315 | 0, 2625 s | failed | 1.57e-11 | 2 | 2.7e-11, not converged | no trial step accepted |

The max\|F\| after each accepted step (`on k:` lines of the logs):

| state | start | step 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|
| D 260.0073 (lam 0.5, 0.031, 0.125, 0.031, 0.0625, 0.0625, 0.0625, 0.25) | 9.54e-12 | 4.03e-12 | 1.71e-12 | 2.57e-12 | 2.02e-12 | 3.50e-12 | 2.65e-12 | 2.65e-11 | 9.05e-12 |
| D 259.4568 (lam 0.0625, 0.25, 0.0078) | 1.57e-11 | 9.39e-12 | 1.24e-12 | 2.26e-11 | | | | | |

What the logs show, no cause claimed:

- Under natural the polish takes steps where the own test took none: every step's lam 0.0078 to 0.5 trial was accepted (ratio against its bound in each trial line), 8 steps at D 260.0073 and 3 at D 259.4568. Step 0 at both states lowers max\|F\| (9.54e-12 -> 4.03e-12; 1.57e-11 -> 9.39e-12) where the own test raised it.
- max\|F\| reaches a lowest of 1.71e-12 (D 260.0073, step 1) and 1.24e-12 (D 259.4568, step 2), about one order and one to two orders below the start, then rises again (D 260.0073 to 2.65e-11 at step 6, D 259.4568 to 2.26e-11 at step 3). Neither approaches the tolerance 2e-34; the gap is about 1e22 at the lowest values.
- D 259.4568 stopped at step 3 ('no trial step accepted'); D 260.0073 was still stepping when the cap fell (its step 8 trials lam 1 to 0.0625 were all refused, the last with max\|F\| 1.79e-13 and ratio 0.985 against the bound 0.984).
- The strong chord is refused at step 0 in both (194.7 s and 164.33 s), as under the own test.
- Compared with the own test at the same states: natural runs more steps and ends no nearer the tolerance (the last od lines, 2.3e-11 against 2.7e-11 at D 259.4568; none against 5.7e-11 at D 260.0073).
- The double-double \|F\| in the 'base ...' lines is not a residual (AGENTS.md, #903) and is not quoted as one.

Start max\|F\| at order 315 across the states tried (the first \|F\| of each ks 315 log's step 0 line): D 259.4568 1.57e-11, D 260.0073 9.54e-12, D 261.0721 1.36e-11 (dh610's `ks315.log`; the 1.35e-11 of the hc is `ks295.log`'s), D 261.6229 1.15e-08. All failed under the own test; D 261.6229 also under natural (`../natural/`).

Information (not in the readings): each control's base against its stored state (`delta1064_D260.0073_ctl_vs_state.json`, `delta1064_D259.4568_ctl_vs_state.json`): D equal to 50 digits, Delta(b) - Delta(a) = 0.0 in both, `xcheck PASS`.

`table_precross_natural.md` is written by `report_precross_natural.py`. Per-step and per-trial lines are in `D<D>_ks315.log`.

Memory: lowest available 51.12 GB, peak commit 49.49 GB of 101.47 GB, page file peak 2610 MB (as at the start); no alert fired (no `alerts.log`). win2b's jobs were on the machine throughout.
