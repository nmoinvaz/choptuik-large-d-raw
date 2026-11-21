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
Stage 1 (`locate018.py run`) exit 0, 14:04:11-15:31:17 UTC (1 h 27 min). `locate018.py check` exits `0 1 1` (plain, `--mutate=shift`, `--mutate=sign`), as required (`logs/check.log`):

| target | Newton's end (argcount `locate_many`, 0.18) | sign | \|R\| | stage 1 |
|---|---|---|---|---|
| U1 (want +1) | (4.0624743, 0.51893798), inside U1 | +1 | 763 (0.338 sigma) | located |
| U2 (want -1) | (4.2700301, 0.54449949), inside U2 | -1 | 5.92e4 (0.334 sigma) | located |
| C0 planted at P0 (3.9623456, 0.5615432) | (3.9623456, 0.5615432) to 1e-13 | +1 | 1.9e-7 | PASS |

The shift control (P0 moved one box width in A) FAILs and the sign control FAILs, as required. Under the sign mutation both unions are reported "not located, nearest": U1 (4.0623102, 0.51888029), 0.151 sigma, and U2 (4.2701146, 0.54447804), 0.177 sigma, of 60 new points each. `leaf_boxes.jsonl` holds the three relocation boxes (B1 A 4.0562-4.0718 x w 0.51394-0.52644, B2 A 4.2638-4.2794 x w 0.53950-0.55200, C0). Stage 2 plain recount started 15:31:17.

Driver: start 2026-11-21 14:04:04 UTC, `driver exit 0` 20:56:00 UTC (6 h 52 min), `end` line in `logs/exits.txt`. All the required exits came out as required:

| step | time (UTC) | length | exit |
|---|---|---|---|
| argcount selftest, 5 mutations | 14:04 | | `0 1 1 1 1 1` |
| locate018 and plant_check selftests | | | `0 0` |
| union_winding, `--mutate=conj` | | | `0 1` |
| stage 1 `run` | 14:04:11-15:31:17 | 1 h 27 min | 0 |
| stage 1 check, shift, sign | | | `0 1 1` |
| stage 2 plain recount | 15:31:17-18:03:59 | 2 h 33 min (count's own 9162 s) | 0 |
| stage 2 plant recount (`--plant=P0`) | 18:03:59-20:56:00 | 2 h 52 min (10321 s) | 0 |
| check2, shift, sign | | | `0 1 1` |
| plant_check, shift | | | `0 1` |
| samebits recount3 -> loc018 | | | 0 |

### Stage 2, plain count at xi1 0.18 (3 boxes, 0 splits, 977 points, 0 unresolved cells)
| box | winding (boundary) | zeros | argcount's Newton at 0.18 | at 0.17 (`--r1b`) | check2 |
|---|---|---|---|---|---|
| B1 in U1: A 4.0562-4.0718 x w 0.51394-0.52644 | +1, resolved | 1, sign +1 | none | (4.068055, 0.520571), sign +1, \|R\| 4.3e4 against a floor of 4.1e4 | PASS: counted, not located |
| B2 in U2: A 4.2638-4.2794 x w 0.53950-0.55200 | -1, resolved | 1, sign -1 | (4.2700036, 0.54450292), \|R\| 1.6e4, sign -1; 2.7e-5 in A and 3.4e-6 in w from stage 1's point | none | PASS: located |
| C0: A 3.9561-3.9717 x w 0.55654-0.56904 | 0, resolved | 0 | | | PASS |

`check2` with `--mutate=sign` FAILs (all three boxes) and with `--mutate=shift` FAILs on B2, as required.

### Stage 2, planted count (`--plant=P0` (3.9623456, 0.5615432), 1109 points, 0 unresolved cells)
B1 +1, B2 -1, C0 +1. C0's zero is located at P0 to 6.2e-14 with Jacobian sign +1 (\|R\| 1.9e-7), at 0.17 too. `plant_check.py` PASSes: one +1 zero whose cell contains P0; C0 winds the plain winding plus 1; B1 and B2 as in the plain count; the 2 zeros outside C0 are the plain count's. With `--mutate=shift` (the plant point moved to (4.2123456, 0.5615432)) it FAILs. Its line "same 32 boxes" is the copied script's fixed text; here it compares the 3 boxes. In the planted run argcount's Newton in B1 ends at (4.049986, 0.514842), outside B1 (A below 4.0562) and with Jacobian sign -1, and in B2 at (4.270019, 0.544457), sign -1.

### samebits
712 of 712 valued records of recount3's cache are bit-identical in loc018's cache (1132 lines: recount3's 735 unchanged, then 397 new lines); 8 old points without value, 0 valued now; `bit check: PASS`. (recount4's criterion-4 failure does not arise here: loc018 appends no fu row.)

### Criteria (the driver README's)
| # | criterion | result |
|---|---|---|
| 1 | stage 1: C0 planted passes; each union has a point; check, shift, sign exit `0 1 1` | met: U1 located at (4.0624743, 0.51893798), sign +1, \|R\| 763 (0.34 sigma); U2 at (4.2700301, 0.54449949), sign -1, 5.92e4 (0.33 sigma) |
| 2 | stage 2 check2 on the plain count, `0 1 1` | met: B1 and B2 wind +1 and -1, resolved, one zero each, of sign W(U); B2 located within 0.1 of the box size of stage 1's point; B1 counted, not located; C0 0 |
| 3 | plant_check PASS, shift FAIL | met |
| 4 | samebits exit 0 | met |
| 5 | xfchecks' sheet check of the new points | pending (xfchecks') |

What the run shows: in each lower cell a zero of sign W(U) is counted in a box under 0.02 that lies inside U (U1: B1, +1; U2: B2, -1). U2's is located (Newton, Jacobian sign -1, 2.7e-5 in A from stage 1's point). U1's is counted; stage 1's Newton point (4.0624743, 0.51893798) has sign +1, but stage 2's Newton in B1 does not confirm it (none in the plain count, an end outside B1 with sign -1 in the planted count), which is the noise-floor behavior xfchecks' dry run found: B1's Jacobian sign is not determined at its floor. By additivity the rest of each union (U minus its box) winds 0. A pair of opposite sign inside a box is not excluded: argcount's resolution test applies to whole cells only.

### Cost and load
CPU summed from the per-point lines of the logs: stage 1 13134 s (136 point lines), plain 22295 s (208), plant 25757 s (236), 61186 s in all (17.0 h of CPU in 6 h 52 min of wall, so about 2.5 cores on average: two `winding2.py` jobs of the negative-mass project ran at nice 10 beside it for most of the run). Memory, sampled with `ps` and `free -m` (no peak was recorded): the main process 33-36 MB, a spawn worker about 81 MB; the system used 2.1-2.3 GB of 7.9 GB with 5.6-5.8 GB available; swap 481 MB of 1 GB in use at the end (not attributed to this run). New cache lines: 397 at 0.18, 183 at 0.17 (the 0.17 file has 813 lines, recount3's seed file 630).

### Deviations and discrepancies
- The live clone could not pull; `rpi5_loc018/` was copied from the push worktree (identical, `SHA256SUMS` check passed).
- The Mac's dry run and this run agree on B2 (located, sign -1) and on B1 (counted, not located); the Mac's stage 1 had no Newton point for U1 (it left the cell's double after 18 steps) and used the nearest point, while this run's Newton ended inside U1 with sign +1. The Mac's stage 1 used 2 processes; these differences are reported, not explained.
- Nothing else differs from the driver README.
