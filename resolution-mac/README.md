# resolution-mac: chain and full-system states resampled from M = 32 to M = 48 (hp/resolution_check.py)

Machine: the coordinator's Mac (Apple M5), venv-anm (quad-double kernel, built for M = 32 and 48). Runs of 2026-11-07,
16:50-19:00 UTC. Each log is one `resolution_check.py` run (main 9b0398f and later): the round-trip check, the solve at
M = 32 and at M = 48, Delta and the pivots. The clean measurement is `scan_chainfit_D80.log` (pinned, converged at
M = 48 to 1.4e-38, Delta moved -2.4e-25). The full-system states (D 61.66-73) do not converge at M = 48 with their
junk directions frozen, and above D 80 the pinned states' horizon block is not re-seeded at the new M, so their start
residual grows to 2e15 at D 200; neither measures resolution. `mutate_D100.log` is the resampling control (exit 1).
