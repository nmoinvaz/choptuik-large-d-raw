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
| `curve_ref.log`, `.json` | REF (refused, D 242.5459), the pilot, code 085fbdff: (Z0) and (Z1) pass, the flat-chart control (Z2a) fires, and Newton stops at 1e-6 on both rays | 1 |
| `curve_planted_bridge.log`, `.json` | the plant with the chord bridge from 1e-24 (a diagnostic added after the pilot), code 46f250b3 | 0 |
| `curve_planted_bridge_mut_fold.log`, `.json` | its control, a symmetric coupling: the pair ratio rho turns positive | 1, as it must |
| `curve_ref_bridge.log`, `.json` | REF, the chord bridge alone (`--newton=0`), code 46f250b3: converged from 1e-24 to 3.16e-18, failed at 5.62e-18 | 0 |
| `curve_classA.log`, `.json` | the class A start (D 249.3927), with the bridge (and its linear-regime pair test) before the Newton points, code 203e56a0: the bridge converged from 1e-24 to 1e-18; (Z0) and (Z1) pass, (Z2a) fires, Newton stops at 1e-6 on both rays | 1 |
| `curve_ref_bridge2.log`, `.json` | REF's bridge again with the linear-regime pair test and the parts as vectors, to 1e-21 (`--bridge_to=1e-21`, code 96b4d34a) | running |
| `run_i698.sh`, `exits.txt` | the runner, and every run's start and exit | |
