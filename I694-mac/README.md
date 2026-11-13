# I694-mac: where the weak left vectors U live, by block, field and harmonic, and whether those rows are affine

Machine: the coordinator's Mac (M5), 2 threads, nice 10, OPENBLAS_NUM_THREADS=1, one compute process at a time.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/694

Code: `hp/reduced_cubic.py rows` (branch `wip/i694-subagent`), protocol and results in `notes/REDUCED_CUBIC.md`
section 10. Kernel: main's 3c35f0c build (multishoot 1.2.2, exact freeze projector), the Mac's scratchpad build
`i599/site2`. Inputs: the four starts of #677 (`I461-win2`, `I462-win`/`I513-win`, `I603-win2`/`I677-mac/classA`).

- `run_i694.sh`: runs everything (`bash run_i694.sh RAW OUT [planted|ref|acc|d232|classA|all]` from the checkout's `hp/`).
- `exits.txt`: each run's start, code commit and exit, in order. Its first `rows_planted*` and `rows_ref` entries are
  the files renamed with the suffix of their code commit below.
- `rows_planted*_b6abb010.log`, `.json`: the first run of the plant and its controls `--mutate=quadA`, `--mutate=parity`.
- `rows_ref_pilot_8cbd3f31.log`, `.json`: the REF pilot, before the diagnostics of 848f7c06 (each block's part of
  U^T x, the pairing of the last two blocks' rows, w_ee by unknowns); its judged numbers are those of the final run.
- `rows_planted*.log`, `.json` and `rows_{ref,acc,d232,classA}.log`, `.json`: the final runs, code 848f7c06.
