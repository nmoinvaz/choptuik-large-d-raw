# I776-dh370: the chain's series at three of #603's states past D 259, toward the real-axis singularity at 259.95

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/776.

Scripts: #760's, with the folder, the bases and the bars' point changed (written by the coordinator): `run776.sh` (the
24-order series, `anm_run.py --save_jet 2` with #603's chain_nsr flags, at D 259.0505, 259.2582 and 259.4928, in
#712's worktree choptuik-large-d-685 at main f40deb4a and the venv of choptuik-large-d-614; the bases and #603's
chain_nsr records are taken from origin/main into ~/scratch776, so the live clone is not pulled),
`stage_summary776.sh` (jet_singularity.py summary, table685.py, report776.py, and repro_check776.py with its control),
`repro_check776.py`, `report776.py`.

Bars, written before any series was read (#776): (1) each series equals #603's record of the step from its base in all
25 norms and both pivots, and the control (the next base's record) differs; (2) Delta's root test within 5% of
|P - D0|, P = 259.95 + 0.00i; (3) Delta's nearest stable Pade pole has |Im D*| <= 0.1 and |Re D* - 259.95| <= 0.2.
On #760's three bases read as new (`--D_min=255.8` on jet_760.json), bars 2 and 3 pass at D 258.7829 (+4.5%, pole
259.96 + 0.00i) and fail at 256.5686 and 257.6853, and the control `--mutate=shiftP` (P moved by +1.0) fails bar 3 at
every base.

## Results (dh370, 2026-11-14)

Runs. `run776.sh 259.0505 259.2582 259.4928` as the user unit `i776` (under `systemd-inhibit`, the same command and log
`~/scratch776_run.log` as the brief's nohup line), 12 threads at nice 10, 15:47:27 to 17:44:08 UTC. Series exits 0, wall 2332, 2333 and
2336 s, no Traceback, `Result=success`. Staging (`stage_summary776.sh`) 17:44:34 to 17:55:38 UTC, `summary776.log` ends "exit 0".
Code: worktree choptuik-large-d-685 at main f40deb4a, venv of choptuik-large-d-614, raw origin/main 05bb9058 for the bases and #603's records.

The bars at each base (numerical evidence, P = 259.95 + 0.00i):

| D0 | bar 1: norms of 25, pivots | control (next base's record) | bar 2: root test / \|P - D0\| | bar 3: nearest stable Pade pole of Delta (D*) | rows within 0.2 of P |
|---|---|---|---|---|---|
| 259.0505 | 25, equal: identical (met) | 0 of 25, DIFFERS | 0.925 / 0.900 = +2.9% (met) | 259.94 + 0.00i, n 9 (met) | 24 of 24 |
| 259.2582 | 25, equal: identical (met) | 0 of 25, DIFFERS | 0.707 / 0.692 = +2.3% (met) | 259.92 + 0.00i, n 9 (met) | 24 of 24 |
| 259.4928 | 25, equal: identical (met) | 0 of 25, DIFFERS | 0.457 / 0.457 = +0.0% (met) | 259.91 + 0.00i, n 9 (met) | 24 of 24 |

Bar 1's control (`repro_check776.py --control`) exits 0, which is the control working (every base DIFFERS). `report776.txt`: bar 2 failed at 0 of 3,
bar 3 at 0 of 3. The control `report776.py ... --mutate=shiftP` (P + 1.0, `report776_shiftP.txt`) exits 0: bar 3 fails at 3 of 3 (and bar 2 at 3 of 3).
Tool check (`report776_selftest760.txt`, `jet_760.json` read as new with `--D_min=255.8`, exit 1 as the script says): bars pass at D 258.7829
(+4.5%, 259.96 + 0.00i) and fail at 256.5686 and 257.6853, the README's numbers.

The track toward P (Delta's nearest stable pole, the recurrence fit's D*, the rows' median D*, all on the real axis, Im D* 0.00 to 0.00 in all 24 rows):

| D0 | \|s\| of the nearest pole | pole D* | recurrence D* (spread) | rows' median D* |
|---|---|---|---|---|
| 258.7829 | 1.176 | 259.96 | 260.03 (2.09) | 259.95 |
| 259.0505 | 0.889 | 259.94 | 260.00 (0.26) | 259.94 |
| 259.2582 | 0.665 | 259.92 | 259.95 (0.10) | 259.92 |
| 259.4928 | 0.420 | 259.91 | 259.93 (0.07) | 259.91 |

Caveats. The nearest pole's D* drifts down from 259.96 to 259.91 as D0 rises, and at the last base Delta has four real stable poles (259.91 n 9,
259.95 n 8, 260.00 n 3, 260.01 n 5) over 0.10, where a single simple pole would give one; the exponent is untested, so a simple pole is not
established and a branch point is not either. The spread of the recurrence fit falls with |s| (2.09, 0.26, 0.10, 0.07), which is a spread over fit
choices, not an enclosure. The singularity is 0.42 to 0.46 ahead of the last base (259.4928), so the chain at D 259.52 is inside its reach.

Recommended tasks (for the coordinator): (1) the exponent of the real-axis singularity from these three series and #760's last, with planted
square-root and simple-pole controls through the same locate code, accepted when both plants are recovered and the three bases' exponents agree
within their spread; (2) the series at the next #603 state past D 259.5, accepted by these bars, to see whether D* stays at 259.91 to 259.93
as |s| falls below 0.4.
