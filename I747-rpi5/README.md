# I747-rpi5: a pre-registered scan for the far Padé poles alone

Machine: rpi5 (Raspberry Pi 5, 4 cores, 8 GB), one process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/747

Code: `solver/inner_amp/pade_far_poles.py` of the repository's branch `wip/i747`. Criteria: notes/PADE_FAR_END.md §18, committed
before any plant was judged (fb21b909), with the script after it (10b90d9b). The planted-truth amendment is 458ba32b,
the post-freeze `robust` stage 0c861b7d, the results and proposed text aee63c5e (all on `wip/i747`).

## Files

| file | what |
|---|---|
| `control.log\|json`, `control_mutate_{shift_poles,tol,noise,len}.*` | selftest R1-R3, J+, J-, P' with its context ladder and the first P as a finding, R4, and the four mutations (each fired, exit 1) |
| `control_first_run_P_fired.*` | the first run, whose planted truth P fired; kept apart, it was replaced by P' |
| `diag/` | the diagnostics after P fired (`diag_P*.py` and their outputs in its README) |
| `plants.jsonl` | every plant record of the scan: 35520 (30720 stage A at wf 1.00, 8 x 200 stage B at three nodes), resumable |
| `scan.log\|json`, `scan.stdout` | stages A to C and the verdict (frozen criteria in scan.json) |
| `report.log\|stdout` | the post-freeze maps (smallest d_P per position, by strength, by phase) |
| `robust.log\|json\|stdout` | the post-freeze noise check and the moves of the passing plants (section 18.5) |

## Result

The scan's frozen answer is **yes**: 202 plants pass (b), admissible with d_P <= 0.03 at wf 0.99, 1.00 and 1.01, rechecked
through `pade_record`. All 202 come from stage B (starts 4 and 7, 136 arc and 66 chord2) and lie in one place: Q ends near
1.50 + 1.08i at wf 1.00, L 0.40-0.47, theta 30-47 deg, eta 0.011-0.054, phi 121-178 deg, offset o = (-0.53, -0.15) (lattice
units (-2.1, -0.6)). The best has D3 = 0.0217. None of the 30720 lattice plants passes (smallest d_P 0.0701), so no position is
located and stage C was empty. Seen at eta >= 0.3, where P' is calibrated, the smallest D3 is 0.0312 (eta 0.96) and none passes.

The tolerance is below the noise there (post-freeze, notes 18.5): noise at the real series' measured per-order errors moves the
passing plants' poles 0.036-0.061 at the median, and 0 of 16 draws keep all three nodes within 0.03 of the plant's own poles.
The passes are fits to the real series' noise draw. The end point's pass is about 0.01-0.02 wide.

## Discrepancies

- The first planted truth P (three point masses at #541's places) fired, d_P 0.109-0.216 at every strength: the Pade poles
  need not mark singularities at their own places (resolution). Replaced by P', a gate; P kept as a finding (notes 18.3).
- The `prec` selftest mutation first ran at 30 digits and did not fire; it runs at 12 digits (before any plant was judged).
- The strengths were extended from eta 1 to 10 after P (the grid from 26624 to 30720 plants).
- P' passes at eta = 1 and 10 and fails at eta = 0.01 and 0.1 (the tolerance is below the noise floor there), and the passes
  lie at eta 0.011-0.054. The "yes" is the frozen verdict, and does not say that the real series has such a set.
- `check_numbers.py --selftest` cannot run on the rpi5 (no `hpkernel`): the coordinator runs it on merge.

## Recommended tasks (full text)

1. **A joint judge of the passers.** What: judge (a) and (c') on the 202 passing plants of `plants.jsonl` and on the plants of
   the cluster's neighbourhood, with #703's and #718's frozen rules at the three nodes. Why: (b) is met at eta 0.011-0.054,
   inside #718's (c') window, and only a joint pass says the real series' structure is reproduced. Acceptance: each passer
   judged by the frozen rule, a planted truth and its mutation first. Depends on #747.
2. **A (b) whose tolerance includes the noise.** What: replace 0.03 by a distance set from the plant's own noise scatter (the
   copy-to-copy d_P at that plant, 0.036-0.061 here), and rescore the scan's plants and P'. Why: at eta <= 0.1 P''s truth fails
   0.03. Acceptance: P' at eta = 0.01, 0.1, 1 and 10 passes the true plant and fails its four neighbours, and its mutations fire.
   Depends on #747.
3. **A stage 2 around the passing region.** What: a fine grid in (Re o, Im o) near (-0.53, -0.15) and the four lattice
   neighbours' diagonals, with eta, phi, L and theta refitted at each, at the three nodes. Why: the pass is 0.01-0.02 wide,
   narrower than the lattice 0.25. Acceptance: #718's located rule on the fine grid, or the width stated. Depends on #747.
4. **Restarts at eta >= 0.3.** What: Nelder-Mead from many starts at eta 0.3-10 (starts 0, 1, 3 ended at D3 0.065, 0.065,
   0.0312), with 1000 evaluations. Why: where P' is calibrated nothing passes yet, and 0.0312 is 4% above the tolerance.
   Acceptance: a pass, or the smallest D3 after N restarts with N stated. Depends on #747.
5. **The refinement on a planted truth.** What: take the best passer as truth, make noise copies (10 draws) at the real
   errors, run stage B from the lattice's best starts on each copy against its own reference. Why: P' tests the judge at one
   lattice point, not the refinement that found the passes. Acceptance: the refinement ends within 0.03 of the true offset
   in a stated share of the draws, and `--mutate=shift_poles` fires. Depends on #747.
