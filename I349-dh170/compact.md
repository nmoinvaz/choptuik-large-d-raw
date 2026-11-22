### Whole README

| id | command | from | exit | files | number printed vs quoted | wall | verdict |
|---|---|---|---|---|---|---|---|
| files_named | `every file name in a code span` | . | 0 | none named | none quoted | 0 s | FAIL: 119 file names in code spans: 89 exist as written, 28 found elsewhere in the repository or the raw clone, 1 patterns, 1 not found / I200-mac... |

### Main results

| id | command | from | exit | files | number printed vs quoted | wall | verdict |
|---|---|---|---|---|---|---|---|
| largeD_formal_check | `solver/largeD_formal_check.py` | . | 0 | none named | none quoted | 39 s | OK |
| largeD_transport_sympy | `solver/largeD_transport_sympy.py` | . | 0 | none named | none quoted | 18 s | OK |
| heat_form | `solver/inner_pert/heat_form.py` | . | 0 | none named | none quoted | 2 s | OK |
| fixed_point | `fixed_point.py` | . |  | none named | none quoted |  | NOT RUN: named as the code of certified lemmas; the README quotes no invocation and no number (PROOF.md and proof/A_certify.md hold the commands: out... |
| fixed_point_M | `fixed_point_M.py` | . |  | none named | none quoted |  | NOT RUN: named as the code of certified lemmas; the README quotes no invocation and no number (PROOF.md and proof/A_certify.md hold the commands: out... |
| validated_int | `validated_int.py` | . |  | none named | none quoted |  | NOT RUN: named as the code of certified lemmas; the README quotes no invocation and no number (PROOF.md and proof/A_certify.md hold the commands: out... |
| krawczyk | `krawczyk.py` | . |  | none named | none quoted |  | NOT RUN: named as the code of certified lemmas; the README quotes no invocation and no number (PROOF.md and proof/A_certify.md hold the commands: out... |
| fast_eigenvalues | `solver/proof/fast_eigenvalues.py` | . | 0 | none named | none quoted | 3 s | OK |

### Results

| id | command | from | exit | files | number printed vs quoted | wall | verdict |
|---|---|---|---|---|---|---|---|
| plot_delta | `cd solver/data && python3 ../plot_delta.py --raw ../../../choptuik-large-d-raw` | solver/data | 0 | all exist | none quoted | 4 s | OK; the regenerated file differs from the committed one: solver/delta.svg |
| plot_echo | `hp/plot_echo.py` | hp | 2 | all exist | none quoted | 4 s | FAIL: exit 2. Adapted `python3 plot_echo.py ../../choptuik-large-d-raw` from hp/: exit 0, OK |
| formula_all | `solver/formula_all.py` | solver/data | 1 | all exist | D = 4: 0/2 MISMATCH | 2 s | FAIL: exit 1; D = 4: not printed: 3.4454524 (nearest printed 2, 0 digits agree); 0.3739610 (nearest printed 0.500000, 0 digits agree). Adapted `python3 ../formula_all.py` from solver/data/: exit 0, OK (one-line patch in a scratch copy) |
| rational_fit | `solver/rational_fit.py` | solver | 1 | none named | none quoted | 5 s | FAIL: exit 1. Adapted `python3 ../rational_fit.py` from solver/data/: exit 0, OK |
| formula_refit | `python3 ../formula_all.py --refit` | solver/data | 1 | none named | none quoted | 2 s | FAIL: exit 1. Adapted `python3 ../formula_all.py --refit` from solver/data/: exit 0, OK (one-line patch in a scratch copy) |
| formula_cut_fit | `hp/formula_cut_fit.py` | . | 0 | all exist | limit: 1/1 | 62 s | OK |
| formula_cut | `hp/formula_cut.py` | hp | 1 | none named | none quoted | 95 s | FAIL: exit 1 |
| lowD_max | `cd hp && python3 lowD_max.py` | hp | 0 | all exist | maximum: 2/2 | 1 s | OK |
| export_lowD | `hp/export_lowD.py` | . | 0 | none named | none quoted | 1 s | OK |
| export_dd | `hp/export_dd.py` | . | 0 | none named | none quoted | 1 s | OK |
| plot_lowD_values | `hp/plot_lowD_values.py` | . | 0 | all exist | none quoted | 5 s | OK |
| lowD_formula | `hp/lowD_formula.py` | hp | 1 | none named | delta poly: 0/9 MISMATCH; gamma poly: 0/7 MISMATCH | 4 s | FAIL: exit 1; delta poly: not printed: 1.752403 (nearest printed 2, 0 digits agree); 2.486429 (nearest printed 2, 1 digits agree); 8.257623 (neare.... Adapted `python3 lowD_formula.py ../ecc` from hp/: exit 0, OK |
| plot_lowD_limits | `hp/plot_lowD_limits.py` | . | 0 | all exist | none quoted | 5 s | OK; the regenerated file differs from the committed one: hp/lowD_limits.svg |
| plot_lowD_logslope | `hp/plot_lowD_logslope.py` | . | 0 | all exist | none quoted | 4 s | OK; the regenerated file differs from the committed one: hp/lowD_logslope.svg |
| lowD_logslope | `hp/lowD_logslope.py` | . | 0 | none named | prediction: 2/2 | 3 s | OK |
| gamma_dd | `hp/gamma_dd.py` | . | 1 | all exist | none quoted | 1 s | FAIL: exit 1 (existing build) |
| gamma_m48_gap | `hp/gamma_m48_gap.py` | . | 1 | none named | none quoted | 1 s | FAIL: exit 1 (existing build) |
| gamma_compare | `cd hp && python3 gamma_compare.py data/gamma_dd.jsonl data/local/gamma_dd.jsonl` | hp | 0 | all exist | lambda-2 by powers: 5/6 MISMATCH; lambda a1: 1/1; gamma a1 = lambda a1 / 4 (derived): 1/1; lambda a2 (not printed by this script): not checked | 1 s | FAIL: lambda-2 by powers: not printed: 2.2×10⁻⁶ (nearest printed 0.0000021, 1 digits agree) (existing build) |
| plot_extrapolation | `solver/plot_extrapolation.py` | solver | 1 | all exist | none quoted | 21 s | FAIL: exit 1. Adapted `python3 ../plot_extrapolation.py` from solver/data/: exit 0, OK |
| export_delta_all | `cd hp && python3 export_delta_all.py ../../choptuik-large-d-raw` | hp | 0 | all exist | none quoted | 4 s | OK; the regenerated file differs from the committed one: hp/data/delta_all.csv |
| export_delta_all_verify | `--verify` | hp | 1 | none named | none quoted | 48 s | FAIL: exit 1 |
| values_table | `cd hp && python3 values_table.py` | hp | 0 | none named | D = 4: 2/2; gamma(70): 1/1; gamma(100): 1/1; gamma(1000): 1/1 | 3 s | OK |
| track_c | `hp/track_c.py` | hp | 1 | none named | series: 0/6 MISMATCH; limit: 0/2 MISMATCH | 3 s | FAIL: exit 1; series: not printed: 1.684955205950 (nearest printed 2, 1 digits agree); 8.1×10⁻¹¹ (nearest printed -, 0 digits agree); 1.6781710154.... Adapted `python3 track_c.py real` from hp/: exit 0, OK |
| plot_physics | `solver/plot_physics.py` | . | 0 | all exist | none quoted | 2 s | OK; the regenerated file differs from the committed one: solver/physics.svg |
| modecount_test | `hp/modecount_test.py` | . | 1 | none named | none quoted | 1 s | FAIL: exit 1 (existing build) |
| dd_D5 | `hp/compare/dd_D5.py` | . | 0 | all exist | D = 5: 2/2 | 246 s | OK (existing build) |
| data_all | `solver/data_all.py` | solver | 1 | none named | D = 5 f64: 0/1 MISMATCH | 19 s | FAIL: exit 1; D = 5 f64: not printed: 3.221701945 (nearest printed 2, 0 digits agree). Adapted `python3 ../data_all.py` from solver/data/: exit 0, OK |
| cmp_ecker | `hp/compare/cmp_ecker.py` | hp/compare | 1 | none named | moves: 0/1 MISMATCH; offset: 0/2 MISMATCH | 1 s | FAIL: exit 1; moves: not printed: -1.66×10⁻⁴ (nearest printed -, 0 digits agree); offset: not printed: 2.7×10⁻⁷ (nearest printed -, 0 digits agree.... Adapted `python3 cmp_ecker.py ../ecc` from hp/compare/: exit 0, OK |
| identity_check | `I200-mac/identity_check.py` | . | 0 | all exist | none quoted | 7 s | OK |
| eeg20 | `solver/eeg20/` | . | 0 | none named | ratio: 2/2 | 3 s | OK (existing build) |
| tilt | `solver/eeg20/` | . | 0 | none named | measured/predicted at x = 1 (derived): 4/4 | 2 s | OK (existing build) |
| maxc | `solver/eeg20/` | . | 0 | none named | ratio: 2/2 | 3 s | OK (existing build) |

### How the points are computed

| id | command | from | exit | files | number printed vs quoted | wall | verdict |
|---|---|---|---|---|---|---|---|
| plot_solver_limits | `hp/plot_solver_limits.py` | hp | 2 | all exist | none quoted | 3 s | FAIL: exit 2. Adapted `python3 plot_solver_limits.py ../../choptuik-large-d-raw` from hp/: exit 0, OK |

### Validation and controls

| id | command | from | exit | files | number printed vs quoted | wall | verdict |
|---|---|---|---|---|---|---|---|
| rv2_noise | `hp/review/rv2_noise.py` | . | 0 | none named | rms: 1/1 | 4 s | OK |
| dd_fits_clean | `hp/dd_fits_mp.py --clean` | . | 0 | none named | dropped: 1/1 | 335 s | OK |
| dd_fits_10_45 | `hp/dd_fits_mp.py 10 45 --clean --dmax=60.1` | . | 0 | none named | 1/D, degree 16: 3/3; 1/D, degree 18: 3/3; 1/(D-2), degree 18: 3/3; (D-2)^{-1/2}, degree 20: 3/3; D^{-1/2}, degree 20: 3/3 | 106 s | OK |
| dd_fits_10_375 | `10 37.5 --clean --dmax=60.1` | . | 0 | none named | 1/D, degree 16: 1/1; 1/D, degree 18: 1/1; 1/(D-2), degree 18: 1/1; (D-2)^{-1/2}, degree 20: 1/1; D^{-1/2}, degree 20: 1/1 | 119 s | OK |
| dd_fits_mixed | `hp/dd_fits_mp.py 10 45 --clean --mixed --dmax=60.1` | . | 0 | none named | coefficient: 2/2; limits: 2/2 | 58 s | OK |
| dd_fits_1e9 | `hp/dd_fits_mp.py 10 1e9 --clean --dmax=60.1` | . | 0 | none named | limits: 2/2 | 344 s | OK |
| dinf_budget | `hp/dinf_budget.py` | . | 0 | none named | range: 3/3 | 214 s | OK |
| planted_dinf | `hp/planted_dinf.py` | hp | 1 | all exist | centre: 0/2 MISMATCH | 2382 s | FAIL: centre: not printed: 0.79×10⁻⁸ (nearest printed 8.4e-9, 0 digits agree); 0.88×10⁻⁸ (nearest printed 8.55e-9, 1 digits agree) [inside range True in 6 of 6, junk caught False in 6 of 6 (README: all six; every case)] [composite log, see Prioritised fixes] |
| rv2_planted | `hp/review/rv2_planted.py` | . | 0 | none named | offset: 1/1 | 13 s | OK |

### Large D: what the 1/D expansion can and cannot see

| id | command | from | exit | files | number printed vs quoted | wall | verdict |
|---|---|---|---|---|---|---|---|
| largeD_scaling | `hp/largeD_scaling.py` | . | 0 | none named | none quoted | 2 s | OK (existing build) |
| largeD_F | `hp/largeD_F.py` | . | 0 | none named | D = 20: 5/5; D = 30: 5/5; D = 40: 5/5; D = 50: 5/5; D = 60: 5/5 | 3 s | OK (existing build) |
| plot_wave_family | `hp/plot_wave_family.py` | . | 2 | all exist | none quoted | 1 s | FAIL: exit 2. Adapted `python3 plot_wave_family.py ../../choptuik-large-d-raw` from hp/: exit 0, OK (existing build) |
| largeD_expand | `largeD_expand.py 4` | . | 0 | none named | none quoted | 584 s | OK |
| largeD_fast_transport | `solver/largeD_fast_transport.py` | . | 0 | none named | no gravity: 5/5; with gravity: 5/5 | 36 s | OK |
| largeD_fast_transport_full | `solver/largeD_fast_transport_full.py` | . | 0 | none named | full background: 5/5 | 24 s | OK |
| largeD_exponent | `hp/largeD_exponent.py` | . | 0 | none named | n<G(1)>/2: 5/5; <F^2>: 5/5; shift: 5/5 | 2 s | OK (existing build) |
| plot_light_cone | `hp/plot_light_cone.py` | . | 0 | all exist | none quoted | 1 s | OK |
| largeD_linear_late | `solver/largeD_linear_late.py` | . | 0 | none named | 1/\\sqrt2: 4/4; 0\.8: 4/4; 0\.9: 4/4 | 2 s | OK |
| largeD_dingle_K | `solver/largeD_dingle_K.py` | . | 0 | none named | K ratio: 10/10 | 2 s | OK |
| largeD_linear_poles | `solver/largeD_linear_poles.py` | . | 0 | none named | none quoted | 59 s | OK |
| largeD_linear_poisson | `solver/largeD_linear_poisson.py` | . | -15 | none named | none quoted | 1810 s | NOT RUN: not finished in 30 min (stopped by pid 1352830) |
| euler_late | `solver/largeD_prop4/` | . | 0 | none named | none quoted | 85 s | OK |
| kcheck | `kcheck.py` | solver/largeD_prop4 | 0 | none named | deviation c0: 2/2 | 17 s | OK [1 + c/k: c = 3.652, 3.651, 3.651 (README 3.65)] |
| switch2 | `switch2.py` | . | 0 | none named | singulant: 1/1 | 1 s | OK |
| largeD_linear_truncation | `solver/largeD_linear_truncation.py` | . | 0 | none named | x = 0.9: 4/4 | 1 s | OK |
| hier_schur | `hier.py --schur` | solver/inner_stokes | 1 | none named | none quoted | 3 s | FAIL: exit 1 |
| largeD_stokes_C | `solver/largeD_stokes_C.py` | . | 0 | none named | ratios: 2/2; n(ratio-1): 2/2; |s^2| (derived, not printed): not checked | 1 s | OK |
| largeD_inner | `solver/largeD_inner.py` | . | 0 | none named | none quoted | 1 s | OK |
| amp_series | `amp_series.py` | . | 0 | none named | agreement: 2/2 | 5 s | OK |
| largeD_Fratios | `hp/largeD_Fratios.py` | . | 0 | none named | ratios (|F5/F1| derived as |F3/F1||F5/F3|): 6/6 | 4 s | OK (existing build) |
| amp_flint_par | `solver/inner_amp/amp_flint_par.py --fit phys` | solver/inner_amp | 1 | all exist | none quoted | 1 s | FAIL: exit 1 |
| zero_selection | `zero_selection.py` | . | 0 | none named | none quoted | 1 s | OK |
| arg_crossing | `arg_crossing.py` | solver/inner_amp | 1 | none named | none quoted | 3 s | FAIL: exit 1. Adapted `python3 arg_crossing.py scan13b` from solver/inner_amp/: exit 0, OK |
| amp_flint | `amp_flint.py` | . |  | none named | none quoted |  | NOT RUN: named as the legacy basis; no invocation or number quoted, and it is the serial reference (AGENTS.md: hours) |
| harm_pred | `harm_pred.py` | . | 0 | none named | tracks: 10/10 | 643 s | OK |
| plot_selection | `solver/plot_selection.py` | . | 0 | all exist | none quoted | 11 s | OK |
| plot_spectrum | `solver/plot_spectrum.py` | . | 0 | all exist | none quoted | 15 s | OK; the regenerated file differs from the committed one: solver/spectrum.svg |
| expand_pert | `solver/inner_pert/expand_pert.py` | . | 0 | none named | none quoted | 16 s | OK |
| pert_check | `pert_check.py` | . | 0 | none named | residual: 1/1 | 1 s | OK |
| pert_check2 | `pert_check2.py` | . | 0 | none named | residual: 1/1 | 1 s | OK |
| rw_map | `solver/inner_pert/rw_map.py` | . | 0 | none named | none quoted | 2 s | OK |
| pert_check3 | `solver/inner_pert/pert_check3.py 45 11` | . | 0 | none named | misses: 1/1 | 3 s | FAIL: worst deviation 2.1e-178 against 10^-180 (j = 1: 1.3e-180; 2 of 11 j round to 10^-180) |
| plot_first_order | `solver/plot_first_order.py` | . | 0 | all exist | none quoted | 3 s | OK; the regenerated file differs from the committed one: solver/first_order.svg |
| struct_css | `solver/matter/struct_*.py` | . | 0 | none named | none quoted | 4 s | OK |
| struct_inner | `solver/matter/struct_*.py` | . | 0 | none named | none quoted | 10 s | OK |
| struct_outer | `solver/matter/struct_*.py` | . | 0 | none named | none quoted | 45 s | OK |
| struct_symmetry | `solver/matter/struct_*.py` | . | 0 | none named | none quoted | 227 s | OK |
| struct_eqs | `solver/matter/struct_*.py` | . | 0 | none named | none quoted | 376 s | OK |
| plot_matter | `solver/plot_matter.py` | . | 0 | all exist | none quoted | 3 s | OK |

### Limits and open problems

| id | command | from | exit | files | number printed vs quoted | wall | verdict |
|---|---|---|---|---|---|---|---|
| singularity_type | `hp/singularity_type.py planted` | hp | 1 | none named | sqrt exponent: 1/1 | 49 s | FAIL: exit 1 |
| track_c_fold | `hp/track_c_fold.py` | hp | 1 | all exist | none quoted | 1 s | FAIL: exit 1. Adapted `python3 track_c_fold.py run` from hp/: exit 0, OK |
| horizon_toy | `hp/horizon_toy.py` | . | 0 | none named | none quoted | 1 s | OK |
| plot_dropoffs | `hp/plot_dropoffs.py` | hp | 1 | all exist | none quoted | 4 s | FAIL: exit 1. Adapted `python3 plot_dropoffs.py ../../choptuik-large-d-raw/T76` from hp/: exit 0, OK |
| plot_gamma | `solver/plot_gamma.py` | . | 0 | all exist | none quoted | 3 s | OK; the regenerated file differs from the committed one: solver/gamma.svg |
| plot_modecount | `hp/plot_modecount.py` | . | 0 | all exist | none quoted | 3 s | OK; the regenerated file differs from the committed one: hp/modecount.svg |

### How this work was done

| id | command | from | exit | files | number printed vs quoted | wall | verdict |
|---|---|---|---|---|---|---|---|
| mutation_controls | `solver/proof/mutation_controls.py` | . | 0 | none named | eight versions: 1/1 | 1 s | OK |
| check_numbers_selftest | `check_numbers.py` | . | 1 | none named | none quoted | 23 s | FAIL: exit 1 (existing build) |
| check_numbers | `check_numbers.py` | . | 1 | none named | none quoted | 29 s | FAIL: exit 1 (existing build) |

### Reproduce

| id | command | from | exit | files | number printed vs quoted | wall | verdict |
|---|---|---|---|---|---|---|---|
| reproduce_sh | `./reproduce.sh` | . | 1 | none named | none quoted | 1037 s | FAIL: exit 1; 13 checks (11 passed, 1 failed, 1 skipped), README says 14 |
| reproduce_sh_hp | `./reproduce.sh` | . | 1 | none named | none quoted | 506 s | FAIL: exit 1 [14 checks (13 passed, 1 failed, 0 skipped), README says 14] (existing build) |
| reproduce_sh_full | `--full` | . | 1 | none named | none quoted | 510 s | FAIL: exit 1; 14 checks (12 passed, 1 failed, 1 skipped), README says 15 |
| reproduce_sh_full_hp | `--full` | . | 1 | none named | none quoted | 474 s | FAIL: exit 1 [15 checks (14 passed, 1 failed, 0 skipped), README says 15] (existing build) |
| hp_build_sh | `hp/build.sh` | . | 0 | none named | none quoted | 1 s | OK (existing build) |
| states_module | `hp/states.py` | . |  | none named | none quoted |  | NOT RUN: a module the profile scripts import (where the states are read from), not a command; the README quotes no invocation |
| pip_install | `pip install .` | . | 1 | none named | none quoted | 1 s | NOT RUN: no existing build on this machine has rustkernel (the 5 venvs under ~/Source tried) (existing build) |
| cargo_test | `cargo test --release` | . |  | none named | none quoted |  | NOT RUN: cargo build: no builds on this pass (coordinator) |
| test_bindings | `python tests/test_bindings.py` | . | 1 | all exist | none quoted | 1 s | NOT RUN: no existing build on this machine has rustkernel (the 5 venvs under ~/Source tried) (existing build) |
| build_sh_main | `./build.sh main` | . |  | none named | none quoted |  | NOT RUN: build: no builds on this pass (coordinator) |
| git_clone_raw | `git clone https://github.com/nmoinvaz/choptuik-large-d-raw ../choptuik-large-d-raw` | . | 0 | all exist | none quoted | 281 s | OK |

