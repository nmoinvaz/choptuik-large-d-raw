# I893-winb: Theorem B(1)'s certified constants reproduced on Windows x86-64

Machine: winb (Surface Laptop 4, Windows 11, i7-1185G7). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/893.
The commands are the coordinator's `run893.sh` (in this folder; placed md5 4c67a3e49412bc1a09b2958b31757434, mine
cbea0533427de7834250a0eaf69105aa, only its RAW path line changed): the 64 commands of proof/B8_constants.md 13,
B5_inner.md 10 and B_chain.md 11, run in Git Bash from `solver/proof/` of the worktree `choptuik-i893` at main 27a3f1cd
(after #885 and #887), one process at a time at below-normal priority, with the venv `venv-choptuik-314` (Python 3.14.10,
python-flint 0.9.0 with FLINT 3.6.0, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0; `env.txt`), `PYTHONUTF8=1`. The Mac's
`I887-mac` and the Pi's `I882-rpi5` are read from a separate worktree of raw main 7fab2b18. `exits_893.txt` has each run's
exit code and wall time (UTC); each command's output is `<name>.log`.

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
| b8m_numcheck_weight | ctrl | 1 | 1 | (C) Lemma K on the arc ... OK, SOME CHECK FAILED |
| b8m_numcheck_kernel | ctrl | 1 | 1 | (C) ... 4.689e+00 (must be <= 0) FAIL; SOME CHECK FAILED |
| b8m_numcheck_tau | ctrl | 1 | 114 | (A) FAIL; SOME CHECK FAILED |

## The B5 part (02:07:34 to 02:08:15 UTC)

Every run exits 0, and the two scans exit 1 as documented (`b5_bounds_scan`: certified False, contraction False at
Z = 0.009, ln n0 >= 69.02; `b5_bounds_rp`: certified True, contraction False with rp = 0.15). The controls exit 0 by design
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
| b5_bounds_scan | scan | 1 | 2 | certified False; contraction False (Z = 0.009, ln n0 >= 69.02) |
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

(the B chain follows)
