# I688-dh370: where the 0.975 layout's weak residual component comes from, u1^T F by block (the dh370 run of #688)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB. Run at `nice -n 10`, 12 threads, `OPENBLAS_NUM_THREADS=1`, no memory guard.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/688 (recommended by #673, whose starts are in I673-dh370/).
Code: choptuik-large-d main at f40deb4a (hp/near_null.py, hp/src and hp/python unchanged since aedb403b), worktree `choptuik-large-d-685`, the venv of `choptuik-large-d-614` (the 3c35f0c build).
`near_null.py` does not print u1^T F (the issue assumes it does), so `uf688.py` in this folder does: it takes near_null's own functions (`layout`, `subspace`, `printed`, `step_report`) and repeats the body of its `main` for the setup, the octo-double LU, the subspace iteration and the exact Jacobian-vector product of v_1 at 140 digits, which gives sigma_1 u_1 = J v_1, then sums u_1^T r by residual block, r = F - c being the pinned system's residual (the pinned step is -J^-1 r, c the held offset). It is a script of this folder, not a change to main.

Inputs: I673-dh370/start_integrate.npz, I673-dh370/start_f64.npz, I654-dh370/start/start_0975.npz (the `--last horizon` start) and S = I603-win2/chain/anm_pin3_D252.2497.npz, all at D 252.2497.

## The prediction and the controls, written before any run

Prediction (the issue's): near_null's pinned step at start_integrate.npz and start_f64.npz is within 1% of 2.139e-02, and V^T dz on v_1 within 1% of -1.86e-01 (the values at the horizon start, I673-dh370/nn_0975.log).
Controls: (a) the route through the solves, u_1^T r = -sigma_1 (v_1^T dz_pinned), which does not use J v_1, must equal the sum over the blocks to 1e-3 relative (v_1 is in f64); (b) a planted residual r' = r + beta u_1 with beta = 1e-30 through the same code must return beta as the change of the sum, to 1e-10 relative, and beta |u_1,block|^2 as the change of each block; (c) `--mutate=shift` moves the rows of the sum by one row, which must break (a).
Rows of r are partitioned as the residual blocks of `renode_o.blocks`: rows 4 M b to 4 M (b + 1) for b = 0 (centre>n0), 1..K-1 (n(b-1)>n(b)), K (horizon>n(K-1)), the last row the phase row.

## Result

The weak component of the residual, u_1^T r = 8.68725e-41, is the same at the three 0.975 starts to every printed digit, and it sits in the two residual blocks that meet at the last node, n3>n4 and horizon>n4 (|u_1|^2 is 0.500 in each). Which of the two carries it depends on the last-node rule.
The prediction held: the pinned step is 2.139310e-02 with V^T dz on v_1 -1.858749e-01 at all three starts, equal to the last printed digit (within 1% of 2.139e-02 and -1.86e-01).

| start | max\|r\| and where | u_1^T r by block, signed | blocks carrying 99% of sum \|u_i r_i\| | u_1^T r | -sigma_1 v_1^T dz_pinned |
|---|---|---|---|---|---|
| `--last horizon` (I654-dh370/start/start_0975.npz) | 7.22e-37 in n3>n4 | n3>n4 8.687e-41, every other block below 1e-132 | n3>n4 | 8.68725e-41 | 8.687246e-41 |
| `--last integrate` | 7.33e-37 in horizon>n4 (n3>n4 is 0) | horizon>n4 8.687e-41, others below 1e-132 | horizon>n4 | 8.68725e-41 | 8.687246e-41 |
| `--last f64` | 2.06e-16 in n3>n4 and horizon>n4 | n3>n4 +1.99e-17 and horizon>n4 -1.99e-17, cancelling to 8.687e-41 | both | 8.68725e-41 | 8.687246e-41 |
| S, the 0.70 layout (D 252.2497) | 6.6e-92 in horizon>n4 | n3>n4 +1.4e-99, horizon>n4 -1.4e-99 | horizon>n4 | -2.1e-123 | -2.1e-123 |

sigma_1 is 4.674e-40 at the three starts (7.365e-32 at S), and the sum |u_i r_i| is 2.57e-36 at the horizon and integrate starts, so u_1^T r is 3.4e-5 of it (cancellation inside the two blocks). The f64 start's 2e-16 residual lies nearly orthogonal to u_1 (its two blocks cancel to 4e-24 of themselves), as a rounding of node 0.975's own value must: that value enters both blocks and u_1^T J = sigma_1 v_1^T. What does not cancel is the difference of the two arrivals at node 0.975, the Taylor steps of the planned segment from node 0.6 against the horizon series, which is the 7.2e-37 gap of I673-dh370/renode_*.log, and u_1 takes 1.2e-4 of it.

Controls: (a) the route through the solves agrees with the block sum to 3.5e-16 (0.975 starts) and 7.3e-7 (S, at the 1e-123 level, v_1 in f64); (b) the planted r + beta u_1 returns beta to 1e-129 or better at every run (tolerance 1e-10); (c) `--mutate=shift` (`uf_horizon_mutate_shift.log`) breaks both (relative 1.1e+02, exit 1).
All runs: exit 0 except the control (exit 1), 323 to 379 s each.

## Files

| file | what |
|---|---|
| `uf688.py`, `run688.sh`, `phases.log` | the script, the runs in order and their exits |
| `uf_horizon.*`, `uf_integrate.*`, `uf_f64.*`, `uf_070.*` | `.log` and `.json` of each state |
| `uf_horizon_mutate_shift.*` | the control, exit 1 |
