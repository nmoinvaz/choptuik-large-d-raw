# I882-rpi5: Theorem B(1)'s certified constants (B8, B5, B_chain) reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/882. Script (the coordinator's): `run882.sh`, every command of
proof/B8_constants.md 13, proof/B5_inner.md 10 and proof/B_chain.md 11 as written, from `solver/proof/` of the worktree
`~/Source/choptuik-large-d-882` (wip/i882-rpi5 at origin/main 4f2595c7, never committed), one process at a time at nice 10.
Exits and wall times in `exits_882.txt`; versions in `env.txt`; each command's stdout and stderr in `<name>.log`.

The commands overwrite the worktree's stored files, and the scan commands append to their `--log` file, so the script ends
by recording `status_after.txt` and `diff_against_stored.txt` and copying every changed or new file of `solver/proof/` to
`changed/`.

## Result

Started 2026-11-16 00:09 UTC, finished 01:28 UTC (1 h 18 min of wall time; the coordinator's estimate was 2 to 3 h). 64
commands: 35 `run` (all exit 0), 27 `ctrl` and 2 `scan`. `env.txt`: python-flint 0.9.0, FLINT 3.6.0, numpy 2.5.4,
mpmath 1.3.0, scipy 1.18.1, python 3.13.7, worktree commit 4f2595c7.

The two scan lines exit as documented: `b5_bounds_scan` (Z = 0.0085, 0.009, 0.0091) and `b5_bounds_rp` (r+ = 0.15) both
exit 1, and their lines equal the stored blocks (stored lines 73-108 of `b5_bounds_scan.log`, 13-24 of `b5_bounds_rp.log`).

Headline numbers equal the stored ones in every printed digit: `b7_ift.log` (41 lines, no difference) gives n0 = e^89.75
and C7 = 2.8959e+29 = e^67.838; `b8m_lc.log` and `b8m_lc_lipcheck.log` give theta = 0.7355 (Perron root 0.7051);
`b5_bounds.log` and the scan give contraction 0.9519 (k = 12, rp = 0.14); `b5_jump.log` and `b5_jump_d0.log` and
`b5_label*.log` equal the stored logs line for line.

## Controls (27)

Each verdict is read from the log. `exit` is the process exit code (many controls exit 0 by design).

| control | exit | verdict in its log |
|---|---|---|
| `b8m_identities_rho2old`, `_q` | 1 | `SOME IDENTITY FAILS` (relative residuals 0.0038 to 1.07) |
| `b8m_numcheck_weight`, `_kernel`, `_tau` | 1 | `SOME CHECK FAILED` ((B) b 1.79 and c 1.86 against bound for weight, (C) +4.689 for kernel, (A) FAIL for tau) |
| `b5_system_epsCB`, `_theta`, `_t5`, `b5_formulas_res` | 0 | `some check must FAIL: caught` |
| `b5_numeric_offsol` | 0 | `GROWS: not O(eps/\|z\|)`, spread factor 3.69 (the unmutated run is bounded) |
| `b5_bounds_check_res`, `_jacP`, `b5_bounds_jac`, `_series` | 0 | `must FAIL: caught` |
| `b5_data_gauge` | 0 | `agreement with first_order_jet 1.8e+00 (< 1e-6): FAIL` |
| `b5_threshold_sum`, `b5_jump_sum`, `b5_label_Ct2`, `_scale` | 0 | `a check must FAIL: caught` |
| `b5_path_stokes` | 0 | `the bound must be violated: caught` |
| `b7_check_mutT`, `b7_ift_JD` | 0 | `MUTATION transpose` and `MUTATION JD`: caught |
| `b8m_lc_numcheck_mut` (rho2L), `_d0`, `_weight` | 0 | `a check must FAIL: caught` |
| `b8m_lcj_kernel`, `b8m_lcj_Om` | 0 | `the contraction must FAIL: caught` |

All 27 give their documented verdict. Each verdict line also equals the stored one (`b5_mutations.log`,
`b5_label_mutations.log`, `b8m_lc_numcheck_mut.log`, `b8m_identities_mut.log`, `b8m_numcheck_mut*.log`,
`b7_ift` and `b8m_lcj_mutations.log`).

## Comparison with the stored files (`compare_stored.txt`, made by `cmp882.py RAW WORKTREE`)

The comparator reads the stored file from `git show HEAD:solver/proof/<name>` of the worktree, removes timings, and
compares each line's text and then its numbers as printed. A stored log that holds several commands (`b5_mutations.log`,
`b5_label_mutations.log`, `b8m_lc_numcheck_mut.log`, `b8m_lcj_mutations.log`) is matched line by line to the closest new
line. JSON files are compared leaf by leaf, a ball string `[m +/- r]` by midpoint and radius. Structural, count and flag
differences: none.

| group | pairs | result |
|---|---|---|
| logs | 42 | 29 equal in every printed digit, 13 with a number that differs (below), 0 with different text |
| JSON (changed/) | 10 | 0 structural differences, all 112 balls overlap their stored balls (14, 26, 16, 28 and 28 in the five `b7_` files that hold balls) |
| appended scan and lc logs | 5 | the stored lines are a prefix of the new file, every new record has the same `closes` as its stored one |
| `b8m_lc_lip.json`, `b8m_lcj.json` | 2 | not changed by the run, so identical to the stored files byte for byte |

### The numbers that differ

| file | difference | size |
|---|---|---|
| `b8m_numcheck`, `_tau`, `_weight`, `_kernel` | floating-point (numpy, ODE) checks: line 1 `1.3e-14` against `5.8e-15`, the table of relative differences at the 1e-6 to 1e-4 level, the angle of the worst point of each ray | every verdict line and every PASS/FAIL equal |
| `b8m_scan_box` record L0 = 62 | the fixed-point iteration stops after 67 iterations, not 70 (relative change per step 1.2e-5); `hyp` V, S, b, c differ by up to 4.2e-7 | `closes` true in all four records, as stored |
| `b7_box`, `b7_point`, `b7_adjoint`, `b7_check`, `b7_adjoint_mutT` | ball radii (certified, from the Lohner steps) | radius ratio 0.995 to 1.002 (`b7_box.json`), 0.992 to 1.000 (`b7_adjoint.json`), 0.457 to 1.466 (the two `_point` files); `b7_box` midpoints agree to 40 digits, `b7_adjoint` to 6.7 digits (its radius is 6e-8); `b7_check` radii 3.4e18 against 3.6e18 (5.6%); all PASS |
| `b7_ift.json` | 457 of 1024 float leaves, worst relative difference 8.1e-8 | the log (41 lines) is identical |
| `b8m_lc` | 21 numbers, worst 2.1e-15 (20.139783666122348 against 20.139783666122305) | none printed differs |
| `b8m_lc_mut_rho2L` | a mutation's output, 9.1468e-07 against 9.1834e-07 (4.0e-3); the appended record's `diag.int_F` 8.7e-4 | `closes` equal, caught |
| `b8m_lc_numcheck` | the jump of the two continuations, 1.18e-20 against 1.40e-20 (a roundoff-level quantity), which is the only difference | every verdict `OK` |
| `b8m_lcj_Om` | the weight 0.02135935140664794 against 0.02135936024788961 (4.1e-7) | caught |
| `b5_bounds_k0.3_Z0.0085.json` | 39 float leaves, worst 4.4e-15 | none printed differs |
| `b5_label.json`, `b5_jump.json`, `b5_jump_d0_1e7.json` | 2, 3 and 3 float leaves, worst 2.6e-15, 3.7e-16 and 4.4e-16 | none printed differs |

### Differences of format, not of numbers

- The new records of `b8m_scan.py` carry a key `"d0": "0"` that the stored records lack (the stored logs predate it).
  The comparator removes it before comparing (`compare_stored.txt` says how many records).
- `b8m_h8_K4_L73.89_d0_1e7.log`: the script copies `b8m_h8_d0.log` over the stored file, and the stored file has one
  more line, `exit 0` (`diff_against_stored.txt` shows `1 -`). Its other 12 lines are equal.
- `b8m_numcheck_n1000_tau.npz` is a new file (the tau control writes it); the stored directory has none.
  `b8m_numcheck_n1000.npz` has the same size, different bytes.
- The appended logs `b8m_scan_K4_box.log` (+4 records), `b8m_scan_K4_d0_1e7.log`, `b8m_scan_K4_k0.85.log`,
  `b8m_lc_K4.log` and `b8m_lc_K4_mut_rho2L.log` (+1 each) are the stored files plus the Pi's records. The readers
  (`b8m_h8`, `b8m_numcheck`, `b8m_lc_numcheck`, `b8m_lcj`) take the last closing record, so the downstream steps
  used the Pi's records, and `b8m_lcj.json` and `b8m_lc_lip.json` came out identical to the stored ones.

## Files

`<name>.log` one per command (64); `exits_882.txt`; `env.txt`; `status_after.txt`, `diff_against_stored.txt`;
`changed/` (18 files); `compare_stored.txt` and `cmp882.py`; `run882.sh` (unedited, md5 9bea2d2c).
