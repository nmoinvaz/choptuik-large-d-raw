# I1010-mac-review: logs of the independent review of c2 = -lambda_1 (L2_MODE.md section 9), its symbolic checks and second implementation

Machine: mac (Apple M5). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1010

The review is notes/L2_C2_REVIEW.md on branch review/l2-c2-1010 of choptuik-large-d, made from wip/l2-c2-calc at
bda254b9. Its scripts are solver/inner_pert/l2_c2_review_sym.py and l2_c2_review_num.py. venv-314 (Python 3.14.7,
sympy 1.14.0, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0), one process at nice 10. Each log ends with `time`'s lines and
`exit <code>`.

The review's own runs. Code at 60edcacf unless a commit is named; the c2 path of l2_c2_review_num.py is the same in
9acabdd8, 60edcacf and 13f4508b (which adds the mutations bg, lin, dlam and ser, off by default).

| file | command (from solver/inner_pert/) | result |
| --- | --- | --- |
| `sym.log` | `l2_c2_review_sym.py` (09609067) | 25 checks, all passed, exit 0 |
| `sym_mutate_{fibre,lin,bg,k,sign}.log` | `l2_c2_review_sym.py --mutate=NAME` | 11, 10, 1, 10 and 4 checks fail, exit 1 |
| `sym_mutate_{hand,mu,warp,static}.log` | `l2_c2_review_sym.py --mutate=NAME` (09609067) | 10, 14, 1 and 1 checks fail, exit 1; with these every check fails under some mutation |
| `num_checks.log` | `l2_c2_review_num.py checks` (13f4508b) | 7 planted checks, PASS, exit 0 |
| `num_checks_mutate_{bg,lin,dlam,ser,fc}.log` | `l2_c2_review_num.py checks --mutate=NAME` (13f4508b) | checks 1-4; 2-4; 5; 6; 7 fail, exit 1 |
| `num_c2_M1.log`, `.json` | `l2_c2_review_num.py c2` (9acabdd8) | M = 1 against l2_c2.py: max relative difference 1.3e-10, PASS |
| `num_c2_M1_mutate_fc.log` | `l2_c2_review_num.py c2 --mutate=fc` (9acabdd8) | FAIL, exit 1, as required |
| `num_c2_M1_r0.25.log`, `.json` | `l2_c2_review_num.py c2 --r1=0.25 --delta=0.3927` | slices agree to 2.6e-10; the left-singular-vector value moves to -7.94356; PASS (slices only) |
| `num_c2_M1_own_zero.log`, `.json` | `l2_c2_review_num.py c2 --own-zero --delta=0.9` | its own zero, a third ray; PASS |
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
