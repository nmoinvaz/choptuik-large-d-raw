# I887-mac: the B(1) chain scripts with their working precision stated, traced and rerun

Machine: mac (Apple M5 Mac), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0 with FLINT 3.6.0), one
process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/887. Code: branch `wip/sa-887`, on top
of #885. Eight scripts of `solver/proof/` now state their precision in one line after their imports: `b8_atoms.py`,
`b8_bounds.py`, `b8m_bounds.py`, `b8m_lc.py`, `b8m_lcj.py` and `b8m_scan.py` at `b8_formal.PREC`, 256 bits, and
`b5_jump.py` and `b5_threshold.py` at 192 bits.

## The traces

`traces/runs_<script>.json` are `prec_survey.py run --only=<script> --limit=5` for the eight scripts and for
`b8_formal.py`, `b8m_atoms.py` and `b8m_h8.py`: every documented command of each, and the script with no argument.
27 runs, 0 with an early read.

## The rerun

`run_i887.sh <python> <output directory>` ran the 17 commands of `I885-mac/run_i885.sh` and three more, `b5_jump.py`
with `--json` and with `--mutate=sum`, and `b5_threshold.py`. Every output went to its own folder. `exits.txt`: all 20
exit 0. `compare.txt` is `compare_i885.py` against the stored files.

| output | against the stored file | against `I885-mac/` |
|---|---|---|
| the printed output of `b5_jump.py` (two runs) and `b5_threshold.py` | every line equal | |
| `b5_jump.json`, `b5_jump_d0_1e7.json` | numbers within 9.5×10⁻¹⁵ | `b5_jump_d0_1e7.json` differs, in the 15th digit |
| `b7_ift.json`, which reads `b5_jump_d0_1e7.json` | within 9.8×10⁻¹⁵ | differs, in the 15th digit |
| `b7_ift.log`, n₀ = e^89.75 | every line equal | equal |
| the 15 other outputs of the B8 scripts | as in `I885-mac/` | equal |

So the six B8 scripts give the outputs of #885 exactly: after #885 they already ran at 256 bits from the import of
`b8_formal.py`, and their own line states it. `b5_jump.py` moves from 53 to 192 bits, which changes its saved floats
in the 15th digit and nothing it prints. θ = 0.7355, n₀ = e^89.75 and lemma J's θ = 0.17593 are unchanged, and every
mutation is caught.
