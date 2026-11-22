# I1021-mac/fu021_controls: xfchecks' recomputation of fu021's retest controls from its rows (criterion 3)

The Mac, by the coordinator session (hc t5), 2026-11-22, for https://github.com/nmoinvaz/choptuik-large-d/issues/1021.

Criterion 3 of `../rpi5_fu021/README.md`: `--mutate=f3` must fire in every pass that accepted a row and
`--mutate=lowguard` in every pass where the guard alone blocked a row, and xfchecks recomputes both from the rows with
`../merge_fu/fu_controls.py` (unchanged, from origin/main), which shares no code with `fu_value.py`.

Inputs, from raw 425ba356 (fu021's end): `I1021-rpi5/fu021/rows_pass1.jsonl` (120 rows) and `rows_pass2.jsonl` (18
rows), copied as `rows_step1_pass1.jsonl` and `rows_step1_pass2.jsonl`, the names `fu_controls.py` reads; and the four
retest exits of `I1021-rpi5/fu021/logs/exits.txt`, rewritten into `exits_fu.txt` in its format (`step1_passN retest
--mutate=M exit E`). Nothing else changed. Commands, from a folder holding `fu_controls.py` and `in/`:

    nice -n 19 python3 -I fu_controls.py in                  # fu_controls.log
    nice -n 19 python3 -I fu_controls.py in --mutate=exits   # fu_controls_mutate.log, must exit 1

## Result

| pass | rows | accepted | f3: rows changed, exit rows -> reported | lowguard: rows changed, exit rows -> reported |
|---|---|---|---|---|
| 1 | 120 | 64 | 64, 1 -> 1 | 38, 1 -> 1 |
| 2 | 18 | 6 | 6, 1 -> 1 | 5, 1 -> 1 |

`fu controls: PASS (0 reported exits disagree with the rows)`, exit 0; the control `--mutate=exits` prints FAIL and
exits 1. Both mutations could change rows in both passes, so neither exit 1 is vacuous. Criterion 3 is met.
