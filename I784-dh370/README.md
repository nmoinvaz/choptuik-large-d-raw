# I784-dh370: the A/B of newton_od's refusal at iteration 1 on #608's step from D 249.5375

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/784.

Code: main fdfc5dfa (`newton_od(..., abort_theta)`, `anm_run.py --od_abort_theta`; `hp/abort_replay.py` fixed R = 1e8
from #603's and #608's logs: 102 converged attempts with theta at iteration 1 up to 5.8e6, 12 refused at the step limit
from 7.0e9 up), in the worktree choptuik-large-d-784, with the venv of choptuik-large-d-614. Scripts (written by the
coordinator): `run784.sh` and `compare784.py`.

Criteria, fixed before the run (#784): (1) A, #608's flags, reproduces #608's attempts from that base (a 0.4883 not
converged after 20 steps, then a smaller a accepted); (2) B, with `--od_abort_theta 1e8`, refuses a 0.4883 at iteration 1
and accepts the same smaller a; (3) the two accepted states agree in every unknown to 1e-55 at the same D_str; (4) B's
wall time is below A's. `compare784.txt` ends `exit 0` when all hold; its selftest must pass.

## Results (dh370, 2026-11-14)

Runs. `run784.sh` as the user unit `i784` (under `systemd-inhibit`, log `~/scratch784_run.log`), 12 threads at nice 10, 21:12:52 to 22:57:07 UTC.
A (#608's flags) exit 0, wall 3124 s (ended 22:04:56 UTC), B (`--od_abort_theta 1e8` added) exit 0, wall 3131 s (ended 22:57:07 UTC), no Traceback,
`Result=success`. Code: worktree choptuik-large-d-784 at main fdfc5dfa, venv of choptuik-large-d-614, raw origin/main d3658d62.

What A did. From the stored base D 249.5375 the first attempt was a = 1.0000 (a_max 1.996, `--h_max 1.0`; the stored base carries no a, so the step
starts at 1), re-seeded ok (150 s), the octo-double Newton converged in 10 steps (max|F| 7.0e-92), saved at D 250.5375 (Delta
1.684868014971749071143894056145638513902), 1565 s. There was no 0.4883 attempt and no 20-step limit. The simplified-correction ratio at Newton iteration 1
(lam 1) was 2.454e-07 (accepted, bound 0.750), far below R = 1e8, so B's rule did not fire (its log has no "attempt refused at iteration 1" line).

The bars as `compare784.txt` prints them (it ends `exit 1`; `compare784_selftest.txt` ends `exit 0`, "selftest passed"):

| bar | printed | reading |
|---|---|---|
| (1) A: a 20-step attempt not converged, then a state saved | FAILED | not reproduced on this start: the step began at a = 1 and converged |
| (2) B: refused at iteration 1, then a state saved | FAILED | not tested: the ratio 2.454e-07 is below R, nothing to refuse |
| (3) the states at the same D_str (250.53750000000000000555...) agree to 1e-55 | met, max 0.0 | the option leaves a converged step bit-identical |
| (4) B's wall below A's | FAILED, B 3131 s, A 3124 s | not tested: neither refuses, the 7 s (0.2%) is timing noise |

B against A. Their logs agree line for line once the seconds are removed (0 differing lines), the two saved states `A/anm_pin3_D250.5375.npz` and
`B/anm_pin3_D250.5375.npz` are byte-identical (`cmp`), and the exact eight-part sums agree (max difference 0.0). This is one step, with the rule not firing
(numerical evidence); where the option fires (the step forced to a 0.4883) is not tested here, the coordinator runs that A/B (`--a0`) on #608's own build.

Recommended tasks (for the coordinator): the forced-a A/B (the step at a 0.4883 with `--a0`) on dh370's build as well, accepted by the same four bars, so that
bar 3 where the option fires has a second build.
