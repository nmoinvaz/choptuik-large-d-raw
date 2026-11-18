# I955-mac-review: xfchecks's independent review of PR #955 (the series' order-k sums in rounds), its test runs

Machine: mac (Apple M5), agent xfchecks. PR: https://github.com/nmoinvaz/choptuik-large-d/pull/955 at ed081a8d
(multidouble from perf/field-par-at-sums at de7da525). Asked by the coordinator on 2026-11-18. The review itself is the
PR's review comment; this folder holds its runs.

Built and run in a fresh worktree of the PR head: `cargo test --profile release-dev --lib`, CARGO_BUILD_JOBS=3, nice
10, through the Mac's shared cargo lock.

| log | what | result |
| --- | --- | --- |
| `test1.log` | `oseries_by_order` tests at the PR head | both pass: control 9600 rows (JET_MUT_AT_KEEP); 0 rows on one thread and on four, 0 of 43064 words between the pools, control 3200 rows (JET_MUT_AT_ROUND) |
| `test2.log` | with `reviewer_mutations.diff` applied, env-gated: unset; REV955=h, (p p)_k formed in the horizon's first round, before p_k's solve; REV955=c, (c p)_k and (c m)_k in the centre's first round, before c_k; then `split_tests` unset | unset passes (as test1); h fails, 4224 rows on both pools; c passes, 0 rows; split_series_accuracy passes |
| `test3.log` | REV955=c2, (a q^2)_k in the centre's first round, before q^2_k | fails, 4224 rows on both pools |

REV955=c changes no bit because those sums read c_k only through c_k p_0 and c_k m_0, and p_0 = m_0 = 0 in the centre
series. The mutations were applied only in the review's scratch worktree, which was reverted to ed081a8d afterwards.

## The fixes (2026-11-18, the coordinator's word)

Findings 1, 3, 4 and 5 applied on perf/series-par-at in 900649b3 (hp: JET_MUT_AT_ROUND_C = 27, the one-thread pool,
the series_split comment) and 6d7b2927 (jet_by_order_check.py: the centre's control, --compare's control, N guard and
saved thread count); 2 not taken. `fix_test.log`, release-dev at 6d7b2927: oseries_by_order_bitwise passes (control
9600 rows), oseries_by_order_threads_bitwise passes (0 rows on one thread and on four, 0 of 43064 words between the
pools; controls: the horizon's round 3200 rows, the centre's 4224), split_series_accuracy passes. The script was
checked by py_compile only.
