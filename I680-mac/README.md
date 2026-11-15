# I680-mac: the freeze projector's Delta shift at D 80, exact rows minus rounded rows from T138-win2's state

Machine: the Mac (Apple M5, the coordinator's machine), one process at a time, 2 threads, nice 10, OPENBLAS_NUM_THREADS=1.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/680. Code: main 6d80ca0e (`hp/anm_run.py`, `hp/delta_diff.py`,
`hp/freeze_round.py`), as #595 made its rows. State: `T138-win2/chain/anm_pin3_D80.0000.npz` (the state #636 used at D 80).

**The kernels, identified before the runs** (`projector_check_*.log`). `freeze_round.py --mutate=proj` emulates the
frozen horizon rows with the exact projector and compares them with the kernel's rows. It needs a stored plan, so the
state is #603's D 226.13.

| kernel | built | exact emulation minus the kernel's rows | projector |
|---|---|---|---|
| venv-314's installed hpkernel | 2026-11-09 00:24 UTC | 1.68e-34 (the double-double rounding is 1.78e-34) | rounded |
| i599/site2 (main 3c35f0c) | 2026-11-13 01:03 UTC | 1.2e-132 | exact |

**The runs** (`run_680.sh`, `exits.txt`). Each is a base polish of the D 80 state with crawlJ's chain flags (`--steps 0
--save_base 1 --tol_od 1e-60`): first `polish_rounded`, then `polish_exact`, then `polish_rounded2`, the control. All three
converged in 3 octo-double steps (1.7e-90, 2.4e-84, 1.7e-90), and all three made the same plan.

| difference (`delta_diff_D80*.log`, 140 digits) | value |
|---|---|
| Delta(exact) − Delta(state) | +3.18095e-27 |
| Delta(rounded) − Delta(state) | −7.06999e-29 |
| **Delta(exact) − Delta(rounded), the projector's shift** | **+3.25165e-27** |
| Delta(rounded2) − Delta(rounded), the control | 0, and the two bases are bit-identical |

**Against #636.** #636's figure is the M 32 re-solve on main 3c35f0c: +3.2e-27 from the stored state, and its first
Newton step's Delta part +3.252e-27 (`I636-mac/planted/resolution_check_D80_thisbuild.log`). The shift is within 1.6%
of the first and 0.01% of the second, against the bar of 10%.
