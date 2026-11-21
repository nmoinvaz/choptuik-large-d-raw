# I1064-win2: base polishes from the chain's front on win2: ks_chain3b's leg 14 state at D 261.6229 at ks 293 (control), 315 and 316

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1064. Task: the coordinator's hc of 2026-11-21 (read 08:37 UTC): "#1064 on win2: the order raise from a later chain state. dh610's polishes to ks 315, 316, 317 and 318 from D 261.0721 (inside the D 260.85 crossing) all failed at their 2 h caps. The Delta mode is now leaving the crossing: share 0.693 in the lowest vector at D 261.6229 (#1057), heading to 0.9 near D 261.84. Test whether the raise works already here." Companion: `I1064-dh610/` (dh610's rungs from D 261.0721: control ks 293 converged in 90 s; 315, 316, 317, 318 did not converge).

## Setup (written 2026-11-21 08:39 UTC, before any run)

| | |
|---|---|
| state | `I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D261.6229.npz` (blob e0737904cb19..., raw origin/main dbbaa570; read from the push worktree `D:/choptuik-large-d-raw-push`, read only; the run script checks the blob) |
| code | worktree `D:/choptuik-i1060` at main **8179068d** (clean; the #1060 worktree), `hp/anm_run.py` and `hp/exact_recip_check.py`; venv `C:\Users\nathan\Source\venv-i1058b` (hpkernel from 8179068d) |
| command | dh610's `run1064.sh` line (comment 7056415743 on #1064): leg 13's own anm_run line (`I966-dh370/ks_chain3b_q_dry.log`) with only `--state`, an absolute OUT, and `--steps 0 --keep_plan 0 --save_base 1 --ks K` changed (#973's form), `--threads 10`, `--D_max 270.8483`: `python -u anm_run.py D:/choptuik-large-d-raw-push D:/choptuik-i935-raw/I1064-win2/ks<K> --state I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D261.6229.npz --kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 10 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --steps 0 --ks <K> --keep_plan 0 --save_base 1 --D_max 270.8483` (also in `flags_leg13.txt` and the first line of each `ks<K>.log`) |
| leg 14's own line differs (reported, not used) | the chain's own line for this state (leg 14, `ks_chain3b_s_dry.log`) has one more option, **`--reseed_o_bar 1e-17`**, and `--D_max 271.1415`; otherwise it is leg 13's line. The coordinator named dh610's (leg 13's) line, which is what I run (so the rungs compare with dh610's from D 261.0721). The coordinator (hc, 21 Nov): the bar acts only on a step attempt's re-seed and a `--steps 0` run has none; `--D_max` does not matter either; so leg 13's line is equivalent for a base polish and no rung with `--reseed_o_bar` is needed (not tested here; the coordinator's statement) |
| rungs | 1. **control ks 293** (the state's own order; must converge), 10 threads; 2. **ks 315 and 316 side by side**, 10 threads each (the machine's 20). ks 317 and 318 are not ordered here. Each run is capped at **7200 s by its exact root pid** (command line checked for `anm_run.py`, `taskkill /T /F /PID`), BelowNormal; if the control fails the rungs are not started |
| controls first | dh610's, copied: `gate1064.py --selftest` (exit 0) and `--selftest --break` (exit 1); `xcheck1064.py --planted STATE ctl_test` (exit 0) and `--mutate` (exit 1). The run stops if one is wrong |
| files copied from dh610's `I1064-dh610/` | `gate1064.py` (blob 27aa4d76) and `table1064.py` (360e1082) unchanged; `xcheck1064.py` (dh610's blob 5b99266c) with **its two paths to `cmp1060.py` changed**: dh610's imports it from `../I1060-dh610/` (his folder, not present here), mine from `cmp_lib/cmp1060.py`, a copy of dh610's current `I1060-dh610/cmp1060.py` (blob **fce27737**, commit ed42fee0 "exact-sum verdict", which has the `exact()` function xcheck needs; the older `cmp1060.py` I used in #1060, blob 953872c9, does not). Two launches stopped at their own controls before any rung started, as designed ("a control is wrong: stop"): the first (08:39:39 UTC) on the import path, the second (08:40:31 UTC) on the missing `exact()` (`stopped_first_try/`, `stopped_second_try/`, each with its files); the third launch follows |
| memory | alert-only watches (`mem_watch.ps1`, `commit_watch.ps1`, 30 s samples, kill nothing); I tell the coordinator at commit over 99 GB, a page file up by 2 GB, or available under 1 GB for 5 min. win2b's det points (k_c 71) may still run on the machine |

## Readings fixed before the runs (#1064's)

1. **Converged by the gate** (#973's, as dh610's `gate1064.py`): a rung converges when the LAST octo-double Newton line of its log says "converged" (not "not converged") and the base is saved (`base_pin3_D*.npz` in its OUT). Reported for every rung: converged or not, its iteration lines and seconds, its exit and wall.
2. **For each converged rung, Delta(K) - Delta(293)** with both states at the same D to 50 digits (`exact_recip_check.py delta`, then `xcheck1064.py`, a second sum of the parts as an independent check).
3. **If the control (ks 293) fails: stop and report** (the rungs are not started). **If neither 315 nor 316 converges:** reported as it is; the issue's decision (another route, or the other rungs 317 and 318) is the coordinator's.
4. A cap that fires is a result (the gate then reads "no octo-double Newton line", as at dh610's). Nothing is rerun or loosened.
Information (not in the readings): the control's base against the stored state (`--keep_plan 0` plans the base again), as at dh610's `delta1064_ctl_vs_leg13`.

## Result (run 2026-11-21 08:41:25 to 09:29:14 UTC)

Readings 1 and 3: the control converged, and neither ks 315 nor ks 316 converged. Reading 2: no rung converged, so there is no
Delta(K) - Delta(293). Nothing was rerun or loosened.

| K | exit | wall s (own, by exact pid) | gate | od Newton lines and seconds |
|---|---|---|---|---|
| 293 (control) | 0 | 61 | converged: 1 step, max\|F\| 2.0e-36, base saved | step 0: \|F\| 1.96e-36, converged |
| 315 | 0 | 2781 | failed: 2 steps, max\|F\| 1.9e-08, not converged, base not saved | step 0: strong chord (4 weak directions) refused, 251.34 s; trials lam 1 to 0.0625 refused, lam 0.03125 taken: \|F\| 1.15e-08 -> 1.88e-08, 1058.16 s in all; step 1: nine trials lam 1 to 0.0039 refused, 'no trial step accepted, stopping' |
| 316 | 0 | 1918 | failed: 1 step, max\|F\| 1.1e-08, not converged, base not saved | step 0: strong chord refused, 245.63 s; nine trials lam 1 to 0.0039 refused, 'no trial step accepted, stopping' |

Per-step trial lines are in `ks315.log` and `ks316.log`. What the logs show, without a cause:

- The control's od residual is 1.96e-36 at the stored state. At ks 315 and ks 316 the polish starts at od max\|F\| 1.15e-08 (both).
- The first chord of each polish is refused (chord 0 max\|F\| 9.63e-10 at ks 315 and 9.38e-11 at ks 316, chord 1 8.59e+11 and
  1.72e+12; theta at its point inf, bound 0.750).
- The trials at lam 1 reach max\|F\| 9.63e-10 (ks 315) and 9.38e-11 (ks 316), below the start, and are refused by the
  \|dz_t\| < \|dz\| test (raw \|dz_t\| 8.9e-20 against \|dz\| 8.9e-21, and 7.8e-19 against 9.6e-21).
- ks 315 took one step (lam 0.03125) that raised \|F\| from 1.15e-08 to 1.88e-08; the polish was 'not adopted' and the stored state stays the base.
- Both rungs stopped on their own ('no trial step accepted'), at 1919 s and 2782 s, well inside the 7200 s caps. No cap fired.
  dh610's polishes from D 261.0721 ended at their 2 h caps (the coordinator's hc), so the stop mode differs; the end state, no converged base, is the same.
- The double-double \|F\| that the 'base ...' line prints (1.0e+32 to 1.6e+32) is not a residual (AGENTS.md, #903) and is not quoted as one.

Information (not in the readings): the control's base against the stored state (`delta1064_ctl_vs_state.json`, `xcheck1064_ctl_vs_state.txt`):
D equal to 50 digits (261.62291163319045732282841498772540944628417491913), Delta(b) - Delta(a) = 0.0 by the exact reciprocal sums and by the
independent exact sums; `xcheck PASS`. A `--keep_plan 0` polish of the converged state changes nothing in Delta at the check's bound (1e-30).

`table_1064.md` was written by dh610's `table1064.py` unchanged. Its closing note ('Wall of ks293 to ks318 ... exits_1064b.txt') is the
script's fixed text for dh610's run and does not apply here: this run has one exits file, `exits_1064.txt`, and each rung's wall is its own, from its own crun.

Memory: lowest available 51.22 GB, peak commit 49.03 GB of 101.47 GB, page file peak 2610 MB (as at the start); no alert fired. win2b's jobs were on
the machine throughout.

Slips: two launches (08:39:39 and 08:40:31 UTC) stopped at their own controls before any rung started, on `xcheck1064.py`'s import of
`cmp1060.py`; both are in `stopped_first_try/` and `stopped_second_try/`. The third launch (08:41:25) is the run above.

See [natural/](natural/README.md) for the same rungs with `--od_accept natural` (README first, readings fixed before the runs).
See [precross/](precross/README.md) for ks 315 from two states before the crossing (D 260.0073, D 259.4568).
