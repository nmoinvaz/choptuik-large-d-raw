# I883-mac: lemma6b1_cover.py (M = 1) with --tag, every command run while the stored rows are renamed away

Machine: mac (Apple M5 Mac), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0 with FLINT 3.6.0), one
process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/883. Code: branch `wip/sa-883` on main
20f9e9ca. With `--tag=T` the script's run directory is `lemma6b1_runs<T>/` in place of `lemma6b1_runs/`.

`run_i883.sh <python> <output directory>`, from `solver/proof`, renames the stored `lemma6b1_runs/` to
`lemma6b1_runs_away/`, runs every command with `--tag=_x`, and renames it back. A read of the stored rows would then
fail. `exits.txt` has each exit status and `<name>.log` each output.

| command, each with `--tag=_x` | exit | result |
|---|---|---|
| `check`, before any run | 1 | fails as it must: no `lemma6b1_runs_x/ray.json` |
| `ray` | 0 | 452 steps, 17 s |
| `rows` | 0 | 12 rows, 178 discs, all certified, 284 s |
| `check --json=check_x.json` | 0 | PASS: 178 tiles, 566 polar rectangles, 450 links |
| `check --drop=5,6` | 3 | FAIL as it must, 3 failures |
| `--mutate=sign` | 0 | 0 of 7 discs of row 11 certified |
| `control --json=control_x.json` | 0 | no disc of radius above 5.12 certified |

`files_in_runs_x.txt`: the 13 files `ray.json` and `row_00.json` to `row_11.json`, all in `lemma6b1_runs_x/`, which
is copied here. `run_directories_during.txt` lists the run directories during the run: no `lemma6b1_runs/`.

After the stored folder is back:

| check | result |
|---|---|
| the 20 stored files, SHA-256 before and after (`stored_sha_*.txt`) | equal |
| `rows --from=11 --tag=_y`, with only `ray.json` in `lemma6b1_runs_y/` | row 11 is computed, 7 discs, though the stored folder has its `row_11.json`; the stored files keep their SHA-256 |
| `check` without a tag, on the stored rows (`check_stored.log`) | PASS with 178, 566 and 450, and byte for byte the output from before the change (`check_before.txt`, `check_after.txt`) |

The rows computed here agree with the stored ones, which another machine made, to 5.8×10⁻⁸ in every number of
the disc records, with the same 178 verdicts.
