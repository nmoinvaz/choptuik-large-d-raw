# I879-mac: the survey of solver/proof for decimals read into balls before the precision is set

Machine: mac (Apple M5 Mac), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0 with FLINT 3.6.0), one
process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/879. Tools:
`solver/proof/prec_trace.py` and `solver/proof/prec_survey.py`, branch `wip/sa-879` on main dacbb5d8. The note is
`notes/PRECISION_SURVEY.md`. Paths in these files are relative to `solver/proof/`, and RAW is the raw-data clone.

| file | what it holds |
|---|---|
| `prec_survey_cmds.json` | the 330 command lines collected from the notes, the shell scripts and the run records |
| `prec_survey_runs.json` | the 347 traces of 5 s each, and the 51 commands skipped for a placeholder: how each run ended, its early reads and the wide module-level balls |
| `table.txt` | `prec_survey.py table`: the 28 places that read a decimal early, and the commands that reach them |
| `run.log` | the trace run's progress, 657 s |
| `extra/` | the 21 commands traced by hand with their shell variables filled in: the covering, lemma 6a, lemma S, the rechecks, the Krawczyk tests and the certificate box runs |
| `review_dirs.txt` | the 18 reviewers' scripts that import flint, traced with no argument from their own folders |
| `prec_survey_rerun.json`, `rerun.log` | the 31 flagged commands run as written and with `prec_trace.py --prec=320`: exit statuses, and the lines that differ |
| `reruns/` | results compared as files: the lemma's start-data rows at M = 3 and M = 5 both ways, lemma LC's Lipschitz matrix as written (`lip_fresh_plain.json`) and with the precision set first (`lip_320.json`), and the outputs of `fixed_point.py --sector=0.2` and of `b8m_lc.py --lipcheck` |

## Result

No exit status changes in any of the 31 reruns. Seven commands print other last digits. Two results move beyond
that:

- the first row of each `fixed_point_M.py --data-table` invocation, by 2.0×10⁻⁸ relative at M = 3 and by at most
  1.2×10⁻⁸ at M = 5, as #484 found;
- lemma LC's Lipschitz matrix, where 552 of 1600 entries move by factors between 0.733 and 1.014 while the certified
  contraction constant stays θ = 0.7355.

The Theorem A chain at M = 3 and M = 5 shows no early read on any traced path.
