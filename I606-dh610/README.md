# I606-dh610: setup and bit checks of main's hp build (multishoot kernel) on dh610 (Fedora Linux 45, i7-12700)

Machine: dh610 (the former win3), Fedora Linux 45 Workstation (kernel 7.3.3), Intel Core i7-12700 (12 cores, 20
threads, AVX2 and FMA, no AVX-512), 62 GB. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/606

Code: choptuik-large-d main at a879ccc3. Toolchain: clang 23.1.5 (`CC`, `CXX` and the cargo linker), rustc 1.99.1,
maturin 1.16.0, Python 3.14.10, numpy 2.5.4 (scipy-openblas 0.3.34), python-flint 0.9.0 (FLINT 3.6.0); versions.txt.
The build was `hp/build.sh` after `pip uninstall multidouble` (it was not installed), as `nice -n 10`, under
`systemd-inhibit` and `/usr/bin/time -v`. The checks ran as five chains in parallel at nice 10 with two BLAS threads
each, from `checks606.sh`.

| file | what |
|---|---|
| build.log, build.time, build.start, build.end | `hp/build.sh` output, `/usr/bin/time -v` of it, wall-clock marks |
| build_mem.log | system memory used (MiB) and the largest rustc's RSS (kB) every 10 s, from 3.5 min into the build |
| versions.txt, import.log | package and toolchain versions, the import test |
| selftest.log | `check_numbers.py --selftest` |
| ref.log, scaled.log, jets.log, jets_mutate_kappa.log | `highm_check.py` against T81 and anm-mac references |
| bits.json, bits_perturb.json, bits_dump.log, bitsperturb_dump.log | `xsolve_bits.py dump` and `dump --perturb` |
| api.json, api_perturb.json, api_dump.log, apiperturb_dump.log | `api_bits.py dump` and `dump --perturb` |
| bits_vs_mac.log, bitsperturb_vs_mac.log, api_vs_mac.log, apiperturb_vs_mac.log | compares against I523-mac/c3 |
| bitsperturb_vs_own_unperturbed.log, apiperturb_vs_own_unperturbed.log | the controls: must differ |
| exits.txt, checks606.sh | exit status of each step, the script that ran them |

Results: build exit 0, 21 min 57 s, peak 24.1 GB resident. Imports pass. Selftest 1047 of 1049 (the two
`formula_refit` items, #183). ref 72, scaled and jets 28 bit-identical, `jets --mutate=kappa` fails 28 of 28.
xsolve_bits 21 of 21 and api_bits 176 of 176 byte-identical with the Mac's, perturbed and unperturbed; each
perturbed dump differs from its own unperturbed one (0 of 21, 21 of 176).
