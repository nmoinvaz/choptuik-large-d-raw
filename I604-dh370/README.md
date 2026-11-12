# I604-dh370: the new hp kernel (multishoot 1.2.1, #523) built and checked on dh370 (Fedora Linux 45, AVX2)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/604
Code: choptuik-large-d main at e835d9469626943b184d830cee00ffbd257dd4d8 (1658a4f is an ancestor), a worktree with its own
venv, so no multidouble was installed before the build. Toolchain: clang 23.1.5 (`cc`, `c++` and the cargo linker),
rustc 1.99.1, maturin 1.16.0, Python 3.14.10, python-flint 0.9.0 (FLINT 3.6.0). `hpkernel.isa()` and `multidouble.isa()`
print `avx2`. The multidouble Python package (commit f092018) came from pip's wheel cache.

Build: `hp/build.sh` took 1873 s (31 min), exit 0, with a peak of 23498 MiB in its cgroup (limit 26 GB, swap peak 5.4 MiB).

## Files

| file | command (from `hp/` of the worktree; RAW is the raw clone) | exit | last line |
|---|---|---|---|
| build.log, build604.sh | `hp/build.sh` in a systemd scope | 0 | `hpkernel avx2 multidouble avx2` |
| ref.log | `highm_check.py ref --compare=RAW/T81/ref_main.json --Ms=48,64,80` | 0 | `PASS: 72 outputs bit-identical` |
| scaled.log | `highm_check.py scaled --compare=RAW/T81/scaled_main.json` | 0 | `PASS` |
| jets.log | `highm_check.py jets --compare=RAW/anm-mac/jets_inputs/jets_inputs.json` | 0 | `PASS: 28 outputs bit-identical` |
| jets_mutate_kappa.log | the same with `--mutate=kappa` | 1 | `FAIL: 28 of 28 outputs differ` (the control fires) |
| bits_dump.log, bits.json | `xsolve_bits.py dump RAW bits.json` | 0 | |
| bits_vs_mac.log | `xsolve_bits.py compare RAW/I523-mac/c3/bits.json bits.json` | 0 | `21 of 21 outputs byte-identical` |
| bitsperturb_dump.log, bits_perturb.json | the dump with `--perturb` | 0 | |
| bitsperturb_vs_mac.log | compare with `RAW/I523-mac/c3/bits_perturb.json` | 0 | `21 of 21 outputs byte-identical` |
| bitsperturb_control.log | compare `bits.json` with `bits_perturb.json` | 1 | `0 of 21 outputs byte-identical` (the control fires) |
| api_dump.log, api.json | `RAW/I523-mac/api_bits.py dump WT/hp RAW api.json` (571 s) | 0 | |
| api_vs_mac.log | compare with `RAW/I523-mac/c3/api.json` | 1 | `175 of 176 outputs byte-identical`, the one difference is `jacobian_f64/mut1` |
| apiperturb_dump.log, api_perturb.json | the dump with `--perturb` | 0 | |
| apiperturb_vs_mac.log | compare with `RAW/I523-mac/c3/api_perturb.json` | 1 | `175 of 176 outputs byte-identical`, the same output |
| apiperturb_control.log | compare `api.json` with `api_perturb.json` | 1 | `21 of 176 outputs byte-identical` (the control fires) |
| api_bits_nan1.py | `api_bits.py` with every NaN hashed as one pattern (#600's reading) | | |
| api_nan1_dump.log, api_nan1.json | `api_bits_nan1.py dump WT/hp RAW api_nan1.json` | 0 | replaced 45414 NaN, all `fff8000000000000` |
| api_nan1_vs_mac.log | compare with `RAW/I523-mac/c3/api.json` | 0 | `176 of 176 outputs byte-identical` |
| apiperturb_nan1_dump.log, api_perturb_nan1.json | the same with `--perturb` | 0 | replaced 45414 NaN, all `fff8000000000000` |
| apiperturb_nan1_vs_mac.log | compare with `RAW/I523-mac/c3/api_perturb.json` | 0 | `176 of 176 outputs byte-identical` |
| apiperturb_nan1_control.log | compare `api_nan1.json` with `api_perturb_nan1.json` | 1 | `21 of 176 outputs byte-identical` (the control fires) |
| checks604.sh, nan604.sh | the drivers that ran the steps above, five chains in parallel at nice 10 | | |

The one difference of the plain `api_bits` compare is `jacobian_f64/mut1` of `anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz`,
a mutation control whose Jacobian holds 45414 NaN. x86 writes them as 0xFFF8000000000000, the Mac (arm64) as
0x7FF8000000000000. With each NaN set to 0x7FF8000000000000 before hashing, all 176 hashes equal the Mac's.
