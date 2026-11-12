# I575-win3: setup of win3 and its hp build checked against the stored references

Machine: win3 (NATHAN-PC, Windows 11 Pro, i7-12700, 12 cores / 20 logical processors, 64 GB).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/575

Holds the logs of `hp/build.sh` and of the checks `check_numbers.py --selftest`, `highm_check.py ref`, `scaled`
and `jets` (with `--mutate=kappa`), one `.log` per command with its exit code on the last line.

| file | command (from the stated directory) | exit |
|---|---|---|
| build.log | `hp/build.sh` (venv, Rust 1.99.1, maturin 1.16.0), 07:21 to 08:16 UTC | 0 |
| versions.log | the import check, toolchain and package versions, checkout commit | 0 |
| check_numbers_selftest.log | `python check_numbers.py --selftest` | 1 (1046 of 1049; the three `formula_refit` items, #183) |
| formula_refit_values.log | `formula_all.refit_distance()` | 0 |
| highm_ref.log | `highm_check.py ref --compare=T81/ref_main.json --Ms=48,64,80` | 0 |
| highm_scaled.log | `highm_check.py scaled --compare=T81/scaled_main.json` | 0 |
| highm_jets.log | `highm_check.py jets --compare=anm-mac/jets_inputs/jets_inputs.json` | 0 |
| highm_jets_mutate_kappa.log | the same with `--mutate=kappa` (must fail) | 1, as required |
