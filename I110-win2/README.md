# I110-win2: lemma 6a(5) with the other machine's B

Machine: win2 (Windows 11 Pro, build 26300 after the 2026-11-08 04:29 UTC update restart; Intel Core Ultra 7 265K, 20
cores, AVX2). venv choptuik-venv (python-flint 0.9.0, mpmath 1.3.0, Python 3.12.8).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/110

Worktree `..\choptuik-i104` at origin/main 700da3a, run from `solver/proof/`, 1 thread, Normal priority.
`b_diff.py` is the entry-by-entry diff of two `--save-B` files (`--selftest` plants one changed digit and finds it).

Results:
- `lemma6a_loadB_macm3.log` (exit 0, 3 s): win2 with I103-macm3's B prints macm3's numbers. Max radius of B is
  3.24e-05, |H| <= 7.30e+01, G_slow^-1 <= 5.92e+00 and rho_6a = 2.310e-01 < 1, against win2's own 3.36e-05, 67.8, 5.48
  and 2.181e-01 (I104-win2). The command has no `--json`, so rho_6a is compared only at the 4 digits printed.
- `b_diff_win2_vs_macm3.log`: across the 760 balls of X and B (I104-win2's B against I103-macm3's), the midpoints are
  identical in every entry to all stored digits, and the radii differ in 748. The first difference is the radius of
  X[1][0]: 2.982435555e-11 on win2 against 2.982435582e-11 on macm3. The win2/macm3 radius ratios run from 0.840
  through 1.0017 (median) to 1.223. No ball pair is disjoint.
- `lemma6a_loadB_macm3.json` and `lemma6a_loadB_macm3_json.log` (the cross-load rerun with `--json`, exit 0, 2 s; the
  log is identical to the first cross-load's apart from the seconds): rho_6a = [0.2309898806 +/- 4.01e-11] against
  I103-macm3's [0.2309898799 +/- 4.42e-13]. The balls are **disjoint**, although B and the box are the same files.
  Lambda's radius differs too (6.92e-12 against 6.91e-12). H_max and Gslow_inv_max are equal as doubles. win2's
  python-flint 0.9.0 bundles FLINT 3.6.0 (`flint.__FLINT_VERSION__`); macm3's is not recorded.
