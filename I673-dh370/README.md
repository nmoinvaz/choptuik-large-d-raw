# I673-dh370: why the 0.975 start's first Newton step is 3e34 times its residual, near_null at both layouts and the other last-node rules (the dh370 run of #673)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB. Run at `nice -n 10`, 12 threads, `OPENBLAS_NUM_THREADS=1`, no memory guard.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/673 (recommended by #654, whose start and logs are in I654-dh370/).
Code: choptuik-large-d main at 37c7955c, worktree `choptuik-large-d-654` (as for #654), run in the venv of `choptuik-large-d-614` (the 3c35f0c build, multishoot 1.2.2, multidouble 4.2.1).
Start states: `I654-dh370/start/start_0975.npz` (the `--last horizon` renode of S, as #654 left it) and S = `I603-win2/chain/anm_pin3_D252.2497.npz`, both read in place.

## Result

Run order and exits are in `phases.log` (run673.sh, all from the worktree `choptuik-large-d-654`). Tables of step 1 are in `nn_table.txt` (from `nn_table.py`).

| step | exit | wall |
|---|---|---|
| `near_null` at the unpolished 0.975 start (`nn_0975.log/.json`) | 0, check pass | 372 s |
| `near_null` at S, D 252.2497 (`nn_070.log/.json`) | 0, check pass | 296 s |
| `near_null --mutate=sigma` at the 0.975 start (`nn_0975_mutate_sigma.log`), the control | 1, check FAIL (‖J v₁‖/σ₁ = 0.952381) | 371 s |
| `renode_o.py --last integrate` (`renode_integrate.log`, `start_integrate.npz`) | 0, check pass | 5 s |
| its control `--mutate sign` (`renode_integrate_ctl_sign.log`) | 1, check FAIL, as it must | 4 s |
| `renode_o.py --last f64` (`renode_f64.log`, `start_f64.npz`) | 0, check pass | 4 s |
| its control `--mutate sign` (`renode_f64_ctl_sign.log`) | **0, check pass: the control does not fire** | 3 s |
| polish of `start_integrate.npz`, `--qd_it 3` (`polish_integrate.log`) | 0, not adopted | 1335 s |
| polish of `start_f64.npz`, `--qd_it 3` (`polish_f64.log`) | 0, adopted (unconverged), `base_f64/base_pin3_D252.2497.npz` | 1350 s |

The f64 control cannot fire: `renode_o.py` skips the refinement of the new node for `--last f64` (renode_o.py line 143, `continue`), the check has no node to test, and `--mutate sign` changes nothing.
The control's state equals the plain f64 state in every array (only the `meta` record of the mutation differs).

### The three last-node rules, the same polish

| rule | start's max\|F\| | where | step 0 \|dz\| | step 0 Δ part | \|F\| after steps 0, 1, 2 | smallest pivot at steps 0, 1, 2 |
|---|---|---|---|---|---|
| horizon (#654, `I654-dh370/base.log`) | 7.22e-37 | n3>n4 | 2.14e-02 | +7.11e-03 | 3.25e-06, 8.51e-09, 3.28e-18 | 4.6e-07, 2.6e-11, 5.7e-19 |
| integrate | 7.33e-37 | horizon>n4 (n3>n4 is 0) | 2.14e-02 | +7.11e-03 | 3.25e-06, 8.51e-09, 3.28e-18 | 4.6e-07, 2.6e-11, 5.7e-19 |
| f64 | 2.06e-16 | n3>n4 and horizon>n4 | 2.14e-02 | +7.11e-03 | 3.25e-06, 8.51e-09, 3.28e-18 | 4.6e-07, 2.6e-11, 5.7e-19 |

Every printed number of steps 0 to 2 (|dz|, lam 0.125, 1, 1, the Δ components +7.11e-03, +8.29e-07, +4.17e-10) is the same for the three starts.

## Files

| file | what |
|---|---|
| `run673.sh`, `phases.log` | the runs of the task in order, and their exits |
| `nn_0975.*`, `nn_070.*`, `nn_0975_mutate_sigma.*`, `nn_table.py`, `nn_table.txt` | step 1 |
| `renode_integrate*.log`, `start_integrate.npz`, `ctl_sign_integrate.npz`, `polish_integrate.log` | `--last integrate` |
| `renode_f64*.log`, `start_f64.npz`, `ctl_sign_f64.npz`, `polish_f64.log`, `base_f64/` | `--last f64`; `base_f64/` holds an unconverged iterate (max\|F\| 3.3e-18), not a chain start |
