# I760-dh370: the chain's series at three of #603's newest bases, toward the near track at 258.60 + 2.79i

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/760.

Scripts: #712's, with only the folder, the bases and the bars' track changed (written by the coordinator): `run760.sh`
(the 24-order series, `anm_run.py --save_jet 2` with #603's chain_nsr flags, at D 256.5686, 257.6853 and 258.7829, in
#712's worktree choptuik-large-d-685 at main f40deb4a and venv), `stage_summary760.sh` (jet_singularity.py summary,
table685.py, report760.py, and repro_check760.py with its control), `repro_check760.py`, `report760.py`.

Bars, written before any series was read (#760): (1) each series equals #603's record of the step from its base in all
25 norms and both pivots, and the control (the next base's record) differs; (2) Delta's root test within 5% of
|T - D0|, T = 258.60 + 2.79i; (3) the Pade pole of Delta within 0.4 of T has Im D* within 0.1 of 2.79. Track A
(255.71 + 4.99i) is listed at each base. On #712's three bases read as new, bar 2 passes only at D 255.37 (-0.7%), and the
control `--mutate=shiftT` (T moved by 1.0) fails bar 3 at every base.
