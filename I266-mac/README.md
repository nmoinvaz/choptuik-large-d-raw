# I266-mac: gamma_dd's D 50 M 48 self-convergence gap, the two M 48 solutions, the weak direction between them, their quad-double polish, and lambda's convergence in M

Machine: mac (Apple M5, 10 cores, shared with other sessions; at most 2 processes, nice 10, caffeinate).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/266 (from #254's discrepancy 2).
Code: `hp/gamma_m48_gap.py` (`solve`, `analyze`, `qd`) on the branch wip/i266 of the main repository. The runners are
`scripts/run_solve.sh` and `scripts/run_cmd.sh`, run from the worktree root; every exit is in `logs/exits.txt`.

## The question

At D 50.0075 (`hp/data/states/up8_D50.0075.npz`, M 32, nodes 0.3-0.7, kt 36, kc 420, ks 100, kfreeze 13) two M 48
solutions of one layout disagree. `gamma_dd.py --M48` (f64 resample, Newton to max(10 |F_32|, 1e-27), then LM) gives
Delta(48) - Delta(32) = +1.2e-11 and lam(48) - lam(32) = +6.7e-13. Review R2 (`rv2_resolve.py --M 48 --corrector dnp`,
resample at 40 digits, deflated Newton then Newton to 1e-40) gives +3.1e-20 in Delta. Both have |F| near 1e-24.

## Steps

1. `solve --path=gamma` and `solve --path=r2` reproduce the two M 48 states (G and R) from the same M 32 state.
2. `analyze G R` evaluates both on one solver (R's segment plan), with |F| in double-double and quad-double, the
   linearised Delta correction, the Newton step, both series' tails, lam, and the projection of G - R on the 24 weakest
   right singular directions of the M 48 Jacobian at R (kf 13). Its control is `--mutate=plant` (a planted 1e-12 along
   the third weakest direction and 1e-20 along a strong one must come back), which must pass, and
   `--mutate=plant_strong` (the amplitudes swapped), which must fail.
3. `qd` polishes G, R and the M 32 state by the quad-double Newton, and lam is located on the results.

## Pass and fail criteria of step 3 (written before step 3 ran)

(a) **The reference.** G and R are each polished by the quad-double Newton on one system (M 48, kfreeze 13, R's
segment plan). It passes when both converge to max |F|_qd <= 1e-40 and their Delta agree to 1e-30. Otherwise there is no
reference, and which dd solution is converged is reported as undecided. Its control is the same polish with Ctx::mutate
9 (QD_MUT_STATE_DD, the state read in its double-double part only), which must not converge (exit 1).

(b) **Which M 48 solution is converged.** A double-double M 48 state is converged when |Delta_dd - Delta_qd| <= 1e-17
(R2's linearised corrections at D 50 and 60 are 1e-19 to 1e-17), and not converged when |Delta_dd - Delta_qd| > 1e-14.
In between it is reported as marginal.

(c) **lam's convergence in M at D 50.** The M 32 state is polished in quad-double the same way (M 32, kfreeze 13, its
own plan), and lam is located by gamma_dd.py's find_lam (brentq, xtol 1e-14) on the double-double rounding of both
quad-double solutions. The README's "about 10^-12 for D = 16-58" is consistent with D 50 when |lam(48) - lam(32)| <=
1e-12, and contradicted at D 50 when it is larger. A difference below 2e-14 is reported as below the root's tolerance,
not as a measured value. The same holds for Delta(48) - Delta(32), which is reported from the quad-double solutions.

(d) **Other D** (if time allows): the same at D 58.006 (`up12_D58.0060.npz`, the top of the quoted range), with the
same criteria.

(e) **M 64** (if cheap): the M 48 quad-double solution resampled at 40 digits to M 64 and solved in double-double with
R2's corrector to 1e-40, on the plain layout if the M 64 start's tails are both <= 1e-15, else on #141's fitted layout
(a node at 0.15). It passes when its linearised Delta correction is <= 1e-17 and |lam(64) - lam(48)| <= 1e-12.

## Results

All numbers are printed by `python3 scripts/tabulate.py` (run in this folder) into `table.txt`, from the records listed
under Files.

**Step 1.** Both M 48 states were reproduced from `up8_D50.0075.npz`. The R2 path gives Delta(48) - Delta(32) = +9.3e-20
at |F| 5.4e-25, and the gamma path +1.198e-11 at |F| 2.2e-24. I254's gamma-path state
(`I254-mac/states/up8_D50.0075_M48_kf13.npz`, M 32 polished first as gamma_batch does) gives +1.200e-11. In the gamma
path, Newton stops at max(10 |F_32|, 1e-27) = 4.2e-24 (9.7e-24 unpolished), above the residual it reaches.

**Step 2.** On one solver (M 48, kf 13), the gamma state's linearised Delta correction is -1.200e-11. Its exact Newton
step equals -(G - R) to cosine 1 - 1e-13 and length ratio 1.00000004. The R2 state's correction is -2.4e-19.
|G - R| is 8.2e-5, and 1 - 3.9e-7 of it lies in the six weakest right singular directions of the unscaled Jacobian.
Those come as pairs, the two quadratures of one tau-harmonic of p1 (98% of each vector's norm):

| pair | p1 harmonic | sigma | Delta component | share of Delta(G) - Delta(R) |
|---|---|---|---|---|
| 0, 1 | 13 (the top one the cut leaves free) | 4.97e-21 | 3.2e-8, 5e-11 | -1.5e-12 |
| 2, 3 | 11 | 2.71e-19 | 5.2e-7, 7.1e-8 | +1.07e-11 |
| 4, 5 | 9 | 2.55e-17 | 1.7e-7, 8.1e-6 | +2.7e-12 |

In norm, G - R is 93% harmonic 13 and 7% harmonic 11. p1's pinned harmonics (k > 13) hold 6e-22 of it, the
double-double zero, and Delta holds 1.2e-11 against |G - R| = 8.2e-5. The sigmas are Rayleigh-Ritz values on the
subspace of inverse subspace iteration (12 sweeps, 24 vectors; the first 17 converged, `analyze.jsonl`). lam on the two
states differs by +6.93e-13, the whole of gamma_compare's "M48 dlam 6.7e-13".

**Step 3.**
- (a) passes. The quad-double polishes of G (5 steps, |F| 8.3e-49) and R (2 steps, 1.8e-46) end at the same state,
  with a largest entry difference of 1.2e-36. The control (Ctx::mutate 9) stays at |F| 2.1e-25 after 3 steps and exits
  1.
- (b) The R2 state is converged (Delta 9.3e-20 from the quad-double solution) and the gamma state is not (1.2e-11).
- (c) At D 50 the quad-double solutions give Delta(48) - Delta(32) = -2.4e-24 and lam(48) - lam(32) = -1.6e-15. The
  latter is below the M 48 root's resolution there, about 1e-14. Under noise of 1e-30 (relative) on the state the root
  moves by -1.0e-14 to +3.8e-15, and on the state itself the interpolated and refined roots differ by 4.4e-15. The
  resolutions quoted here are spreads over noise draws, not bounds. lam on R2's double-double state is 7.8e-15 above
  its quad-double polish's. |lam(48) - lam(32)| <= 1e-12, so it is consistent with "about 10^-12".
- (d) At D 58.006: Delta(48) - Delta(32) = -3.9e-24 and lam(48) - lam(32) = +8.9e-14 (quad-double solutions). That
  is below the M 48 root's resolution there. Under noise of 1e-32 (relative, the double-double rounding) the M 48
  sign change sits at +1.5e-13 and -1.2e-13 from the refined root in two draws, and leaves +-2e-13 in the third. On
  the M 48 solution itself det M has no sign change within +-2e-13 of the refined root, and its sign pattern flips
  between draws. find_lam's coarse root and the refined one differ by 1.1e-13. So the M 48 root is resolved to about
  5e-13 at D 58. The M 32 root, where the gamma points come from, moves by up to 6.7e-14 under the same noise
  (2-5e-12 under 1e-30). lam on the double-double states is 1.2e-14 (M 48) and 1.4e-14 (M 32) from their quad-double
  polishes. |lam(48) - lam(32)| <= 5e-13 <= 1e-12, so it is consistent with "about 10^-12".
- (e) M 64 was not run. At D 50 the quad-double M 32 and M 48 solutions already agree to 2.4e-24 in Delta, and lam is
  resolved only to about 1e-14 there, so an M 64 lam could not show more.

**Verdict.** Measured as the change from M 32 to 48 and the root's resolution, the README's "about 10^-12 for D =
16-58" holds. The change is below the root's resolution at D 50 (1.6e-15 against about 1e-14) and at D 58 (8.9e-14
against about 5e-13). The D 20, 30 and 40 records of `hp/data/local/gamma_dd.jsonl` give 0, 4.4e-16 and -8.9e-16, at
find_lam's xtol of 1e-14. The one entry that seemed to support the statement, D 50's "M48 dlam 6.7e-13" in
`hp/data/local/gamma_compare.txt`, measures gamma_dd.py --M48 stopping early and not convergence in M. The kfreeze cut
and the node layout are not measured here.

## Files

- `states/solve.jsonl`, `states/*_M48_gamma.npz`, `states/*_M48_r2.npz`: step 1's records and states.
- `analyze.jsonl`: step 2 (A = gamma path, I254's state and this run's; B = R2 path). `states/weak_dirs_D50_M48_at_r2.npz`
  holds the 8 weakest directions, all 24 sigmas, G - R and both Newton steps.
- `controls.jsonl`: the projection's control (plant passes, exit 0; plant_strong fails, exit 1). `controls_firstrun.jsonl`
  and `logs/*_firstrun.log` are the same runs before the log message printed the planted amplitudes. The logic was
  unchanged and the verdicts were the same.
- `states/qd.jsonl`, `states/*_qd.npz` (four parts): the quad-double polishes, and the control `*_qd_mut9.npz`.
- `lam.jsonl`: lam on each state. `lamres.jsonl`: the root's jitter under noise on the state.
- `logs/`: one log per step. `logs/exits.txt` holds every exit. The two `lam_D50` exits 1 are the first lam runs, which
  stopped at scipy's brentq rtol floor before lam_fine moved to a double-double lam. Their logs were overwritten by the
  reruns.
- `scripts/`: the runners and `tabulate.py`.
