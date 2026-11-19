# I1029-win: do the low-omega harmonics decay in the amplitude series? K 25 series at the two M = 7 excited zeros (A 2.233308, wf 0.065740) and (A 2.573290, wf 0.100532), J 750 and 1000, F_nu summed with tuned_profile.py (#1029, from #1027)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, 4 cores / 8 threads, 32 GB, Windows 11). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1029 (coordinator's plan, DIRECTION_REVIEW.md 2.3, #1027's recommendation). Status: **done**, 2026-11-19 15:50 to 18:02 UTC. Reading: **INCONCLUSIVE at both zeros** (the series does not converge there: fits break down from order 9 and the first terms of F_3 grow).

## Question

#1027 found hier_nb.py's harmonics at the two low-omega M = 7 zeros do not decay: |F3/F1|, |F5/F1|, |F7/F1| are 0.330, 0.194, 0.131 at (A, wf) = (2.233308, 0.065740) and 0.332, 0.184, 0.117 at (2.573290, 0.100532), so |F7/F5| is 0.68 and 0.63 (0.676 and 0.634 in I1027-dh610's logs), against 0.055 to 0.057 per pair at the known zero. Every excited-zero reading so far (#1013, #1020, #1026, #1027) comes from the same inner solver. The amplitude expansion (`solver/inner_amp/amp_flint_par.py`) shares no code with it. This task sums the amplitude series' tuned harmonics F_nu at the two zeros and reads whether they decay.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i1029`, detached at main `4a056a28` (`solver/inner_amp/amp_flint_par.py`, `solver/eeg_profile/tuned_profile.py`, `hp/raw_out.py`) |
| interpreter | `venv-t151`: Python 3.10.0, python-flint 0.9.0, mpmath 1.3.0, numpy 2.2.6, scipy 1.15.3 (versions also printed by the driver into `logs/run_1029.log`) |
| scheduling | `run_1029.py` via `start_1029.cmd`: at most two runs at once, 3 processes each (`--procs 3`), BelowNormal (nice 10 on Linux; the spawned workers inherit it), 1 BLAS thread, a 4 h cap per run killed by the exact pid of the run's main process with `taskkill /T /F /PID` (that tree only), the order reached read from `OUT.partial.json` |
| evaluator | `eval_1029.py`: executes the head of `tuned_profile.py` unchanged for `load_f` and `harmonics(f, K, A, numax)`, so the sums are the repository's |

## Commands

Series (cwd `<worktree>\solver\inner_amp`, the queue's order; at most two at once; `<raw>` is this folder):

```
python -u amp_flint_par.py 0.100532 25 750  640 --procs 3 --fit phys --mf 6:12 --out <raw>/sigF_w0.100532_K25_J750.json
python -u amp_flint_par.py 0.100532 25 1000 640 --procs 3 --fit phys --mf 6:12 --out <raw>/sigF_w0.100532_K25_J1000.json
python -u amp_flint_par.py 0.065740 25 750  640 --procs 3 --fit phys --mf 6:12 --out <raw>/sigF_w0.065740_K25_J750.json
python -u amp_flint_par.py 0.065740 25 1000 640 --procs 3 --fit phys --mf 6:12 --out <raw>/sigF_w0.065740_K25_J1000.json
```

Not `--trunc` (the truncated series carries ln j terms past sigma_(M+1), #1016). No `--phys-prec` (the issue's commands have none; the default is used).

Checks and evaluation (before the series finish):

```
python -I -X utf8 eval_1029.py --selftest      # the convergence rules and readings on planted series (logs/selftest_eval.log)
python -I -X utf8 eval_1029.py --checks        # tuned_profile.py --plant (exit 0), --plant --mutate=drift (exit 1), the K 45 file at A 2.72 (logs/checks.log)
python -I -X utf8 run_1029.py --selftest       # the two-slot scheduler on dummy children (logs/selftest_run.log)
python -I -X utf8 eval_1029.py > eval_1029.txt # after the runs: the tables and the readings
```

## Checks, fixed before the runs (the issue's)

- Evaluator: `tuned_profile.py --plant` exits 0 and `--plant --mutate=drift` exits 1. Through the same evaluation, the stored K 45 file `solver/inner_amp/scan45J1250/sigF_w1.0000_K45_J1250_p1280.json` at A 2.72 gives F3/F1 within 1e-4 of 0.05482 + 0.00543i (taken as the absolute difference of the complex numbers).
- Convergence at the point: the series converges there when, at both J, the last term of each sum is at most 1e-2 of F_nu for nu = 3, 5, 7 (nu = 1 is the single term A sin theta), and the two J agree to 1e-3 in |F_nu/F_1|. My reading of the second: the absolute difference for nu = 3, 5, 7 (the relative difference is printed too).

## Readings, fixed before the runs (the issue's), per zero where the series converges

- |F7/F5| of the series at least 0.3: non-decay **confirmed**.
- |F7/F5| at most 0.2: **contradicted** (hier_nb.py's low-omega harmonics are wrong somewhere).
- Between: **undecided**. The difference to hier is reported (hier drops F9, about 0.6 of F7 here).
- Not converged at the point: **inconclusive**, with the last-term sizes.

My reading where the issue is silent: the class is that of the larger J (1000), and it is undecided unless the J 750 value gives the same class. The bars are inclusive.

Reported per zero and J: |F_nu/F_1| and |F_(nu+2)/F_nu| for nu = 1 to 11 (F_13 only for the last ratio), the number of terms and the last term relative to F_nu, beside #1027's values (|F3/F1|, |F5/F1|, |F7/F1| and |F7/F5|).

## Plan and estimate

Queue as above, two slots. A run is guessed at 1 to 4 h at 3 processes beside the other run on 4 cores, so the four take about 7 h (unknown). A run past 4 h is stopped by its exact pid and the order reached is reported (OUT.partial.json holds sigma and f up to that order, but the issue's readings need the full K 25).

## Files

| file | content |
|---|---|
| `README.md` | this file |
| `sigF_w{0.100532,0.065740}_K25_J{750,1000}.json` (and `.partial.json`) | the four series (sigma, f, fit_info, order_times). `f` entries beyond a double (mostly orders 21 to 25: 33, 26, 29 and 18 of 78 entries) are stored as `Infinity`, which Python's json reads and strict JSON parsers refuse |
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

The sums themselves are numerical garbage: \|F_3/F_1\| = 5e604 (J 750) and 1.6e505 (J 1000) at wf 0.065740, 1.3e554 and 6e454 at wf 0.100532, because the f at the highest orders (k = 21 to 25) reach 1e270 to 1e540 and dominate. Hier's \|F_nu/F_1\| (0.330, 0.194, 0.131 and 0.332, 0.184, 0.117) has nothing to be compared with. The table of F_nu and the ratios is in `eval_1029.txt`, but it carries no information.

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
- Orders 1 to 5 are fine and agree between the two J to 1e-9 or better (sigma_1 = -0.8857 + 1.1061i and sigma_2 = 0.1284 - 0.6748i at wf 0.100532). From order 9 (order 7 at wf 0.065740, J 750) the fit's own error estimate is as large as the value, and the value depends on J by 4 to 5 decades (S_1^(9) falls 4e4 times from J 750 to 1000 at both zeros). So the breakdown is the late-order fit's, not a property of the series. Its steepness in J suggests J 750 and 1000 are below the scale where the 1/j expansion of the fit applies at this omega (untested).
- Separately, the first terms of the sums already grow at these A, in orders where the f agree between J: |f(k,3) A^k| = 4.03, 39.8 at k = 3, 5 at wf 0.065740 and 4.12, 34.3 at wf 0.100532 (equal across J), then 211 (J 750) and 457 (J 1000) at k = 7 at wf 0.065740, 316 and 319 at wf 0.100532. Hier's |F_3| is 0.368 and 0.427. At the working case (A 2.72, wf 1.0) the same terms are 0.086, 0.013, 0.0016, 2e-4. If the growth stayed geometric (a factor 5 to 12 per order step), the series' radius in A would be about A/3, so these zeros lie outside the circle where the direct sum converges and the amplitude series would need resummation (Padé) with reliable high orders. `terms_1029.txt` has the numbers.
- The stored amplitude scans cover wf 0.7 to 1.04. Nothing was validated near wf 0.1 before, and the issue's commands (default `--phys-prec`, J 750 and 1000) are the ones run here.
- Run times were 55 to 67 min each, against the guess of 1 to 4 h: the fits (about 2500 to 2900 s) dominate, as in #1003.

Limits: two J only, K 25, the issue's `--fit phys --mf 6:12` basis at default `--phys-prec`. Whether a larger J, a larger `--phys-prec` or a different fit basis restores the series at low omega is untested. The reading rests on the issue's fixed rules, which have no branch for a series that diverges before the fit breaks. The JSON files carry `Infinity` for f beyond a double (see Files).

## Commands, as run

The four series as in Commands above. Driver started 15:50:29 UTC, all four done at 18:02:25 UTC (`logs/run_1029.log`: w0.100532 J 750 3293 s, J 1000 4033 s, w0.065740 J 750 3333 s, J 1000 3883 s). Evaluation: `python -I -X utf8 eval_1029.py > eval_1029.txt` and `python -I -X utf8 terms_1029.py > terms_1029.txt` (venv-t151).
