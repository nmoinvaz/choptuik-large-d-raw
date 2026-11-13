# I628-macm3: gamma(3.5) at M 160 on lowD_gamma.py's path (the M 160 part of #628)

Machine: macm3 (Apple M3, 24 GB RAM, 6 threads for this run), venv-macm3-314 (Python 3.14.3, numpy 2.5.4, scipy, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main b58895b. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/628 (the coordinator's message of 2026-11-13 01:12 UTC assigned the M 160 part to macm3; M 96 and M 128 are dh370's).

Command (run_628.sh), from the root of the worktree, one run, nice 10, caffeinate -is: python3 -u hp/lowD_gamma.py <raw>/I628-macm3/lowD_gamma_D3.5_M160.jsonl hp/data/lowD_states/lowDmac15_D3.5000_M160.npz --threads=6 --polish=2 --lam0=3.1018757202 --xtol=1e-11. State sha256 3da16d9c68116795... (tracked in main). Started 01:13 UTC.

Written before the run (the issue's). Pass: exactly one sign change in the bracket, and F after the polish recorded in the record. Report lambda and gamma against M 96's 0.32238557898599024 (lambda 3.1018757202022877, 16 determinants, 3355 s) and dh370's M 128; the M 128 to 160 change below 1e-6 would mean gamma(3.5) is resolved to that, otherwise unresolved; Ecker et al.'s 0.32239 against the resulting error. Each determinant at M 160 is about 5 times M 96's; if the first determinant takes more than 30 min its time is posted and the run carries on. Estimate 2 to 4 h.

## Result so far (2026-11-13 01:14 UTC)
The run exited 1 at 01:13:23 UTC, before any determinant: ValueError: newton: the dense n x n path is limited to M <= 128 (memory); at M = 160 use newton_mixed (block storage), from hp/lowD_gamma.py line 81 (newton_solve without mixed=) via hpkernel/driver.py newton_step. Nothing was changed; the coordinator decides (message of 2026-11-13 01:14 UTC, comment on the issue).
