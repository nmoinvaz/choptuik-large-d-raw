# I1025-dh610/kc79_far: lambda_1 on each point of win2's k_c 79 far scout (tag l1kc79Lw1025i, h 0.0625, from D 21.21875), one subfolder per D

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 11:15 UTC, before any run of this folder. The k_c 79 roots are not yet physical. Sister folder: `../kc79_leg/` (win2's tag g leap, h 0.03125, which keeps priority); every script here is a copy of that folder's with the changes listed below.

## Order (coordinator t5, hc, 24 Nov, verbatim)
"win2 starts a k_c 79 far scout (tag l1kc79Lw1025i, h 0.0625, from D 21.21875 to 22.5) beside the tag g leap. Scan its points too, as a second lane on your spare threads: tag i in its own tag.txt, prediction = the previous k_c 79 root - 0.0215 per 0.0625 step (slope about -0.33), window +-0.015 at 0.005 plus a repeat, raw I1025-dh610/kc79_far/<D>/. The tag g lane keeps priority."
Later order, same day (hc, on the #1076 recount): the recount reruns at nice 10 "below your #1025 lanes".

## What win2 runs (checked against win2's README on origin/main before this folder was written)
win2's `I1025-win2/kc79_leap/README.md` section "The k_c 79 far scout" and `run_leap10.sh` (raw commit 0f6691f2, 2026-11-24 03:08:52 -08:00 = 11:08:52 UTC, "plan before the start"): `ell_leap.py l1kc79Lw1025i 1 79 data/sol_l1kc79Lw1025g_D21.187500.npy 21.1875 data/sol_l1kc79Lw1025g_D21.218750.npy 21.21875 22.5 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold`; 4 threads, 12 h cap by exact pid, a cap restart to D_end 22.5 authorized as before (a restart would carry a new tag: I would then follow the tag ruling of `../kc79_leg/README.md`, after checking win2's README, and record it here); the leap halves h to 0.03125 if a step fails. Seeds are the tag g records at D 21.1875 and D 21.21875 (state blobs 9d3351f6 and 5d263c46, the ones the tag g lane of `../kc79_leg/` pinned). The scout waits for the end of win2's k_c 71 leg 9, which stopped at its psi-constraint bar. Its states and records go to `I1025-win2/kc79_leap/states/` like the leap's (`sol_l1kc79Lw1025i_D<D:.6f>.npy`, `l1kc79Lw1025i.jsonl`); `fetch_point.sh` finds a state by its file name anywhere under `I1025-win2/`, so a different folder would not hide it, and prints the path it found.
Points: D = 21.21875 + n x 0.0625, so 21.28125, 21.34375, 21.40625, 21.46875, 21.53125, ... up to 22.5 (the last grid point is 22.46875; a shorter final step to 22.5 would be a point of its own). **At D 21.28125, 21.34375, 21.40625 and 21.46875 the tag g leap (h 0.03125) has a state too**; where both are scanned the two roots can be compared (information, see the predictions).

## Method, per point D (`lane_far.sh D CENTER PRED`, a copy of `../kc79_leg/lane_leg.sh`)
1. **Pin** win2's state and record by git blob as in the commit that added the state (`fetch_point.sh`, from origin/main after a fetch; exit 2 if the record lacks a row for D with kc 79 or a blob differs); `in/` holds the same readers as `../kc79_leg/in/` (blobs in `in_blobs.txt`, checked equal to the leg's).
2. **Accept** the state with `kc79_syscheck_1025.py` (29dce7ea; exit 0; `--mutate=F` and `--mutate=steps` exit 1); a refusal stops the lane and I report it.
3. **Scan** `d18_hybsign.py` (e089207a, unmodified) at CENTER-0.015 to CENTER+0.015 by 0.005 (CENTER the multiple of 0.005 nearest the prediction) plus a repeat of CENTER: 8 processes of 1 thread, in `~/Source/choptuik-large-d-1025f` at 505d8399 beside the solver worktree `-1025g` at 48c36355 (both pinned).
4. **Read** with `read_lower.py`, `repeat_check.py`, `leg_read.py` (bar 0.01; no change in the window: widen once by 0.015, as the leg's standing rule; the order does not repeat this rule and I apply it unless the coordinator says otherwise). `summarize_far.py D PRED` prints the tables.
**Prediction:** the previous k_c 79 root on this chain minus 0.0215 (the order); the first point's previous root is the measured root at D 21.21875 of the tag g leap (0.841733, the scout's seed). Bar 0.01 as on the leg (the order gives none).
**Differences from the leg's lane:** tag i (`D<D>/tag.txt`); its own lock (`/tmp/claude-1000/kc79_far.lock`), so it runs beside the tag g lane; scan processes at nice 8 (the tag g lane's scan runs at nice 5 from D 21.25 on, the recount at nice 10); `fetch_point.sh` finds the state by name; `lane_far.sh D C PRED check` runs the pins, selftests and the source check with its controls and stops before the scan; and a thread gate before the lock (below).

## Threads and priority (the cap of 20 threads of mine)
| job | threads | nice |
|---|---|---|
| tag g lane (`../kc79_leg`), while a point runs (about 27 of every 80 min) | 8 | 5 |
| this lane, while a point runs | 8 | 8 |
| #1076 recount rerun (unit i1076c), 48 h | 12 | 10 |
All three at once would be 28 of 20. `wait_and_run.sh` therefore starts this lane's scan only when the planned threads fit: 12 if unit i1076c is active, plus 8 if the tag g lane holds its lock, plus this lane's 8, at most the number in `budget.txt` (default 20; `budget.txt` absent now). The tag g lane never waits for this one, so a g point that lands while this lane runs makes 28 for its duration (the g scan and the recount are at lower nice values than this one only in the order g 5, far 8, recount 10). The coordinator is told this arithmetic; a different rule is one number in `budget.txt`.

## Tests of the lane before the first point (`test_g21.21875/`, on the tag g state at D 21.21875, pinned equal to the leg's)
`fetch_point.sh` with TAG g: exit 0, state 5d263c46 and record bf1b941f, equal to `../kc79_leg/D21.21875/in_blobs.txt`; with an absent state (tag i, D 21.28125): exit 1; with the control NEED_KC=87: exit 2. `lane_far.sh 21.21875 0.840 0.8413 dry`: selftests `0 0 1 1 0 0 1`. `... check`: source check exit 0, `--mutate=F` exit 1, `--mutate=steps` exit 1, same numbers as the leg's lane (record |F| 4.5647827663e-10, 2658 steps). The gate's lock test: held lock read as busy, released lock as free. These are tests of the machinery only; nothing is scored.

## Points (rows added as each point is done; roots det-linear, bracket = the grid step 0.005, orientation as the reader prints it)
| D | state (win2 commit, time, tag i) | source check | window | root (bracket, estimator range) | against the prediction | repeat | notes |
|---|---|---|---|---|---|---|---|

## Status
- 2026-11-24 11:15 UTC: folder, scripts and tests written; the first point D 21.28125 (prediction 0.841733 - 0.0215 = 0.8202, centre 0.820, window 0.805 to 0.835) has its README and `tag.txt`; its unit `i1025-far-21_28125` is started next and waits for win2's state.
