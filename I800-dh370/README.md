# I800-dh370: track A stage 1, the homotopy in the horizon series' tail at D 245.1366

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/800
(notes/FACTORED_HORIZON.md 4.7).

Code: branch wip/i800 153aaf12 (`--ks_w_from`: orders 131..ks weighted by `--ks_w`; its Rust test
`ksw_tail_ends_and_middle` checks w = 0 bit for bit, w = 1/2 at the midpoint to 1e-32 and a control), in the worktree
choptuik-large-d-800 with its own venv and release build (venv-i800). Scripts (written by the coordinator): `run800.sh`
(the climb t0, w = 1/64 ... 1, then near_null.py's sigma at w = 0, 1/2 and 1) and `table800.py` (its selftest must pass).

Criteria, fixed before the run (4.7): (1) t0 (orders 131..250 weighted 0, re-planned) equals #696's r130k base in Delta
to 1e-40; (2) each rung converges, or the first that does not is reported with its projection lines; (3) at w = 1,
Delta - Delta(t0) against #796's single-order climb and the model's T_omit / sigma_inf (2.7e-12, a conjecture good to a
factor 100); (4) sigma_3 from w = 0 to 1: the reading of 4.3 holds if ln sigma_3 rises by the model's -ln f at ks 130,
about 50.7, within 30%, and fails if sigma_3 changes by less than a factor 2.

## Results (dh370, stopped 2026-11-15 01:57:32 UTC by the coordinator's order)

What ran. The release build of hpkernel at 153aaf12 (33 min, exit 0, `build800.log`) in `venv-i800`, made with
`python -m venv` because `uv` is not installed on this machine (the Python is the same uv-managed 3.14.10 as the other
venv, `requirements.txt` pinned). `set_ks_w_from` is present and `table800.py --selftest` exits 0. Then unit `i800`
(`run800.sh`, 12 threads at nice 10) from 2026-11-14 23:32:39 UTC to 2026-11-15 01:57:32 UTC, when
`systemctl --user stop i800` ended it (`i800_journal.log`, 2 h 24 min wall, no Traceback, no non-zero exit).

Exits (`exits_800.txt`). t0 exit 0, converged: yes, 23:32:40 to 01:04:37 UTC (92 min), 15 octo-double steps, max|F|
4.3e-93, Delta 1.68576124519581128. t015625 (w = 1/64) started 01:04:37 UTC and never exited. No sigma run and no
`table800.txt` (run800.sh never reached them), so `table800_stopped.txt` is `table800.py` run once on the stopped
folder (exit 0).

| criterion | verdict |
|---|---|
| (1) t0 equals #696's r130k base in Delta to 1e-40 | NOT MET, Delta(t0) - Delta(r130k) = 4.7e-13 |
| (2) each rung converges | the first rung, w = 1/64, did not converge in 53 min; all 8 trials refused, then stopped |
| (3) Delta - Delta(t0) at w = 1 | not reached |
| (4) sigma_3 from w = 0 to 1 | not measured |

t0's polish. The re-plan (`--keep_plan 0`, ks 250 with orders 131..250 weighted 0) leaves the r130k base at max|F|
6.05e-36 with pivots from 1.1e-26 (4 weak directions); its first chord was refused (projection failed, point max|F|
1.05e+14) and the polish went on by trial steps (lam 0.5 at step 0), |dz| 4.70e-13, 2.17e-13, 1.09e-13, 6.12e-14,
1.15e-14, 7.18e-16, 1.50e-18, 1.28e-23, 4.72e-34, 1.25e-43, ... to 1e-86, 105 to 534 s per step (1628 s for step 0).

The rung w = 1/64 (`t015625.log`, from t0's base, which keeps its stored plan, 23 steps). Its start is max|F| 9.42e+44
with a first chord |dw| 3.878e+44, and the projection ladder fails every time (8 rungs, last u 0.3). Step 0's trials,
each 318 s and each refused:

| lam | max\|F\| at the trial | simplified correction / \|dz\| | bound |
|---|---|---|---|
| 1 | 9.42e+44 | 4.589e+68 | 0.750 |
| 0.5 | 2.70e+42 | 1.782e+66 | 0.875 |
| 0.25 | 1.06e+40 | 6.943e+63 | 0.938 |
| 0.125 | 4.14e+37 | 2.695e+61 | 0.969 |
| 0.0625 | 1.62e+35 | 1.028e+59 | 0.984 |
| 0.03125 | 6.29e+32 | 3.635e+56 | 0.992 |
| 0.015625 | 2.43e+30 | 8.226e+53 | 0.996 |
| 0.0078125 | 9.05e+27 | 6.121e+51 | 0.998 |

max|F| falls by about 2^8 per halving of lam. The next trial (lam 1/256) was about 3 min old when the unit was stopped.

Findings, from the coordinator's analysis of these logs (not re-derived here).

1. Criterion 1 failed because of the design, not the run. `--ks 250` makes `anm_run` plan the base again (a stored plan
   does not carry a changed `--ks`), so t0 solved ks 130's equations on another plan, and Delta(t0) - Delta(r130k) =
   4.7e-13 measures that plan change at D 245.14. That is 20 times r130k's own re-plan effect (2.4e-14) and as large as
   order 131's term (3.8e-13).
2. The rung w = 1/64 started at max|F| 9.4e44: orders 131 to 250 at the last node sum to about 6e46 (6e46 / 64 =
   9.4e44), so the horizon series diverges there, and no weight on the whole tail to 250 can be climbed.

The control fired, so the climb stops until the cause is known (AGENTS.md).
