# I936-win2: the octo-double bits of win2's chain build (multidouble 4.1.0) against multidouble 4.8.2

Machine: win2 (Windows desktop, 20 threads, 95 GB), win2 build session beside win2b's #903 ks-tied chain.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/936 (follow-up of #934 and #935).

| | |
|---|---|
| state | `I903-win2/ks_chain/leg06_D212.0000_ks230/anm_pin3_D215.0000.npz` (eight parts, D 215, ks 230, stored plan) |
| old build | `C:\Users\nathan\Source\venv-i600`, multidouble 4.1.0 / multishoot 1.2.1, hpkernel from `D:\choptuik-i600` (fc697f3a) |
| new build | `C:\Users\nathan\Source\venv-md482`, multidouble 4.8.2 / multishoot 3.2.0, `D:\choptuik-i935` (d7b59668), #935 |
| script | `state_dump.py` is #934's (`I934-dh610/`), only `STATES` differs; `run_936.sh` runs it |

## Result (2026-11-17)

The old build (venv-i600) and the 4.8.2 build (venv-md482) give the same bits for `residual_o` and `newton_o` on the D 215
state, and the control differs.

| criterion | verdict | number |
|---|---|---|
| residual `F0..F7`, old against new | equal | 0 of 6152 entries differ (8 parts x 769) |
| Newton step `dz0..dz7`, `a1`, `a2`, `f3`, `f4`, old against new | equal | 0 of 7692 entries differ |
| control (new build, `newton_o(mutate=25, tangents=4)`, tangents reversed) against old | differs | 6120 entries differ |
| old build run twice (the trial dump and the final one) | equal | 0 of 13844 entries differ |
| `run_936.sh` exit | 0 | `states.log`, 15:59:24 to 16:05:25 UTC |

13844 entries over 20 arrays (N = 769 unknowns). The residual has nonzero entries in all eight parts (769, 769, 503, 128,
82, 32, 32, 32 in parts 0 to 7), max|F0| 9.027e-4, so the low parts the renormalization bug touches are populated.

The Python is the new worktree's `hp/` for both builds, as in #934 (`state_dump.py`'s HP_DIR), because the producing
worktrees (`D:\choptuik-i600`, the chain's `D:\choptuik-i603r`) have no `octo_corrector.truth_system`. Only the kernel
differs: venv-i600's hpkernel was built from `D:\choptuik-i600` (fc697f3a, multidouble 4.1.0 / multishoot 1.2.1, direct_url in its
dist-info), venv-md482's from `D:\choptuik-i935` (d7b59668, 4.8.2 / 3.2.0). The old-kernel run was only this one state, a base
of the ks-tied chain (`ks_chain/leg06_D212.0000_ks230`, ks 230, M 32, stored plan). It shows this state does not hit the bug, not
that no state does.

The `PinnedO` wrapper's Python helpers (`od_axpy`, `od_add_dd`) are not on this path: see `../I935-win2/README.md`, "The Python
package is still at multidouble 4.6.0".

Files: `states.log`, `states_{old,new,ctl}_ks_D215.npz`, `trial_old_ks_D215.npz` and `trial_old_dump.log` (the first old-build dump),
`state_dump.py`, `run_936.sh`.
