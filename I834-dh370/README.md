# I834-dh370: the pilot, re-planned polishes at D 259.4928 and 259.7436 with --od_full_drop 1e-2

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/834.

`run834p.sh` (written by the coordinator, md5 0945010b, run unedited by absolute path under user unit `i834p`): two of #603's
chain_nsr states, D 259.4928 and 259.7436, polished at their own D on a new plan (`--steps 0 --keep_plan 0`), #603's held values
(`data/held_fit.json`) and flags, plus `--od_full_drop 1e-2`, 6 threads each at nice 10; worktree choptuik-large-d-808b at main
bd4ada6c, venv-i800. Bar: both reach max|F| <= 1e-60; stop a polish past 3 h.

## Results (dh370, 2026-11-15)

Unit `i834p`, 11:36:10 to 12:30:17 UTC, both jobs exit 0 (`exits_834.txt`, `i834p_journal.log`); neither converged and neither saved a base.

| polish | start max\|F\| | first correction \|dz\| | trials at step 0, lam 1 to 1/256, max\|F\| | steps | final max\|F\| | first dDelta | Delta - Delta(#603) |
|---|---|---|---|---|---|---|---|
| s259.4928 | 5.5e-36 | 1.670e-03 | 2.75e68 to 2.96e46, all 9 refused | 1, no trial accepted | 5.5e-36, the start's | none | none |
| s259.7436 | 5.3e-36 | 7.123e-04 | 8.53e62 to 7.49e42, all 9 refused | 1, no trial accepted | 5.3e-36, the start's | none | none |

Each trial took 290 to 360 s. The raw simplified correction |dz_t| was never below |dz| (1.7e65 and 6.8e59 at lam 1, 3.3e44 and 5.6e39 at lam 1/256),
so the drop rule had no trial to accept: at 5e-36 nothing falls to 1e-2 of the start except a result below 5e-38. The trials' max|F| fell about 200 times
per halving of lam (s259.4928: 1.6e51, 6.4e48, 3.0e46 at lam 1/64, 1/128, 1/256).
