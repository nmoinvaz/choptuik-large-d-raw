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

## Results (run 2026-11-22 11:02 UTC, raw commit 425ba356, 2.2 s of wall in all, 1 process, nice 19)

Verdict: **PASS.** The exits are `0 0 0 1 1 0 1 0`, as required. fu021's final cache has no pair across a sheet, so the
counts of pass 2 (and of pass 1) are released as far as criterion 5 goes.

The inputs are the pushed ones: `sha256.txt` has the final cache at 981f49fc... (the one rpi5's end post quotes), the
record's cache at ff39089e..., `sheet_check.py` at a157c277... and `prefix_keys.py` at 1ace1313..., the same two scripts
and the same record as pass 1's check.

### Sheet check (`sheet_leaves.log`, `sheet_lines.log`, `sheet_lines_count.log`, `sheet_record_lines.log`)

| | record (check 4) | fu021 pass 1, lines (929dceca) | fu021 final, lines | fu021 pass 1, leaves | fu021 final, leaves |
|---|---|---|---|---|---|
| valued points | 3144 | 3272 | 3294 | 3272 | 3294 |
| pairs | 5382 | 5556 | 5597 | 1739 | 1760 |
| median \|dF_3\|/length | 0.178 | 0.178 | 0.178 | 0.167 | 0.166 |
| largest \|dF_3\| | 0.056 | 0.056 | 0.056 | 0.0394 | 0.0394 |
| flagged pairs | 0 | 0 | 0 | 0 | 0 |
| cells across a switch | | | | 0 of 512 | 0 of 518 |

- The final cache has 22 more valued points than pass 1's (3294 against 3272) and 150 more than the record's, with 41
  more pairs on the lines (215 more than the record's) and 21 more on the 518 leaves' edges. The record's check, run here
  (check 4), gives its README's numbers: 3144, 5382, 0.056, 0 flagged.
- The largest |dF_3| are the same as the record's and as pass 1's, to the printed digits (0.056 on the lines, 0.0394 on
  the leaves). So no pair that one of the 22 added valued points makes exceeds them, and every pair is at most 0.056,
  against the flag at 0.1. This covers pass 2's three accepted points, (3.3498456, 1.05654321),
  (3.527579975, 0.21279321) and (3.7248456, 1.08154321), whose own |dF_3| to the nearest valued neighbour in
  `fu021/logs/value_pass2.log` are 0.0092, 0.00049 and 0.0052.
- The count has 1 zero, W +1, in cell A 3.4435956 to 3.4592206, wf 0.34404321 to 0.35029321, at (3.446204, 0.347602). Its
  cell's boundary is on one sheet, against the leaves' pairs (1a) and the lines' pairs (1c). This check does not test
  whether that zero's |R| is above the noise floor: it is counted, not located (|R| 16.8 against 36.1 at xi1 0.17).
- The check reads the 3294 valued points of the whole cache on the lines and the edges of the 518 leaves (the 11 recounted
  cells) on the leaves. The scope paragraph above stands.

### Controls

- 2a, `--mutate=switch` on the lines: exit 1. It moved F_3 of (2.72343935, 1.01591821) by 0.3i (the same point as in
  pass 1's check), and the check flagged 2 pairs, largest |dF_3| 0.301.
- 2b, the same on the leaves: exit 1, 3 flagged pairs of largest |dF_3| 0.3 at (3.3107831, 0.21904321), and 3 of the 518
  cells across a switch.
- 3b, `prefix_keys.py --mutate=edit`: exit 1, with (a) turned from True to False (the edit makes the record's 3229
  lines no longer the first lines) and no unexpected later record.

### Prefix and keys (`prefix_keys.log`)

Exit 0: the record's 3229 lines are fu021's first lines byte for byte, and 0 later records of old keys are unexpected.
There are 15 later records of old keys, in lines 3230 to 3242, 3330 and 3378:

| kind | lines | count | the record had them | now |
|---|---|---|---|---|
| accepted fu row, variant default | 3231 3232 3233 3235 3236 3237 3238 3239 3240 3241 3242 | 11 | | |
| accepted fu row, variant s0.2 | 3230 3234 | 2 | | |
| (of those 13) for a point without value | 3230 3233 3234 3235 3239 3242 | 6 | not valued3 | \|R\|/sigma 6.7e4 to 2.2e6 |
| (of those 13) for a guard-blocked point | 3231 3232 3236 3237 3238 3240 3241 | 7 | valued3, 4.65 to 9.86 sigma | 13.2 to 34.4 sigma |
| argcount `--retry` record | 3330 3378 | 2 | not valued3, at (3.9123456, 0.20654321) | still not valued3 |

These are pass 1's 14 records plus the second `--retry` record of (3.9123456, 0.20654321) (line 3378, from pass 2's
recount). The 13 fu rows are pass 1's "13 of 20 accepted". Pass 2's 3 accepted rows are for keys the record did not have
(points that pass 1's refinement created), so they are not in this list. `prefix_keys.py` takes an fu row as expected
when its point had no usable value in the record; it does not test the row against fu_value's rules, and the printed
|R|/sigma of 13.2 and above shows the 10 sigma one for the 7 guard points.

### Notes

- The scripts' strings say "recount3" and "recount4" (their #1013 names). Here they mean the record and fu021.
- Nothing disagrees with the record's README, with pass 1's check, or with rpi5's end post: its 3397 lines (sha256
  981f49fc...), 518 leaves, 1 zero and 16 accepted fu rows (13 old keys, 3 new keys) all appear above.
- The scope limits stand: a screen for a jump of 0.3 or more, on the stored files only; the zero's |R| against its noise
  floor is not tested here.
