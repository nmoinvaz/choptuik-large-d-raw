#1109 stage 1c on macm3 (runner t5-macm3, MacBook Air M3), started 2026-11-28 06:36 UTC. Raw: `I1109-macm3/` (README first).

- Checkout `~/Source/choptuik-ell1fast` at 693a4d79 (wip/i1101-weakdir), venv `venv-macm3-1058b`; ellrs built here (`ellrs neon accelerate`).
- Step 1 passed: `ell_b12rs.py selftest` exit 0, `--mutate=nolam` exit 1, `--mutate=harm` exit 1, `check` (k_c 31, D 10.5, lambda 2.87, 2 threads, controls) exit 0: 15010 of 15010 entries bit for bit, both controls 0 of 15010.
- Step 2 running since 2026-11-28 06:27:28 UTC: r0 (0.0440, 0.0470), w01 (0.0400, 0.0500), w10 (0.0350, 0.0550), `--b12=rust --b12_threads=2 --tol=1e-6 --maxev=20`, 3 processes x 2 threads, nice 10, 14400 s cap each. First evaluation about 532 s each with the three at once; RSS about 3 GiB each; load average 15 (other processes).
