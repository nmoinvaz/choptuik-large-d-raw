# I1025-dh610/kc79_leg/D20.9375: lambda_1 on win2's k_c 79 leg point D 20.9375 (tag l1kc79Lw1025f), window 0.910 to 0.940 around the prediction 0.9274

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-23 22:00 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 20.9375: **predicted 0.9274 +-0.01** (the previous measured root 0.938234 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D20.937500.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.925 (the multiple of 0.005 nearest 0.9274); the scan: 0.910, 0.915, 0.920, 0.925, 0.930, 0.935, 0.940 and a repeat of 0.925. The widening, if there is no robust change: low 0.905, 0.900, 0.895; high 0.945, 0.950, 0.955 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 20.9375 0.925 0.9274` as the systemd user unit `i1025-leg-20_9375` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 20.9375 with both controls exit 1; all 8 processes print the record system; the repeat of 0.925 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.9274 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the three earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (78%), none (14%), two or more (8%). The change within 0.01 of 0.9274 (the coordinator's reading): 70%; within 0.005: 45%. The measured steps so far are -0.010169 and -0.009717, against the prediction's -0.0108, and the residuals +0.000120, +0.000951, +0.002234 grow: I expect the root between 0.9275 and 0.9320 (60%).
- Each scan point takes 2500 to 4300 s (60%) while the d19_k95 scan runs and the recount (its round 2 ends about 22:35 to 23:20 UTC), shorter after (the earlier points: 1531 to 1825, 2021 to 2474, 3050 to 4171 s); the point is done (no widening) within 75 min of the lane's start (60%).
- The state is on origin by 22:30 UTC (70%; win2's cadence 84 min, the last state 20:45:51 UTC).

## Status
- 2026-11-23 22:00 UTC: folder and README written; the unit `i1025-leg-20_9375` waits for the state (expected about 22:10 UTC).
