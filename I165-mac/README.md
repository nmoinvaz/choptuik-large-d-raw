# I165-mac: independent check of a write-up on Eq. (16) of arXiv:2611.07007v1, logs and planted inputs

Machine: Apple M5 Mac (`mac`), one process under `nice -n 10`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/165

Code: `solver/independent_eeg_eq16/` of the main repository, branch `wip/i165`. Python 3.13 with mpmath 1.3.0,
sympy 1.14.0, numpy 2.5.4, scipy 1.18.1. Shared input: `solver/eeg_profile/data/tuned_profile_A2.72.txt` only.
Paper: arXiv:2611.07007v1 PDF, sha256 2052bd92c384186ff53494278812a6a18ce0167f382ad148a48ed333238723ae (not stored).

Files:
- `check.log`, `check.json`: `python3 solver/independent_eeg_eq16/check.py` from the main repository's root, exit 0.
- `controls.log`: `controls.py --out <this folder>`, planted profiles then the 15 mutations, exit 0.
- `check_base.json`, `check_mut_<name>.json`: the per-check verdicts of the unmutated and each mutated run.
- `planted_<name>.txt`: the planted profiles in the data file's format (exact, smooth, kink, branch, pole2).
