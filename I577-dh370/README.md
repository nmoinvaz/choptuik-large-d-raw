# I577-dh370: setup and bit checks of the hp build on dh370 (Fedora Linux 45, i7-8700)

Machine: dh370, Fedora Linux 45 Workstation (kernel 7.2.11, glibc 2.44), Intel Core i7-8700 (6 cores, 12 threads,
AVX2 and FMA, no AVX-512), 31 GB. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/577

Code: choptuik-large-d main at 80b505688d21bfe6e47fbfc8b2ea59891e1ec5be. Build: `hp/build.sh` with clang 23.1.5 as
`cc` and the cargo linker (LLD 23.1.5), rustc 1.99.1, maturin 1.16.0, pyo3 0.30.1, multidouble crate 4.1.0,
Python 3.14.10, numpy 2.5.4 (scipy-openblas 0.3.34, Haswell), python-flint 0.9.0 (FLINT 3.6.0). `hpkernel.isa()` and
`multidouble.isa()` both print `avx2`.

## Contents

| file | command (from `hp/` for the highm_check ones) | exit | last line |
|---|---|---|---|
| selftest.log | `check_numbers.py --selftest` before hpkernel was built | 1 | `ModuleNotFoundError: No module named 'hpkernel'` (the `hopf_law` check imports it) |
| build.log | `hp/build.sh` (nice 10, CARGO_BUILD_JOBS=8) | 0 | `hpkernel avx2 multidouble avx2` |
| selftest2.log | `check_numbers.py --selftest` after the build | 1 | `1047 of 1049 checks pass`, `1049 of 1049 checks reject a value shifted by one unit` |
| ref.log | `highm_check.py ref --compare=RAW/T81/ref_main.json --Ms=48,64,80` | 0 | `PASS: 72 outputs bit-identical` |
| scaled.log | `highm_check.py scaled --compare=RAW/T81/scaled_main.json` | 0 | `PASS`, control fires |
| jets.log | `highm_check.py jets --compare=RAW/anm-mac/jets_inputs/jets_inputs.json` | 0 | `PASS: 28 outputs bit-identical` |
| jets_mutate_kappa.log | the same with `--mutate=kappa` | 1 | `FAIL: 28 of 28 outputs differ` (the control fires, as required) |

A first `hp/build.sh` linked with gcc was stopped (exit 143, not kept) when Nathan made clang the default compiler.
The machine was suspended for about 8 hours during the first build, which is why the wall time of build.log is long.

## Discrepancies

- selftest2.log, group `formula_refit`, 1 of 3 pass. The first failing value is "refit within 1e-9 of the stored Delta
  on 4-30.2 (1 = yes)": computed 0.0, quoted 1. The second is "refit - stored Delta(80) between 0.5e-7 and 2e-7 in
  size (1 = yes)": computed 0.0, quoted 1. This is the BLAS-dependent item of issue 183.
- jets.log: the M = 32 input resampled on this machine has sha a0c329b2dbe896e9, the reference's is 710ec9904d60d5ac
  (DIFFERENT). M = 48 and 64 are the same. The check runs on the stored input, so its 28 outputs are unaffected.
