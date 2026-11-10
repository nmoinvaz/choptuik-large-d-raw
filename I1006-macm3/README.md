# I1006-macm3: lambda(48) at D 61.03, kf 27 and kf 25, with --fmax=1e-18 (the looser residual threshold the coordinator wrote before the run)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon). Task 1006 of the project (https://github.com/users/nmoinvaz/projects/1).
Code: the worktree ../choptuik-large-d-i271 at 408b4d6, as #290. Beside I251, I285, I292, I293 and I1001.

Commands (run.sh, caffeinate -is, nice 10, one thread, kf 27 then kf 25): the task body's, as written.

Written before the run (the task body's). Threshold 1e-18, chosen by the coordinator; a lam found this way answers the 1e-5-level question only and is not quoted as a converged value. A solve stopping above
1e-18, or a refusal by the series gate, is reported with |F| and tails and the next cut runs; the threshold is not raised. Acceptance: lam(48) at kf 25 and 27 with |F(48)| and est; the circles' zeros at
kf 25 (2.043535 +0.000004i, estimate 9.5e-7) and kf 27 (2.043502736 -0.000013053i, estimate 1.3e-5) each within its own estimate of the root at that cut, or not; the M 32 lam of each record equals
2.043532530673195 bit for bit. The estimates are the circles' own ranges, not bounds.

## Results


Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/460 (was project item 1006; the coordinator moved it back to an issue at 08:15 UTC).
