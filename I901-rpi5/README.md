# I901-rpi5: the second start-value implementation (fixed_point_M_b.py) reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/901 (proof/A_lemmas_M.md 2.5; the Mac's runs are `I427-mac/`,
`I866-mac/`, `I869-mac/`, `I870-mac/`, `I877-mac/`, `I878-mac/`). Script (the coordinator's, md5 841c6350, unedited):
`run901.sh <python> <raw clone>`, run from `solver/proof/` of the worktree `~/Source/choptuik-large-d-901`
(wip/i901-rpi5 at origin/main 62f64c9a, never committed), one process at a time at nice 10. Each run's output is
`<name>.log`, each line of `exits.txt` has the run, its exit status, the status it must have (0 for checks, 3 for
mutations), its wall time and its command. Versions in `env.txt`.

Started 2026-11-16 03:57 UTC, `all done` 05:00:30 UTC. python-flint 0.9.0, FLINT 3.6.0, python 3.13.7, aarch64 glibc 2.42
(`env.txt`), worktree commit 62f64c9a, never committed (`git status` clean).

## Result

The second start-value implementation reproduces on aarch64 Linux. All 53 runs of `run901.sh` exit with the status they
must have (27 checks exit 0, 26 mutations exit 3), in 63 min (the Mac, about 25 min), and every Pi log equals the Mac's
log of the same run in every printed number, in every verdict and in all text but the timings, the path of the stored
set and one trailing `time` line of one Mac log. The contraction constants and the overlap counts are the Mac's.

| acceptance | verdict |
|---|---|
| every exit as required | 53 of 53 (`exits.txt`, `compare_mac.txt`) |
| stored start sets overlap per component | `start_M5` against I38-macm3: 21 of 21 values and 126 of 126 derivative columns overlap, all 21 balls inside the stored ones; `start_M5_sector`, `start_M5_k40_sector` and `start_M5_vs_win2` (against I121-win2) the same; `start_M3_cert` 15 of 15 and 60 of 60; the 4 JSON sets: 269, 269, 269 and 133 balls, all overlap the Mac's, midpoints identical, radius ratio 1.000 |
| the certificates' own start data overlap per component | `cert` M3 and M5 (h 1e-9, 1e-10, 1e-11): values 13 of 13 or 19 of 19, derivatives 52 of 52 or 114 of 114, jets 1197 of 1197 (M5); `cert2` (3 boxes): values 19 of 19, V0 114 of 114, W0 399 of 399, 21 of 21 pairs in all 19 components; all PASS |
| contraction constants equal the Mac's | all 40 logs that print one are equal as printed (below) |
| overlap counts equal the Mac's | all 53 logs equal (planted M1/M3/M5 4/8/12 True, `planted_M5_mut_truth` 0 of 12) |
| python-flint and FLINT versions | 0.9.0 and 3.6.0 (`env.txt`), the Mac's versions |

| group | runs | exit 0 / exit 3 | wall |
|---|---|---|---|
| #427 (planted, check_m1, lip, two truncations, start sets) | 32 | 18 / 14 | 215 s |
| `cert` (M3, M5 at h 1e-10, 1e-9, 1e-11, each with sign and radius mutations) | 12 | 4 / 8 | 1751 s |
| `cert2` (3 boxes, mutations w0 and sign at h 1e-10) | 5 | 3 / 2 | 1763 s |
| `kernel`, `cli` (with `offbyone` and `read53`) | 4 | 2 / 2 | 54 s, 13 s |

### Contraction constants (equal to the Mac's in every run)

| run | constants |
|---|---|
| `planted_M1`, `M3`, `M5` | 0.0127, 0.0446, 0.0733 |
| `check_m1`, mutations coef, sign, scale | 0.1045, 0.1045, 0.0989, 0.1060 |
| `two_M5_60_105`, `two_M5_95_105` | 0.1509 and 0.1000, 0.1079 and 0.1000 |
| `start_M5`, `_sector`, `_k40_sector` | 0.1000 and 0.1002, 0.1135 and 0.1137, 0.2355 and 0.2360 |
| `start_M3_cert` | 0.1674 and 0.1681 |
| `cert_M3` | 0.0984, 0.0987, 0.0984, 0.0987 |
| `cert_M5` (all three h) | 0.0886, 0.0888, 0.0886, 0.0888 |
| `cert_M5`, `cert_M3` sign mutations | 0.0879, 0.0881, 0.0879, 0.0881 (M5), 0.0978, 0.0980, 0.0978, 0.0980 (M3) |

### Controls (26, all exit 3 as on the Mac)

| mutation | verdict line |
|---|---|
| `planted_M5` truth, coef, radius | `FAIL; largest midpoint distance 2.29e-13`, `NOT PROVED`, `NO CONTRACTION ... row sums up to 2.4856` |
| `check_m1` coef, sign, scale | `FAIL (no contraction)`, `FAIL`, `FAIL` |
| `lip_M5` drop | `LIPSCHITZ COMPARISON: FAIL` |
| `two_M5_60_105` forcing | `FAIL; largest ratio 819.573` |
| `start_M5` radius, coef, sign, scale, rho0; `start_M3_cert` sign | `START SET: FAIL` (6) |
| `cert` M3, M5 (3 h): sign, radius | `CERTIFICATE START DATA: FAIL` and `FAIL (no contraction)` (8) |
| `cert2` h 1e-10: w0, sign | `C2 START DATA: FAIL` (2) |
| `kernel` offbyone, `cli` read53 | `KERNEL BOUND [MUTATION offbyone]: FAIL`, `COMMAND LINE PRECISION: FAIL` |

### Differences from the Mac's logs

`compare_mac.txt` (`cmp901.py`, run with `python -I`) compares each Pi log with the Mac's log of the same run, with
the numbers masked for the text, then every number by itself, and each start-set JSON leaf by leaf as a ball
(midpoint digits, overlap, radius ratio). The largest relative difference of any printed number is 0, and the four JSON
sets have identical midpoints and radii.

| difference | where |
|---|---|
| wall times: the 42 bracketed times of 5 s or more on the Mac are 1.7 to 2.8 times longer on the Pi, median 2.3 (`start_M5` 25 s against 9 s; `cert2` h 1e-10 349 s against 160 s) | every log with a time |
| the path in the `stored set ...` line | the logs that load a stored set |
| the Mac's `cert2_M5_1e-10.log` has a 30th line, the shell's `time` output of the command (`nice -n 10 $PY ... 156.49s user ...`), which `run901.sh` does not print | `I869-mac/cert2_M5_1e-10.log`, so the comparator exits 1 on the line count (29 against 30) |

No discrepancy of a result, no script fault.

### Recommended tasks

None.
