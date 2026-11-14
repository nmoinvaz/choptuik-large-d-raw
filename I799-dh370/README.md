# I799-dh370: the series at D 259.63 and 259.67, nearest the real-axis singularity near 259.95

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/799.

Scripts (written by the coordinator): `run799.sh` (#776's series command at #603's chain_nsr states D 259.6306 and
259.6657, in #776's worktree choptuik-large-d-685 and venv; the bases and #603's records from origin/main), `repro_check799.py`
(#776's check of the series against #603's records, and its control), `report799.py` (bars 2 and 3 on Delta's series,
and the control `--mutate=shiftP`), and `singularity_type.py` of origin/main (#782's estimators, its plants first).

Criteria, fixed before any series was read (#799): (1) each series equals #603's record in all 25 norms and both pivots,
and the control differs (`repro_check799_control.txt` ends `exit 0`); (2) Delta's root test within 5% of |259.95 - D0|;
(3) Delta's nearest stable Pade pole has |Im D*| <= 0.1 and |Re D* - 259.95| <= 0.2 (`report799.txt` ends `exit 0`, and
`report799_shiftP.txt` ends `exit 0`, bar 3 failing at every base with P moved by 1.0); (4) the Dlog estimate of mu on
Delta and on the 24 rows, with its spread and band, reported without a bar (`type799.txt`).

## Results (dh370, 2026-11-14)

Runs. `run799.sh` as the user unit `i799` (under `systemd-inhibit`, log `~/scratch799_run.log`), 12 threads at nice 10, 19:42:19 to 21:00:49 UTC.
Series exit 0, wall 2340 s (D 259.6306, ended 20:21:19 UTC) and 2339 s (D 259.6657, ended 21:00:18 UTC), no Traceback, `Result=success`. Code:
worktree choptuik-large-d-685 at main f40deb4a, venv of choptuik-large-d-614, raw origin/main 4ab8ce3a, `hp/singularity_type.py` from the code
repository's origin/main d284a229.

The bars (P = 259.95 + 0.00i; numerical evidence):

| D0 | bar 1: norms of 25, pivots | control (the record of the neighbouring base) | bar 2: root test / \|P - D0\| | bar 3: nearest stable Pade pole of Delta (D*) |
|---|---|---|---|---|
| 259.6306 | 25, equal: identical (met) | 0 of 25, DIFFERS (record D0 259.6462) | 0.3081 / 0.3194 = -3.5% (met) | 259.9093 + 0.0000i, n 9, spread 1.9e-02 (met) |
| 259.6657 | 25, equal: identical (met) | 0 of 25, DIFFERS (record D0 259.6462, the previous, as the last) | 0.2697 / 0.2843 = -5.1% (FAILED) | 259.9086 + 0.0000i, n 9, spread 1.9e-02 (met) |

`repro_check799.txt` and `repro_check799_control.txt` end `exit 0`. `report799.txt` ends `exit 1` (bar 2 failed at 1 of 2, bar 3 at 0 of 2),
`report799_shiftP.txt` ends `exit 0` (P + 1.0: bar 3 fails at 2 of 2, and bar 2 at 2 of 2). Other stable real poles of Delta: 259.927 (n 7),
259.960 (n 6), 260.016 (n 5) at D0 259.6306; 259.924 (n 7), 259.953 (n 7), 260.001 (n 5) at D0 259.6657.

#782's estimators (`type799.txt`, no bar; band S = mu in [0.25, 0.75], spreads are over windows or approximants of one method):

| D0 | Delta ratio: D* (s), mu, spreads | Delta Dlog: D* (s), mu, spreads | 24 rows' ratio: D* median, mu median (range) | 24 rows' Dlog: D* median, mu median (range) |
|---|---|---|---|---|
| 259.6306 | 259.9032 (0.2725), +0.5216 S, 3.1e-04 3.6e-02 | 259.9036 (0.2730), +0.4699 S, 3.2e-03 7.3e-02 | 259.903 (259.903 to 259.903), +0.529 (+0.522 to +0.530) | 259.905 (259.904 to 259.906), +0.285 (+0.260 to +0.470) |
| 259.6657 | 259.9032 (0.2375), +0.5173 S, 1.9e-04 2.6e-02 | 259.9034 (0.2377), +0.4787 S, 2.1e-03 9.3e-02 | 259.903 (259.903 to 259.903), +0.524 (+0.517 to +0.525) | 259.905 (259.903 to 259.905), +0.307 (+0.285 to +0.479) |

The planted check of `singularity_type.py` (`type799_planted.txt`) ends `exit 1`, as its docstring records from #782's first run: the clean S and P
plants pass (mu to 1e-9), the contaminated S and P plants FAIL the 10% bar, the near plants (s 0.457, built for D0 259.4928) pass. There is no near
plant at s 0.27 or 0.24, so the estimators are validated to 10% only for an isolated singularity (the docstring's words), not at these two bases.

Readings and caveats. Bar 2 fails at D0 259.6657 by 0.0004 of root radius (0.2697 against the bound 0.95 x 0.2843 = 0.2701). Its reference
P = 259.95 is 0.047 above the estimators' D* 259.903; against |259.903 - D0| the root test reads +13.1% (0.3081 / 0.2725) and +13.6%
(0.2697 / 0.2375). The estimators' D* does not move with D0 at the three bases nearest the point: ratio 259.9029 (D0 259.4928, #776), 259.9032,
259.9032, Dlog 259.9037, 259.9036, 259.9034. The Padé pole of bar 3 (259.909, n 9) is 0.006 from it. Delta's mu is in the S band by both
estimators at both bases; the rows' Dlog mu median (+0.285, +0.307) lies nearer the band's lower edge 0.25 than Delta's (+0.470, +0.479).

Recommended tasks (for the coordinator): (1) a near plant for these two bases (a square-root and a simple pole at s 0.2725 and 0.2375 with the second
real pole near 259.96 and the conjugate pair, judged as the contaminated ones), so that type799's mu has a validated band at s below 0.3; (2) the root
test of a planted square-root point at s 0.2375 and 0.2725 (N 24) through `locate_one`, to see whether it reads +13% above s, which would make bar
2's -5.1% an effect of P = 259.95 against D* 259.903.
