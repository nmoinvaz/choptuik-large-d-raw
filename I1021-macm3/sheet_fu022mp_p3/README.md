# sheet_fu022mp_p3: the sheet check of macm3's fu022mp cache after pass 3 (#1021 criterion 4), and the prefix check

Part of `I1021-macm3`. Machine: macm3 (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1, arm64), 1 thread, `nice -n 19`, read-only.
Issues https://github.com/nmoinvaz/choptuik-large-d/issues/1076 and https://github.com/nmoinvaz/choptuik-large-d/issues/1021.
Task from the coordinator (hc of 2026-11-23, after pass 3's acceptance): the sheet check of fu022mp's cache after pass 3,
the `run.sh` of dh370's `I1021-dh370/sheet_fu021p1/` with the changes below. Written 2026-11-23 09:32 UTC, before any check ran.
The pass rules are the coordinator's.

## Inputs (raw at 81794560, taken with `git show`, nothing pulled into a live clone)

| role | path in raw | lines | blob |
|---|---|---|---|
| fu022mp's cache | `I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl` | 3605 | 3a12c814 |
| pass 3's leaves | `I1021-macm3/fu022mp/m3/leaves_M3_fu022mp_pass3_r0.17.jsonl` | 533 | 2f6df7a9 |
| pass 3's count | `I1021-macm3/fu022mp/m3/count_M3_fu022mp_pass3_r0.17.json` | 336 | 876087ee |
| the record's cache | `I1021-mac/final/record/points_M3_r0.17.jsonl` | 3229 | 0a47e348 |
| sheet check | `I1021-mac/diag/sheet_check.py` |  | 2dca3139 |
| prefix check | `I1021-mac/rpi5_fu021/prefix_keys.py` |  | 32ad6e19 |

fu022mp's cache has 3605 lines, of which 30 are `fu: "mp"` rows (the extended-precision values of passes 1 to 3).
Pass 3's count has 17 unresolved leaves and 2 zeros (sum over leaves).

## Command

`run.sh` is dh370's (`run.sh.dh370`, copied from raw at the same commit) with these changes only (`run.sh.diff`; the comment
on line 2 is the only change that is not a path, a revision or the hash tool):

```
2c2
< # #1021 sheet check of rpi5's fu021 pass 1 (README.md): bash run.sh RAW PY WORK
---
> # #1021 sheet check of macm3's fu022mp cache after pass 3 (README.md): bash run.sh RAW PY WORK
6c6
< REV=${REV:-c31e459b}
---
> REV=${REV:-81794560}
14,16c14,16
< get I1021-rpi5/fu021/m3/points_M3_r0.17.jsonl "$WORK/fu/points_M3_r0.17.jsonl"
< get I1021-rpi5/fu021/m3/leaves_M3_fu021_pass1_r0.17.jsonl "$WORK/fu/leaves_M3_fu021_pass1_r0.17.jsonl"
< get I1021-rpi5/fu021/m3/count_M3_fu021_pass1_r0.17.json "$WORK/fu/count_M3_fu021_pass1_r0.17.json"
---
> get I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl "$WORK/fu/points_M3_r0.17.jsonl"
> get I1021-macm3/fu022mp/m3/leaves_M3_fu022mp_pass3_r0.17.jsonl "$WORK/fu/leaves_M3_fu022mp_pass3_r0.17.jsonl"
> get I1021-macm3/fu022mp/m3/count_M3_fu022mp_pass3_r0.17.json "$WORK/fu/count_M3_fu022mp_pass3_r0.17.json"
20,21c20,21
< CACHE=$WORK/fu/points_M3_r0.17.jsonl; LEAVES=$WORK/fu/leaves_M3_fu021_pass1_r0.17.jsonl
< COUNT=$WORK/fu/count_M3_fu021_pass1_r0.17.json; RECORD=$WORK/rec/points_M3_r0.17.jsonl
---
> CACHE=$WORK/fu/points_M3_r0.17.jsonl; LEAVES=$WORK/fu/leaves_M3_fu022mp_pass3_r0.17.jsonl
> COUNT=$WORK/fu/count_M3_fu022mp_pass3_r0.17.json; RECORD=$WORK/rec/points_M3_r0.17.jsonl
24c24
<   (cd "$WORK" && sha256sum fu/* rec/* scripts/* && wc -l fu/*.jsonl rec/*.jsonl); } > "$HERE/sha256.txt"
---
>   (cd "$WORK" && shasum -a 256 fu/* rec/* scripts/* && wc -l fu/*.jsonl rec/*.jsonl); } > "$HERE/sha256.txt"
```

From this folder, with RAW a clone of `choptuik-large-d-raw` that holds 81794560 (here the worktree
`~/Source/choptuik-large-d-raw-1076p`), PY the interpreter and WORK an empty scratch folder:

    bash run.sh RAW PY WORK

PY is `~/Source/venv-macm3-1058b/bin/python` (3.14.3, numpy 2.5.4); the scripts run unchanged with `python -I`,
`OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1` (set by `run.sh`), each check under `nice -n 19`. It writes `sha256.txt`
(commit, python, hashes of the inputs and scripts, line counts), one log per check, `exits.txt` and `summary.txt`.

## Checks (fixed before running)

| # | command | required exit | log |
|---|---|---|---|
| 1a | `sheet_check.py CACHE LEAVES --count COUNT` | 0 | `sheet_leaves.log` |
| 1b | `sheet_check.py CACHE lines` | 0 | `sheet_lines.log` |
| 1c | `sheet_check.py CACHE lines --count COUNT` | 0 | `sheet_lines_count.log` |
| 2a | `sheet_check.py CACHE lines --mutate=switch` | nonzero (1) | `sheet_lines_switch.log` |
| 2b | `sheet_check.py CACHE LEAVES --mutate=switch` | nonzero (1) | `sheet_leaves_switch.log` |
| 3a | `prefix_keys.py RECORD CACHE` | 0 | `prefix_keys.log` |
| 3b | `prefix_keys.py RECORD CACHE --mutate=edit` | nonzero (1) | `prefix_keys_edit.log` |
| 4 | `sheet_check.py RECORD lines` (dh370's extra: this invocation reads the record as xfchecks did) | 0 | `sheet_record_lines.log` |

CACHE is fu022mp's cache after pass 3, LEAVES and COUNT are pass 3's, RECORD is the record's 3229-line cache. Required exits
in `exits.txt` order: `0 0 0 1 1 0 1 0`.

## Pass rules (the coordinator's)

- `sheet_leaves` (1a) and `sheet_lines` (1b) and the count variant (1c) exit 0 with 0 flagged pairs (|dF_3| above 0.1, or
  above 0.02 with a step per length above 20 times the median: the script's thresholds).
- Both `--mutate=switch` controls (2a, 2b) exit nonzero, and each log names the flagged pair. A control that exits 0 stops
  the work: the sheet check is then not shown able to fail on these files.
- `prefix_keys` (3a) exits 0 and its `--mutate=edit` control (3b) exits nonzero.
- Check 4 adds no criterion beyond exit 0; it reproduces the record's own lines numbers (3144 valued points, 5382 pairs,
  largest |dF_3| 0.056, 0 flagged, `I1021-mac/final/record_checks/README.md`).

Reported, whatever the exits: every exit; the largest |dF_3| in the leaves mode and in the lines mode, with the number of
valued points and pairs; every pair flagged anywhere, and in particular anything flagged near A 3.5265, wf 0.2115 (the
second zero, which pass 3's recount located at A 3.526538, wf 0.211482 at xi1 0.17 and at A 3.526473, wf 0.211498 at
xi1 0.2); for each located zero whether its cell's boundary is on one sheet (1a and 1c).

For comparison (read before the run, from `I1021-dh370/sheet_fu021p1/README.md` at raw c31e459b): on fu021's pass 1 cache
(3369 lines, 512 leaves) dh370 read 3272 valued points, 5556 pairs on the lines, 1739 pairs on the leaves, largest
|dF_3| 0.056 on the lines and 0.0394 on the leaves, 0 flagged, 1 zero on one sheet; the record's cache gave 3144 valued points,
5382 pairs, 0.056, 0 flagged. This cache has, beyond fu021's first 3397 lines, the 30 `fu: "mp"` rows and the records of the three
recounts, so more valued points and pairs are expected, not a pass criterion.

Scope: the leaves mode compares only the edges of pass 3's 533 leaves, which lie inside the 11 recounted cells; the lines
mode reads the whole cache; the count holds the located zeros of the 11 cells only. An error bar here: none; the
thresholds are the script's. The check shares its inputs with the run it checks and no code beyond the cache format. It is a
screen for a jump of 0.3 or more, not a proof that every value is on the sheet.

## Results (run 2026-11-23 09:32 UTC, raw commit 8179456070e64d5626999effc3418c38fe1d3857, about 1 s wall in all)

Verdict: **PASS.** The exits are `0 0 0 1 1 0 1 0`, as required (`exits.txt`, `summary.txt`). `sha256.txt` shows the record's
cache, `sheet_check.py` and `prefix_keys.py` with the same sha256 as in dh370's run (`I1021-dh370/sheet_fu021p1/sha256.txt`);
python 3.14.3, numpy 2.5.4 (his: 3.14.10, 2.5.4). WORK was empty at the start.

### Sheet check (`sheet_leaves.log`, `sheet_lines.log`, `sheet_lines_count.log`, `sheet_record_lines.log`)

| | record (check 4) | fu021 pass 1 (dh370) | fu022mp after pass 3, lines | fu022mp after pass 3, leaves |
|---|---|---|---|---|
| valued points | 3144 | 3272 | 3457 | 3457 |
| pairs | 5382 | 5556 | 5792 | 1873 (the 533 leaves' edges) |
| median \|dF_3\|/length | 0.178 | 0.178 | 0.18 | 0.166 |
| largest \|dF_3\| | 0.056 | 0.056 | **0.056** | **0.0394** |
| flagged pairs | 0 | 0 | 0 | 0 |
| cells across a switch | | 0 of 512 | | 0 of 533 |

- "Valued" is the script's reading (`info` below 1e-8 or an ok `fix`, and a finite F_3); it does not read the 10 sigma guard.
- The record's numbers on this machine equal its README's and dh370's check 4: 3144, 5382, 0.056, 0 flagged.
- The largest |dF_3| are the record's and fu021's, to the printed digits (0.056 on the lines, 0.0394 on the leaves): no pair that
  one of the 185 valued points added since fu021's pass 1 cache makes exceeds them.
- The count (1a, 1c) has 2 zeros, both W +1, and each cell's boundary is on one sheet in the leaves and in the lines:

  | cell | located at (xi1 0.17) |
  |---|---|
  | A 3.5217206 to 3.5373456, wf 0.20654321 to 0.21279321 | (3.526538, 0.211482) |
  | A 3.4435956 to 3.4592206, wf 0.34404321 to 0.35029321 | (3.446204, 0.347602) |

- **Near A 3.5265, wf 0.2115 (the second zero): nothing is flagged**, in the leaves mode, the lines mode or the count variant.
  `near_zero.py` (my own, not part of `run.sh`; it re-reads the lines-mode pairs by the script's rules and reproduces the
  script's 3457 points, 5792 pairs, median 0.18 and largest 0.056) gives, for the zero's cell: 81 valued points, 79 pairs
  with an end in the cell, largest |dF_3| 0.0394, largest |dF_3|/length 0.698 against the median 0.18 (the script flags
  above 20 times the median with |dF_3| above 0.02), 0 flagged. The valued points nearest the zero have F_3 -0.0009 - 0.4883j (the
  zero's own point) and -0.0009 - 0.4882j (`near_zero.log`).

### Controls

- 2a, `--mutate=switch` on the lines: exit 1. It moved F_3 of (2.72343935, 1.01591821) by 0.3i; 2 pairs flagged, largest
  |dF_3| 0.301.
- 2b, the same on the leaves: exit 1. It moved F_3 of (3.755119038, 0.43154321), a point valued in pass 3, by 0.3i; 2 pairs
  flagged, largest |dF_3| 0.3, and 2 of the 533 cells across a switch (A 3.7248456 to 3.7873456, wf 0.40654321 to 0.43154321
  and 0.43154321 to 0.45654321).
- 3b, `prefix_keys.py --mutate=edit`: exit 1, with (a) turned from True to False (the record's 3229 lines are no longer the
  cache's first lines) and 0 later records of old keys not expected.

### Prefix and keys (`prefix_keys.log`)

Exit 0: the record's 3229 lines are the cache's first lines byte for byte, and 0 later records of old keys are not
expected. There are 24 later records of old keys:

| kind | lines | count | the record had them | now |
|---|---|---|---|---|
| fu row, variant default | 3231 to 3242 | 11 | 7 guard-blocked (valued3, 4.65 to 9.86 sigma) and 4 without value | accepted |
| fu row, variant s0.2 | 3230, 3234 | 2 | without value | accepted |
| `fu: "mp"` row (passes 1 to 3's valuing) | 3399 to 3404 | 6 | guard-blocked (valued3, 0.415 to 9.24 sigma) | \|R\|/sigma 3.63e+18 to 1.09e+20 |
| `argcount --retry` record, at (3.9123456, 0.20654321) | 3330, 3378, 3428, 3463, 3599 | 5 | not valued3 | still not valued3 |

(The first two rows are dh370's 13 fu rows of fu021, lines 3230 to 3242; the `--retry` record of line 3330 is his, too.
Of fu022mp's 7 pass 1 mp rows one, (3.5266034125, 0.21279321), is a key the record did not have, so 6 enter this list.)
The other 3605 - 3229 - 24 = 352 later lines are keys the record did not have.

### Notes

- As in dh370's check, the scripts' strings say "recount3" and "recount4": here the record and fu022mp's cache.
- The scope of the README stands: a screen for a jump of 0.3 or more, on the stored files, with the script's thresholds.
  It does not test whether a located zero's |R| is above the noise floor (pass 3's recount: |F| 220.5 against a floor of
  195.9 at xi1 0.17 for the second zero, and |F| 0.092 against 0.545 at xi1 0.2).
- Nothing disagrees with the record's README, with dh370's fu021 numbers or with pass 3's count.
