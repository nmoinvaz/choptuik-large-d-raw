# I590-macm3: the root search's resolution at D 55.04 and M 64, five brackets (kf48 33)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (hpkernel cp314 neon of 2026-11-09 02:44). Code: the git worktree ~/Source/choptuik-large-d-b458 at main c845cc99 (hp/gamma_dd.py with --bracket and --xtol, which acts at --Mhi=64 too). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/590 (recommended by macm3 in #458's closing summary; the coordinator's commands: issue comment of 2026-11-12 11:26 UTC).

Runs (common.sh run(), chain1.sh to chain3.sh, one thread per run, three at a time, nice 10, caffeinate -is): python3 -u hp/gamma_dd.py <raw>/gamma_D55_NAME.jsonl hp/data/states/up10_D55.0351.npz --threads=1 --polish=4 --Mhi=64 --kf48=33 --bracket=A,B --xtol=1e-16 (state sha256 945714e9bda3700d...), brackets b1 to b5, the control b1r (must equal b1 bit for bit) and none (no sign change, must exit 1 with lam null). The reference: #470's kf 33 run, lambda(64) 2.0476841266944525, lambda(32) 2.0476841277123925.

Written before the run (the issue's). The spread of lambda(32) and lambda(64) over b1 to b5, with n_det and each run's floor check; controls b1r = b1 bit for bit and none exits 1; the verdict: the spread of lambda(64) against 4.4e-10 (#470's differences between kf 31, 33 and 35): below 4.4e-11, the kf differences are not root noise; above 4.4e-10, they may be.

## Results


(2026-11-12 12:40 UTC, macm3) All seven runs finished (exits.txt), last at 12:39:52 UTC (started 11:50:23 UTC; M 32 108 to 118 s, M 64 988 to 1539 s). Every one exits 1, bracketed or not: the M 64 solve ends with floor check ABOVE (est -1.2075e-15, |est| > 1e-15), the same line and number as #470's kf 33 and kf 35 runs, which exited 1 too, so the exit status cannot separate the runs; none is told apart by lam null (n_signchanges 0). The Newton solve is identical in all (F 3.9995e-24 at the floor, tails 2.0e-34 at most).
| bracket | λ(32) | λ(64) | n_det (M 32) | M 64 floor check (est) | M 64 tails max | Newton steps | exit |
|---|---|---|---|---|---|---|---|
| b1 | 2.047684127712392 | 2.0476841275012796 | 6 | ABOVE (-1.208e-15) | 2.0e-34 | 0 | 1 |
| b2 | 2.047684127712392 | 2.0476841280061455 | 7 | ABOVE (-1.208e-15) | 2.0e-34 | 0 | 1 |
| b3 | 2.0476841277123925 | 2.047684127567935 | 7 | ABOVE (-1.208e-15) | 2.0e-34 | 0 | 1 |
| b4 | 2.047684127712392 | 2.0476841269633494 | 6 | ABOVE (-1.208e-15) | 2.0e-34 | 0 | 1 |
| b5 | 2.047684127712392 | 2.0476841283086755 | 6 | ABOVE (-1.208e-15) | 2.0e-34 | 0 | 1 |
| b1r | 2.047684127712392 | 2.0476841275012796 | 6 | ABOVE (-1.208e-15) | 2.0e-34 | 0 | 1 |
| none | None | None | 2 | - | - | - | 1 |

Spread over b1 to b5: λ(32) 4.441e-16 (min 2.047684127712392, max 2.0476841277123925); λ(64) 1.345e-09 (min 2.0476841269633494, max 2.0476841283086755).
#470 kf 33 (default search): λ(32) 2.0476841277123925, λ(64) 2.0476841266944525; b1 to b5 against it: λ(64) +2.69e-10 to +1.61e-09.
Control b1r vs b1: λ(32) bit for bit equal, λ(64) bit for bit equal. Control none: exit 1, lam None, n_signchanges 0.
mean of λ(64) over b1-b5: 2.047684127669477 ; sorted: [2.0476841269633494, 2.0476841275012796, 2.047684127567935, 2.0476841280061455, 2.0476841283086755]
λ(64) - λ(32) per bracket: ['-2.111e-10', '+2.938e-10', '-1.445e-10', '-7.490e-10', '+5.963e-10']

Verdict (the issue's): the spread of lambda(64) over b1 to b5 is 1.345e-9, above 4.4e-10 (#470's differences between kf 31, 33 and 35), so the kf differences may be root noise; they are not shown to be larger than the root search's resolution. b1r equals b1 in lambda(32) and lambda(64) bit for bit and the M 64 solve is the same state in every run (the same F), so the spread is the root search's, not the solve's. The default search of #470 (lambda(64) 2.0476841266944525) lies 2.7e-10 below the lowest bracketed value.
