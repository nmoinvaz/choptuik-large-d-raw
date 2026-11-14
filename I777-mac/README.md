# I777-mac: newton_od's full-step drop with the default own test, at #752's crawl and #713's checks

Machine: the Apple M5 Mac (`mac`), issue https://github.com/nmoinvaz/choptuik-large-d/issues/777.

Code: main 8e10d127 (`newton_od(..., full_drop)` for the own test, `crawl_probe.py fixrun --full_drop`), in the
worktree /Users/nathan/Source/choptuik-large-d-777. Scripts (written by the coordinator): `run.sh` (one job, old or new
build) and `queue.sh` (the jobs in order, stopping at the first unexpected exit). Builds: "old" is venv-314's hpkernel,
before #523's exact freeze projector, which #742 and #752 ran on; "new" is the i599/site2 build of main 3c35f0c, after
#523, which #713 ran on.

Criteria, fixed before any run (#777, with f = 1e-6 as #752 recommended): the toy passes and its control fails; at
#752's crawling iterate the own test without the option crawls (lam 1/2 at step 1, not converged in 6 steps) and with it
converges to 1e-60 within 6 steps; #713's C2 at D 252.6 at switch 0 with the option: each seed below 1e-40, the seeds'
Delta agree to 1e-30, and both controls still fail; #713's s0_D200 with the option meets planted's bar against s0_D200's
Delta; #713's C3 wall at D 254.4 with the option exits 0, and both its controls fail.
