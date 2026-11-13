# I698-mac: the reduced map along the first weak move out to 1e-2, the strong rows solved by Newton (hp/reduced_cubic.py curve)

Machine: the M5 Mac (the coordinator's), 2 threads, nice 10, OPENBLAS_NUM_THREADS=1, one compute process at a time.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/698.

Code: `hp/reduced_cubic.py curve` of choptuik-large-d (branch `wip/i698-subagent`), run by `run_i698.sh` from `hp/`.
Kernel: main 3c35f0c's hpkernel build (multishoot 1.2.2, the exact freeze projector), the Mac's scratchpad build
`i599/site2`, with venv-314's Python 3.14 and its multidouble package. Protocol and results: `notes/REDUCED_CUBIC.md`
section 11. Inputs from this repository: `I461-win2/probeG03125a`, `probeG03125b` (REF), `I603-win2/chain/` and
`I677-mac/classA/` (the class A start), `I677-mac/ray_ref.json`, `ray_classA.json` (#677's rays, for the lead-in check)
and `I694-mac/rows_ref.json`, `rows_classA.json` (#694's F''(e, e) rows, for the flat chart's check).

| file | what | exit |
|---|---|---|
| `curve_planted.log`, `.json` | the curve plant (seed 5), code 085fbdff | 0, every check passes |
| `curve_planted_mut_w0.log`, `_chord` | its two controls, code 085fbdff | 1 each, as they must |
| `curve_ref.log`, `.json` | REF (refused, D 242.5459), the pilot | running |
| `curve_classA.log`, `.json` | the class A start (D 249.3927) | |
| `run_i698.sh`, `exits.txt` | the runner, and every run's start and exit | |
