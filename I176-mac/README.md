# I176-mac: independent check of the size of the NNLO correction with Eq. (16) as beta~

Machine: the Apple M5 Mac (`mac`). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/176

Code: `solver/independent_eeg_effect/` of nmoinvaz/choptuik-large-d, branch `wip/i176` at commit 1aceb79. Inputs: arXiv:2611.07007v1
(main.tex of the arXiv e-print, supplement (S35)-(S51) and Eq. (16)) and the correction formulas stated in #176.

| File | Command, from `solver/independent_eeg_effect/` | Exit |
|---|---|---|
| derive.log | `python3 derive.py` | 0 |
| derive_mutate_printed.log | `python3 derive.py --mutate=printed` (control) | 1 |
| effect.log, effect.json | `python3 effect.py --out effect.json` | 1, the table check fails at Pi, D 50 |
| effect_check_*.log | `python3 effect.py --check <scaling, x0, planted>` | 0 |
| mutate_pi_eps.log | `python3 effect.py --mutate=pi_eps --check scaling` (control) | 1 |
| mutate_pi_offset.log | `python3 effect.py --mutate=pi_offset --check x0` (control) | 1 |
| mutate_xrange.log | `python3 effect.py --mutate=xrange --check planted` (control) | 1 |
| effect_fine.log | `python3 effect.py --nth 4096 --nx 40` (quadrature convergence) | 1 |
| crosscheck.log | `python3 crosscheck.py 25 50 200` (second route, mpmath) | 0 |
| alt_period.log | `python3 alt_period.py` (tau over the fitted Delta(D), an alternative reading) | 0 |
| versions.txt | Python and package versions | |
