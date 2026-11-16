# I908-winb: the second start-value implementation (fixed_point_M_b.py) reproduced on Windows x86-64

Machine winb (Surface Laptop 4, Windows 11 Pro, i7-1185G7), issue https://github.com/nmoinvaz/choptuik-large-d/issues/908
(follows #901, proof/A_lemmas_M.md 2; the Mac's runs are `I427-mac/`, `I866-mac/`, `I869-mac/`, `I870-mac/`, `I877-mac/`,
`I878-mac/`, the Pi's are `I901-rpi5/`). Script (the coordinator's, md5 3aaf112a459a154d404f6d2b4629abd0, unedited):
`bash run908.sh <python> <raw root> <worktree>` from this folder, with the venv python
`C:/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe`, the raw root `C:/Users/nathan/Source/choptuik-large-d-raw-754`
(a worktree of raw main e331ca7a that holds `I38-macm3/`, `I121-win2/` and the Mac's folders) and the worktree
`C:/Users/nathan/Source/choptuik-i908` (detached at origin/main 321fcdb8, 49bfccec is an ancestor, never committed, `git status`
clean). One process at a time, started detached at below-normal priority (the script has no `nice`). Each run's output is
`<name>.log`, each line of `exits.txt` has the run, its exit status, the status it must have (0 for checks, 3 for mutations),
its wall time and its command. Versions in `env.txt`.

Started 2026-11-16 06:05:39 UTC, `all done` 07:01:37 UTC (56 min). python-flint 0.9.0, FLINT 3.6.0, Python 3.14.10,
Windows-11-10.0.26200-SP0 (`env.txt`), worktree commit 321fcdb8. The logs print the same `python-flint 0.9.0, FLINT 3.6.0,
512 bits` lines as the Mac's (compared line by line).

## Result

The second start-value implementation reproduces on Windows. All 53 runs of `run908.sh` exit with the status they must have
(27 checks exit 0, 26 mutations exit 3), in 56 min (the Pi 63 min, the Mac about 25 min), and every Windows log equals the
Mac's log of the same run in every printed number, in every verdict and in all text but the timings, the path of the stored
set and one trailing `time` line of one Mac log. The contraction constants and the overlap counts are the Mac's.

| acceptance | verdict |
|---|---|
| every exit as required | 53 of 53 (`exits.txt`, `compare_mac.txt`): 27 checks exit 0, 26 mutations exit 3 |
| stored start sets overlap per component | `start_M5` against I38-macm3: 21 of 21 values and 126 of 126 derivative columns overlap, all 21 balls inside the stored ones; `start_M5_sector`, `start_M5_k40_sector` and `start_M5_vs_win2` (against I121-win2) the same; `start_M3_cert` 15 of 15 and 60 of 60; the 4 JSON sets: 269, 269, 269 and 133 balls, all overlap the Mac's, midpoints identical, radius ratio 1.000 |
| the certificates' own start data overlap per component | `cert` M3 and M5 (h 1e-9, 1e-10, 1e-11): values 13 of 13 or 19 of 19, derivatives 52 of 52 or 114 of 114, jets 1197 of 1197 (M5); `cert2` (3 boxes): values 19 of 19, V0 114 of 114, W0 399 of 399, 21 of 21 pairs in all 19 components; all PASS |
| contraction constants equal the Mac's | all 33 logs that print one are equal as printed (below) |
| overlap counts equal the Mac's | all 53 logs equal (planted M1/M3/M5 4/8/12 True, `planted_M5_mut_truth` 0 of 12) |
| `kernel`, `cli` | `KERNEL BOUND: PASS` (largest true value / bound 0.999815, 0 of 11336 not certainly at or below the bound), `COMMAND LINE PRECISION: PASS` |
| python-flint and FLINT versions | 0.9.0 and 3.6.0 (`env.txt`), the Mac's and the Pi's versions |

| group | runs | exit 0 / exit 3 | wall |
|---|---|---|---|
| #427 (planted, check_m1, lip, two truncations, start sets) | 32 | 18 / 14 | 179 s |
| `cert` (M3, M5 at h 1e-10, 1e-9, 1e-11, each with sign and radius mutations) | 12 | 4 / 8 | 1536 s |
| `cert2` (3 boxes, mutations w0 and sign at h 1e-10) | 5 | 3 / 2 | 1588 s |
| `kernel`, `cli` (with `offbyone` and `read53`) | 4 | 2 / 2 | 50 s |

(`times.txt`, made by `times908.py`; the sum of the wall times is 3353 s.)

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

`compare_mac.txt` is the output of the Pi's `cmp901.py` (`I901-rpi5/cmp901.py`, unedited, md5 b8684d07c7399c210593ad35f01f25e2,
run with `python -I -X utf8`; its column headed "Pi" is this run). It compares each log with the Mac's log of the same run, with
the numbers masked for the text, then every number by itself, and each start-set JSON leaf by leaf as a ball (midpoint
digits, overlap, radius ratio). The largest relative difference of any printed number is 0 in every log, and the four JSON sets
have identical midpoints and radii. The lines it masks (`stored set`, `python-flint`) I compared separately: the
`python-flint` lines are equal in all 53 logs, the `stored set` lines differ in the path only.

| difference | where |
|---|---|
| wall times: the 35 bracketed times of 5 s or more on the Mac are 1.60 to 2.12 times longer here, median 1.88 (`cert2` h 1e-10 158 s against 77 s, `cert2` mutation w0 174 s against 82 s) | every log with a time (`times.txt`) |
| the path in the `stored set ...` line (`C:/Users/nathan/Source/choptuik-large-d-raw-754/I38-macm3/...` against the Mac's `/Users/nathan/Source/choptuik-large-d-raw-427/I38-macm3/...`) | the 7 logs that load a stored set from the raw clone: `start_M5`, `start_M5_sector`, `start_M5_k40_sector`, `start_M5_mut_sign`, `start_M5_mut_scale`, `start_M5_mut_rho0`, `start_M5_vs_win2` (against I121-win2) |
| the Mac's `cert2_M5_1e-10.log` has a 30th line, the shell's `time` output of the command (`nice -n 10 $PY ... 156.49s user ...`), which `run908.sh` does not print | `I869-mac/cert2_M5_1e-10.log`, so the comparator exits 1 on the line count (29 against 30), as on the Pi |

`compare_mac.txt` equals the Pi's `I901-rpi5/compare_mac.txt` line for line except the total wall time on its first line
(3353 s here, 3796 s on the Pi), so Windows and aarch64 agree with the Mac, and with each other, in the same 53 logs and 4 sets.

No discrepancy of a result, no script fault. One count differs from the Pi's README: it says "all 40 logs that print" a
contraction constant, and its own `compare_mac.txt` (and this one) lists 33 such logs; the constants are equal in all of them.

### Recommended tasks

None.

## Files

`<name>.log` one per run (53), `exits.txt`, `env.txt`, `run908.sh` (unedited), `start_M5.json`, `start_M5_sector.json`,
`start_M5_k40_sector.json`, `start_M3_cert.json` (the start sets), `compare_mac.txt` and `cmp901.py` (the Pi's comparator),
`times.txt` and `times908.py` (this runner's group walls, bracketed times against the Mac's, and the `stored set` lines).
