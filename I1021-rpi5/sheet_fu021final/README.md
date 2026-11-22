# sheet_fu021final: the sheet check of rpi5's fu021 final cache (#1021 criterion 5), and the prefix check of that cache

Part of `I1021-rpi5`. Machine: rpi5, Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi, agent claude-me
(session choptuik-rpi5-i1021), 1 process, `nice -n 19`, read-only. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1021. Task from the coordinator (hc of 2026-11-22 ~11:05 UTC):
criterion 5 of `I1021-mac/rpi5_fu021/README.md`, "the counts are on hold until xfchecks' sheet check of fu021's new points
passes", here for fu021's final cache (pass 1 passed: `I1021-dh370/sheet_fu021p1`, raw 929dceca, #1021 comment 7075944014).
This README is written before any check ran; the results follow it. The `running` label was already on #1021, so I
leave it.

## Inputs (raw origin/main at 425ba356, taken with `git show`, nothing pulled into a live clone)

| role | path in raw | lines |
|---|---|---|
| fu021's final cache | `I1021-rpi5/fu021/m3/points_M3_r0.17.jsonl` | 3397 |
| pass 2's leaves | `I1021-rpi5/fu021/m3/leaves_M3_fu021_pass2_r0.17.jsonl` | 518 |
| pass 2's count | `I1021-rpi5/fu021/m3/count_M3_fu021_pass2_r0.17.json` | |
| the record's cache | `I1021-mac/final/record/points_M3_r0.17.jsonl` | 3229 |
| sheet check | `I1021-mac/diag/sheet_check.py` | |
| prefix check | `I1021-mac/rpi5_fu021/prefix_keys.py` | |

`run.sh` prints the sha256 of each input and of both scripts into `sha256.txt`. The scripts are run unchanged, with
`python -I` (the venv's Python 3.13.7, numpy 2.5.4; pass 1's check ran Python 3.14.10 on another machine),
`OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`.

## Command

From this folder, with RAW a clone of `choptuik-large-d-raw` that holds 425ba356, PY the interpreter and WORK an empty
scratch folder:

    bash run.sh RAW PY WORK

It writes `sha256.txt`, one log per check below, `exits.txt` (the exit codes in the order of the table) and
`summary.txt`.

## Checks (fixed before running)

| # | command | required exit | log |
|---|---|---|---|
| 1a | `sheet_check.py CACHE LEAVES --count COUNT` | 0 | `sheet_leaves.log` |
| 1b | `sheet_check.py CACHE lines` | 0 | `sheet_lines.log` |
| 1c | `sheet_check.py CACHE lines --count COUNT` (extra: the zero's cell against the lines' pairs) | 0 | `sheet_lines_count.log` |
| 2a | `sheet_check.py CACHE lines --mutate=switch` | 1 | `sheet_lines_switch.log` |
| 2b | `sheet_check.py CACHE LEAVES --mutate=switch` (extra: the leaves mode's control) | 1 | `sheet_leaves_switch.log` |
| 3a | `prefix_keys.py RECORD CACHE` | 0 | `prefix_keys.log` |
| 3b | `prefix_keys.py RECORD CACHE --mutate=edit` | 1 | `prefix_keys_edit.log` |
| 4 | `sheet_check.py RECORD lines` (extra: this invocation read on the record, as pass 1's check did) | 0 | `sheet_record_lines.log` |

CACHE is fu021's 3397-line final cache, LEAVES and COUNT are pass 2's, RECORD is the record's 3229-line cache. Required
exits `0 0 0 1 1 0 1 0`.

Pass criteria:
- Check 1 passes when 1a and 1b exit 0, so 0 flagged pairs (|dF_3| > 0.1, or |dF_3| > 0.02 with a step per length above
  20 times the median). I report valued points, pairs, largest |dF_3| and flagged pairs of each run, and whether the
  located zero's cell boundary is on one sheet. 1c and 2b are extras on the same script, and I report them too.
- Check 2 passes when each control exits 1 and its log names the flagged pair. A control that exits 0 stops the work,
  and the sheet check is then not shown able to fail on these files.
- Check 3 passes when 3a exits 0 (the record's 3229 lines are fu021's first lines byte for byte, and each later record
  of an old key is an accepted fu row for a point the record had without a usable value, or an argcount `--retry`
  record of a point the record had not valued3) and 3b exits 1. I report what the later records of old keys are, by
  kind (fu row or `--retry` record), from the log.

Compared with, as read: pass 1's check (`I1021-dh370/sheet_fu021p1`, 929dceca): 3272 valued points; lines 5556 pairs,
largest |dF_3| 0.056, 0 flagged; leaves 1739 pairs, 0.0394, 0 flagged; 14 later records of old keys (13 fu rows and 1
`--retry` record). The record's own (`I1021-mac/final/record_checks/README.md`): 3144 valued points, lines 5382 pairs
and 0.056, leaves 2976 pairs and 0.0394. Expected from the driver's `exits.txt`: 16 accepted fu rows in all (13 + 3)
and a second `--retry` record of (3.9123456, 0.20654321) (lines 3330 and 3378 of prefix_keys' list). Any disagreement is
reported.

Scope: the leaves mode compares only the edges of pass 2's 518 leaves, which lie inside the 11 recounted cells, so it
covers those cells and not the rest of the record's box. The lines mode reads the whole cache. The count holds the
located zeros of the 11 cells only: here 1 zero, W +1, counted, not located (|R| 16.8 under its noise floor 36.1), which
this check does not test.

An error bar here: none. The two thresholds (0.1 and 0.02, ratio 20) are the script's, set from the distribution of
|dF_3| in the stored files (the script's docstring). The check shares its inputs with the run it checks and no code with
it beyond the cache format. The pass is a screen for a jump of 0.3 or more, not a proof that every value is on the sheet.
