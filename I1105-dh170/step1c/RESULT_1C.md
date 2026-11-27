## Result (27 Nov 09:35:24 to 10:19:14 UTC; units `i1105u040b`, `i1105u040c`; re-solves 2 threads, roots 1 thread, nice 10; `results_1c.md`, `root_u040b.jsonl`, `root_u040c.jsonl`, `resolve_*.log`, `l1kc55u040[bc].jsonl`, `sol_l1kc55u040[bc]_D16.0000.npy`, `steps_1c.txt`)
Both re-solves exited 0 within the cap with |F| below 1e-8, so both were rooted; both roots ended with status `tol`, both bracket ends robust with opposite signs. State and record blobs: U40b 78af2111 / 15d999a9, U40c 898360c0 / 4a9c9182. `read_1105c.py` selftest exit 0 and `--mutate=ref` exit 1. The `d18_secant.py` selftest exit 0 before each root.

| run | start | \|F\| | steps | Delta | Delta - U40 | Delta - source | re-solve s | root s | final bracket | root (lam_lin) | root - r40 | evals |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| U40b | U30 (939aca10) | 1.7854e-10 | 2565 | 1.0017134698359 | +4.31e-8 | -4.39e-8 | 1535 | 1080 | (2.2447948479, 2.2447948979), width 5.0e-8 | 2.2447948485 | **-1.069e-4** | 9 |
| U40c | U50 (85c1d8f3) | 1.7841e-10 | 2565 | 1.0017132114199 | -2.15e-7 | -3.02e-7 | 1546 | 1081 | (2.2449630615, 2.2449631115), width 5.0e-8 | 2.2449631108 | **+6.14e-5** | 9 |
| U40 (step 1b) | source | 1.7851e-10 | 2565 | 1.0017134267209 | 0 | -8.70e-8 | 2354 | 1311 | (2.2449017139, 2.2449017639), width 5.0e-8 | 2.2449017148 | 0 | 9 |
| source (step 1b control) | - | 1.7853e-10 | 2565 | 1.0017135137307 | +8.70e-8 | 0 | - | 845 | (2.2440423618, 2.2441319612), width 9.0e-5, status nonrobust | 2.2440424200 | -8.59e-4 | 9 |

**Against the bars (written before the run):** U40b is -1.069e-4 from r40 and U40c +6.14e-5, so not both within 1e-4 (U40b misses by 6.9e-6), and neither is beyond 5e-4: **mixed**, as the bar reads.

**What the four numbers say (arithmetic on the table, estimator values from `lam_lin`, widths 5e-8):**
- The three re-solves of the u0 0.04 system (U40, U40b, U40c) have roots 2.2449017, 2.2447948 and 2.2449631: range **1.68e-4**, sample standard deviation 8.5e-5 (n = 3). That is 17 times the 1e-5 that step 1b's bars assumed, and below the 5e-4 line.
- The source record's root (2.2440424, step 1b control) lies 7.5e-4 (U40b), 8.6e-4 (U40) and 9.2e-4 (U40c) below them, 4 to 5.5 times their range. So the source state is the outlier of the u0 0.04 system's roots (the first alternative in t5's comment), and the re-solves add their own scatter of about 1.7e-4. The source's offsets do not follow the Delta shift: Delta - source is -4.4e-8, -8.7e-8 and -3.0e-7 for offsets +7.5e-4, +8.6e-4, +9.2e-4.
- **T3 against each re-solve** (U30's robust bracket, outside the written rule as in step 1b): -1.841e-3 to -1.820e-3 against U40b, -1.948e-3 to -1.926e-3 against U40, -2.009e-3 to -1.988e-3 against U40c: 11 times the re-solves' range, in the >= 3e-4 band against each.
- **T5 = root(U50) - root(U40x):** +7.8e-6 against U40, +1.147e-4 against U40b, -5.4e-5 against U40c. The step 1b statement that |T5| <= 1e-4 holds against two of the three and is inside the re-solve scatter.
- For the u0 0.02 re-solve of ELL.md (root 2.2432297, a different lineage with 3078 steps and |F| 1.0e-9): its shift is -8.1e-4 from the source's root and -1.66e-3 from the mean of the three u0 0.04 re-solves (2.2448866).

| prediction | result |
|---|---|
| \|F\| <= 1e-8 after each re-solve (90% each) | right: 1.7854e-10, 1.7841e-10 |
| steps 2565 for both (90%) | right |
| both roots within 1e-4 of r40 (45%) | WRONG by a hair: U40b is 1.069e-4 away (6.9e-6 over the bar), U40c 6.14e-5 |
| either root beyond 5e-4 (35%) | WRONG: 1.07e-4 and 6.1e-5 |
| mixed (20%) | right, as the bar reads |
| Delta against U40 within 1e-7 (50%) | half: U40b +4.3e-8 yes; U40c -2.15e-7 no |
| re-solve wall 0.3 to 0.8 h (60%) | right: 1535 s and 1546 s (0.43 h) |
| root wall 1000 to 1400 s (60%) | right: 1080 s and 1081 s |

## Status
- 10:20 UTC: step 1c done. The three u0 0.04 re-solves have roots within 1.7e-4 of each other; the source record's root is 7.5e-4 to 9.2e-4 below all three. Posted on #1105.
