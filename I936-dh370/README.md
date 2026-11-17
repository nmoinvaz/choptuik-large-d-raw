# I936-dh370: #841's own build against multidouble 4.8.2, octo-double residual and Newton step on one chain state

Machine dh370 (Fedora 45, i7-8700, 12 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/936

`states936.sh` (run unedited by absolute path, unit `i936`, 13:52:55 to 13:57:37 UTC on 2026-11-17, nice 10, 5 threads in the dump):
#934's `state_dump.py` (a copy, md5 3c226e4d, `cmp` identical to `I934-dh610/state_dump.py`) through `state_dump936.py`, which replaces
its two-state `STATES` with one state of #841's chain, `I841-dh370/chain/anm_pin3_D254.9015.npz` (D 254.901496803760, M 32, 8 parts,
stored plan). Each build runs its own worktree's hp Python:

| | code | venv | multidouble / multishoot (hp/Cargo.lock) | `_hpkernel` sha256 |
|---|---|---|---|---|
| old | `choptuik-large-d-841` at 0cfff3c4 | `~/Source/venv-i800` | 4.2.1 / 1.2.2 | 3a53cbd7... |
| new | `choptuik-large-d-935` at 043834d9 | its `.venv` (#935) | 4.8.2 / 3.2.0 | 23b1e178... |

Dumps: `residual_o(z)` and `newton_o(z)` (default tangents) of the stored state, saved as `states_old_*.npz` and `states_new_*.npz`;
the control `states_ctl_*.npz` is the new build's `newton_o(z, mutate=25, tangents=4)`, each evaluation's tangents read in reverse.
`state_dump.py --compare` passes only when every part of every entry of the residual and the step has the same bits in old and new and the
control's step differs from the old one's. Log: `states.log`.

## Results

| entries compared (bits) | old against new | control against old |
|---|---|---|
| residual, F0..F7, 8 x 769 = 6152 | 0 differ | |
| step, dz0..dz7 6152, a1 769, a2 769, f3 and f4 = 7692 | 0 differ | dz: 6088 of 6152 differ |

`PASS: residuals and steps are the same bits; control fired`, compare exit 0, script exit 0.

What it shows: at this state, #841's build (multidouble 4.2.1) and the 4.8.2 build give the same bits in `residual_o` and `newton_o`, so the
octo-double renormalization bug of multidouble 3.0.0 to 4.8.0 did not change either at this state. It is one state (D 254.9015); the others
of the 59 are not run. The two builds differ in more than multidouble (the kernel source `hp/src/model.rs` and `python.rs`, such as
#921's two-column Jacobian, and multishoot 1.2.2 to 3.2.0), and equal bits cover all of those at once.
