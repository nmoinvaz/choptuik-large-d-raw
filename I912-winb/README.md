# I912-winb: lemma S's series control over a box after #865's fix, on Windows x86-64

Machine winb (Surface Laptop 4, Windows 11 Pro, i7-1185G7), issue https://github.com/nmoinvaz/choptuik-large-d/issues/912
(follows #865; the Mac's outputs are `I865-mac/`, raw f9f5f629). Script (the coordinator's, md5
df8f3da4dcefb54a317c243d36c111ac, unedited): `bash run912.sh <python> <raw root> <worktree> winb` from this folder, with the
venv python `C:/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe`, the raw root
`C:/Users/nathan/Source/choptuik-large-d-raw-754` (a worktree of raw main pulled to f9f5f629) and the worktree
`C:/Users/nathan/Source/choptuik-i912` (detached at origin/main 40cbc871, never committed, `git status` clean; 26eb48e9 is an
ancestor). One process at a time, started detached at below-normal priority. Each line of `exits.txt` has the run, its exit
status, the status it must have and its wall time. Versions in `env.txt`.

Started 2026-11-16 07:12:32 UTC, `done` 07:13 UTC (20 s of run time in all; the estimate was 10 min). python-flint 0.9.0, FLINT 3.6.0,
Python 3.14.10, Windows-11-10.0.26200-SP0 (`env.txt`), worktree commit 40cbc871.

## Result

The fixed control fires on Windows. All 8 runs exit with the status they must have (7 exit 0, the control exits 3), the four
series mutations over boxes report `holds: False` (M = 1: `passes: False`), and the control through the code before the fix
(34b00905) reports `holds: True`, the mutation not caught. The certificate's runs `s3.json` and `s5.json` are not byte for byte
the Mac's: every verdict and parameter field is equal, the f64 weights differ by up to 3.7e-14 (M = 3) and 1.2e-12 (M = 5)
relative, and at M = 5 four balls have equal midpoints and radii that differ by 0.2% to 3.0% (below).

| acceptance | verdict |
|---|---|
| every run has its required exit status | 8 of 8 (`exits.txt`): `s3`, `s5`, `s1`, `m3box`, `m5box`, `m5box9`, `m1box` exit 0, `m3box_prefix` (the control) exits 3 |
| each mutation log reports `holds: False` (M = 1 `passes: False`) | `m3box`, `m5box`, `m5box9`: `lemma S holds: False (must be False)`; `m1box`: `lemma S passes: False (must be False)`; the control `m3box_prefix`: `lemma S holds: True (must be False)`, as the Mac's `box.log` |
| `s3.json`, `s5.json` equal the Mac's byte for byte, or the differing fields are reported | not equal, reported: `s3.json` 39 of 55 fields differ, `s5.json` 61 of 73 (below); the script's own `cmp` lines say `DIFFERS` for both |
| the logs equal the Mac's | `s3.log`, `s5.log`, `s1.log`, `m3box.log`, `m5box.log`, `m5box9.log` and the control against `box.log` equal the Mac's line for line except the Mac's trailing `exit 0` line (`compare_logs.txt`); `s1.log` `ALL CHECKS PASS: True`, `s3.log` M = 3 and `s5.log` M = 5 `ALL CHECKS PASS: True` |
| python-flint and FLINT versions | 0.9.0 and 3.6.0 (`env.txt`), the Mac's |

## The certificate's JSON against the Mac's

`compare_mac.txt` (`cmp912.py`, run with `-X utf8`) compares this run's file with the Mac's committed blob (`git show
HEAD:I865-mac/<name>.json`) field by field. My files have CRLF line endings (Python's text mode on Windows, 62 and 80 CR); the
Mac's checked-out copies have them too (the raw worktree is CRLF) and equal its blob once CRLF is read as LF, so the `DIFFERS`
of the script's `cmp` is the digits, not the line endings.

| file | fields | equal | f64 fields that differ | largest relative difference | balls that differ |
|---|---|---|---|---|---|
| `s3.json` (M = 3, box 1e-6) | 55 | 16 | 39: `wts_R_diag` 13, `wts_R_plain` 13, `wts_S` 13 | 3.74e-14 (`wts_R_plain[8]`), median 6.27e-15 | none (`F_S`, `Lambda_plain`, `lip_S`, `rho_S` equal as strings) |
| `s5.json` (M = 5, box 1e-6) | 73 | 12 | 57: `wts_R_diag` 19, `wts_R_plain` 19, `wts_S` 19 | 1.23e-12 (`wts_S[5]`), median 4.31e-13 | 4, midpoints equal at the printed digits |

The equal fields include every verdict and parameter (`ok`, `ok_S`, `ok_old` True, `M`, `N`, `k`, `box`, `Z`, `rp`, `a_eff`,
`Lambda_diag`, `lip_old`). The four balls of `s5.json` that differ, by their radii:

| ball | midpoint | radius here | radius on the Mac | ratio |
|---|---|---|---|---|
| `F_S` | 1.373802916e+35 | 5.49e+24 | 5.33e+24 | 1.0300 |
| `Lambda_plain` | 0.4233267068 | 6.85e-12 | 6.90e-12 | 0.9928 |
| `lip_S` | 0.7246665601 | 1.65e-11 | 1.63e-11 | 1.0123 |
| `rho_S` | 1.995838813e+36 | 4.36e+26 | 4.35e+26 | 1.0023 |

## Discrepancies (listed, not fixed)

- `s3.json` and `s5.json` are not byte for byte the Mac's, as the issue allows for the f64 weights: the weights differ by
  3.7e-14 (M = 3) and 1.2e-12 (M = 5) relative, which is more than the last digit at M = 5 (the weights are `wts_R_diag`,
  `wts_R_plain`, `wts_S`), and four M = 5 balls differ in their radii by up to 3.0% with equal midpoints. The verdicts are the
  Mac's.
- The script's `cmp` compares bytes of files that both carry CRLF here (the Mac's blob has LF); a byte comparison with the blob
  needs `git show` and CRLF read as LF, as `cmp912.py` does.
- The Mac's logs end with a line `exit 0` that the script's logs do not have.

### Recommended tasks

None.

## Files

`<name>.log` one per run (8), `exits.txt`, `env.txt`, `run912.sh` (unedited), `s3.json`, `s5.json`, `compare_mac.txt` and
`cmp912.py` (this runner's field-by-field comparison), `compare_logs.txt` (`diff` of each log with the Mac's).
