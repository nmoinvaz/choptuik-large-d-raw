# I737-win: the horizon series' transient at M = 32 against M = 48 at D 80 and 100

Machine win (Surface Laptop 4, 8 threads, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/737.

Scripts (written by the coordinator): `run737.ps1` (every step) and `table737.py` (the peaks, the rule and the
verdict, registered in its docstring before the runs). Code: worktree `choptuik-i737` at main 0209d4d2, venv-t179. The
horizon series reads only the horizon data (m_h, a_h, Delta) and D, not the freeze projector, so this build gives the
terms of main's.

Inputs, read from the raw repository's GitHub copy into `C:\Users\nathan\scratch737`: the M = 32 chain states
`T138-win2/chain/anm_pin3_D80.0000.npz` and `anm_pin3_D100.0000.npz`, and #636's M = 48 solutions of the same states,
`I636-mac/planted/m48_anm_pin3_D80.0000.npz` and `I636-mac/chain/m48_anm_pin3_D100.0000.npz` (quad-double, pinned
max|F| 1e-35 to 3e-34).

Why D 80 and 100, not 55 to 76: these are the D where M = 48 solutions of chain states already exist. At D 253.8
(#697) a resampled M = 48 base was off its own equations by 1.1e-22 in a_h, and the mass mode's gain turned that
into growth. Here the gain is about 0.7^-(n - 1), 1e12 at D 80 and 1e15 at D 100, and the M = 48 data are solutions,
so S2 tests whether they suffice.

Result: no verdict. S1 fails at D 80 (no hump, terms fall from Re s) and D 100 (hump 3.6, against the bar 10). The scale48 control could not fire because S1 is judged first. The a_h response (S2) shows that quad-double M = 48 bases cannot resolve the transient past D 100.
