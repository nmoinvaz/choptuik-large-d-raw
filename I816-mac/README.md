# I816-mac: Newton from #713's planted truth at D 252.6, and the drop's trial line

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/816.

Code: branch `wip/i816` at ec917706, on main 95039603, in the worktree /Users/nathan/Source/choptuik-large-d-816.
Build: main 3c35f0c's hpkernel (i599/site2, sha256 13b27ce3f9b60464...), the "new" build of #713 and #777's rerun.
Both run at 3 threads and nice 10.

## Plan and criteria (written by 2026-11-15 03:40 UTC, before the run of 03:41:08)

1. **Is the planted truth the octo-double root along Delta?** The command is #777's rerun flags plus `--rel 0
   --it_max 2`, so the start is the truth itself (`plant_start` moves nothing):

       run.sh truth_D252 octo_corrector.py planted RAW I603-win2/chain/anm_pin3_D252.6135.npz --threads 3 --switch 0 \
           --reseed_o 3 --reseed_start pred --qd 0 --full_drop 1e-6 --rel 0 --it_max 2 --out RAW/I816-mac/truth_D252

   `verdict_816.py truth_D252.json` reads the first Newton step's Delta correction dD from the JSON (`od.hist[0]`):
   - **truth**: |dD| < 1e-20, so the truth is the root along Delta.
   - **corrector**: |dD - (-2.018e-11)| <= 1e-12, so the root lies at the corrector's Delta (#713, #777).
   - **neither**: anything else, reported as such.

   Its check: `verdict_816.py --selftest` runs planted dD values (0, 9.9e-21, -3e-20, -2.0184e-11, ±1e-12 around the
   reference, +2.018e-11, 1.1e-5) through the same rule and must pass, and `--mutate=sign` flips the reference's sign
   and must fail. Both were run before the real run: PASS and FAIL. The script's reading of the JSON format was tried
   on #777's `s0_D252.json`, whose first step from the planted start, not the truth, reads -2.018440e-11.

   planted's own exit is reported, not judged. It compares against the truth itself, and 2 steps need not reach 1e-40.

2. **The drop's trial line.** In `newton_od`'s own-test branch, a trial accepted by the drop now prints its line at
   verbose 1 (`octo_corrector.py`). `newton_od_toy.py` requires the line in its first drop case for both tests, and
   `--mutate=noline` (`DROP_MUT["noline"]`) omits it in the own test, so that case must fail.

       cd hp && python3 newton_od_toy.py                    # must PASS, exit 0
       cd hp && python3 newton_od_toy.py --mutate=noline    # must FAIL, exit 1

   Before the fix, the new check failed on 95039603's code: own test, line printed False, FAIL.
