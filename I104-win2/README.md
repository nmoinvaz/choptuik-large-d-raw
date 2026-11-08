# I104-win2: lemma 6a(5) on the sub-box 1e-18, reproduced on win2

Machine: win2 (Windows 11 Pro 10.0.26200, Intel Core Ultra 7 265K, 20 cores, AVX2, 95.6 GB RAM).
`python -c "import flint; print(flint.__version__)"`: 0.9.0 (venv choptuik-venv, Python 3.12.8, mpmath 1.3.0).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/104

Checkout: worktree `..\choptuik-i104` at origin/main 700da3a (contains 7a36683), run from `solver/proof/`.
The four commands of the issue run in order, 1 thread each (OMP/OPENBLAS/MKL threads 1), Normal priority, beside #82.
The chain stops if Krawczyk or export6a exits non-zero. `run_i104.sh` is the script that ran them, and
`exits.txt` has each command's exit code and wall time.

Results (exits in exits.txt, all 0):
- Krawczyk: K(X) in int X True, relative margins +1.000, +1.000, +0.980, +0.980, +0.932, +0.932 (as I103-macm3).
- export6a: A_M2_6a_M5_sub1e-18.json is byte-identical to I103-macm3's.
- lemma 6a: rho_6a = [0.2181093594 +/- 4.74e-11] < 1, ok; I103-macm3 has [0.2309898799 +/- 4.42e-13]. The balls are
  disjoint (a discrepancy, reported on #104). Lambda agrees ([0.4233267068 +/- 6.92e-12] against +/- 6.91e-12); max
  radius of B 3.36e-05 against 3.24e-05, |H| <= 67.8 against 73.0, G_slow^-1 <= 5.48 against 5.92.
- partial control: exit 0, "G_slow is 13 x 17: not square ... lemma 6a NOT established [MUTATION partial: failure
  expected]", as I103-macm3.
