# loc018: the locate at xi1 0.18 of the zeros in recount3's two lower unions U1 and U2 (xfchecks' scripts, run on rpi5)

Part of `I1013-rpi5-cap`. Machine: rpi5, Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi, agent claude-me2.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1013 (also #1021). Started 2026-11-21 14:04:04 UTC on the
coordinator's follow-on after recount4: "loc018, the locate at 0.18, with xfchecks' scripts. Start it only after recount4's
driver has written its end line and you have pushed recount4."

## Plan and criteria (xfchecks', fixed before the run)
`I1021-mac/rpi5_loc018/` (raw 9b9c59af): `run_loc018.sh` (the driver), `locate018.py`, `plant_check.py`,
`union_winding.py`, `SHA256SUMS`, `in/SHA256SUMS_recount3`, and the README with the stages and the criteria 1 to 5.
In short: the driver reads recount3's cache (pinned by sha256, not recount4's), checks the selftests, then
- stage 1 (`locate018.py run`, 4 processes at nice 10, 8 h cap): argcount's Newton (`locate_many`) from the centres of
  U1 (4.0654706, 0.51904321) and U2 (4.2685956, 0.54404321), plus a control from C0 on a map with a +1 planted at P0;
- stage 2 (8 h cap per count): three relocation boxes B1, B2, C0 recounted plain and with the plant, `--r1b=0.17`;
- the checks: stage 1 `check` (and `--mutate=shift`, `--mutate=sign`), `check2`, `plant_check`, and `argcount_samebits.py`
  recount3 -> loc018 (exit 0). B1's zero is counted, not located (its Jacobian sign is not determined at its noise floor).
- Required exits: argcount selftest and 5 mutations `0 1 1 1 1 1`; locate018 and plant_check selftests `0 0`; union_winding
  and `--mutate=conj` `0 1`; stage 1 check, shift, sign `0 1 1` or `2 1 1`; check2, shift, sign `0 1 1`; plant_check,
  shift `0 1`; samebits `0`. Any other exit stops the work and is posted.
- xfchecks' sheet check of the new points comes before the result is used.

## Command and setup
From the live raw clone root (`$PWD` as RAW):
`bash I1021-mac/rpi5_loc018/run_loc018.sh ~/Source/cl-1013fix ~/Source/venv-choptuik/bin/python "$PWD" > I1013-rpi5-cap/loc018_driver.out 2>&1`
(run in the background by the tool; `../loc018_driver.start` has the start and `driver exit` lines).
- Code: `~/Source/cl-1013fix` at 6da7da7b, no local changes. Python 3.13.7, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0.
- Deviation from the coordinator's step 2: the live clone is not sparse, is far behind and holds my folders untracked, so I
  did not pull. I copied `I1021-mac/rpi5_loc018/` from the push worktree (`~/Source/choptuik-large-d-raw-964`, last commit
  touching the folder 9b9c59af) with `cp -a`, checked `diff -r` (identical) and the driver's `SHA256SUMS` check.
- Start condition: recount4's `end` line (2026-11-21 14:01:48) is in `../recount4/logs/exits.txt` and recount4 is pushed
  (raw 7e0e9c22). recount4 left both lower cells unresolved, so the coordinator's "do not start" case does not apply.
- Pushes during the run come only from the push worktree (rsync of `I1013-rpi5-cap/`).

## Runs
Start 2026-11-21 14:04:04 UTC. Before stage 1 (from `logs/exits.txt`): argcount selftest and 5 mutations `0 1 1 1 1 1`;
locate018 and plant_check selftests `0 0`; union_winding PASS and `--mutate=conj` FAIL, exits `0 1`. Stage 1 started 14:04:11.
(filled in as the run goes)
