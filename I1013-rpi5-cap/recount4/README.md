# recount4: #1013's 13 unresolved cells of recount3 valued again from other starts and seeds at xi1 0.18 (xfchecks' driver run_fu018.sh), then recounted

Part of `I1013-rpi5-cap` (rpi5, Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi, agent claude-me2; issue https://github.com/nmoinvaz/choptuik-large-d/issues/1013). Started 2026-11-21 00:33:05 UTC on the coordinator's word (message of 21 Nov, "GO for #1013's next step, recount4 by the start-and-seed-variant (fu) route on all 13 unresolved cells").

## Plan and criteria (xfchecks', fixed before the run)
`I1021-mac/rpi5_fu018/` of the raw repository at 9d64a727 holds the driver (`run_fu018.sh`, blob 5f6dcec6), its README (blob 270d440b, the 13 cells, the 5 variants, the pass loop, the criteria), `fu_value.py` (dh610's, raw 18338ce4, sha256 b36fb3e9...) and `fu_value018.py` (sha256 2b4a1bf5...). In short:
- 9 points without value in recount3's unresolved leaves (7 at w/w_inf 1.0065-1.3065, 2 at the guard: (4.063517475, 0.51904321) at |R|/sigma 9.18 and (4.2685956, 0.54404321) at 9.8) are valued again in 5 variants (default, s0.25, seed2, seed3, s0.25seed2), each run capped at 3600 s, 45 runs per pass at 4 processes. A row is accepted only by fu_value.py's tests: valued (|r3| < 1e-8 or the continuation's fix ok), max|Y| <= 100, |R| >= 10 sigma, |dF3| to the nearest valued neighbour <= 0.1.
- Each pass: value step (10 h cap) -> retests `--mutate=f3` (must fire in a pass that accepted a row) and `--mutate=lowguard` (must fire where the guard alone blocked a row) -> if nothing accepted, end -> recount of the 13 cells with recount3's arguments (16 h cap) -> if 0 unresolved cells, end. At most 3 passes. At the end `argcount_samebits.py` compares recount3's 735-line cache with recount4's (must exit 0).
- Criteria 1 to 6 as in the driver's README: (1) argcount selftest and five mutations `0 1 1 1 1 1`, `fu_value018.py --selftest` 0 and with `--break` 1; (2) acceptance only by those tests; (3) the retests as above, else reported vacuous; (4) samebits exit 0; (5) counts reported as printed and held until xfchecks' sheet check of recount4 passes; (6) the step is accepted at 0 unresolved cells, or when each unresolved leaf is named with its blocking points and each variant's cause.

## Command and setup
From the live raw clone `~/Source/choptuik-large-d-raw` (the root, `$PWD` as RAW):
`bash I1021-mac/rpi5_fu018/run_fu018.sh ~/Source/cl-1013fix ~/Source/venv-choptuik/bin/python "$PWD" > I1013-rpi5-cap/recount4_driver.out 2>&1` (run in the background by the tool; `I1013-rpi5-cap/recount4_driver.start` has the start and `driver exit` lines).
- Code: worktree `~/Source/cl-1013fix` at `wip/argcount-m3-bounds` 6da7da7b, no local changes (the driver checks). Python 3.13.7, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0.
- Deviation from the driver's README: the live clone is not sparse, is 886 commits behind and holds my folders untracked, so a pull would refuse. I copied `I1021-mac/rpi5_fu018/` from the push worktree (`~/Source/choptuik-large-d-raw-964`, raw 9d64a727 or later) with `cp -a`, checked it with `diff -r` (identical) and the driver's own `SHA256SUMS` check. No pull in the live clone. Recount3's four inputs in this clone match `in/SHA256SUMS_recount3` (the driver checks again).
- Pushes during the run come only from the push worktree (rsync of this folder), never from the live clone.
- Beside it nothing else runs; the driver uses 4 processes at nice 10.

## Runs
(filled in as the run goes)
