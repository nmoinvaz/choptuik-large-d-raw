# I888-mac: a check that fails on a decimal read before the precision is set, over the Theorem A chain

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0), one process at nice 10, every run under a time cap. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/888 (task 4 of the survey #879). Code:
`solver/proof/prec_chain_check.py`, branch `wip/sa-888` on main 2a7b65fa: the script at c5d0c5ae, the notes
(notes/PRECISION_SURVEY.md §7 and one command in proof/A_lemmas_M.md §10) at baaed0cb.

`exits.txt` has each run's command, its exit status and the status it must have; each log is `<name>.log`, and
`chain.json` is the clean run's record.

## The check

`prec_chain_check.py` runs `prec_trace.py` (#879) over 45 documented commands of the Theorem A chain at M = 3 and 5,
each for 6 seconds in its own process group:

| part of the chain | scripts | commands |
|---|---|---|
| step (i), first implementation | `fixed_point_M.py` (the lemma at points and boxes, `--data`, `--table`, `--data-table`) | 8 |
| step (i), second implementation | `fixed_point_M_b.py` (plain, box, `--planted`, `--kernel`, `--start`) and its harness (`m1`, `lip`, `cert`, `cert2`) | 10 |
| (H0) | `start_cover_M2.py` | 2 |
| (H1) | `lemma6_sector_M.py` | 2 |
| (H2) | `lemma6b1_cover_M.py` (`design`, `ray`, `row`, `check`, `c1check`), `theorem_A_sets_M.py`, `start_cover_lemmas_M.py` | 10 |
| (H3) | `lemma6_jump_M.py` | 2 |
| the point certificates | `certify_M.py`, `certify_M2.py`, `certify_M_recheck.py` (box run, Krawczyk, controls, recheck, export) | 11 |

The placeholders of the notes are filled from the stored files (the certificates' centres and boxes). Outputs go to a
temporary directory and the covering's ray and row runs to a scratch tag that is removed afterwards; the worktree is
unchanged after a run (`git status --ignored` shows only `__pycache__`). An early read passes only if it is one of
three known ones, listed in the script by file and function with the reason: `fixed_point_M.data_table` (#484,
held), `fixed_point_M.W0` in the table runs, and `start_cover_M2.lemma_runs` (intended).

## Results

| run | what must hold | result |
|---|---|---|
| chain: the check on main, with the raw clone | exit 0: every trace starts, no early read outside the known ones | PASS: 45 traced, 30 known early reads, 0 new, 0 not started, 141 s |
| chain_mut_early: the control | exit 1, naming the read | FAIL as it must: 6 new early reads, `fixed_point_M_b.py:999 in main: arb('2.7185…') at 53 bits` and the five other parameters |
| chain_noraw: without `--raw` | exit 0, the raw-dependent commands skipped and counted | PASS: 41 traced, 4 skipped |
| selftest | exit 0 only if the clean check passes and the control fails | PASS, 286 s |

The 30 known reads are those of the survey: 1 each in the two `--table` commands (W0), 6 and 8 in the two
`--data-table` commands, and 8 and 6 in the two `start_cover_M2.py` commands.

**The control.** A copy of `fixed_point_M_b.py` is written to a temporary directory with the line of `main()` that
sets the precision moved below the reads of `--x`, `--box` and `--cbox`, which is the state before #878. Its plain
command is traced in place of the real one. The mutation is made from the current source at each run, by moving
that one line, so it stays runnable while the line exists; the script stops with an assertion if it does not find it.

## Limits

As `prec_trace.py`'s: a read is seen only if the run reaches it within 6 seconds and on the path its arguments take,
and a command that starts other processes is traced without them. The long commands (box runs, the ray, the rows,
lemma 6a) are cut at the limit; their parameters are read in the first second. The list of commands is explicit, so
a new documented command of the chain has to be added to it by hand.

## Recommended tasks

None.
