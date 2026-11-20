# I1010-mac-review: logs of the independent review of c2 = -lambda_1 (L2_MODE.md section 9), its symbolic checks and second implementation

Machine: mac (Apple M5). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1010

The review is notes/L2_C2_REVIEW.md on branch review/l2-c2-1010 of choptuik-large-d, made from wip/l2-c2-calc at
bda254b9. Its scripts are solver/inner_pert/l2_c2_review_sym.py and l2_c2_review_num.py. venv-314 (Python 3.14.7,
sympy 1.14.0, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0), one process at nice 10. Each log ends with `time`'s lines and
`exit <code>`.

The branch was rebased onto main on 2026-11-20, which changed its hashes: 5112139e is now 4792f8f5, 9acabdd8 is
617e33d7, 60edcacf is 12c36a13, 13f4508b is 17d7bc73, 09609067 is b8d0513f and bb883710 is 51c00805. The commits
named below are the old ones unless they are de940355, which is on the rebased branch.

The review's own runs. Code at 60edcacf unless a commit is named; the c2 path of l2_c2_review_num.py is the same in
9acabdd8, 60edcacf and 13f4508b (which adds the mutations bg, lin, dlam and ser, off by default). de940355 adds
the guards of PR #1053's review threads and changes no number of the M = 1 run.

| file | command (from solver/inner_pert/) | result |
| --- | --- | --- |
| `sym.log` | `l2_c2_review_sym.py` (de940355) | 25 checks, all passed, exit 0 |
| `sym_mutate_{fibre,lin,bg,k,sign}.log` | `l2_c2_review_sym.py --mutate=NAME` (`sign` rerun at de940355) | 11, 10, 1, 10 and 4 checks fail, exit 1 |
| `sym_mutate_{hand,mu,warp,static}.log` | `l2_c2_review_sym.py --mutate=NAME` (09609067) | 10, 14, 1 and 1 checks fail, exit 1; with these every check fails under some mutation |
| `num_checks.log` | `l2_c2_review_num.py checks` (de940355) | 7 planted checks, PASS, exit 0 |
| `num_selftest_before_fixes.log` | `l2_c2_review_num.py selftest` (51c00805 with the selftest alone added, before its guards) | all 7 tests fail, exit 1: each guard's test fails without the guard |
| `num_selftest.log`, `num_selftest_O.log` | `l2_c2_review_num.py selftest`, and under `python3 -O` (de940355) | 7 tests, PASS, exit 0 |
| `num_checks_mutate_{bg,lin,dlam,ser,fc}.log` | `l2_c2_review_num.py checks --mutate=NAME` (13f4508b) | checks 1-4; 2-4; 5; 6; 7 fail, exit 1 |
| `num_c2_M1.log`, `.json` | `l2_c2_review_num.py c2` (de940355) | M = 1 against l2_c2.py: 16 values compared, max relative difference 1.3e-10, PASS |
| `num_c2_M1_mutate_fc.log` | `l2_c2_review_num.py c2 --mutate=fc` (9acabdd8) | FAIL, exit 1, as required |
| `num_c2_M1_r0.25_same_ray.log`, `.json` | `l2_c2_review_num.py c2 --r1=0.25` (de940355) | the radius alone: slices agree to 2.6e-10; the left-singular-vector c2 moves to -7.94356367; PASS (slices only) |
| `num_c2_M1_r0.2_ray_pi8.log`, `.json` | `l2_c2_review_num.py c2 --delta=0.3927` (de940355) | the ray alone: all 16 values agree to 9.3e-11, the left-singular-vector c2 is -7.95908853; PASS |
| `num_c2_M1_r0.25.log`, `.json` | `l2_c2_review_num.py c2 --r1=0.25 --delta=0.3927` | both changed: slices agree to 2.6e-10; the left-singular-vector c2 is -7.94356367; PASS (slices only) |
| `num_c2_M1_unverified.log` | `l2_c2_review_num.py c2 --forcing=l2c,Gc` (de940355) | 0 values compared, UNVERIFIED, exit 3 |
| `num_c2_M1_own_zero.log`, `.json` | `l2_c2_review_num.py c2 --own-zero --delta=0.9` (de940355) | its own zero (accepted at a step of 3.3e-10, tolerance 1e-9), a third ray; max relative difference 4.4e-9, PASS |
| `num_c2_M3.log`, `.json` | `l2_c2_review_num.py c2 --M=3` (9acabdd8) | M = 3, one-shot 4 x 4 solve: max relative difference 4.7e-8, PASS |
| `num_c2_M5.log`, `.json` | `l2_c2_review_num.py c2 --M=5 --tol=1e-3` (the working tree before 9acabdd8, same c2 path) | M = 5, one-shot 6 x 6 solve, condition 7.6e17: absolute differences up to 1.8e-4, its own linearity residuals 3.2e-5 and 1.2e-4; FAIL on the relative bar (G), exit 1. WATCH in the note |
| `num_diag.log` | `l2_c2_review_num.py diag` (9acabdd8) | the control forcing's two evaluations by radius (finding 25) |

The original's documented commands (L2_MODE.md section 10), rerun as written at bda254b9 for finding 28:

| file | command | result |
| --- | --- | --- |
| `orig_flat.log`, `orig_check.log` | `l2_mode.py --flat`, `l2_mode.py --check` | PASS, PASS |
| `orig_forcing.log`, `orig_forcing_p1.log` | `l2_c2_forcing.py`, `l2_c2_forcing.py --p1` | PASS (390 s), PASS |
| `orig_checks.log` | `l2_c2.py --checks` | exit 1 from the control's check 3, as documented |
| `orig_M1_planted.log` | `l2_c2.py 1 --planted-lam` | 1.7691220084, PASS |
| `orig_M1.log`, `orig_M1_G.log` | `l2_c2.py 1 --forcing=l2,l2_ctrl,l0,sym --lamcheck`, `l2_c2.py 1 --forcing=l2,l0,G,sym --lamcheck` | the values of section 9.5, PASS |
| `orig_summary.log` | `l2_c2_summary.py` | the table of section 9.5, PASS |

Those reruns rewrote two files of solver/inner_pert/data/ in fields that carry no result (finding 28). The changes
were not committed.
