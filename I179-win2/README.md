# I179-win2: Python 3.14 venv, hp build and identity checks on win2

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/179 (the win2 part).

Interpreter: Python 3.14.10 (`C:\Users\nathan\Source\venv-t177`, installed in #177, install record in `../I177-win2/install_record.txt`).
Checkout: `D:\choptuik-large-d`, origin/main 188853c. Run at Normal priority, no affinity, all cores (coordinator, 2026-11-08).
Pass criteria (written before the run): `hp/build.sh` exits 0 and prints `hpkernel avx512 multidouble avx512`; the amplitude copy
hashes to fd6b5ef2f90d4f559a1a1ab68a7e85fe7c9b8538cc7e50ac41d2fb5510eb47d8; `highm_check.py ref`, `scaled` and `jets` exit 0 against
their stored files; `jets --mutate=kappa` exits non-zero; `check_numbers.py --selftest` is reported as it comes out.

## Results (2026-11-09 01:30 UTC)

Interpreter Python 3.14.10 (`venv-t177`), python-flint 0.9.0 with FLINT 3.6.0, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, mpmath
1.3.0, maturin 1.16.0 (added for the build), multidouble at git f092018 (`freeze_venv-t177_final.txt`; before the build
`freeze_venv-t177_before.txt`). Checkout `D:\choptuik-large-d` at origin/main 188853c.

- `hp/build.sh` as written (fat LTO, one codegen unit, `target-cpu=native`): exit 0, 2026-11-08 23:48:17 to 2026-11-09 01:11:26
  UTC (83 min; `build_times.txt`, `build.log`). Last line `hpkernel avx2 multidouble avx2` (the Core Ultra 7 265K has no AVX-512).
  Wheel `hpkernel-0.1.0-cp314-cp314-win_amd64.whl`, sha256 fd4dd0c4a33f553e66c0f02754f2f24bf15e34472ab297acf1dfd4faa6f42ced.
- `run_i179.sh` ran the five checks at once, one thread each (`exits.txt`):
  `check_numbers.py --selftest` exit 1 (1040 of 1043 pass, `formula_refit` 0 of 3; all 1043 reject a shifted value);
  `highm_check.py ref` exit 0, PASS 72 outputs bit-identical; `scaled` exit 0, PASS, its control (scale wrong at order 7,
  M = 192) fires; `jets` exit 0, PASS 28 outputs bit-identical; `jets --mutate=kappa` exit 1, FAIL 28 of 28 differ (the
  control fires).
- The amplitude copy (`amp_copy.json`, exit 0, 486 s, 1 process): canonical sha256 (timing keys dropped, I140-win2/compare.py)
  fd6b5ef2f90d4f559a1a1ab68a7e85fe7c9b8538cc7e50ac41d2fb5510eb47d8, equal to #161's. The control (the last digit of the last
  sigma changed) gives 4924553c, which differs.
- `refit_probe.py` (`formula_all.refit_distance()`): delta_fit_range 1.32e-09 (limit 1e-9), gamma_fit_range 2.52e-08 (limit
  1e-8), delta_80 9.60e-09 (window 0.5e-7 to 2e-7). These equal I179-win's 3.14 numbers with the OpenBLAS Haswell kernel forced
  (1.3e-9, 2.5e-8, 9.6e-9), and this CPU has AVX2 and no AVX-512, so its default OpenBLAS kernel is Haswell's.
