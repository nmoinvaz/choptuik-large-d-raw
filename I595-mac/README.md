# I595-mac: the projector's Delta shift, D 215-240, measured by base polishes on the exact and the rounded rows

Machine mac (the shared Apple M5 Mac, 4 threads at nice 10, one job at a time), issue https://github.com/nmoinvaz/choptuik-large-d/issues/595 (subagent).
Kernels: #523's cadcaf1 checked wheel (freeze projector in octo-double, the exact rows), in a scratch target first on PYTHONPATH, and main's old wheel (venv-314, the double-double projector, the rounded rows); each log's first line prints `hpkernel.__file__`.
Code: main d020d58's `hp/anm_run.py` (its od gate, 62bc52a) for the polishes, `--steps 0 --save_base 1 --tol_od 1e-60` with crawlJ's chain flags (`--held_o 1 --reseed 2 --reseed_q 1 --reseed_o 3 --od_junk 0 --lam_stall 0.04`, `run_595b.sh`, `run_595c.sh`, and I562-mac's `run_562d.sh`); `hp/delta_diff.py` (8f311d5) for the exact eight-part Delta differences. Starts: #589's re-planned states `I589-mac/sNNN.npz`.

| file | what | exit |
|---|---|---|
| `planted235_w_tau0.*` | a planted start z0 + tau0 (discarded during its probe: b = F(z0) - F(z0 + tau0) is 2e16, the strong rows' quadratic at the 0.7 layout) | stopped |
| `plantedrho235.*` | held_homotopy control mode, a planted offset 1e-18 of r0's horizon p rows: rung 0 at h = 1 refused (corrections 5.6e-34, 5.6e-34, Delta +-5e-34: Newton oscillates in the weak block) | stopped |
| `real235.*` | a trace started by a script error and stopped within its first line | stopped |
| `failed_import/` | the first polish attempts: main's tree lacked solver/data | 1 |
| `polish_c2_s215`, `polish_main_s215` | D 215.0000, both converged (2.7e-79, 9.3e-98) | 0 |
| `polish_c2_s225`, `polish_main_s225` | D 225.1312, both converged (4.2e-95, 3.2e-64) | 0 |
| `polish_c2_s235` | D 235.1312 on cadcaf1, converged (1.5e-94) | 0 |
| `polish_main_s235` | D 235.1312 control: step 0 dDelta -2.60e-14 at lam 1, then lam 1/2 steps halving max\|F\| (1.27e-27 -> 1.59e-28, dDelta <= 4e-27); stopped by me after 4 steps with Delta settled to 1e-26 | stopped |
| `delta_diff_s215.log`, `delta_diff_s225.log`, `delta_diff_s235.log` | the exact Delta differences | 0 |

Results are on #595.
