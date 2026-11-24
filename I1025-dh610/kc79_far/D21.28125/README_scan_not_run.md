# I1025-dh610/kc79_far/D21.28125: lambda_1 on win2's k_c 79 far scout point D 21.28125 (tag l1kc79Lw1025i, the first point), window 0.805 to 0.835 around the prediction 0.8202

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, win2's plan, method, threads). Written 2026-11-24 11:15 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, hc of 24 Nov)
lambda_1 on win2's k_c 79 far scout at D 21.28125: **predicted 0.8202 +-0.01** (the previous k_c 79 root 0.841733, measured at D 21.21875 on the tag g leap, which is the scout's seed, minus 0.0215 for one 0.0625 step); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report (the leg's standing rule). The state comes from win2's far scout under tag **l1kc79Lw1025i** (`tag.txt`; `ell_leap.py l1kc79Lw1025i 1 79 <D 21.1875 g state> 21.1875 <D 21.21875 g state> 21.21875 22.5 0.0625 ...`, win2's plan at raw 0f6691f2).

## This point
- State `sol_l1kc79Lw1025i_D21.281250.npy` and record `l1kc79Lw1025i.jsonl` of win2's `states/` folder: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The scout waits for the end of win2's k_c 71 leg 9 (which stopped at its psi-constraint bar), then runs with 4 threads; a point at h 0.0625 takes win2 an unknown time (the tag g points took 4711 to 4896 s at h 0.03125), so I expect the first state between 12:45 and 14:30 UTC.
- Grid centre 0.820 (the multiple of 0.005 nearest 0.8202; 0.0002 away); the scan: 0.805, 0.810, 0.815, 0.820, 0.825, 0.830, 0.835 and a repeat of 0.820. The widening, if there is no robust change: low 0.800, 0.795, 0.790; high 0.840, 0.845, 0.850 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.28125 0.820 0.8202` as the systemd user unit `i1025-far-21_28125` (waits for the state, pins, pushes the pins, waits for free threads under the budget of the parent README, takes the lock, runs `lane_far.sh`; every script reads `tag.txt`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.28125 with both controls exit 1; all 8 processes print the record system; the repeat of 0.820 agrees (`repeat_check.py`); the selftests as wanted (`0 0 1 1 0 0 1`). A failing control or check stops the lane and I report it. A record of the scout with |F| above 1e-9 would be refused by the check (the record class), and I would report it, not loosen it.
- `fetch_point.sh` exits 2 and the lane stops when the record has no row for D 21.28125 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range (a spread over interpolation choices, not an enclosure)) beside the prediction 0.8202 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran; the seconds win2 took per point at h 0.0625 (from its record) against 4711 to 4896 s at 0.03125.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (14%), two or more (6%). The change within 0.01 of 0.8202: 82%; within 0.005: 65%. The measured steps of the tag g leap per 0.03125 in D grew in size from -0.008945 (D 21.03125) to -0.010336 (D 21.21875), against the order's -0.0108 per 0.03125 and -0.0215 per 0.0625; I expect -0.0207 to -0.0212 per 0.0625, so the root between 0.8205 and 0.8225 (55%), the bracket (0.820, 0.825) (70%).
- The float64 sign agrees with the hybrid at all 8 evaluations (25%; it differed at 1 to 4 grid points in each of the last seven points of the leg).
- Each scan point takes 1500 to 3500 s (65%; with the recount's 12 processes beside it the load is about 20; the leg's points took 1524 to 1709 s at load 9 to 10, and 2984 to 3341 s at load 19 on 22 Nov). The point is done (no widening) within 70 min of the lane's start (60%).
- The first scout state is on origin by 14:30 UTC (65%).
- Once the tag g leap has D 21.28125 and I have scanned it (the leg's lane does), the two det-linear roots at D 21.28125 (g, h 0.03125; i, h 0.0625) differ by less than 0.003 (70%); this compares two leaps' states, not an independent method.

## Status
- 2026-11-24 11:15 UTC: folder and README written; the unit `i1025-far-21_28125` is started next and waits for the state.
