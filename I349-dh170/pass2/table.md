| id | README | command (dir) | exit | files | number printed vs quoted | wall | cpu | rss | verdict |
|---|---|---|---|---|---|---|---|---|---|
| hp_build_sh | 2183 | `hp/build.sh` | 0 | none named | none quoted | 1 s | 0 s | 18 MB | OK (existing build) |
| gamma_compare | 465 | `cd hp && python3 gamma_compare.py data/gamma_dd.jsonl data/local/gamma_dd.jsonl` | 0 | all 2 exist | lambda-2 by powers: 5/6 MISMATCH; lambda a1: 1/1 (3.0324=3.03239); gamma a1 = lambda a1 / 4 (derived): 1/1 (0.7581=0.758055); lambda a2 (not printed by this script): not checked | 1 s | 1 s | 87 MB | FAIL: lambda-2 by powers: not printed: 2.2×10⁻⁶ (nearest printed 0.0000021, 1 digits agree) (existing build) |
| check_numbers_selftest | 2160 | `check_numbers.py` | 1 | none named | none quoted | 23 s | 23 s | 139 MB | FAIL: exit 1 (existing build) |
| largeD_scaling | 954 | `hp/largeD_scaling.py` | 0 | none named | none quoted | 2 s | 1 s | 57 MB | OK (existing build) |
| largeD_F | 954 | `hp/largeD_F.py` | 0 | none named | D = 20: 5/5; D = 30: 5/5; D = 40: 5/5; D = 50: 5/5; D = 60: 5/5 | 3 s | 3 s | 54 MB | OK (existing build) |
| largeD_exponent | 1224 | `hp/largeD_exponent.py` | 0 | none named | n<G(1)>/2: 5/5; <F^2>: 5/5; shift: 5/5 | 2 s | 2 s | 57 MB | OK (existing build) |
| largeD_Fratios | 1569 | `hp/largeD_Fratios.py` | 0 | none named | ratios (|F5/F1| derived as |F3/F1||F5/F3|): 6/6 | 4 s | 4 s | 55 MB | OK (existing build) |
| eeg20 | 740 | `solver/eeg20/` | 0 | none named | ratio: 2/2 (0.98=0.98776, 1.06=1.0569) | 3 s | 2 s | 55 MB | OK (existing build) |
| tilt | 740 | `solver/eeg20/` | 0 | none named | measured/predicted at x = 1 (derived): 4/4 (0.69=0.70, 0.78=0.778354, 0.84=0.843050, 0.88=0.877706) | 2 s | 1 s | 56 MB | OK (existing build) |
| maxc | 740 | `solver/eeg20/` | 0 | none named | ratio: 2/2 (0.36=0.3572, 0.86=0.8570) | 3 s | 2 s | 54 MB | OK (existing build) |
| check_numbers | 2160 | `check_numbers.py` | 1 | none named | none quoted | 29 s | 28 s | 139 MB | FAIL: exit 1 (existing build) |
| gamma_dd | 457 | `hp/gamma_dd.py` | 1 | all 2 exist | none quoted | 1 s | 1 s | 85 MB | FAIL: exit 1 (existing build) |
| gamma_m48_gap | 461 | `hp/gamma_m48_gap.py` | 1 | none named | none quoted | 1 s | 0 s | 40 MB | FAIL: exit 1 (existing build) |
| modecount_test | 602 | `hp/modecount_test.py` | 1 | none named | none quoted | 1 s | 1 s | 84 MB | FAIL: exit 1 (existing build) |
| dd_D5 | 654 | `hp/compare/dd_D5.py` | 0 | all 1 exist | D = 5: 2/2 (3.22170194461806=3.22170, 3.22170194462672=3.22170) | 246 s | 1004 s | 343 MB | OK (existing build) |
| pip_install | 2197 | `pip install .` | 1 | none named | none quoted | 1 s | 0 s | 17 MB | NOT RUN: no existing build on this machine has rustkernel (the 5 venvs under ~/Source tried) (existing build) |
| test_bindings | 2199 | `python tests/test_bindings.py` | 1 | all 1 exist | none quoted | 1 s | 0 s | 31 MB | NOT RUN: no existing build on this machine has rustkernel (the 5 venvs under ~/Source tried) (existing build) |
| plot_wave_family | 978 | `hp/plot_wave_family.py` | 2 | all 1 exist | none quoted | 1 s | 0 s | 42 MB | FAIL: exit 2 || adapted `python3 plot_wave_family.py ../../choptuik-large-d-raw` (hp/): exit 0, none quoted, OK (existing build) |
| reproduce_sh_hp | 2170 | `./reproduce.sh` | 1 | none named | none quoted | 506 s | 447 s | 132 MB | FAIL: exit 1 (existing build) |
| reproduce_sh_full_hp | 2179 | `--full` | 1 | none named | none quoted | 474 s | 443 s | 132 MB | FAIL: exit 1 (existing build) |
