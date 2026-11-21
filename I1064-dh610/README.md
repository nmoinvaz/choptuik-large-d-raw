# I1064-dh610: base polishes from the chain's front, leg 13's D 261.0721 state of ks_chain3b, at ks 293 (control), 315, 316, 317 and 318

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
