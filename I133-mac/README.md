# I133-mac: rational [L/N] fits of the D = infinity tuned profile's harmonics, planted tests and controls

Machine: mac (Apple M5), a subagent of the coordinator, 2 processes at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/133

Every file here is written by `solver/eeg_profile/rational_fit.py` (its `--log` and `--out`) or by
`solver/eeg_profile/rational_controls.py` (`--log=`), at commit 34eb75f of branch wip/i133 of the main repository
(rational_fit.py is unchanged since 28fcfaa). The input is the tuned harmonics of `solver/inner_amp/scan45J1250/` and
`scan45J1500/` (K = 45, omega_inf), summed at A as in `solver/eeg_profile/tuned_profile.py`. The write-up is
notes/EEG_PROFILE.md section 8.

| file | command (from solver/eeg_profile) | exit |
|---|---|---|
| real_A2.72.log, .json | `rational_fit.py` (pade, ls, minimax; both J) | 0 |
| real_A2.72_tail.log, .json | `rational_fit.py --tail` (the A series' geometric tail estimate added) | 0 |
| real_A2.71918.log, .json | `rational_fit.py --A 2.71918` | 0 |
| plant_rational.log | `rational_fit.py --plant=rational` | 0 |
| plant_rational_mutate_gauge.log | `rational_fit.py --plant=rational --mutate=gauge` | 1, as it must |
| plant_rational_mutate_drop.log | `rational_fit.py --plant=rational --mutate=drop` | 1, as it must |
| plant_branch.log | `rational_fit.py --plant=branch` | 0 |
| plant_poles.log | `rational_fit.py --plant=poles` | 1: its "converged" half fails as stated (reported) |
| controls.log | `rational_controls.py` | 0, "all controls behave" |

The .json files hold every fit's P and Q coefficients (30 digits), its errors e_k for k = 0..12, its poles and zeros
in theta (paper's gauge) with relative residues, and the data c_k with their remainder estimates.
