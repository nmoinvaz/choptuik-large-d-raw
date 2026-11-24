# I1025-dh610/kc79_leg/D21.1875: lambda_1 on win2's k_c 79 leg point D 21.1875 (tag l1kc79Lw1025g, the first point of the cap restart), window 0.835 to 0.865 around the prediction 0.8514

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 07:27 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.1875: **predicted 0.8514 +-0.01** (the previous measured root 0.862190 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g; the restart was checked against win2's README, `../README.md`): its record file `l1kc79Lw1025g.jsonl` and states are its own, started from the tag f states of D 21.125 and D 21.15625.

## This point
- State `sol_l1kc79Lw1025g_D21.187500.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The first g state is expected about 08:35 UTC (the restart began at 07:19:49 UTC; a point takes win2 about 4500 s).
- Grid centre 0.850 (the multiple of 0.005 nearest 0.8514; 0.0014 away; 0.855 lies 0.0036 away); the scan: 0.835, 0.840, 0.845, 0.850, 0.855, 0.860, 0.865 and a repeat of 0.850. The widening, if there is no robust change: low 0.830, 0.825, 0.820; high 0.870, 0.875, 0.880 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.1875 0.850 0.8514` as the systemd user unit `i1025-leg-21_1875` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`; every script reads `tag.txt`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.1875 with both controls exit 1; all 8 processes print the record system; the repeat of 0.850 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- A check specific to the restart: the g record's row for D 21.1875 has kc 79, and the record file's rows for D 21.125 and D 21.15625 (if it carries them) equal tag f's by |F| and steps; if the state is not under tag g or the record is not k_c 79's, the lane stops and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8514 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (86%; the eleven earlier points passed, this is the first state of a restarted leap, as D 20.90625 was under tag f), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8514: 83%; within 0.005: 70%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598 and -0.009898 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849, +0.001286, +0.001188, +0.000890: I expect the root between 0.8520 and 0.8545 (55%).
- The float64 sign agrees with the hybrid at all 8 evaluations (25%; it differed at 2 to 4 grid points in each of the last four points).
- Each scan point takes 1400 to 2300 s (65%; the last three points 1504 to 2574 s; this scan runs beside the recount only). The point is done (no widening) within 50 min of the lane's start (65%; the last 29 min).
- The state is on origin by 09:00 UTC (75%; win2's points take about 4500 s, the restart began 07:19:49 UTC).

## Status
- 2026-11-24 07:27 UTC: folder and README written; the unit `i1025-leg-21_1875` is started next and waits for the state.
