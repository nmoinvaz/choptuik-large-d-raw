# I485-win2: bisect of the commit that moved the D 30 determinants off October's cache (#442)

Machine win2 (Windows x86-64, Intel Core Ultra 7 265K, no AVX-512), issue https://github.com/nmoinvaz/choptuik-large-d/issues/485 (after #482, verdict "code").
Bisect worktree `D:\choptuik-bisect` (detached at 2ef50229, 2026-10-22), bisect venv `C:\Users\nathan\Source\venv-bisect` (Python 3.12.8, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0,
python-flint 0.9.0, maturin 1.16.0; made with `python3 -m venv` because uv is not installed on win2 and installing it would change the machine's package managers).
One process at a time, below-normal priority, beside #461's crawlJ, which runs on venv-t126 and is never touched. Results follow in this README.
