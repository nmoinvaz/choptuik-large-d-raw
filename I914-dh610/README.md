# I914-dh610: the octo-double series one order at a time (Solver.series_o) against the jets, bits and time at D 253

Machine: dh610, Fedora Linux 45, Intel i7-12700 (20 threads, AVX2), 62 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/914
Code: branch `hp/order-by-order` at 0cf9b94a (#911's bump, then taylor_coeffs_at, centre_state_at, horizon_state_at,
psolve_at, Solver.series_o and hp/jet_by_order_check.py), built by #911 (worktree `/home/nathan/Source/choptuik-large-d-911`, its venv; #911's
`tests.sh` runs `oseries_by_order_bitwise`). State: #608's `I608-dh610/restart4_d6/anm_pin3_D253.3382.npz` (eight parts, stored plan).

Script, started as `systemd-run --user --scope bash check.sh` from this folder once #911 has closed: `check.sh`.
