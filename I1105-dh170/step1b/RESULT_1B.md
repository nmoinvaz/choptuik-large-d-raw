## Result (27 Nov 08:11:55 to 09:31 UTC; units `i1105u030`, `i1105u040`, `i1105u050` and the added `i1105src`; re-solves 2 threads, roots 1 thread, nice 10; `results_1b.md`, `root_*.jsonl`, `root_*.log`, `resolve_*.log`, `l1kc55u0*0.jsonl`, `sol_l1kc55u0*0_D16.0000.npy`, `steps_1b.txt`)
All three re-solves exited 0 within the cap (2301 to 2477 s) with |F| below 1e-8, so all three were rooted. Selftests before each root: `d18_secant.py` exit 0. `read_1105b.py` selftest exit 0 and `--mutate=ref` exit 1. State and record blobs of the re-solves: U30 939aca10 / 46b7ea52, U40 491eb1e4 / 12a42fc8, U50 85c1d8f3 / 91d66dd0.

| run | u0 | \|F\| | steps | Delta | Delta - source | re-solve s | root s | status | final bracket (robust ends, opposite signs) | root (lam_lin) | evals |
|---|---|---|---|---|---|---|---|---|---|---|---|
| source (added control) | 0.04 | 1.7853e-10 (record) | 2565 | 1.0017135137307 | 0 | - | 845 | nonrobust | (2.2440423618, 2.2441319612), width 8.96e-5 | 2.2440424200 | 9 |
| U30 | 0.03 | 2.5624e-10 | 2778 | 1.0017135137230 | -7.7e-12 | 2474 | 1338 | nonrobust | (2.2429536199, 2.2429752386), width 2.16e-5 | 2.2429751796 | 8 |
| U40 | 0.04 | 1.7851e-10 | 2565 | 1.0017134267209 | -8.7e-8 | 2354 | 1311 | tol | (2.2449017139, 2.2449017639), width 5.00e-8 | 2.2449017148 | 9 |
| U50 | 0.05 | 1.8882e-10 | 2400 | 1.0017132545 | -2.6e-7 | 2301 | 1050 | tol | (2.2449095054, 2.2449095973), width 9.18e-8 | 2.2449095063 | 8 |

**Added control (not in t5's order; t5 accepted it at 09:2x UTC):** the source record (94c8b048, 5be40af4) rooted with the same command (`run_src_root.sh`, unit `i1105src`, 845 s). Its final robust bracket is (2.2440423618, 2.2441319612); the run stopped as `nonrobust` because its last interior point (2.2440424205, hybrid sign -) has dln 0.74. P4's re-root of the record, 2.2440428096, lies inside that bracket, 4.5e-7 above its lower end. **So this scanner and P4 agree on the source state, and the re-solve at the record's own u0 moved the root: U40 - source = +8.59e-4 (lam_lin; +7.70e-4 to +8.59e-4 over the source's bracket).** U50 - source = +8.67e-4; U30 - source is -1.178e-3 to -1.067e-3.

**Readings against the bars (written before the run):**
- **T5 = root(U50) - root(U40) = +7.79e-6**: |T5| <= 1e-4, as predicted (estimator values from `lam_lin`, widths 5e-8 and 9e-8).
- **T3 = root(U30) - root(U40): not formed**, because U30's run ended with status `nonrobust` (the written rule needs `tol`). Its final bracket ends are robust with opposite signs, which bounds T3 to **-1.948e-3 to -1.926e-3**: in the |T3| >= 3e-4 band whichever point of the bracket is the root. This bound is outside the written rule.
- **The bars' premise failed.** The bars assumed a solve scatter of about 1e-5. A re-solve at the record's own u0 and kappa moved the root by +8.6e-4 while |F| stayed 1.785e-10 and Delta moved by -8.7e-8 (steps equal), 86 times the assumed scatter and the size of the effect sought (-8.1e-4 at u0 0.02, ELL.md). U40 and U50 agree to 7.8e-6 and both sit +8.6e-4 above the source; U30 sits 1.1e-3 below it, with a Delta equal to the source's to 8e-12. The root is not a function of Delta here. T3 is 2.2 times the one same-u0 shift measured, a sample of one. So the reading attached to the >= 3e-4 band ("the bias is smooth in u0, so u0 0.04 is biased too") is not drawn: the same-u0 re-solve scatter is as large as T3.
- Against t5's hypothesis (T3 about -1.5e-5, T5 about +9e-7): T5 is 8 times its value and inside the bar; T3 is more than 100 times its value, but the scatter above sits between them.

| prediction | result |
|---|---|
| \|F\| <= 1e-8 after each re-solve (U40 90%, U30 90%, U50 85%) | right: 2.56e-10, 1.785e-10, 1.888e-10 |
| root(U40) within 1e-4 of 2.2440428096 (85%) | WRONG: +8.59e-4 |
| T3: \|T3\| <= 1e-4 55%, >= 3e-4 20%, between 25% | not formed under the written rule; the robust bracket puts it at -1.948e-3 to -1.926e-3, the >= 3e-4 band (my 55% bin is wrong) |
| \|T5\| <= 1e-4 (65%) | right: +7.79e-6 |
| re-solve wall 0.5 to 2 h (60%) | right: 2301 to 2477 s (0.64 to 0.69 h) |
| root wall 1 to 3 h per state (50%) | WRONG, shorter: 1050 to 1338 s |

## Status
- 2026-11-27 09:45 UTC: step 1b done. T5 +7.79e-6; T3 not formed by the written rule, bounded to -1.95e-3..-1.93e-3; the control (re-solve at u0 0.04 against the source) moved the root by +8.6e-4, so the solve scatter is the limit. Posted on #1105.
