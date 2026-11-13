# I715-mac: the strong-row chord's horizon offset, point by point, at chain_ns's a = 0.0543 attempt

Machine: the coordinator's Mac (Apple M5, `mac`), 2 threads at nice 10, `OPENBLAS_NUM_THREADS=1`. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/715. Code: `hp/crawl_probe.py` (`chord`, `chordstat`) on branch
`wip/i715-subagent` of the main repository; kernel: main's #523 build (the exact freeze projector), venv-314.

Files:

- `chord_ns_D253.9368.log`: `crawl_probe.py chord` rebuilding #603's chain_ns attempt D 253.8825 -> 253.9368
  (a = 0.05429687500004832) from `I603-win2/chain_ns/anm_pin3_D253.8825.npz` and its series
  `jet_pin3_D253.8825.npz`, with #603's flags, to the strong-row chord's point. The prediction is checked bit for bit
  against `I603-win2/chain_ns/pred_pin3_D253.9368.npz`, and the chord's point against #700's iterate
  `I700-mac/crawl_iter_D253.9368.npz`.
- `chord_trace_D253.9368.npz`: the start and each chord point (`p<k>_z0..7`), each one's projection (`p<k>_P0..7`,
  formed with the switch off where the switch skipped it), each chord solve J0^-1 F (`x<j>_0..7`), the weak subspace
  `V` with its singular values, the first Newton step `dz_*` and the chord's last point `zc_*`; meta has the run.
- `chord_trace_D253.9368.jsonl`: `chordstat`'s records, one per point (the switch's test value, the own and the
  projected residual by block, P(z) - z by group and harmonic) and one per chord step (x, V^T x, dw by group, drop_V's
  f64 rounding, the switch's test value with one group of dw applied).

Results: the prediction and the chord's point equal #700's bit for bit, and theta is 7.993e-12. The chord's first step
(point 0 -> 1) takes the switch's test value from 1.42e-17 to 0.1288, and the later steps keep it there. Its x = J0^-1 F
lies in the weak subspace V to 3e-16 of |x| (|x| 2.5e-21), so dw = drop_V(x), |dw| 3.7e-37 = 1.5e-16 |x|, is what
the f64 V leaves of it. Applied alone, dw's m_h part (6.5e-38) gives 0.105 and its a_h part (5.9e-41) gives 0.085,
while its centre and node parts leave 1.42e-17. P(z) - z after that step is those two parts (correlation 0.97),
spread over every odd harmonic, and it is carried unchanged (to 1e-16 relative) to the chord's last point, the crawl
iterate. notes/CRAWL.md of the main repository has the account.
