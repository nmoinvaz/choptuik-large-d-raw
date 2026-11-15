# I827-mac: Newton's Delta step at s0_D252's truth under 1e-65 perturbations of one block

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/827.

Code: branch `wip/i827` at daf24da5 (`hp/step_spread.py`, on main 78687d7c), worktree
/Users/nathan/Source/choptuik-large-d-827. Build: main 3c35f0c's hpkernel (i599/site2), as #816 and #823. 3 threads,
nice 10.

## Plan and criteria (written by 2026-11-15 07:01 UTC, before the run)

    run.sh spread step_spread.py RAW I603-win2/chain/anm_pin3_D252.6135.npz --threads 3 --rel 1e-65 --seeds 1,2,3,4 \
        --ref 3.3110848587422764e-08 --json RAW/I827-mac/spread.json

The system is proj_shift's (#823): planted's pinned system at the truth, no projection. The plain pinned Newton step
is taken at the unperturbed truth, at the horizon data (m_h, a_h) perturbed by z_i -> z_i (1 + 1e-65 s_i) with
random signs s_i for seeds 1-4, and at each other block alone (centre, nodes 0-4, Delta) by the same size with seed 1.

- **Check:** the unperturbed step's Delta part equals +3.3110848587422764e-08 exactly (I823-mac's dz0_truth).
- **Control (reported beside it):** the centre data alone, perturbed by the same size.
- **Verdict:** "determined" if every horizon seed's Delta step is within 1e-3 relative of the unperturbed one, else
  "not determined", with the spread over seeds. Its rule's self-test passes, and `--mutate=bar` (the bar at 1e3)
  fails. Both were run before the real run: selftest.log, PASS, exit 0; selftest_bar.log, FAIL, exit 1.

Estimate: 12 Newton steps at 2.5–3.5 min each (#823's proj_shift), about 35 min.
