# planted-k16-mac: the K = 16 stages of the planted-truth test (notes/PLANTED_SELECTION.md section 8), stage logs

Machine: mac (coordinator), 2026-10-27 22:19–22:25 UTC. `solver/inner_amp/planted_k16.py` at the commit that holds its
ring-stage fix, run from `solver/inner_amp/` on the σ₁₆ JSONs of T83-mac (3ab8a95), copied into main's `scan33J1000/`
and `scan33J1250/`. No comms entry: the coordinator's own run.

- `converge.log` and `converge_{err,low,pilot,ratiolaw}.log`: the four convergence checks (all pass) and the four
  mutations (each fires, exit 1).
- `plants.log`, `real.log`, `ring.log`, `calib.log`, `recomplete.log`, `project.log`, `combine.log`: the stages in
  section 8.0's order, all exit 0. `ring.log` is the rerun after the fix (the first run stopped with a KeyError on the
  C13-BP completions); `stages.log` has the timings of every attempt.
- The records and stored checks are in main (`planted_results_k16.jsonl`, `planted_checks_k16.json`).
