# #1025 signtests of the delta table's older records at D 15-17 (win2b, 2026-11-20, from signtest_list.log and signtest_list_kc55.log)

Inputs by `git show` of choptuik-large-d-raw `origin/main` 35affed8 (no checkout), git hashes in `st/hashes.txt`; `signtest.py` blob a2f53a90, from solver/matter of D:/choptuik-i1025b (wip/ell1-highD 5c9d001c), venv-i962, 4 BLAS threads, one signtest at a time per chain (two chains), each capped at 7200 s by exact pid (no cap fired). The planted control printed agree, agree, DISAGREE (signtest.log, 08:15:50 UTC). Pass rule: agree true at both lambda and opposite signs at lambda - 0.02 and lambda + 0.02 (the record's lambda is the midpoint). The table is made by `signtest_table1025.py` (selftest: 4 planted cases).

| row (state) | D | k_c | lambda -0.02 / +0.02 | result | signs at lambda -0.02 | signs at lambda +0.02 | count < 1e-12 sigma_max (-/+) | count < 1e-15 (-/+) | reason |
|---|---|---|---|---|---|---|---|---|---|
| l1kc47Fr1025_D15.0000 | 15 | 47 | 2.39976 / 2.43976 | **pass** | [-1, -1, -1, -1] | [1, 1, 1, 1] | 34 / 34 | 10 / 10 | opposite signs, all four agree at both lambda |
| l1kc47Fr1025_D15.5000 | 15.5 | 47 | 2.31755 / 2.35755 | **pass** | [-1, -1, -1, -1] | [1, 1, 1, 1] | 36 / 36 | 16 / 16 | opposite signs, all four agree at both lambda |
| l1kc47Fr1025_D16.0000 | 16 | 47 | 2.22713 / 2.26713 | **pass** | [-1, -1, -1, -1] | [1, 1, 1, 1] | 38 / 38 | 22 / 22 | opposite signs, all four agree at both lambda |
| l1kc47Fp1025_D16.2500 | 16.25 | 47 | 2.17480 / 2.21480 | **pass** | [-1, -1, -1, -1] | [1, 1, 1, 1] | 38 / 38 | 22 / 22 | opposite signs, all four agree at both lambda |
| l1kc47Fr1025_D16.5000 | 16.5 | 47 | 2.13482 / 2.17482 | **pass** | [1, 1, 1, 1] | [-1, -1, -1, -1] | 38 / 38 | 24 / 22 | opposite signs, all four agree at both lambda |
| l1kc47Fq1025_D16.7500 | 16.75 | 47 | 2.08963 / 2.12963 | **pass** | [1, 1, 1, 1] | [-1, -1, -1, -1] | 40 / 40 | 23 / 24 | opposite signs, all four agree at both lambda |
| l1kc47Fr1025_D17.0000 | 17 | 47 | 2.01638 / 2.05638 | **FAIL** | [1, 1, 1, 1] | [-1, -1, -1, 1] | 40 / 40 | 24 / 24 | agree false at 2.05638 |
| l1kc55Fb1025_D16.5000 | 16.5 | 55 | 2.13912 / 2.17912 | **FAIL** | [1, 1, 1, 1] | [1, 1, 1, 1] | 46 / 46 | 34 / 32 | same sign at both lambda |
| l1kc55Fb1025_D16.0000 | 16 | 55 | 2.22263 / 2.26263 | **pass** | [-1, -1, -1, -1] | [1, 1, 1, 1] | 46 / 46 | 30 / 30 | opposite signs, all four agree at both lambda |
| l1kc55Fb1025_D15.5000 | 15.5 | 55 | 2.31879 / 2.35879 | **pass** | [-1, -1, -1, -1] | [1, 1, 1, 1] | 44 / 44 | 24 / 24 | opposite signs, all four agree at both lambda |
| l1kc55Fb1025_D15.0000 | 15 | 55 | 2.40101 / 2.44101 | **pass** | [-1, -1, -1, -1] | [1, 1, 1, 1] | 42 / 42 | 18 / 18 | opposite signs, all four agree at both lambda |

9 of 11 records pass.
