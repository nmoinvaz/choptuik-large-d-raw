# I1020-dh610: M = 3 relocation of #1013's two partners at xi1 0.3 and 0.17, and the extended box A 1.9-3.0, wf 0.03-0.2

Machine: dh610 (Fedora, i7-12700, 20 threads, 62 GB), beside #1003's K 49 run (5 procs). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1020 (#1013's recommendations 3 and 2; dh610 order of
the coordinator, 2026-11-19 ~10:55 UTC). Code: xfchecks' `argcount.py`, worktree `~/Source/cl-995` at wip/excited-zeros fc7dee4d, python of the main checkout's `.venv` (numpy, scipy, mpmath), 8 workers, nice 10.

## Readings, fixed before the run

- **Step 1 (relocation).** Boxes of A +- 0.05 (control: known zero, A 2.6765-2.7765, wf 0.9956-1.0356; partners: wf 0.205-0.245) counted at xi1 0.3 (`--r1=0.3`, `--nA=4 --nwf=4`), each zero located
  again at xi1 0.17 (`--r1b=0.17`). Pass: a zero of the expected sign located at both radii within 1e-4, in A and in wf separately, of its xi1 0.25 place (#1013's `count_M3_cand_r0.25.json`; the control's is
  `count_M3_cand.json`'s xi1 0.2 place). A partner not found or moving by more fails; a failed control makes the partners' verdicts uninterpretable. `reloc1020.py` evaluates it.
- **Step 2 (extended box).** `--A=1.9,3.0 --wf=0.03,0.2 --nA=8 --nwf=9` at xi1 0.2 with #1013's other step-2 settings, then the recount rungs xi1 0.25 and 0.17 of the unresolved cells. The only
  difference from #1013's step 2: F_3 seeds from #1013's xi1 0.2 points (`inputs1013/points_M3_r0.2.jsonl`, seeds only; the acceptance of a solve, |r_3| < 1e-8, is unchanged).
  Persistence: `persist1020.py` (persist1013.py's rule over the union of #1013's box and this one; its regression on #1013's three counts alone reproduces #1013's table).

## Files

| file | content |
|---|---|
| `common1020.sh`, `run1020.sh` | paths, the driver (the commands are in it) |
| `reloc1020.py`, `persist1020.py`, `persist1013_orig.py` | the step 1 evaluator, the persistence evaluator, #1013's evaluator it imports |
| `inputs1013/` | #1013's three counts and the two points files it seeds from (copied from `I1013-dh610/m3/`) |
| `m3/` | points caches (`points_M3_r*.jsonl`), `count_<tag>.json`, `leaves_<tag>.jsonl` |
| `logs/`, `exits_1020.txt`, `memlog_1020.log` | each step's log, exits, alert-only memory log |

## Results, 2026-11-19

- Step 1 (11:00-11:24 UTC): `reloc1020.py` exits 1, all three boxes FAIL (`logs/reloc_eval_step1.log`; its controls `logs/reloc_selftest.log`, `logs/reloc_eval_mutate_shift.log`). Control: no values at xi1 0.3 (16 of 16 corners unusable). Minus partner: located at xi1 0.3 within 8e-12 of its xi1 0.25 place, no values at xi1 0.17. Plus partner: box winding +1.000, zero not located (one of two unresolved cells).
- Step 2 (11:24-12:15 UTC): `M3_ext` (xi1 0.2, A 1.9-3.0, wf 0.03-0.2, `--nA=8 --nwf=9`, 191 s): 75 leaves after 1 split, 123 points, 12 resolved, 63 unresolved cells, sum over leaves 0. Rung xi1 0.25 (2588 s): 429 leaves after 122 splits, 1565 points, sum -1, 50 unresolved, one zero, sign -1 at (2.338793, 0.096238) (|R| 2.9e-9), not located at xi1 0.2. Rung xi1 0.17 (266 s): 50 leaves, 0 splits, 84 points (no point with a value), 50 unresolved.
- `persist_union_with_partners.txt` and `persist_union_without_partners.txt`: `persist1020.py --counts inputs1013/count_M3_cand*.json --counts m3/count_M3_ext*.json` (the second with `--exclude` of the two partners that failed step 1).
