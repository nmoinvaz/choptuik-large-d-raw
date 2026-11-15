# I813-win2: kf 41's control circle at D 61.0264, M 48, evaluated on win2 from macm3's saved state

Machine win2 (Windows desktop, 20 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/813.

Scripts (written by the coordinator): `run813.sh` (the control on macm3's state with #749's command, worktree and
build, 6 threads beside #343, win2's own saved state moved aside and put back) and `compare813.py` (ln|det| at each
point against macm3's and win2's #749 runs; the bar, fixed before the run, is in its docstring).

Input: `macm3_state/modecount_state_D61.0264_M48_kf41.npz`, md5 106886f37685b762bb4e948c26dc7474. It is macm3's saved
state from #749 (its worktree's hp/data, written 2026-11-14 07:53), copied by the coordinator and checked by md5.

Why (#789, #812): macm3's and win2's kf 41 controls differ below their printed digits (|F| 1.3201e-19 against
1.3170e-19, ln|det| by -0.029 to +0.0115). #812's conjugate lens zeros miss their conjugates by 1.7 to 2.5 times their
quadrature estimates. One stored state evaluated on both machines tells a difference in the states from one in the
evaluation.
