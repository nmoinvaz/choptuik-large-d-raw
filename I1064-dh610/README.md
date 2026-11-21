# I1064-dh610: base polishes from the chain's front, leg 13's D 261.0721 state of ks_chain3b, at ks 293 (control), 315, 316, 317, 318, then 295, 297, 301 and 305

Machine: dh610 (Fedora desktop, Linux 7.3, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1064

Build: main 8179068d in the #1060 worktree `~/Source/choptuik-large-d-1060`, venv-i1058 (the build that ran #1060). Leg 13 itself ran at build 1aa4a4fb (`ks_chain3b_q.log`).
State: `I966-dh370/ks_chain3b/leg13_D260.8483_ks293/anm_pin3_D261.0721.npz` (blob bd2c69a4, taken from raw origin/main a0177d81; D 261.07211346726637581..., ks 293, N 31,
leg 13's last octo-double line there: 3 steps, max|F| 7.4e-38, converged against `--tol_od 2e-34`). Leg 13's own line is `ks_chain3b_q_dry.log` of `I966-dh370/`.

Command: leg 13's line with only `--state`, an absolute OUT, `--steps 0 --keep_plan 0 --save_base 1 --ks K` changed (as in #973), `--threads 10`, `nice -n 10` (the full line is in
`ks<K>.log`'s first line and in the issue comment). Rungs: 1 the control ks 293; 2 ks 315 and 316 side by side; 3 ks 317 and 318 side by side. Each run is capped at 7200 s by TERM to its
exact pid. Reading (the issue's): a rung converges when its last octo-double Newton line says converged and the base is saved (`gate1064.py`); for the converged rungs, Delta(K) - Delta(293)
with both states at the same D to 50 digits (`exact_recip_check.py delta`, then `xcheck1064.py`, a second sum of the parts). If the control fails the rungs are not started.

| file | what |
|---|---|
| `common1064.sh`, `run1064.sh` | the paths and the unit's script (controls, the rungs, the deltas, the table) |
| `gate1064.py` | the verdict of one polish; `--selftest` runs seven planted logs, `--break` must exit 1 |
| `xcheck1064.py` | Delta(b) - Delta(a) of `exact_recip_check.py delta` against exactly summed parts (Fractions); `--planted` makes a state with a known shift of 1e-20; `--mutate` must exit 1 |
| `controls_xcheck1064.txt` | its controls before the run (planted, `--mutate`, a pair at different D, a state against itself) |
| `table1064.py`, `table_1064.md` | the table of every rung |
| `ks<K>.log`, `ks<K>/` | a rung's stdout and output directory; `gate_ks<K>.txt` its verdict |
| `delta1064_K<K>.json`, `.log`, `xcheck1064_K<K>.txt` | Delta(K) - Delta(293) and its check; `delta1064_ctl_vs_leg13.*` the control's base against the stored leg 13 state (information) |
| `exits_1064.txt`, `summary_1064.txt`, `memlog_1064.log` | exits, verdicts, the alert-only memory log |
| `dry_cap/` | the dry test of the cap and the control-failed branch (cap 45 s on the control; it must be killed, fail the gate and start no rung) |

Note on `gate973.py` (reported, not changed): its regex `(NOT converged|converged)` does not match the lower-case `not converged` that anm_run.py of main 796f4bac and 8179068d prints, so a last line
`not converged` is skipped and an earlier `converged` line would be read. `gate1064.py` matches both cases and reads the last line (its selftest has both).

## Added rungs (coordinator, 05:24 UTC 21 Nov)

After rung 2 (ks 315 capped, exit 143; ks 316 stopped itself, exit 0, `octo-double Newton: 4 steps, max|F| 3.2e-10, not converged`), the coordinator asked for rung 3 (317, 318) to run, then ks 295 with 297,
then 301 with 305, the same flags, caps and gate. The control is the converged ks 293 of unit `i1064`.

Defect in `run1064.sh` (reported, not fixed there): each run's wall in `exits_1064.txt` is taken after the whole rung ended, so ks 316 (which ended itself, no `cap` line) shows the rung's 7232 s.
`run1064b.sh` takes each run's own wall (the first 30 s poll that finds its pid gone), and `table1064.py` marks capped runs and says which walls are which.

| file | what |
|---|---|
| `run1064b.sh` | the unit's script for ks 295, 297, 301, 305 (preflight, controls, the two rungs, deltas against the ks 293 base, table); env `OUT1064`, `CAP1064`, `R1_1064B`, `R2_1064B`, `THR1064B` are for the dry test only |
| `check_dry1064b.py` | the pass test of the dry run (ks 293 against ks 315 at a 240 s cap: 293 converges on its own, 315 is killed by its exact pid, the walls differ); `--selftest` has a pass case and five broken ones, `--break` exits 1 |
| `exits_1064b.txt`, `summary_1064b.txt`, `memlog_1064b.log`, `table_1064b.md` | the unit's exits, verdicts, alert-only memory log and the table of every rung |
| `dry_b/` | the dry test's output and `check_dry1064b.txt` |

## Result of rungs 1 to 3 (unit `i1064`, 03:20:43 to 07:23:17 UTC, 21 Nov)

| K | exit | verdict (gate) | end |
|---|---|---|---|
| 293 (control) | 0 | converged: 1 step, max\|F\| 1.5e-36, base saved | 90 s |
| 315 | 143 | failed: no octo-double Newton line | TERM to its exact pid at 7200 s (05:22:15), in step 3's trials |
| 316 | 0 | failed: 4 steps, max\|F\| 3.2e-10, not converged, no base saved | stopped itself: `no trial step accepted, stopping` |
| 317 | 143 | failed: no octo-double Newton line | TERM at 7200 s (07:22:47) after `no trial step accepted, stopping` (max\|F\| 1.66e-10), before its final Newton line |
| 318 | 143 | failed: no octo-double Newton line | TERM at 7200 s (07:22:47), in step 2's trials (max\|F\| 1.05e-09 after step 1) |

`table_1064.md` has the iteration lines. The `wall` in `exits_1064.txt` and in the table is the rung's (7232 s for both of a rung), not each run's own (defect of `run1064.sh`, see above).

Information, not a verdict: the control's saved base against the stored leg 13 state (`delta1064_ctl_vs_leg13.*`): Delta equal in all 40 printed digits, difference 0.0 (xcheck passes). Per entry (exact sums of the eight parts, 769 entries):
the polish moved 64 entries by up to 5.1e-49 (max |S| 1.683), the Delta entry by 0; `zh` and `zl` are byte-equal, `z2` to `z7` differ in 31 to 64 entries. `cmp1060.py bits` does not apply to a base file (no `a` in its meta).

## Result of ks 295 and 297 (unit `i1064b`, 07:28:10 to 08:52:12 UTC, 21 Nov)

Both failed the gate and both stopped themselves (exit 0, no cap): `exits_1064b.txt` has each run's own wall (30 s polls), `summary_1064b.txt` the verdicts, `table_1064b.md` the table.

| K | own wall | gate | steps (max\|F\| before -> after, lam, seconds) | end |
|---|---|---|---|---|
| 295 | 4441 s | failed: 3 steps, max\|F\| 3.1e-08, not converged | 1.35e-11 -> 4.28e-07, 0.25, 1365; -> 1.09e-06, 0.031, 1142; -> 3.06e-08, 0.0078, 1594 | `lam at or below 0.04 twice in a row, stopping (stalled)` |
| 297 | 5041 s | failed: 4 steps, max\|F\| 1.4e-08, not converged | 8.38e-12 -> 3.35e-11, 0.5, 1229; -> 2.52e-08, 0.125, 1404; -> 1.41e-08, 1, 197 | step 3: nine refused trials, `no trial step accepted, stopping` |

Dry test of `run1064b.sh` (`dry_b/`, `check_dry1064b.txt`): passed; its ks 293 base is byte-identical to the control's in all eight parts.

Second rung: no leg 14 state is flagged at a Delta share of 0.9 or more (dh170's #1057 read of D 261.6229, 08:26 UTC: 0.693), so ks 301 with 305 from the D 261.0721 state, as the coordinator's rule says (`run1064b.sh` with `R1_1064B="301 305"`, unit `i1064d`, memory log `memlog_1064d.log`).

## ks 301 and 305 stopped; ks 293, 295 and 297 from D 261.6229 (coordinator, 08:54 UTC 21 Nov)

Unit `i1064d` (ks 301 and 305 from D 261.0721, `run1064b.sh` with `R1_1064B="301 305"`, from 08:53:51 UTC) was stopped at the coordinator's order: TERM to its exact pids 1018097 and 1018102 at 08:54:47 UTC, both exit 143 after 60 s (no cap line; `exits_1064b.txt`). `ks301.log` and `ks305.log` hold the first minute only and are no result.

Instead: ks 293 (the control) alone, then ks 295 and 297 side by side, from `I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D261.6229.npz` (blob e0737904cb191e88a688df2e3968222c0920d3e5, extracted from raw origin/main commit 98e9e284), same flags (leg 13's line, as for every rung), gate and 7200 s caps. Folder `leg14_D261.6229/`, script `run1064c.sh` (env `ST1064C`, `STBLOB1064C`, `TAG1064C`, `R_1064C`), unit `i1064e` from 09:02:12 UTC, memory log `memlog_1064e.log`.
Reading (the coordinator's): small jumps converging here while 315 and 316 fail (win2's, comment 7060065590) means a ladder of small raises can lift the order; all failing means the raise waits for a state past the crossing (Delta share at or above 0.9).

Dry tests before the unit (`dry_c1/`, `dry_c2/`, `check_dry1064c.txt` in each; `check_dry1064c.py` has a selftest of nine cases and `--break` exits 1): pass path (control converged in 120 s, max|F| 2.0e-36; ks 297 killed at the 240 s cap by its exact pid; the control against the stored state has Delta difference 0.0, xcheck passes) and control-failed path (control killed at 45 s, `control failed: rungs not started`, no rung started). Both passed.

## Result of ks 293, 295 and 297 from D 261.6229 (unit `i1064e`, 09:02:12 to 09:54:43 UTC, 21 Nov)

Folder `leg14_D261.6229/` (`table_1064c.md`, `exits_1064c.txt`, `summary_1064c.txt`, `ks<K>.log`, `gate_ks<K>.txt`). No memory alert (`memlog_1064e.log`).

| K | own wall | gate | start max\|F\| at order K | end |
|---|---|---|---|---|
| 293 (control) | 90 s | converged: 1 step, max\|F\| 2.0e-36, base saved | 1.96e-36 | |
| 295 | 3060 s | failed: 1 step, max\|F\| 6.3e-09, not converged, base not saved | 6.34e-09 | step 0: strong chord refused (530 s), nine trials lam 1 to 0.0039 refused (151 to 299 s), `no trial step accepted, stopping` |
| 297 | 3060 s | failed: 1 step, max\|F\| 5.1e-09, not converged, base not saved | 5.13e-09 | step 0: strong chord refused (539 s), nine trials lam 1 to 0.0039 refused (140 to 288 s), `no trial step accepted, stopping` |

Both rungs stopped themselves (exit 0, no cap line). The two walls are the same 30 s poll. Information: the control's base against the stored D 261.6229 state: Delta equal in all 40 printed digits (difference 0.0, xcheck passes); 64 of 769 entries moved by up to 1.05e-52 (exact sums), `zh` and `zl` byte-equal.
Reading (the coordinator's): all failing means the raise waits for a state past the crossing. With win2's ks 315 and 316 from the same state (comment 7060623893, also failed), all four raises tried here failed.

## Two pairs (coordinator, 09:5x UTC 21 Nov): ks 294 from D 261.6229 and D 261.0721, then ks 315 from leg 10's D 260.0073 and D 259.4568

Each state: its own ks 293 control first, then the K rung, as one `run1064c.sh` instance per state (units `i1064f`, `i1064g` for pair 1 from 09:57:59 UTC; `i1064h`, `i1064i` for pair 2, started when pair 1's units have ended), folders `k294_D261.6229/`, `k294_D261.0721/`, `k315_D260.0073/`, `k315_D259.4568/`. States (all under `I966-dh370/ks_chain3b/` in the raw repository, blobs checked on extraction): `leg14_D261.1415_ks293/anm_pin3_D261.6229.npz` e0737904cb19, `leg13_D260.8483_ks293/anm_pin3_D261.0721.npz` bd2c69a4d3fd, `leg10_D256.1776_ks293/anm_pin3_D260.0073.npz` 7d45e68357a3, `anm_pin3_D259.4568.npz` 7e2452f7d7f4. Same flags (leg 13's line), gate and 7200 s caps; `table1064.py` gets a column for each rung's start max|F| at order K (the log's step 0 `|F|`).
Readings (the coordinator's): a converging ks 294 means a ladder of +1 raises is open; a converging ks 315 before the crossing means the chain can rerun from that state at order 315; if nothing converges, the start |F| against D for all the states. `start_1064_next.sh` only launches the four units.

## Result of pair 1: ks 294 from D 261.6229 and from D 261.0721 (units `i1064f` and `i1064g`, from 09:57:59 UTC, 21 Nov)

Folders `k294_D261.6229/` and `k294_D261.0721/` (`table_1064c.md`, `exits_1064c.txt`, `summary_1064c.txt`, `ks293.log`, `ks294.log`, `gate_ks<K>.txt`). No memory alert (`memlog_i1064f.log`, `memlog_i1064g.log`). Both ks 293 controls converged (120 s each, max|F| 2.0e-36 and 1.5e-36), the control's base against its stored state has Delta difference 0.0 (xcheck 0). Both ks 294 runs stopped themselves, neither at the cap.

| state | start max\|F\| at order 294 | own wall | end |
|---|---|---|---|
| D 261.6229 (leg 14) | 2.25e-09 | 4021 s | step 0: strong chord refused (512 s), trial lam 1 refused, then 2.25e-09 -> 1.58e-08 at lam 0.5 (1062 s); step 1: nine trials lam 1 to 0.0039 refused, `no trial step accepted, stopping` at 1.6e-08; not converged, base not saved |
| D 261.0721 (leg 13) | 1.33e-11 | 5881 s | step 0: strong chord refused (549 s), 1.33e-11 -> 4.07e-12 (1614 s); step 1 -> 1.25e-09 (1446 s); step 2 -> 1.15e-09 (1189 s); step 3 -> 6.79e-10 (1270 s), `lam at or below 0.04 twice in a row, stopping (stalled)`; not converged, base not saved |

Reading (the coordinator's): a converging ks 294 means a ladder of +1 raises is open. Neither converged, so it is not open from either state with the old-order base.

## Pair 2 moved to win2 (coordinator, 11:3x UTC 21 Nov)

The coordinator moved ks 315 from D 260.0073 and D 259.4568 to win2. I stopped `start_1064_next.sh` by its exact pid (1024638) at 11:31:02 UTC, while `i1064g` was still running (the units are in systemd's app.slice, not children of the starter; `i1064g` ran on and ended at 11:38:00 UTC). Units `i1064h` and `i1064i` never started and there are no `k315_*` folders here. The two states were extracted from raw origin/main (blobs 7d45e683 and 7e2452f7) and are not used by me.

## The re-seeded base: `--reseed_base 1` (coordinator, ~11:35 UTC 21 Nov; main 276aa1cd)

Worktree `~/Source/choptuik-large-d-1060` moved from 8179068d to 276aa1cd (detached; `git log -1` shows it, tree clean; origin/main's head at the 11:32 UTC fetch). `run1064c.sh` pins 8179068d and no longer runs on it. `hp/` changed from 8179068d: `anm_run.py`, `arclength.py`, `ks_chain.py`, `octo_corrector.py` (Broyden updates, off by default), `od_broyden_ab.py`, `od_broyden_check.py`; `pyproject.toml`, `Cargo.toml` and `build.sh` unchanged (venv-i1058's kernel stays).

From `I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D261.6229.npz` (blob e0737904), leg 13's line plus `--reseed_base 1`, the gate and 7200 s caps of `run1064c.sh`: the control ks 293 alone, then ks 315 and ks 294 side by side. `run1064d.sh` (a copy of `run1064c.sh`: HEAD pinned to 276aa1cd, `--reseed_base 1`, the log's `base re-seed` line copied to `summary_1064d.txt`, the control's Delta against both earlier controls), `check_dry1064d.py` (selftest of 11 cases, `--break` exits 1), `table1064.py` (new column for the re-seed line; planted re-seeded and FAILED lines and logs without a line were checked). Unit `i1064j` (`start_1064_rb.sh`), folder `rb_D261.6229/`, memory log `memlog_i1064j.log`.

Dry runs (`dry_1064d.sh`, 11:40 to 11:48 UTC, `dry_d1/`, `dry_d2/`):
- `dry_d2` (control killed at the 45 s cap): passed.
- `dry_d1` (pass path, 420 s cap, rung 294): failed at the cap, not by the harness. The control printed `base re-seeded at ks 293 (--reseed_base 1), 87.69 s: octo-double max|F| 7.4e-25` (the stored state's own start was 1.96e-36, converged at once without the flag) and was in its first chord at the cap, 3.76e-27. Not rerun at a larger cap: that is the real run.

Pilot (`pilot_1064d.sh`, `dry_d3/`, 11:49 to 11:52 UTC): the real command at ks 294 and ks 315 side by side, each stopped by TERM to its exact pid at its `base re-seed` line.

| K | start max\|F\| without the flag (this state) | re-seeded max\|F\| with the flag | re-seed seconds | refinement rung max\|R\| |
|---|---|---|---|---|
| 293 (`dry_d1`) | 1.96e-36 | 7.4e-25 | 87.7 | 3.31e-12 to 1.25e-25 |
| 294 | 2.25e-09 | 2.3e-09 | 110.4 | 3.31e-12 to 3.84e-10 |
| 315 | 1.15e-08 (win2's, comments 7060065590, 7060623893) | 1.1e-08 | 127.5 | 3.31e-12 to 1.93e-09 |

The two earlier ks 293 controls of this state (`k294_D261.6229/ks293` and `leg14_D261.6229/ks293`) against each other: Delta difference 0.0, xcheck 0 (`dry_d3/delta_earlier_vs_earlier0.*`).

## Rung change (coordinator, ~11:5x UTC 21 Nov): ks 315 at D 261.6229 and at D 262.0099 instead of ks 294

dh170's #1057 trigger: the first chain state with the Delta share at or above 0.9 is `I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.0099.npz` (D 262.0099, share 0.9205; blob eb34f3c845a485d606907b6f7ba2dc9ef429aaf1, raw commit b8cccc18, extracted from origin/main with the blob checked). Unit `i1064j` (control only, from 11:52:12 UTC) was stopped by TERM to its exact pid 1036631 at 11:53:50 UTC (its control exits 143, "control failed: rungs not started"; no rung had started); its output is `rb_D261.6229_i1064j_stopped/`. Restart through `start_1064_rb2.sh` at 11:54:30 UTC: two instances of `run1064d.sh` (unchanged) with `R_1064D=315`, unit `i1064k` (D 261.6229, `rb_D261.6229/`) and unit `i1064l` (D 262.0099, `rb_D262.0099/`), each its own ks 293 control with `--reseed_base 1` first. At D 262.0099 there is no earlier control, so the two "earlier control" paths are the stored state and `delta1064_ctl_vs_earlier*` repeat `delta1064_ctl_vs_state`. No new dry run.

## Result of the re-seeded base run (units `i1064k` and `i1064l`, 11:54:30 to 14:39:33 UTC 21 Nov)

Folders `rb_D261.6229/` and `rb_D262.0099/` (`run1064d.sh` unchanged, main 276aa1cd, venv-i1058, `nice -n 10`, 10 threads each, memory logs `memlog_i1064k.log` and `memlog_i1064l.log` without an alert). The ks 293 controls with `--reseed_base 1` converged; the ks 315 runs did not (capped at 7200 s by TERM to pids 1040361 and 1041200, exit 143, no octo-double Newton line). Posted as comment 7064299181.

| state | K | re-seed line max\|F\| | first `on 0:` \|F\| | verdict | own wall |
|---|---|---|---|---|---|
| D 261.6229 | 293 control | 7.4e-25 | 3.39e-24 | converged, 4 steps, 4.3e-40 | 2040 s |
| D 261.6229 | 315 | 1.1e-08 | 1.89e-12 | capped, 3 steps taken | 7231 s |
| D 262.0099 | 293 control | 3.9e-25 | 1.84e-26 | converged, 5 steps, 2.5e-34 (floor rule) | 2670 s |
| D 262.0099 | 315 | 4.0e-11 | 5.43e-10 | capped, 3 steps taken | 7231 s |

Control Delta against the earlier ks 293 controls: D 261.6229 -3.11364e-20 (all three comparisons, as both earlier controls equal the stored state); D 262.0099 +1.01579e-19 (the stored state only). Projection failures in the ks 315 logs: 7 and 12; none in the ks 293 logs. Discrepancy reported: the pilot's "within 4% of the old start |F|" compared the re-seed line's max|F| with the old runs' first `on 0:` |F|; the re-seeded run's own first `on 0:` |F| at ks 315, D 261.6229 is 1.89e-12 against 1.15e-08 (win2, old base). What the first `on 0:` |F| measures against the re-seed line's is not established. `table_1064d.md` in each folder has the iteration lines.

## The projection switch from D 262.0099 (coordinator, ~14:45 UTC 21 Nov; main 276aa1cd)

Order: from `I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.0099.npz` (blob eb34f3c8), leg 13's line plus `--elim_switch 1e-9` (default 1e-15; no `--reseed_base`): the control ks 293 alone, then ks 315 with `--od_accept own` and ks 315 with `--od_accept natural` side by side, 7200 s caps by exact pid, the gate of `run1064d.sh`. dh170 found the stored state's own residual at ks 315 is 1.67e-30; the 4e-11 start comes from ElimO projecting each point whose pinned quad-double |F| exceeds the switch. Plan comment 7064371031 (thresholds of mine, written before any result: "near 1e-30" is a start |F| of at most 1e-28, "many orders" a step 0 ratio of at least 1e3).

Files: `run1064e.sh` (a braced block; runs `ks293`, `ks315own`, `ks315nat`; summary and table `table_1064e.md` via `table1064e.py`), `check_dry1064e.py` (13 planted cases, `--break` exits 1), `dry_1064e.sh`, `start_1064_sw.sh` (unit `i1064m`, folder `sw_D262.0099/`, memory log `memlog_i1064m.log`). `table1064e.py --selftest` has 12 planted cases (`--break` exits 1); on the old logs `rb_D262.0099/ks315.log`, `rb_D261.6229/ks293.log` and `k294_D261.0721/ks294.log` it reads start |F| 5.43e-10, 3.39e-24, 1.33e-11 and step 0 ratios 0.172, 0.0132, 0.306, as in the earlier posts.

Dry runs (`dry_1064e.sh`, 14:47 to 14:54 UTC, `dry_e1/`, `dry_e2/`, both passed `check_dry1064e.py`):
- `dry_e1` (pass path, 300 s cap): the control converged in 1 step at max|F| 3.9e-36 with no projection (`elim projections ... 'skipped': 1`), own wall 90 s; Delta against the stored state 0.0, against the re-seeded control (`rb_D262.0099/ks293`) -1.01579e-19 (xcheck 0 both). `ks315own` and `ks315nat` started at 14:48:58 with `--elim_switch 1e-9`, `--od_accept own` and `natural`, no `--reseed_base`, and were TERMed by their exact pids at 300 s (exit 143); neither had printed an `on` line by then.
- `dry_e2` (control killed at the 45 s cap): "control failed: rungs not started", no rung.

## The largest order a polish reaches at D 237.7132 (coordinator follow-on, 21 Nov; main 276aa1cd)

Order: from `I973-dh610/ks307_r2/base_pin3_D237.7132.npz` (blob 5b10a9fd, ks 307, the #973 polish from the ks 291 state), leg 13's line with `--steps 0 --keep_plan 0 --save_base 1 --ks K` (no `--reseed_base`, no `--elim_switch`): the control ks 307 first, then K = 331 and 347 side by side, 7200 s caps by exact pid, the gate of `run1064d.sh`. Reading (the coordinator's): the largest converging K is the order for a new chain from D 237.7; report the od lines and Delta(K) - Delta(307). Plan comment 7065209051.

Files: `run1064f.sh` (runs `ks307`, `ks331`, `ks347` into `ho_D237.7132/`; summary and `table_1064f.md` via `table1064f.py`), `table1064f.py` (`--selftest` 9 cases including the #973 `ks307_r2.log`, `--break` exits 1), `check_dry1064f.py` (13 planted cases, `--break` exits 1), `dry_1064f.sh`, `start_1064_ho.sh` (unit `i1064n`, memory log `memlog_i1064n.log`), `chain_1064f.sh` (waits for unit `i1064m`, runs the dry tests, starts `i1064n` only when both pass).

The projection-switch run (unit `i1064m`, `sw_D262.0099/`, started 14:54:52 UTC) is still running at the time of this commit; its results come in their own section.
