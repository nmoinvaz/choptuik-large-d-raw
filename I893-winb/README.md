# I893-winb: Theorem B(1)'s certified constants reproduced on Windows x86-64

Machine: winb (Surface Laptop 4, Windows 11, i7-1185G7). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/893.
The commands are the coordinator's `run893.sh` (in this folder; placed md5 4c67a3e49412bc1a09b2958b31757434, mine
cbea0533427de7834250a0eaf69105aa, only its RAW path line changed): the 64 commands of proof/B8_constants.md 13,
B5_inner.md 10 and B_chain.md 11, run in Git Bash from `solver/proof/` of the worktree `choptuik-i893` at main 27a3f1cd
(after #885 and #887), one process at a time at below-normal priority, with the venv `venv-choptuik-314` (Python 3.14.10,
python-flint 0.9.0 with FLINT 3.6.0, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0; `env.txt`), `PYTHONUTF8=1`. The Mac's
`I887-mac` and the Pi's `I882-rpi5` are read from a separate worktree of raw main 7fab2b18. `exits_893.txt` has each run's
exit code and wall time (UTC); each command's output is `<name>.log`.

## Result

Started 02:01:36 UTC, finished 03:09:22 (1 h 8 min of wall time; the coordinator's estimate was 1.5 h, the Pi's run took
1 h 18 min). 64 commands: 35 `run` (all exit 0), 27 `ctrl` (5 exit 1 and 22 exit 0 by design, every verdict read from its
log in the tables below) and 2 `scan` (both exit 1 as documented). No traceback and no STOP line in any log. `env.txt`:
python-flint 0.9.0, FLINT 3.6.0, numpy 2.5.4, mpmath 1.3.0, scipy 1.18.1, Python 3.14.10, worktree commit 27a3f1cd.

The numbers of the issue, each printed value the same as the stored file's, the Mac's `I887-mac` and the Pi's `I882-rpi5`:

| number | log | Windows |
|---|---|---|
| B5 contraction | `b5_bounds.log`, `b5_label.log` | 0.9519 (lemma S: rp = 0.14, k = 12), certified True |
| n0 | `b7_ift.log` | e^89.75 (D = n + 2) |
| C7 | `b7_ift.log` | 2.8959e+29 = e^67.838 |
| theta | `b8m_lc.log`, `b8m_lc_lipcheck.log` | 0.7355 (Perron root 0.7051), below 1: True |
| lemma J's theta | `b8m_lcj.log` | 1.7593e-01, `(H-J): PROVED for these data` |

### Against `I887-mac` (current code) and the Pi's `I882-rpi5` (old code, from the stored files' time)

`stage893.py` puts this machine's outputs under the Mac's file names (for the five appended logs only the records this run
appended, the lines beyond the stored count), and the Mac's `compare_i885.py` then compares them with `I887-mac/`
(`compare_mac.txt`). The Pi's `changed/` files and logs went through the same steps (`compare_pi_mac.txt` has the Pi against
the Mac, `compare_pi.txt` this machine against the Pi). Largest relative difference of a number, wall times dropped:

| output | Windows against Mac | Pi against Mac |
|---|---|---|
| `b5_jump.json`, `b5_jump_d0_1e7.json` | 0 (every digit, the files agree) | 9.8e-15, 1.0e-14 |
| `b5_jump.log`, `b5_jump_d0_1e7.log`, `b5_jump_mut_sum.log`, `b5_threshold.log` | every line equal | every line equal |
| `b7_ift.log`, `b7_ift_mutJD.log` | every line equal (41 and 42 lines) | every line equal |
| `b7_ift.json` | 506 of 1024 leaves, worst 1.7e-05 (rows[58][3][1], the Krawczyk margin at ln n = 88.5) | 457 leaves, worst 8.1e-08 |
| `b8m_atoms_K4.log`, `b8m_h8_K4_L73.89.log`, `b8m_h8_K4_L73.89_d0_1e7.log` | equal (0) | 0, 3.9e-16, 5.1e-16 |
| `b8m_scan_K4_box.log` (4 records, L0 = 73.89, 70, 66, 62), `_d0_1e7.log`, `_k0.85.log` and their stdout | equal (0) | 1.7e-11, 5.0e-16, 1.0e-12 |
| `b8m_lc_K4.log` (record and stdout) | 8.3e-15 | 5.7e-15 |
| `b8m_lc_K4_mut_rho2L.log` (record and stdout) | 0 | 3.7e-16 |
| `b8m_lc_lip.json` | the same file, byte for byte (md5 0fa33bffad92) | 2.2e-11 on the 416 entries of 1e-60 or more, 515 of the 1184 below it move by more than 1e-9 (the Pi's file equals the stored one) |
| `b8m_lc_lipcheck.log`, `b8m_lcj.log`, `b8m_lcj.json`, `b8m_lcj_mut_kernel.log` | equal (0) | equal (0) |
| `b8m_lc_numcheck_n1e3.log`, `_mut.log`, `_mut_d0.log` | one number, the jump of the two continuations: 1.16e-20 against 1.40e-20 (0.17) | 1.18e-20 against 1.40e-20 (0.16) |

So on the current code the Windows outputs equal the Mac's in every number of the scan records, of the rho2L record and of
the logs of `b5_jump`, `b5_threshold`, `b7_ift`, `b8m_atoms`, `b8m_h8` and `b8m_lcj`, and `b5_jump.json`,
`b5_jump_d0_1e7.json` and `b8m_lc_lip.json` are the Mac's files (line ends aside). What differs is listed below, and it is
all of machine-dependent enclosures or roundoff-level quantities.

The Pi's values beside this machine's, the Mac's and the stored ones (`beside.txt`; the Mac did not rerun the `b7_adjoint`
files, and its `b7_ift.json` read the stored `b7_adjoint.json`):

| number | stored | Mac I887 | Pi I882 | Windows |
|---|---|---|---|---|
| `b5_jump.json` C_E | 2.5323658402810177e+33 | 2.5323658402809938e+33 | 2.5323658402810186e+33 | 2.5323658402809938e+33 |
| `b5_jump_d0_1e7.json` C_E | 2.5974924970901457e+33 | 2.597492497090121e+33 | 2.597492497090147e+33 | 2.597492497090121e+33 |
| `b7_ift.json` C7 | 2.8959328798616165e+29 | 2.8959328798615887e+29 | 2.895932865381755e+29 | 2.8959369547896803e+29 |
| `b7_ift.json` ln C7 | 67.83827499423884 | 67.83827499423883 | 67.83827498923877 | 67.83827640135888 |
| `b7_ift.json` margin at ln n = 88.5 | 7.530353428729857e-11 | 7.530353428729857e-11 | 7.530354035883073e-11 | 7.530227487805501e-11 |
| scan record L0 = 62, iterations | 70 | 67 | 67 | 67 |
| scan record L0 = 62, hyp V | 7158790.435892141 | 7158787.4429175025 | 7158787.442917511 | 7158787.4429175025 |
| `b8m_lc_numcheck` jump of the continuations | 1.40e-20 | 1.40e-20 | 1.18e-20 | 1.16e-20 |
| `b7_box.json` state radius | 8.3144e-09 | | 8.3365e-09 | 8.3347e-09 |
| `b7_adjoint.json` state radius | 6.2380e-08 | | 6.2360e-08 | 6.2430e-08 |
| `b7_adjoint.json` chi relative radius | 2.2963e-04 | | 2.2957e-04 | 2.3008e-04 |
| `b7_box_point.json` state radius | 1.7968e-16 | | 1.7809e-16 | 2.0358e-16 |
| `b7_adjoint_point.json` state radius | 9.0413e-12 | | 9.1542e-12 | 9.2082e-12 |
| `b7_adjoint_point.json` chi relative radius | 2.3977e-08 | | 2.2924e-08 | 2.4368e-08 |
| `b7_adjoint_point_mutT.json` chi relative radius | 1.3817e-08 | | 1.4937e-08 | 1.3578e-08 |

### Against the stored files (`compare_stored.txt`, the Pi's `cmp882.py`)

The Pi's `cmp882.py` run on this folder and the worktree gives the layout of the Pi's `compare_stored.txt`: 0 structural,
count or flag differences in the logs, the JSON files and the five appended logs (prefix intact, the `closes` of each new
record equal to its stored one). Logs with a number that differs from the stored line: `b8m_scan_box` (L0 = 62, 67
iterations against 70, as the Pi, and the lines equal the Mac's), `b8m_numcheck`, `_tau` (10 and 9 floating-point
lines, the angle of the worst point of a ray, worst 4.2e-01 and 4.3e-01; line 1 of `b8m_numcheck` is 5.8e-15 as stored,
the Pi's was 1.3e-14), `b7_box`, `b7_point`, `b7_check`, `b7_adjoint_mutT` (radii), `b8m_lc` (4.6e-15), `b8m_lc_mut_rho2L`
(4.0e-03, the last change of the fixed-point iteration), `b8m_lc_numcheck` (1.16e-20 against 1.40e-20) and
`b8m_lcj_Om` (the weight, 4.1e-07). `b7_adjoint.log`, `b7_ift.log` and `b7_ift_JD.log` have no number that differs (the
Pi's `b7_adjoint.log` differs from the stored in 7 lines, at 7.3e-15).

### Discrepancies (listed, not fixed)

- The scan record L0 = 62 of `b8m_scan_K4_box.log` stops after 67 iterations, the stored record after 70, and `hyp` V, S,
  b, c differ from it by up to 4.2e-07 (known, #885). The Mac's and the Pi's records have the same 67; this machine's equals
  the Mac's in every number.
- `b7_ift.json`: 506 of its 1024 float leaves differ from the stored file, worst 1.7e-05 (the margins before n0 are
  differences of quantities near 1e-10, and this run's `b7_adjoint.json` was made by this run with other enclosure radii).
  The log is equal line for line, n0 = e^89.75, C7 = 2.8959e+29, but ln C7 is 67.838276 against 67.838275.
- The ball radii of the `b7_adjoint.py` files differ from the stored ones. Ratio of this machine's radius to the stored
  one: `b7_box.json` 0.998 to 1.002 (the Pi's 0.995 to 1.002), `b7_adjoint.json` 1.000 to 1.005 (0.992 to 1.000),
  `b7_adjoint_point.json` and `b7_adjoint_point_mutT.json` 0.937 to 1.047 (0.629 to 1.466), `b7_box_point.json` 0.413 to
  3.740 (0.457 to 1.008); the state radius of `b7_box_point.json` is 2.04e-16 against the stored 1.80e-16 and the Pi's
  1.78e-16. Every ball overlaps its stored ball (14, 24, 16, 28 and 28 balls), the midpoints differ by at most 6.9e-46,
  3.6e-40, 0, 2.7e-08 and 2.7e-08 of the sum of the two radii, `b7_check` gives worst excess 0.00e+00 (PASS), and its
  printed radii differ from the stored lines by up to 9.1e-02.
- `b8m_lc_lip.json` differs from the stored file in 759 leaves, worst 2.7e-01 on an entry of 1e-70 (noise of a secant slope,
  below 1e-60; known for the current code, #885 and #887). It is the Mac's file byte for byte. The Pi's old code left it equal
  to the stored one, so it is not in the Pi's `status_after.txt` and is in this run's.
- The floating-point lines of `b8m_numcheck` (and `_tau`) and the jump of the two continuations in `b8m_lc_numcheck`
  (1.16e-20 against the stored and the Mac's 1.40e-20 and the Pi's 1.18e-20), which all give their verdicts as stored.
- Format only: the new scan records carry the key `"d0": "0"` that the stored records lack (known, #885);
  `b8m_h8_K4_L73.89_d0_1e7.log` is the script's copy of `b8m_h8_d0.log` and lacks the stored file's last line `exit 0`;
  `b8m_numcheck_n1000_tau.npz` is a new file and `b8m_numcheck_n1000.npz` has the same size and other bytes (as the Pi's).

## The B8 part (02:01:36 to 02:07:34 UTC)

Every run exits 0. The controls exit 1 and give their documented verdicts in their logs:

| run | kind | exit | wall (s) | verdict line (from its log) |
|---|---|---|---|---|
| b8m_model | run | 0 | 1 | M = 5: max abs(reduced - model) = 3.17e-49 OK; ALL OK |
| b8m_formal | run | 0 | 0 | decay exponents 3.985, 3.998 (expected 4); CHECKS OK |
| b8m_atoms | run | 0 | 0 | (the atoms' table) |
| b8m_identities | run | 0 | 1 | residuals at most 9.57e-79; ALL IDENTITIES HOLD |
| b8m_identities_rho2old | ctrl | 1 | 2 | I1 rho2 0.0132, I2 S-remainder 1.01, I3 0.139 FAIL; SOME IDENTITY FAILS |
| b8m_identities_q | ctrl | 1 | 1 | I2 q forms 0.151, I3 b-remainder 0.011 FAIL; SOME IDENTITY FAILS |
| b8m_scan_box | run | 0 | 118 | the four records L0 = 73.89, 70, 66, 62 (appended to `b8m_scan_K4_box.log` in the worktree) |
| b8m_h8 | run | 0 | 3 | (H8)(ii) with delta <= delta_ref: PROVED |
| b8m_numcheck | run | 0 | 115 | (A) OK; ALL CHECKS OK |
| b8m_numcheck_weight | ctrl | 1 | 1 | (B) weight rho^6: b 1.79e+00, c 1.86e+00 FAIL; SOME CHECK FAILED |
| b8m_numcheck_kernel | ctrl | 1 | 1 | (C) ... 4.689e+00 (must be <= 0) FAIL; SOME CHECK FAILED |
| b8m_numcheck_tau | ctrl | 1 | 114 | (A) FAIL; SOME CHECK FAILED |

## The B5 part (02:07:34 to 02:08:15 UTC)

Every run exits 0, and the two scans exit 1 as documented (`b5_bounds_scan`: certified False, contraction False at
the last Z = 0.0091, ln n0 >= 69.02; `b5_bounds_rp`: certified True, contraction False with rp = 0.15). The controls exit 0 by design
and give their documented verdicts in their logs (`MUTATION ...: caught`, or the check's FAIL):

| run | kind | exit | wall (s) | verdict line (from its log) |
|---|---|---|---|---|
| b5_system | run | 0 | 4 | Phi' formula worst relative difference 1.1e-50 (PASS); abs(z)^2/eps = 14.9 (PASS) |
| b5_system_epsCB | ctrl | 0 | 1 | MUTATION epsCB: some check must FAIL: caught |
| b5_system_theta | ctrl | 0 | 1 | MUTATION theta: some check must FAIL: caught |
| b5_system_t5 | ctrl | 0 | 1 | abs(z)^2/eps = 6.02e+28 (FAIL); MUTATION t5: caught |
| b5_formulas | run | 0 | 1 | res 9.16e-48 (PASS), tF 1.57e-46 (PASS) |
| b5_formulas_res | ctrl | 0 | 1 | MUTATION res: some check must FAIL: caught |
| b5_numeric_residual | run | 0 | 1 | spread of r_Phi over abs(z) <= 1e-3: factor 1.04 (bounded: O(eps/abs(z))) |
| b5_numeric_offsol | ctrl | 0 | 1 | factor 3.69 (GROWS: not O(eps/abs(z))) |
| b5_numeric_lip | run | 0 | 1 | largest entries F-1<-C+0 237, ... |
| b5_bounds | run | 0 | 2 | lemma S: rp = 0.14, k = 12, contraction 0.9519, ok True; certified True; contraction True; ln n0 >= 73.89 |
| b5_bounds_scan | scan | 1 | 2 | certified False; contraction False (the last Z = 0.0091, ln n0 >= 69.02) |
| b5_bounds_rp | scan | 1 | 2 | certified True; contraction False |
| b5_bounds_check | run | 0 | 1 | point checks: inner 0, res 0, jac 0, vt 0 -> PASS |
| b5_bounds_check_res | ctrl | 0 | 2 | res 0.359 -> FAIL; MUTATION res: the check must FAIL: caught |
| b5_bounds_check_jacP | ctrl | 0 | 1 | jac 0.888 -> FAIL; caught |
| b5_bounds_jac | ctrl | 0 | 2 | contraction: False; MUTATION jac: the run must FAIL: caught |
| b5_bounds_series | ctrl | 0 | 1 | contraction: False; MUTATION series: caught |
| b5_data | run | 0 | 1 | z-independence 4.7e-06, first_order_jet 8.0e-08: PASS |
| b5_data_gauge | ctrl | 0 | 1 | first_order_jet agreement 1.8e+00 (< 1e-6): FAIL; MUTATION gauge |
| b5_threshold | run | 0 | 1 | best on this grid: kappa1 = 0.85, ln n >= 104.68 |
| b5_threshold_sum | ctrl | 0 | 0 | MUTATION sum: the check must FAIL: caught |
| b5_path | run | 0 | 8 | max abs(W_C)/eps = 3.403, certified bound 8.231, ratio 4.13e-01: within |
| b5_path_stokes | ctrl | 0 | 2 | MUTATION stokes: the bound must be violated: caught |

B5's contraction 0.9519 is reproduced (`b5_bounds.log`, also in `b5_label.log`). The other numbers of the issue (n0 = e^89.75,
C7 = 2.8959e29, theta = 0.7355, lemma J's theta = 0.17593) come from the chain part below.

## The B chain part (02:08:15 to 03:09:22 UTC)

Every run exits 0, and the ten controls exit 0 by design. Each control's verdict is read from its log:

| run | kind | exit | wall (s) | verdict line (from its log) |
|---|---|---|---|---|
| b5_label | run | 0 | 1 | norm(R~(Z_L)) <= eps_L(0.0081) = 0.35269 (< 1: True); all ok: True |
| b5_label_check | run | 0 | 6 | certified eps_L dominates the numerical label variation: PASS |
| b5_label_Ct2 | ctrl | 0 | 5 | formula (J_F - G)/z vs jac_blocks: worst relative difference 7.16e-01 (FAIL); MUTATION Ct2: a check must FAIL: caught |
| b5_label_scale | ctrl | 0 | 6 | certified eps_L 0.0013 to 0.0030, dominates: FAIL; MUTATION scale: caught |
| b5_jump | run | 0 | 0 | C_E = 2.532366e+33 = e^76.9145; all checks: PASS |
| b5_jump_sum | ctrl | 0 | 0 | C_E = 1.555762e+33; MUTATION sum: the check must FAIL: caught |
| b8m_scan_d0 | run | 0 | 39 | one record, L0 = 73.89, d0 = 1e7, 32 iterations (appended to `b8m_scan_K4_d0_1e7.log`) |
| b8m_h8_d0 | run | 0 | 3 | (H8)(ii) with delta <= delta_ref: PROVED |
| b5_jump_d0 | run | 0 | 1 | C_E = 2.597492e+33 = e^76.9399; all checks: PASS |
| b8m_scan_k085 | run | 0 | 11 | one record, L0 = 104.68, kappa1 = 0.85, 8 iterations (appended to `b8m_scan_K4_k0.85.log`) |
| b7_box | run | 0 | 195 | steps [303, 322, 47], state radius at 0.3 8.33e-09 |
| b7_adjoint | run | 0 | 46 | 196 steps, state radius at 0.09 6.24e-08, chi relative radius 2.30e-04 |
| b7_point | run | 0 | 196 | steps [303, 322, 47], state radius 2.04e-16 |
| b7_adjoint_point | run | 0 | 46 | 196 steps, state radius at 0.09 9.21e-12, chi relative radius 2.44e-08 |
| b7_check | run | 0 | 743 | adjoint vs forward integration: worst relative excess 0.00e+00 (< 1e-6): PASS |
| b7_adjoint_mutT | run | 0 | 45 | the transposed adjoint, 196 steps, chi relative radius 1.36e-08 (read by the next control) |
| b7_check_mutT | ctrl | 0 | 733 | worst relative excess 5.56e+00 (< 1e-6): FAIL; MUTATION transpose: caught |
| b7_ift | run | 0 | 1 | for every n >= n0 = e^89.75: exactly one p_n in X, C7 = 2.8959e+29 = e^67.838 |
| b7_ift_JD | ctrl | 0 | 1 | Krawczyk False at every ln n of the scan, no n passes; MUTATION JD: caught |
| b8m_lc | run | 0 | 256 | Perron root (float) 0.7051; certified theta = 0.7355 (< 1: True) |
| b8m_lc_lipcheck | run | 0 | 0 | saved Lipschitz matrix b8m_lc_lip.json: certified theta = 0.7355 (< 1: True) |
| b8m_lc_mut_rho2L | run | 0 | 119 | writes the mutated record (34 iterations) for the control after it |
| b8m_lc_numcheck_mut | ctrl | 0 | 298 | (3) S.L 1.41e+10 ... FAIL; MUTATION rho2L of the LC certificate: a check must FAIL: caught |
| b8m_lc_numcheck | run | 0 | 298 | (1), (2), (3) OK; ALL CHECKS OK |
| b8m_lc_numcheck_d0 | ctrl | 0 | 298 | (2) d0 = 0.0000e+00 [MUTATION d0] FAIL; MUTATION d0: caught |
| b8m_lc_numcheck_weight | ctrl | 0 | 301 | (3) with weight rho^6: S.N0 2.05e+02, b.N0 1.84e+02, b.L 1.04e+02 ... FAIL; MUTATION weight: caught |
| b8m_lcj | run | 0 | 5 | theta = 1.7593e-01, theta0 = 5.8367e-05; (H-J): PROVED for these data |
| b8m_lcj_kernel | ctrl | 0 | 5 | theta = 1.2183e+30; MUTATION kernel: the contraction must FAIL: caught |
| b8m_lcj_Om | ctrl | 0 | 5 | theta = 2.8342e+02; MUTATION Om: the contraction must FAIL: caught |

The numbers the issue asks for come from this part: n0 = e^89.75 and C7 = 2.8959e+29 in `b7_ift.log`, theta = 0.7355 in
`b8m_lc.log`, lemma J's theta = 0.17593 in `b8m_lcj.log`.

## Files

`<name>.log` one per command (64); `exits_893.txt`, `env.txt`, `status_after.txt`, `diff_against_stored.txt`;
`changed/` (19 files, the Pi's 18 and `b8m_lc_lip.json`); `compare_stored.txt` (the Pi's `cmp882.py`), `compare_mac.txt`,
`compare_pi_mac.txt` and `compare_pi.txt` (the Mac's `compare_i885.py`, see above); `stage893.py` and `beside893.py`
(this runner's helpers, which stage the files under the Mac's names and print `beside.txt`); `run893.sh` (placed md5
4c67a3e4, only its RAW path line changed).
