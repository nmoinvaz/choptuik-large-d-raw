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

(the B5 part and the B chain follow)
