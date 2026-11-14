# I803-win: #780's light-cone comparison at D = 4

Machine win (surface-laptop-4), issue https://github.com/nmoinvaz/choptuik-large-d/issues/803.

Scripts (written by the coordinator): `run803.sh` (#780's `i780_compare.py --dd=0` at I95's D = 4 evaluation points,
then `complex_imag_dd.py count` in B0, U0 and FULL over those values; worktree C:/Users/nathan/Source/choptuik-i803 at
main, venv-t151, no hp kernel) and `summary803.py`.

Criteria, fixed before the run (#803): every point's phase within 1e-3 rad of the double value; B0, U0 and FULL wind as
I95's double counts (1, 0, 0); the largest phase change reported beside #780's 3.4e-4 (D 20.04) and 3.9e-6 (D 10).
