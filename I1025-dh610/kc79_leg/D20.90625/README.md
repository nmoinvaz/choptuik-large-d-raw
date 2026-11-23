# I1025-dh610/kc79_leg/D20.90625: lambda_1 on win2's k_c 79 leg point D 20.90625 (tag l1kc79Lw1025d), window 0.920 to 0.950 around the prediction 0.936

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-23 16:59 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45")
lambda_1 on win2's k_c 79 leg at D 20.90625: **predicted 0.936 +-0.01**; a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025d_D20.906250.npy` and record `l1kc79Lw1025d.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan).
- Grid centre 0.935 (the multiple of 0.005 nearest 0.936); the scan: 0.920, 0.925, 0.930, 0.935, 0.940, 0.945, 0.950 and a repeat of 0.935. The widening, if there is no robust change: low 0.915, 0.910, 0.905; high 0.955, 0.960, 0.965 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 20.90625 0.935 0.936` as the systemd user unit `i1025-leg-20_90625` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 20.90625 with both controls exit 1; all 8 processes print the record system; the repeat of 0.935 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.936 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; win2's states on this build: D 20.8125 passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (75%), none (17%), two or more (8%). The change within 0.01 of 0.936 (coordinator's reading): 45%; within 0.005: 25%.
- Each scan point takes 900 to 1900 s (65%); the point is done (no widening) within 45 min of the lane's start (70%).

## Status
- 2026-11-23 16:59 UTC: folder and README written; the unit waits for the state (expected about 20:35 UTC).
