# I769-win: each last-segment node's effect on Delta at D 99.875 against its shift, 0.25 to 2.0 of A1's

Machine win (surface-laptop-4), issue https://github.com/nmoinvaz/choptuik-large-d/issues/769.

Scripts (written by the coordinator, from #763's): `make_769.py` writes N1 and N2 at s = 0.25, 0.75, 1.5, 2.0 and the
control C_N2_05 (its `--selftest`, 7 of 7); `run_769.py` is run_763.py with only the states changed; `analyze_769.py`
reads #763's s = 0.5 and 1.0 beside these and gives each node's effect against s.

Criteria, written before the run: the control reproduces #763's N2_05 Delta to 1e-40; for each node, the shape over the
six shifts (monotone or not, sign changes, a fitted power with its largest residual) is quoted.

## Results

Run by winb on 2026-11-14, 08:14:54 to 09:03:24 UTC (`logs/run_769.log`), 4 threads at BelowNormal, worktree choptuik-i710 at
`5249c432`, venv-t151. All nine polishes exited 0, with no Traceback. `make_769.py` (sha256 `9c7e6c8dbacc…`) and
`analyze_769.py` (`6dd3dde8c1e9…`) are the versions the coordinator replaced at 08:15:52 UTC, a minute after the run started,
and their selftests passed (10 of 10, and the analyzer's), run before the push. `analyze_769.out` is `analyze_769.py`'s output.

Control: Delta(C_N2_05) − Delta(#763's N2_05) = +0.0000e+00, bar 1e-40: met. C_N2_05 had the same final max|F| as #763's N2_05, 8.5e-62.

Effect on Delta (Delta − X2c's root) of moving one last-segment node by s times A1's shift, s = 0.5 and 1.0 from #763:

| s | 0.25 | 0.5 | 0.75 | 1.0 | 1.5 | 2.0 |
|---|---|---|---|---|---|---|
| N1 (segs[3][1]) | −8.3453e-28 | +8.1947e-28 | −1.0680e-28 | +1.8322e-27 | +1.4197e-27 | +2.6390e-27 |
| N2 (segs[3][2]) | +6.1972e-26 | +9.9008e-26 | +1.0401e-25 | +2.7881e-26 | +1.8823e-25 | −1.2149e-25 |

Shapes, as `analyze_769.py` prints them:
- N1: monotone False, 3 sign changes (between 0.25 and 0.5, 0.5 and 0.75, 0.75 and 1.0), no power.
- N2: monotone False, 1 sign change (between 1.5 and 2.0), no power.

N1's effects are at most 2.6390e-27 in magnitude, N2's are 2.7881e-26 to 1.8823e-25. The last Newton line of each log:

| job | steps | final max\|F\| |
|---|---|---|
| C_N2_05 | 3 | 8.5e-62 |
| N1_025 | 3 | 8.2e-68 |
| N1_075 | 3 | 2.1e-71 |
| N1_15 | 3 | 7.1e-67 |
| N1_20 | 3 | 8.4e-66 |
| N2_025 | 3 | 1.6e-62 |
| N2_075 | 3 | 1.2e-61 |
| N2_15 | 4 | 1.5e-93 |
| N2_20 | 3 | 1.6e-61 |
