# T117-win: the elimination corrector from T116's 149.56 state

Pilot (cloud 2026-11-06 01:17 UTC): --reseed 2 --reseed_q 1, 6 steps, h_max 0.5, from T116-win2/chain/anm_pin3_D149.5559.npz, T112 build with anm_run.py, reseed.py and pinning.py from main 48adb33b, 4 threads, below normal. Pass if a step of 0.125 or more converges at least twice in the first 6 steps. Command in t117.cmd, log chain.log, states in chain/.

Did not start (2026-11-06 01:19 UTC): ImportError, `cannot import name 'QDLu' from 'multidouble'` in reseed.py line 32 (main 48adb33b). venv-t112's multidouble Python package is 0.1.0 at dcadedb4e5ce49a27e00cf64a53303ae826140f4 (the T112 pyproject pin); main's pyproject.toml pins 78efd7edc455d5f7868761beca563b154e0adc10, which reseed.py's QDLu needs. Nothing was changed; chain.log holds the traceback.
