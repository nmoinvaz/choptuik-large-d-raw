# I494-mac: the freeze projector's double-double rounding at crawlJ's D 242.3642 state, and Delta's response to it

Machine: the M5 Mac (coordinator). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/494.

State: `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (nodes 0.3-0.7, M 32, kfreeze 3, L 769, eight parts). Code:
`hp/freeze_round.py` at choptuik-large-d 8a79c0e (branch `wip/i494-coordinator`), python-flint not used, mpmath at
160 digits, hpkernel of main de63a11 as installed in the Mac's venv.

| file | command | exit |
|---|---|---|
| `freeze_round.log`, `freeze_round.json` | `freeze_round.py RAW STATE --threads=2 --json=...` | 0, checks (a) and (b) pass |
| `freeze_round_ctl_proj.log` | `--mutate=proj` (emulates the kernel's rows with the exact projector) | 1, (a) fails as it must |
| `freeze_round_ctl_row.log` | `--mutate=row` (e's largest row times 1.01 before the solve) | 1, (b) fails as it must |
| `line_scan.py`, `line_scan.log` | the pinned residual along z - t x for t = 1e-32 to 1e-20, with the count of entries whose double-double part changed | 0 |

The two control logs were made by the script before its scan along the step was added; their checks are unchanged.

Results: e (exact minus rounded rows) is 1.62e-34, harmonic 1 of p at the horizon match. The first-order shift
-(J^-1 e)_Delta is 2.15e-9, but the exact rows along the step grow as 6.45e17 t^2 for t = 1e-22 to 1e-6, so the
linear model holds only for t < 2.5e-52 and the first-order shift is not an estimate. The pinned residual along the
same step follows 6.452e17 t^2 from t = 1e-26 to 1e-6 with no jump where the double-double parts change (line scan).
