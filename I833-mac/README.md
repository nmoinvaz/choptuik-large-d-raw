# I833-mac: D* on #795's new-plan series against the kept plan, by #829's two approximant families

Machine: the Apple M5 Mac (xfkappa). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/833.
Code: `hp/fold_plan.py` (with `hp/fold_mirror.py`) on wip/xf-833 6ff8f6e2, off main 75f94140.

**Input.** The raw clone at cad6d1a4:
- new plan: `I795-dh370/newplan/jet_pin3_D259.2582.npz` and `D259.4928.npz`;
- kept plan: `I603-win2/chain_nsr/jet_pin3_D*.npz` at the same bases. #776's reproduction equals them (bit for bit at
  259.2582, to 1.6e-44 at 259.4928);
- states: `I603-win2/chain_nsr/anm_pin3_D*.npz`. They satisfy the new plan's equations to 4.7e-36 and 5.5e-36 (#795's
  logs, "base polish not adopted").

## Result
- **The new plan's series miss their own states.** Its 259.2582 series, summed at 259.4928 (25 terms), misses that
  state's Delta by 3.2e-5, with a last term of 1.3e-15. The kept plan's meets it to 1.0e-15. The single-base + sheets at
  the other base miss by 1.7e-5 and 3.2e-5 on the new plan, and by at most 1.9e-17 on the kept plan. Bound: 1e-8.
- **The plant.** #829's plant, noise 1e-30, gives D* errors of 3.7e-7 (P), 7.2e-6 (Sa) and 1.0e-5 (Sb). A planted
  0.010 move reads "moves" and a doubled contamination reads "does not move" in all three, so the main configuration
  is P.
- **Real, P (main).**
  - Kept plan: D* 259.90330382874 (M2) and 259.9033038229 (M1), within 8.8e-11 and 5.9e-9 of #829's.
  - New plan: M1 259.90388 (mu 1.48, a1 -0.20) and M2 259.91343, which disagree.
  - The difference is +5.35e-3 against a combined error of 9.5e-3, so the rule reads "does not move". That rests on
    one form fitted to two series that are not one function.
- **Real, single bases.**
  - Sa: the new plan is +0.01020 (259.91350, mu 0.50005) against a combined error of 1.4e-5, so it reads "moves".
  - Sb: +0.01131 (259.91460, mu 0.504) against 1.0e-4, so it reads "moves".
  - The two new-plan bases disagree with each other by 1.1e-3.
- **The rerun is byte-identical.**
- **check_numbers.py --selftest:** 2091 of 2091, and its selftest 2091 of 2091.

## Files
- `planted.log`, `planted.json`: the plant and its two controls at P, Sa and Sb.
- `real.log`, `real.json`, `rerun_*`, `rerun.log`: the real run and its byte-identical rerun.
- `check.log`: `check_numbers.py --selftest`.

## Recommended task: new-plan series that meet their own states
- **What:** re-plan (`anm_run.py --keep_plan 0`, as #795) at bases within 0.1 of D*: 259.8068, 259.8139, 259.8184,
  259.8228, 259.8283, 259.8318, 259.8352, each with its partner about 0.05 below (#829's pairs: 259.7603, 259.7719,
  259.7792, 259.7864). That is 11 series, or 8 for the registered minimum of 4 bases. First,
  check the new-plan series of two adjacent bases against each other's states, as here. Then run
  `fold_mirror.py`'s configuration on them.
- **Why:** #795's two new-plan series are not series of one function: each misses the other's state by 1.7e-5 to
  3.2e-5, while both states solve the new plan to 5e-36. So their D* shift of +0.010 cannot be read as a moved fold.
  The likely route, not tested, is the new plan's Jacobian, with its 4 weak directions (#795's logs).
- **Acceptance (can fail):**
  - the adjacent-base sums meet the states to 1e-8;
  - then the D* difference against #829's 259.90330382883 is judged by #833's rule, with #833's two controls.
- **Cost:** about 50 min per series on dh370 (#795's walls).
- **Depends on:** #833.
