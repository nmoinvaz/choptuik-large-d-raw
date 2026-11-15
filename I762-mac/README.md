# I762-mac: the pinned quad-double Delta_full1 against the second full-system starts at D 71.5 and 73.0

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/762
Code: `hp/export_pinned_qd.py` (the column minus_qd2) and `check_numbers.py` (`pinned_qd_second`) of choptuik-large-d,
branch wip/xf-762 (4562469c, 7f439acc). Sources: `qd2start-mac/second.jsonl` (its converged records at 71.5 and 73.0),
`T84-mac/*_fullcorr.jsonl`, `T75/pin{5,7}.jsonl` and choptuik-large-d's `hp/data/delta_qd.csv`.

| file | what |
|---|---|
| `export_pinned_qd.log` | `export_pinned_qd.py RAW --verify` (16 of 16 rows equal their rebuild, exit 0) and its control `--mutate=repr` (14 of 16, exit 1) |

| D | pin | Delta_full1 minus the first full-system solution (minus_qd) | minus the second (minus_qd2) |
|---|---|---|---|
| 71.5 | 7 | +3.833e-28 | -5.824e-32 |
| 71.5 | 5 | +3.833e-28 | -5.112e-32 |
| 73.0 | 7 | -8.100e-28 | +2.864e-29 |
| 73.0 | 5 | +1.833e-26 | +1.917e-26 |

The second starts at 71.0 and 72.8 stalled (|F| 2.04e-19, 8.2e-18) and give no column there. check_numbers'
`pinned_qd_second` (7 items) passes on the new note and fails 6 of 7 on notes/QUAD_DOUBLE.md at be22096d (the quoted
text is missing there).
