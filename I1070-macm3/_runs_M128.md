### M 128 pilot: no sign change (stop)

`run_1070.sh M128`, started 2026-11-21 21:23:13 UTC, exit 0 at 22:14:35 UTC (capped_run wall 3082 s, own 3070.0 s, cap 21600 s not
reached), child pid 95148. Files: `run_M128.log`, `lowD_gamma_D3.15_M128.jsonl`, `table_M128.md` (from `table_1070.py`),
`res_M128.log`, `res_summary_M128.txt`, `res_stats_M128.txt`, `exits_1070.txt`.

Acceptance: F after the polish 1.103e-28 (below 1e-27: met). Sign changes in the bracket: 0 (needs exactly one): **not met**. The
script's four-width search (±1e-4, ±1e-3, ±1e-2, ±4e-2 round the guess λ 3.713742) found sign -1 at all 9 points, so λ and γ are
null. Per the issue: report and stop; the M 160 run was not started, and nothing was changed or restarted.

M128: D 3.15, M 128, F after the polish 1.103e-28, guess lam 3.713742062 (gamma guess 0.269270), sign changes 0, determinants 9, lam None, gamma None, own seconds 3070.0

polish lines:
- newton 0: |F| 6.69e-26 |dz| 2.10e-22 lam 1 dDelta +1.49e-31 Delta 2.961319687827138 piv 2.2e-04..9.3e+00  t 141.2s
- newton 1: |F| 1.29e-28 |dz| 9.18e-27 lam 1 dDelta -7.57e-31 Delta 2.961319687827138 piv 2.2e-04..9.3e+00  t 294.6s

| lam | sign | ln\|det\| | pivots | s |
|---|---|---|---|---|
| 3.673742062090 | -1 | 2230.826596 | 2.65e-04..2.90e+02 | 337.1 |
| 3.703742062090 | -1 | 2254.866799 | 2.65e-04..3.16e+02 | 308.7 |
| 3.712742062090 | -1 | 2262.078488 | 2.64e-04..3.24e+02 | 296.9 |
| 3.713642062090 | -1 | 2262.799647 | 2.68e-04..3.25e+02 | 252.8 |
| 3.713742062090 | -1 | 2262.879776 | 2.68e-04..3.25e+02 | 299.9 |
| 3.713842062090 | -1 | 2262.959904 | 2.68e-04..3.25e+02 | 282.8 |
| 3.714742062090 | -1 | 2263.681061 | 2.68e-04..3.26e+02 | 306.1 |
| 3.723742062090 | -1 | 2270.892530 | 2.67e-04..3.35e+02 | 322.2 |
| 3.753742062090 | -1 | 2294.929397 | 2.67e-04..3.65e+02 | 368.1 |

bracket scanned: lam 3.673742 .. 3.753742, gamma 0.266401 .. 0.272202; signs [-1]
d ln|det| / d lam between neighbouring points: min 801.2, max 801.3 (ln|det| rises with lam at every pair: True)
seconds per determinant: mean 308.3, min 252.8, max 368.1; sum 2775 of the run's 3070 s
lam_guess(3.5) = 3.092124 against 1/gamma(3.5) = 3.101876 (#628's M 128 gamma 0.3223855827556097): the guess misses by -0.009751 at D 3.5

Resources, from `res_M128.log`: polls 51 (60 s each), rss GB min 0.19 max 3.36 mean 1.89; cpu% (ps, 100 = one core) min 593.2 mean 598.9 max 600.0; load1 mean 6.33 max 9.62; free memory min 85%; free disk min 22.8 GiB

Machine after the pilot (22:15 UTC): cpu 86.6% idle, free memory 85%, free disk 23 GiB.
