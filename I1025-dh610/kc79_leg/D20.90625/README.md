# I1025-dh610/kc79_leg/D20.90625: lambda_1 on win2's k_c 79 leg point D 20.90625 (tag l1kc79Lw1025f, restarted leap; see Status), window 0.920 to 0.950 around the prediction 0.936

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-23 16:59 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45")
lambda_1 on win2's k_c 79 leg at D 20.90625: **predicted 0.936 +-0.01**; a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D20.906250.npy` and record `l1kc79Lw1025f.jsonl` (changed at 20:01 UTC from tag d, see Status) of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan).
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
- 2026-11-23 20:01 UTC, before any run of this folder: win2's fold watch fired after D 20.875 and the coordinator ruled a restart of the leap from the D 20.84375 and D 20.875 states at h 0.03125 under a new tag l1kc79Lw1025f (`../../../I1025-win2/kc79_leap/README.md`, ruling quoted there; the restart's dry run passed 19:15 UTC). The state and record of this point therefore come under tag f. Changed: `tag.txt` of this folder (l1kc79Lw1025f), and `fetch_point.sh`, `lane_leg.sh`, `summarize_leg.py` of `..` read the tag from `D<D>/tag.txt` (d when the file is absent). Tested: the patched `fetch_point.sh` pins D 20.875 to the same two blobs as the run (2f6d6b8a, e443a587); a tag file naming a tag with no state exits 1; `summarize_leg.py` output for D 20.84375 and D 20.875 is byte-identical to `summary_leg.txt`. Nothing in the pins, the acceptance, the controls or the predictions of this README changed. The expected time of the state moves to about 20:40 UTC (the restarted leap's first new point, 80 min after about 19:20); if win2's files for tag f sit elsewhere than `states/`, the waiter will not find them and I look by hand.
