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

## Files

(filled in as the runs finish)
