# I349-dh170: logs, results and tables of the clean-room reproduction of README.md's commands

Machine: dh170 (Intel Core i7-7700, 8 threads, 31 GB, Fedora 45, Linux 7.2.11), UTC 2026-11-22 03:33 to 09:30.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/349

A fresh clone of choptuik-large-d at d7d54ccf, a venv built per SETUP.md (Python 3.14.10, numpy 2.5.4, scipy 1.18.1,
mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0, maturin 1.16.0), no builds. The runner is `reproduce_readme.py` on branch
`wip/i349-reproduction` of nmoinvaz/choptuik-large-d (the results were made by commits 8a0c35b1 to af96392a, scored again
by later ones; the tools that read them are at 7a97da03). The record with the verdicts and the proposed fixes is
`notes/REPRODUCTION.md` on that branch.

| Path | Holds |
|---|---|
| `commands.txt`, `commands.json` | the command list the runner extracted from the README, saved before any run |
| `pass1/` | pass 1, clean venv: `results.jsonl` (one record per row: exit, files, numbers printed against quoted, wall, cpu, rss), `results.first.jsonl` (the records before the redo and rescoring), `table.md`, `logs/<id>.log` (the raw output of each command, `.fix.log` for an adapted rerun) |
| `pass2/` | pass 2, existing build `~/Source/choptuik-large-d-1058b/.venv` (hpkernel from main 8179068d), import only, nothing installed: the rows deferred for a missing hpkernel, the import checks, and `reproduce_sh_hp`, `reproduce_sh_full_hp` |
| `merged.md`, `compact.md` | both passes merged: the full table (cpu, rss) and the tables of notes/REPRODUCTION.md |
| `control/` | the control: `control.md` (passed 2026-11-22 08:42 UTC, final checker), the README copies with a planted number, a changed command and a second planted number, and `links_planted.log` for the link check on a copy with a broken anchor, a missing file and an undefined footnote |
| `links.txt` | `--links` on the real README |
| `svgdiff/` | the regenerated figures and tables that differ from the committed ones, as `git diff`s (`diffs/`) |
| `evidence/` | `export_delta_all.py --verify` on the committed tables, and the held-out check of `reproduce.py` with an upper bound at D 61.03 and 60.1 |
| `pass1.log`, `redo.log`, `redo2.log`, `pass2.log`, `pass2b.log`, `pass2c.log`, `control.log`, `svgdiff.log` | the runner's own progress logs; `run_rest.sh`, `run_rest2.sh` the batches |
| `post_list.md`, `post_control.md` | the posts on #349 for the command list and the control |

Notes on the data:

- `pass1/logs/planted_dinf.log` is a composite: T1 to T5 are from the 08:08 UTC rerun (stopped after 1800 s at load 8.9; its
  own log is `planted_dinf.redo.log`), T6 and the last line are from the complete run of 06:00 UTC (two runs of 1190 s at load
  5.2; `results.first.jsonl` has that record). The log says so on its last line.
- Each command ran from a throwaway git worktree (`_i349/run`, marker `.i349_run_tree`) that was restored after each row.
- The Ecker data clone (https://github.com/EckerChristian/CriticalSpacetimeCrystal at f002d0a) was read as data and nothing in it
  was run.
- Loads: 4.3 to 9.5 (other jobs on the machine). 2 threads at nice 19, or 4 at nice 10 when the load was under 4.
