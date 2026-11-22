Control passed (2026-11-22 03:37 UTC), `python3 reproduce_readme.py --control --tree ../run` (80 s, fast rows only, `reproduce_readme.py` at 4e5dd94f on `wip/i349-reproduction`).

| plant in a scratch copy of the README | rows flagged | expected |
|---|---|---|
| `| 3.755725 | 3.46677169 |` -> `| 3.755725 | 3.46677179 |` (the `lowD_max.py` row) | `lowD_max` only: "3.46677179 not printed (7 digits agree)" | `lowD_max` |
| `python3 lowD_max.py` -> `python3 lowD_maxx.py` | `lowD_max` only: STALE, span not in the README | `lowD_max` |
| `0.499250` -> `0.499251` (the `values_table.py` row) | `values_table` only: "gamma(1000) 0.499251 not printed (5 digits agree)" | `values_table` |
| a command that exits 1; a named file that does not exist | `ctl_exit`, `ctl_file` flag; `ctl_ok` passes | those two |

Five fast rows ran on the real README and each copy; every other row kept its verdict. The unplanted rows print the quoted digits (`lowD_max.py`: 3.755725 and 3.4667716863 against the quoted 3.46677169). Pass 1 in the clean venv starts now, 2 threads at nice 19 (load 8).
