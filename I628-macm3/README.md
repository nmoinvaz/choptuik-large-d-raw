# I628-macm3: gamma(3.5) at M 160 on lowD_gamma.py's path (the M 160 part of #628)

Machine: macm3 (Apple M3, 24 GB RAM, 6 threads for this run), venv-macm3-314 (Python 3.14.3, numpy 2.5.4, scipy, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main b58895b. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/628 (the coordinator's message of 2026-11-13 01:12 UTC assigned the M 160 part to macm3; M 96 and M 128 are dh370's).

Command (run_628.sh), from the root of the worktree, one run, nice 10, caffeinate -is: python3 -u hp/lowD_gamma.py <raw>/I628-macm3/lowD_gamma_D3.5_M160.jsonl hp/data/lowD_states/lowDmac15_D3.5000_M160.npz --threads=6 --polish=2 --lam0=3.1018757202 --xtol=1e-11. State sha256 3da16d9c68116795... (tracked in main). Started 01:13 UTC.

Written before the run (the issue's). Pass: exactly one sign change in the bracket, and F after the polish recorded in the record. Report lambda and gamma against M 96's 0.32238557898599024 (lambda 3.1018757202022877, 16 determinants, 3355 s) and dh370's M 128; the M 128 to 160 change below 1e-6 would mean gamma(3.5) is resolved to that, otherwise unresolved; Ecker et al.'s 0.32239 against the resulting error. Each determinant at M 160 is about 5 times M 96's; if the first determinant takes more than 30 min its time is posted and the run carries on. Estimate 2 to 4 h.

## Result so far (2026-11-13 01:14 UTC)
The run exited 1 at 01:13:23 UTC, before any determinant: ValueError: newton: the dense n x n path is limited to M <= 128 (memory); at M = 160 use newton_mixed (block storage), from hp/lowD_gamma.py line 81 (newton_solve without mixed=) via hpkernel/driver.py newton_step. Nothing was changed; the coordinator decides (message of 2026-11-13 01:14 UTC, comment on the issue).

## The lowDhm family at M 96 and M 128 (the coordinator's message of 2026-11-13 01:15 UTC: mode_det is dense too, DENSE_M_MAX in hp/src/python.rs, so M 160 is out)
run_628b.sh: python3 -u hp/lowD_gamma.py <raw>/I628-macm3/lowD_gamma_D3.5_hm_MM.jsonl hp/data/lowD_states/lowDhm_D3.5000_MM.npz --threads=3 --polish=2 --lam0=3.1018757202 --xtol=1e-11 for M 96 and 128, two runs at once, 3 threads each, nice 10, caffeinate; states' sha256 6de2033bd059e5bb... (M 96) and 260f26dbe2e41e0e... (M 128). Started 01:16 UTC. Written before the run (the note on the issue). Pass: one sign change each and F after the polish recorded. Report gamma at each M against dh370's lowDvh values at the same M (M 96: 0.32238557898599024, lambda 3.1018757202022877, F 4.388e-30, 16 determinants, 3355 s, in hp/data/lowD_gamma*.jsonl; M 128 from dh370's run); the resolution criterion is gamma(128) - gamma(96) in each family and the family difference at each M, both tabled; gamma(3.5) is resolved to the larger of the two.

## Results of the lowDhm runs (01:42 UTC; exits.txt: hm M96 exit 0 at 01:23:41, hm M128 exit 0 at 01:41:23 UTC)

| family, M | state | λ | γ | F after the polish | determinants | seconds (threads) |
|---|---|---|---|---|---|---|
| lowDhm, 96 | `lowDhm_D3.5000_M96.npz` | 3.101875720205001 | 0.32238557898570824 | 1.356e-30 | 4 | 434 (3, with the M 128 run beside it) |
| lowDhm, 128 | `lowDhm_D3.5000_M128.npz` | 3.1018756839323616 | 0.32238558275561296 | 7.640e-30 | 6 | 1496 (3) |
| lowDvh, 96 (dh370, `hp/data/lowD_gamma_local.jsonl`) | `lowDvh_D3.5000_M96.npz` | 3.1018757202022877 | 0.32238557898599024 | 4.388e-30 | 16 | 3355 (6) |

hm 96->128: gamma +3.770e-09, lambda -3.627e-08
hm - vh at M 96: gamma -2.820e-13, lambda +2.713e-12
Ecker et al. 0.32239 - gamma_hm(128) = +4.417e-06, 0.32239 - gamma_hm(96) = +4.421e-06
Last bracket: M 96 lambda 3.1018757202 (-) to 3.101875720205 (+), M 128 3.101875683932 (-) to 3.101875683937 (+): 5e-12 wide, so gamma is located to about 5e-13 (dgamma = dlambda / lambda^2). dh370's lowDvh M 96 is the stored hp/data value (his rerun, I628-dh370, and his M 128 were running at 01:41 UTC); the family difference at M 128 waits for it.

## dh370's half: the lowDvh family at M 96 (control) and M 128 (the coordinator's message of 2026-11-13 06:02 UTC; dh370 offline)
run_628c.sh: python3 -u hp/lowD_gamma.py <raw>/I628-macm3/lowD_gamma_D3.5_vh_MM.jsonl hp/data/lowD_states/lowDvh_D3.5000_MM.npz --threads=3 --polish=2 --lam0=3.1018757202 --xtol=1e-11, M 96 and 128, two at once, from the worktree ~/Source/choptuik-large-d-b640 at main 9839474 (the lowDhm runs above were at b58895b; hp/lowD_gamma.py and the lowD_states are not among the changes between them). Started 06:02 UTC. Written before the run (the message). Pass: the vh M 96 control reproduces the stored gamma 0.32238557898599024 to the root finder's resolution (the hm M 96 was 2.8e-13 from it: say which); each run has one sign change; report gamma(vh 128) - gamma(vh 96) and gamma(vh 128) - gamma(hm 128) (0.32238558275561296); then close #628 with both families' table and the resolution verdict.

## Results of the lowDvh runs and both families (06:24 UTC; exits.txt: lowD_gamma vh M96 exit 0 at 06:09:59, vh M128 exit 0 at 06:23:33 UTC; table628.py's output below)

| family, M | state | λ | γ | F after the polish | determinants | seconds (threads) |
|---|---|---|---|---|---|---|
| lowDhm, 96 | `lowDhm_D3.5000_M96.npz` | 3.101875720205001 | 0.32238557898570824 | 1.356e-30 | 4 | 434 (3) |
| lowDvh, 96 | `lowDvh_D3.5000_M96.npz` | 3.101875720205001 | 0.32238557898570824 | 4.388e-30 | 4 | 406 (3) |
| lowDhm, 128 | `lowDhm_D3.5000_M128.npz` | 3.1018756839323616 | 0.32238558275561296 | 7.640e-30 | 6 | 1496 (3) |
| lowDvh, 128 | `lowDvh_D3.5000_M128.npz` | 3.101875683932393 | 0.3223855827556097 | 3.373e-30 | 6 | 1221 (3) |
| lowDvh, 96, stored (dh370, lam_guess 3.092124212621165) | `lowDvh_D3.5000_M96.npz` | 3.1018757202022877 | 0.32238557898599024 | 4.388e-30 | 16 | 3355 (6) |

| difference | γ | λ |
|---|---|---|
| γ(hm 128) − γ(hm 96) | +3.770e-09 | -3.627e-08 |
| γ(vh 128) − γ(vh 96) | +3.770e-09 | -3.627e-08 |
| vh 96 − hm 96 | +0.000e+00 | +0.000e+00 |
| vh 128 − hm 128 | -3.275e-15 | +3.153e-14 |
| vh 96 (this run) − stored vh 96 | -2.820e-13 | +2.713e-12 |
| hm 96 − stored vh 96 | -2.820e-13 | +2.713e-12 |

vh 96 and hm 96 identical in λ and γ: True
Ecker et al. 0.32239 − γ(hm 128) = +4.417e-06; − γ(vh 128) = +4.417e-06

The two M 96 results are identical in lambda and gamma because the root finder's output is fixed by its last bracket (lambda 3.1018757202 (-) to 3.101875720205 (+), 5e-12 wide, at both) and not by the root's position inside it; the M 128 brackets are (3.101875683932 (-), 3.101875683937 (+)) in both families. So the families agree to the root finder's resolution (dlambda 5e-12, dgamma 5e-13) and no better.
