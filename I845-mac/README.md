# I845-mac: the sigma-model kernel's deflated Newton on the near-null band at D 10.475, eta = 1: starts A and B

Machine: mac (Apple M5 Mac). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/845. Code: branch `wip/sa-845`.
The kernel module is the build of #652 (`I652-mac/README.md`), run with python 3.14 and `PYTHONPATH` at that build's
site directory, one process with 2 threads at nice 10. Local paths are removed from the copies here.

## Result

Both of #652's starts at D 10.475, eta = 1, M = 32 converge to the chain's solution with `run_eta.py --solver band`:

| start | sigdss's Delta | run | iterations | max \|F\| | Delta | minus the chain's |
|---|---|---|---|---|---|---|
| B | 0.9934860 | `pilotB`, then `bandB` | 2 resolved, 16 band | 6.32e-29 | 1.020104800025154887012 | -3.2e-20 |
| B, one more Newton step | | `bandB_polish` | | 1.40e-31 | 1.020104800025154887044169 | +6.7e-24 |
| A | 1.0340058 | `bandA4` | 5 resolved, 11 band | 6.54e-29 | 1.020104800025154886997 | -4.7e-20 |
| A, one more Newton step | | `bandA4_polish` | | 9.86e-32 | 1.020104800025154887044174 | +1.1e-23 |
| the chain | | `I652-mac/out/sm_eta1_D10.475_M32.npz` | | 1.4e-31 | 1.020104800025154887044163 | |

After the extra step the states equal the chain's to 5e-20 in c0 and 2e-17 elsewhere, except in the centre datum q,
where A, B and the chain differ by 1.6e-16 to 5.0e-16: the band leaves q free at that level at residuals of 1e-31.
A and B differ by 4.6e-24 in Delta.

## The band

32 singular values below 1e-10 of the largest (5.4), then a gap to 1e-4. 89% of it lies in q, and its largest Delta
component is 0.059. In the band's own basis (the SVD of the reduced Jacobian, formed in double-double) the reduced
singular values run from 3.6e-10 to 6e-18: 3 above 1e-11, 6 above 1e-12, 10 above 1e-13, 18 above 1e-14, 24 above
1e-15. At start A's first band step the four best-resolved directions hold 97.3% of B^2 and 0.22% of the squared
length of Newton's band step (72.5).

## Runs (`out/`; `gate.log` has the 1-minute load at each start, all below 31)

| run | code | what happened |
|---|---|---|
| `pilotB.txt` | first version (merged as bd702d7d..c897b582) | 3 + 3 iterations from start B: 125 s each, the spectrum, S 5.0e-4, 1.0e-8, 3.1e-13 |
| `bandB.txt`, `bandB_polish.txt` | the same, ten correctors | continued from the pilot's state: converged, Delta the chain's |
| `bandA.txt`, run 1, stopped | the same | 11 iterations: S at 1.5e-14 times the band step (2.85e-11, 1.53e-11, 4.1e-12 for band steps 2.0e3, 9.7e2, 3.0e2), then 2% of B per iteration, Delta 1.02997 |
| `bandA2.txt`, run 2, stopped | a left space taken from J V (not kept; a86852dc's message records it) | 4 iterations: S converges to 1e-13, but B takes in the resolved residual (1.05e-3 at step 0 against 7e-11) |
| `bandA3.txt`, run 3, stopped | the floor E of the split (a86852dc) | 29 iterations: S at E as designed, B 8.11e-11 to 4.42e-11 and stalling, Newton's band step grown from 40 to 170, Delta 1.02072 |
| `bandA4.txt`, `bandA4_polish.txt` | the damped band step and the checkpoint (wip/sa-845 at 3cd0d486) | converged in 16 iterations; `sm_bandA4_D10.475_M32_ckpt.npz` is the checkpoint of its last step |

Run 4's band steps (S, E, B before the step; the step taken of Newton's band step; Delta after):

| iteration | S | E | B | band step | Delta after |
|---|---|---|---|---|---|
| 5 | 5.2e-12 | 1.1e-12 | 8.11e-11 | 0.36 of 73 | 1.0187254 |
| 6 | 5.7e-13 | 1.4e-13 | 2.26e-11 | 0.72 of 8.9 | 1.0209673 |
| 7 | 5.5e-13 | 1.2e-13 | 7.54e-12 | 1.4 of 7.3 | 1.0209605 |
| 8 | 1.7e-13 | 1.0e-13 | 6.69e-12 | 1.4 of 5.7 | 1.0201206 |
| 9 | 2.7e-13 | 7.1e-14 | 4.53e-12 | 1.4 of 4.6 | 1.0201124 |
| 10 | 8.6e-14 | 5.2e-14 | 2.67e-12 | 1.4 of 3.5 | 1.0200891 |
| 11 | 4.3e-14 | 3.6e-14 | 1.51e-12 | 1.4 of 2.2 | 1.0200695 |
| 12 | 1.6e-14 | 1.3e-14 | 1.28e-12 | 0.88, all | 1.0200926 |
| 13 | 8.7e-16 | 7.3e-16 | 3.49e-13 | 0.047, all | 1.0201047 |
| 14 | 1.2e-17 | 1.3e-17 | 1.23e-15 | 7.9e-4, all | 1.0201048 |
| 15 | 1.2e-21 | 1.3e-21 | 1.85e-19 | 7.8e-8, all | 1.0201048 |

B after the last step is 5.8e-28. `sm_records.jsonl` has every finished run's record with its full history
(`band_sig`, `band_r`, `band_a` per iteration in run 4). The stopped runs have logs only.

## The planted test (`planted/`)

`planted_band.py` and its four mutations with the final code, each run's output and record: the test passes (A in 9
iterations, D in 7), and `noband`, `easy`, `root` and `gamma` each exit 1.

## Scripts

`gate.sh` waits for a 1-minute load below its limit and then starts its command. `run_i845.sh` ran B and run 1 of A,
`run_i845_A2.sh` to `_A4.sh` runs 2 to 4, each stopping the run before it when its gate opened.
