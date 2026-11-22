# sheet_fu021p1: the sheet check of rpi5's fu021 pass 1 points (#1021 criterion 5), and the prefix check of its cache

Part of `I1021-dh370`. Machine: dh370-fedora (i7-8700, 12 threads, 31 GB, Linux 7.3.3), 1 thread, `nice -n 19`,
read-only. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1021. Task from the coordinator (hc of 2026-11-22):
criterion 5 of `I1021-mac/rpi5_fu021/README.md`, "the counts are on hold until xfchecks' sheet check of fu021's new
points passes". This README was written before any check ran, except check 4 (marked) and the results.
The `running` label was already on #1021, so I leave it.

## Inputs (raw origin/main at c31e459b, taken with `git show`, nothing pulled into a live clone)

| role | path in raw | lines |
|---|---|---|
| fu021's cache | `I1021-rpi5/fu021/m3/points_M3_r0.17.jsonl` | 3369 |
| pass 1's leaves | `I1021-rpi5/fu021/m3/leaves_M3_fu021_pass1_r0.17.jsonl` | 512 |
| pass 1's count | `I1021-rpi5/fu021/m3/count_M3_fu021_pass1_r0.17.json` | |
| the record's cache | `I1021-mac/final/record/points_M3_r0.17.jsonl` | 3229 |
| sheet check | `I1021-mac/diag/sheet_check.py` | |
| prefix check | `I1021-mac/rpi5_fu021/prefix_keys.py` | |

`run.sh` prints the sha256 of each input and of both scripts into `sha256.txt`. The scripts are run unchanged, with
`python -I` (Python 3.14.10, numpy 2.5.4, from the venv of the `choptuik-large-d-961` worktree), `OMP_NUM_THREADS=1`
and `OPENBLAS_NUM_THREADS=1`.

## Command

From this folder, with RAW a clone of `choptuik-large-d-raw` whose `origin/main` holds c31e459b, PY the interpreter and
WORK an empty scratch folder:

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
| 4 | `sheet_check.py RECORD lines` (extra, added after the first run of 1 to 3 had exited as required) | 0 | `sheet_record_lines.log` |

CACHE is fu021's 3369-line cache, LEAVES and COUNT are pass 1's, RECORD is the record's 3229-line cache. Required exits
`0 0 0 1 1 0 1 0`.

Check 4 reproduces the record's own lines numbers with the same script on the record's cache: 3144 valued points, 5382
pairs, largest |dF_3| 0.056, 0 flagged (`record_checks/README.md`, written before and not read from fu021's output). It
shows that this invocation reads the record as xfchecks did, so that fu021's excess over it (points, pairs) is its new
points, and that fu021's largest |dF_3| then bounds the new points' pairs. It adds no pass criterion beyond exit 0 and
those four numbers.

Pass criteria:
- Check 1 passes when 1a and 1b exit 0, so 0 flagged pairs (|dF_3| > 0.1, or |dF_3| > 0.02 with a step per length above
  20 times the median). I report valued points, pairs, largest |dF_3| and flagged pairs of each run, and for each located
  zero whether its cell's boundary is on one sheet. 1c and 2b are extras on the same script, and I report them too.
- Check 2 passes when each control exits 1 and its log names the flagged pair. A control that exits 0 stops the work,
  and the sheet check is then not shown able to fail on these files.
- Check 3 passes when 3a exits 0 (the record's 3229 lines are fu021's first lines byte for byte, and each later record
  of an old key is an accepted fu row for a point the record had without a usable value, or an argcount `--retry`
  record of a point the record had not valued3) and 3b exits 1. I report what the later records of old keys are, by
  kind (fu row or `--retry` record), from the log. rpi5's README expects 13 accepted fu rows (3229 -> 3242) and 127 lines
  the recount added (3242 -> 3369).

Compared with the record's own sheet check (`I1021-mac/final/record_checks/README.md`): 3144 valued points; 2976 pairs
on the leaves and 5382 on the lines; largest |dF_3| 0.0394 on the leaves and 0.056 on the lines; 0 flagged; the record's
3 zeros each on one sheet. fu021's numbers are compared with these as read, and any disagreement is reported.

Scope: the leaves mode compares only the edges of pass 1's 512 leaves, which lie inside the 11 recounted cells, so it
covers those cells and not the rest of the record's box. The lines mode reads the whole cache. The count holds the
located zeros of the 11 cells only.

An error bar here: none. The two thresholds (0.1 and 0.02, ratio 20) are the script's, set from the distribution of
|dF_3| in the stored files (the script's docstring). The check shares its inputs with the run it checks, and no code
with it beyond the cache format. The pass is a screen for a jump of 0.3 or more, not a proof that every value is on the
sheet.

## Results (run 2026-11-22 07:30 UTC, raw commit c31e459b, 2 s CPU in all)

Verdict: **PASS.** The exits are `0 0 0 1 1 0 1 0`, as required. fu021's pass 1 cache has no pair across a sheet, so the
counts are released as far as criterion 5 goes.

### Sheet check (`sheet_leaves.log`, `sheet_lines.log`, `sheet_lines_count.log`, `sheet_record_lines.log`)

| | record (check 4, and its README) | fu021 pass 1, lines | fu021 pass 1, leaves |
|---|---|---|---|
| valued points | 3144 | 3272 (+128) | 3272 |
| pairs | 5382 | 5556 (+174) | 1739 (the 512 leaves' edges) |
| median \|dF_3\|/length | 0.178 | 0.178 | 0.167 |
| largest \|dF_3\| | 0.056 | 0.056 | 0.0394 |
| flagged pairs | 0 | 0 | 0 |
| cells across a switch | | | 0 of 512 |

- The record's numbers on this machine (check 4) equal those in its README: 3144, 5382, 0.056, 0 flagged. Its leaves'
  2976 pairs are the record's whole box and fu021's 1739 are the 11 recounted cells, so those two counts are not
  comparable. The record's leaves' largest |dF_3| 0.0394 is the one quoted from its README, and fu021's equals it.
- fu021's largest |dF_3| equal the record's, to the printed digits (0.056 on the lines, 0.0394 on the leaves), so no pair
  that one of its 128 new valued points makes exceeds them. All of fu021's pairs are at most 0.056, against the flag
  at 0.1.
- The count has 1 zero, W +1, in cell A 3.4435956 to 3.4592206, wf 0.34404321 to 0.35029321, located at
  (3.446204, 0.347602). Its cell's boundary is on one sheet, against the leaves' pairs (1a) and the lines' pairs (1c).
- This check does not test whether that zero's |R| is above the noise floor (rpi5 reports |R| 16.8 against a floor of
  36.1 at xi1 0.17).

### Controls

- 2a, `--mutate=switch` on the lines: exit 1. It moved F_3 of (2.72343935, 1.01591821) by 0.3i, and the check flagged 2
  pairs, largest |dF_3| 0.301.
- 2b, the same on the leaves: exit 1, 3 flagged pairs of largest |dF_3| 0.3 at (3.3107831, 0.21904321), and 3 of the 512
  cells across a switch.
- 3b, `prefix_keys.py --mutate=edit`: exit 1, with (a) turned from True to False (the edit is in line 101 of
  fu021's cache, so the record's 3229 lines are no longer its first lines) and no unexpected later record.

### Prefix and keys (`prefix_keys.log`)

Exit 0: the record's 3229 lines are fu021's first lines byte for byte, and 0 later records of old keys are unexpected.
There are 14 later records of old keys, in lines 3230 to 3242 and 3330:

| kind | lines | count | the record had them | now |
|---|---|---|---|---|
| accepted fu row, variant default | 3231 3232 3233 3235 3236 3237 3238 3239 3240 3241 3242 | 11 | |
| accepted fu row, variant s0.2 | 3230 3234 | 2 | |
| (of those 13) for a point without value | 3230 3233 3234 3235 3239 3242 | 6 | not valued3 | \|R\|/sigma 6.7e4 to 2.2e6 |
| (of those 13) for a guard-blocked point | 3231 3232 3236 3237 3238 3240 3241 | 7 | valued3, 4.65 to 9.86 sigma | 13.2 to 34.4 sigma |
| argcount `--retry` record | 3330 | 1 | not valued3, at (3.9123456, 0.20654321) | still not valued3 |

The 13 fu rows are the "13 of 20 accepted" of rpi5's value step. The other lines (3243 to 3369 but 3330) are keys the
record did not have. `prefix_keys.py` takes an fu row as expected when its point had no usable value in the record. It
does not test the row against fu_value's rules, and the printed |R|/sigma of 13.2 and above shows the 10 sigma one for
the 7 guard points.

### Notes

- The scripts' strings say "recount3" and "recount4" (their #1013 names). Here they mean the record and fu021.
- The scope limits of the README's last paragraph stand: a screen for a jump of 0.3 or more, on the stored files only.
- Nothing disagrees with the record's README or with rpi5's: its 3242 and 3369 lines, 13 accepted rows and 1 zero all
  appear above.
