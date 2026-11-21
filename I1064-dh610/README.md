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
