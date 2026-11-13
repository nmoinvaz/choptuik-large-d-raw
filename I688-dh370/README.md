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
