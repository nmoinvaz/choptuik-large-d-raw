# I1025-dh610/kc79_leg/D21.21875: lambda_1 on win2's k_c 79 leg point D 21.21875 (tag l1kc79Lw1025g), window 0.825 to 0.855 around the prediction 0.8413

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 09:16 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.21875: **predicted 0.8413 +-0.01** (the previous measured root 0.852069 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875; the restart was checked against win2's README, `../README.md`): its record file `l1kc79Lw1025g.jsonl` and states are its own.

## This point
- State `sol_l1kc79Lw1025g_D21.218750.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The first g state (D 21.1875) came 85 min after the restart began and its record says 4896 s, so I expect this one about 10:05 UTC (win2's points took 57 to 78 min under tag f).
- Grid centre 0.840 (the multiple of 0.005 nearest 0.8413; 0.0013 away; 0.845 lies 0.0037 away); the scan: 0.825, 0.830, 0.835, 0.840, 0.845, 0.850, 0.855 and a repeat of 0.840. The widening, if there is no robust change: low 0.820, 0.815, 0.810; high 0.860, 0.865, 0.870 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.21875 0.840 0.8413` as the systemd user unit `i1025-leg-21_21875` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`; every script reads `tag.txt`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.21875 with both controls exit 1; all 8 processes print the record system; the repeat of 0.840 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.21875 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8413 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (82%), none (11%), two or more (7%). The change within 0.01 of 0.8413: 85%; within 0.005: 72%. The bracket is (0.840, 0.845): 80%.
- The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598, -0.009898 and -0.010121 against the prediction's -0.0108; the residuals against the registered predictions are +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849, +0.001286, +0.001188, +0.000890 and +0.000669, falling over the last five. I expect the root between 0.8410 and 0.8430 (60%).
- The float64 sign agrees with the hybrid at all 8 evaluations (25%; it differed at 1 to 4 grid points in each of the last five points).
- Each scan point takes 1300 to 2300 s (70%; the last point 1524 to 1709 s with the recount beside it). The point is done (no widening) within 50 min of the lane's start (70%; the last 29 min).
- The state is on origin by 10:30 UTC (75%).

## Status
- 2026-11-24 09:16 UTC: folder and README written; the unit `i1025-leg-21_21875` is started next and waits for the state.
