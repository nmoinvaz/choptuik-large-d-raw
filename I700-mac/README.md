# I700-mac: the crawl's jump along the corrector's Newton step, located at chain_ns's a = 0.0543 attempt

Machine: the coordinator's Mac (Apple M5, `mac`), 2 threads at nice 10, `OPENBLAS_NUM_THREADS=1`. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/700. Code: `hp/crawl_probe.py` on branch `wip/i700-subagent`
of the main repository; kernel: main 3c35f0c's build (the exact freeze projector), venv-314.

Files:

- `iterate_ns_D253.9368.log`: `crawl_probe.py iterate` rebuilding #603's chain_ns attempt D 253.8825 -> 253.9368
  (a = 0.05429687500004832) from `I603-win2/chain_ns/anm_pin3_D253.8825.npz` and its stored series
  `jet_pin3_D253.8825.npz`, with #603's flags, to the first crawl iterate; the rebuilt prediction is checked bit for
  bit against `I603-win2/chain_ns/pred_pin3_D253.9368.npz`.
- `crawl_iter_D253.9368.npz`: that iterate z (eight parts `z0`..`z7`) and its Newton step dz (`d0`..`d7`), as
  `ElimO.newton_o` formed them inside `newton_od`; meta has the attempt and the corrector's history.
- `probe_*.log`, `crawl_probe_*.jsonl`: `crawl_probe.py probe` on that iterate, the residual along z + lam dz per arm
  (E the corrector's own, U never projected, P always projected), lam*, the jump per block and the rows carrying it.
- `selftest.log`: the planted check and its five mutations.
