
## Files

| file | content |
|---|---|
| `README.md` | this file |
| `sigF_w{0.100532,0.065740}_K25_J{750,1000}.json` (and `.partial.json`) | the four series (sigma, f, fit_info, order_times). `f` entries beyond a double (orders 21 to 25 mostly: 33, 26, 29 and 18 of 78) are stored as `Infinity`, which Python's json reads and strict JSON parsers refuse |
| `run_1029.py`, `start_1029.cmd` | the driver (two slots, 4 h cap by exact pid, status log) and its detached launcher |
| `eval_1029.py`, `eval_1029.txt` | evaluator (`--checks`, `--selftest`, tables and readings), its output. Entries beyond a double are rebuilt from the run logs' 10 digits (`load_run`) and all sums are in mpmath |
| `terms_1029.py`, `terms_1029.txt` | supplementary (not a reading of the issue): |sigma_n|, and the sizes of the first terms of F_3, F_5, F_7's sums, beside the working case (the stored K 45 file at A 2.72) |
| `logs/` | `checks.log`, `selftest_eval.log` (first version), `selftest_eval_final.log`, `selftest_run.log`, `run_1029.log`/`.exit`, `status_1029.log` (free memory and order every 10 min), per run `w<wf>_J<J>.log` and `.exit` |
| `tmp/` | the small patch scripts I used on my own evaluator and driver |

## Result

**INCONCLUSIVE at both zeros.** The amplitude series cannot be summed at these A with these runs, so it neither confirms nor contradicts hier_nb.py's non-decaying harmonics. The series' fits break down from order 9 (order 7 at wf 0.065740, J 750), and even the first terms of F_3's sum grow (4.0, 40, 200 to 460 at k = 3, 5, 7 against hier's |F_3| = 0.37 to 0.43).

Checks (before the runs, as the issue fixes them):

| check | result |
|---|---|
| `tuned_profile.py --plant`, `--plant --mutate=drift` | exit 0, exit 1 (as it must) |
| K 45 J 1250 file at A 2.72, F_3/F_1 | 0.054816 + 0.005433i against 0.05482 + 0.00543i, difference 4.8e-6 (bar 1e-4); a reference 1% higher fails it |
| `eval_1029.py --selftest`, `run_1029.py --selftest` | pass (readings, both convergence rules, inclusive bars, a mutated bar; two slots, cap with order reported, crash, STOP) |
| the four runs | all exit 0, 3282 to 4024 s each (two at once, 3 processes each, BelowNormal, verified by Win32_Process priority 6 on the main and every worker), no cap hit, at least 13.3 GiB free throughout |

Readings (the issue's rules; the evaluator's tables are in `eval_1029.txt`):

| zero | convergence: last term at most 1e-2 of F_nu, nu = 3, 5, 7, both J | the two J agree to 1e-3 in \|F_nu/F_1\| | reading |
|---|---|---|---|
| (2.233308, wf 0.065740) | no: last term / F_nu = 1.0 at every nu and J (the last term, k = 25, is the sum) | no | INCONCLUSIVE |
| (2.573290, wf 0.100532) | no: 1.0 at every nu and J | no | INCONCLUSIVE |

The sums themselves are numerical garbage: \|F_3/F_1\| = 5e604 (J 750) and 1.6e505 (J 1000) at wf 0.065740, 1.3e554 and 6e454 at wf 0.100532, because the f at k = 21 to 25 reach 1e330 to 1e550 and dominate. Hier's \|F_nu/F_1\| (0.330, 0.194, 0.131 and 0.332, 0.184, 0.117) has nothing to be compared with. The table of F_nu and the ratios is in `eval_1029.txt`, but it carries no information.

Where it breaks, from the logs (`fit err` is the plateau change between Mf = 6 .. 12 fits, S_1^(k) the order-k multiplier; at the working case wf 1.0 sigma_n falls 1, 0.91, 0.42, 0.13, 0.031, ...):

| zero | order k | S_1^(k) at J 750 (fit err) | S_1^(k) at J 1000 (fit err) |
|---|---|---|---|
| wf 0.100532 | 5 | -0.345161112118 - 0.265138744368i (4.1e-11) | -0.345161112138 - 0.265138744335i (1.0e-13) |
| | 7 | -0.218 + 0.461i (6.7e-2) | -0.253 + 0.404i (2.3e-5) |
| | 9 | -2.4e9 + 3.7e7i (2.4e9) | -6.1e4 + 3.9e3i (6.1e4) |
| | 11 | -7.4e27 + 8.4e28i (8.4e28) | 7.0e17 + 1.2e18i (1.4e18) |
| wf 0.065740 | 5 | -0.207791604384 - 0.549035503247i (9.4e-10) | -0.207791605116 - 0.549035503750i (2.1e-12) |
| | 7 | -13.0 + 3.2i (12) | -0.995 + 0.488i (3.7e-3) |
| | 9 | 3.1e12 - 2.1e12i (3.7e12) | 6.9e7 - 6.2e7i (9.3e7) |
| | 11 | -2.8e36 + 1.6e35i (2.8e36) | -3.4e25 + 1.4e25i (3.6e25) |

Observations:
- Orders 1 to 5 are fine and agree between the two J to 1e-9 or better (sigma_2 = 0.1284 - 0.6748i and -0.8857 + 1.1061i at wf 0.100532). From order 9 (order 7 at wf 0.065740, J 750) the fit's own error estimate is as large as the value, and the value depends on J by 4 to 5 decades (S_1^(9) falls 4e4 times from J 750 to 1000 at both zeros). So the breakdown is the late-order fit's, not a property of the series. Its steepness in J suggests J 750 and 1000 are below the scale where the 1/j expansion of the fit applies at this omega (untested).
- Separately, the first terms of the sums already grow at these A, in orders where the f agree between J: |f(k,3) A^k| = 4.03, 39.8 at k = 3, 5 (both zeros the same to 3 digits across J), then 211 (J 750) and 457 (J 1000) at k = 7 at wf 0.065740, 316 and 319 at wf 0.100532. Hier's |F_3| is 0.368 and 0.427. At the working case (A 2.72, wf 1.0) the same terms are 0.086, 0.013, 0.0016, 2e-4. If the growth stayed geometric (a factor 5 to 12 per order step), the series' radius in A would be about A/3, so these zeros lie outside the circle where the direct sum converges and the amplitude series would need resummation (Padé) with reliable high orders. `terms_1029.txt` has the numbers.
- The stored amplitude scans cover wf 0.7 to 1.04. Nothing was validated near wf 0.1 before, and the issue's commands (default `--phys-prec`, J 750 and 1000) are the ones run here.
- Run times were 55 to 67 min each, against the guess of 1 to 4 h: the fits (about 2500 to 2900 s) dominate, as in #1003.

Limits: two J only, K 25, the issue's `--fit phys --mf 6:12` basis at default `--phys-prec`. Whether a larger J, a larger `--phys-prec` or a different fit basis restores the series at low omega is untested. The reading rests on the issue's fixed rules, which have no branch for a series that diverges before the fit breaks. The JSON files carry `Infinity` for f beyond a double (see Files).

## Commands, as run

The four series as in Commands above. Driver started 15:50:29 UTC, all four done at 18:02:25 UTC (`logs/run_1029.log`: w0.100532 J 750 3293 s, J 1000 4033 s, w0.065740 J 750 3333 s, J 1000 3883 s). Evaluation: `python -I -X utf8 eval_1029.py > eval_1029.txt` and `python -I -X utf8 terms_1029.py > terms_1029.txt` (venv-t151).
