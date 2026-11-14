# I784-dh610: the A/B of newton_od's refusal at iteration 1 on #608's step from D 249.5375, the step forced to a 0.48828125

Machine dh610 (Fedora 45, i7-12700; 4 threads beside #608), issue https://github.com/nmoinvaz/choptuik-large-d/issues/784.

Code: main fdfc5dfa (`newton_od(..., abort_theta)`, `anm_run.py --od_abort_theta`; `hp/abort_replay.py` fixed R = 1e8
from #603's and #608's logs: 102 converged attempts with theta at iteration 1 up to 5.8e6, 12 refused at the step limit
from 7.0e9 up), in the worktree choptuik-large-d-784, with #608's own build (the main checkout's .venv, a879ccc3). dh370's A/B (I784-dh370) started its step at a = 1, which converged, so it could not test the refusal; here `--a0 0.48828125` forces #608's crawling attempt. Scripts (written by the
coordinator): `run784b.sh` and `compare784.py`.

Criteria, fixed before the run (#784): (1) A, #608's flags, reproduces #608's attempts from that base (a 0.4883 not
converged after 20 steps, then a smaller a accepted); (2) B, with `--od_abort_theta 1e8`, refuses a 0.4883 at iteration 1
and accepts the same smaller a; (3) the two accepted states agree in every unknown to 1e-55 at the same D_str; (4) B's
wall time is below A's. `compare784.txt` ends `exit 0` when all hold; its selftest must pass.
