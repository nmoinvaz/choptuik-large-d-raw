# I677-mac: the reduced map along rays in the weak coordinates at four corrector starts (hp/reduced_cubic.py ray)

Machine: the M5 Mac (the coordinator's), 2 threads, nice 10, OPENBLAS_NUM_THREADS=1, one compute process at a time.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/677.

Code: `hp/reduced_cubic.py ray` of choptuik-large-d (branch `wip/i677-subagent`; the results from 321954dc, earlier
versions in the table), run by `run_i677.sh` from `hp/`. Kernel: main 3c35f0c's hpkernel build (multishoot 1.2.2, the
exact freeze projector), the Mac's scratchpad build `i599/site2`, with venv-314's Python 3.14 and its multidouble
package. Protocol and results: `notes/REDUCED_CUBIC.md` section 9. Inputs from this repository:
`I461-win2/probeG03125a`, `probeG0078`, `probeG03125b` (REF and ACC), `I462-win/chain_d10/anm_pin3_D231.1312.npz` and
`I513-win/run_d10/` (D 232.13), and `I603-win2/chain/anm_pin3_D248.6298.npz` (the class A base).

| file | what | exit |
|---|---|---|
| `run_classA.sh`, `classA.log` | #603's class A attempt (D 248.6298 -> 249.39, a 0.762939453125) made again with anm_run.py --save_dz0 1, #603's flags, 2 threads (main 58628d94); stopped by hand after the attempt's first Newton step. Its lines repeat #603's (I644-win2/own.log lines 3 to 10) except the seconds and the 3-digit \|dz\| | 143 (stopped) |
| `classA/dz0_pin3_D249.3927_a0.762939.npz` | that attempt's corrector start and first Newton step, eight parts each | |
| `classA/pred_pin3_D249.3927.npz` | its prediction before the re-seed (--save_pred 1) | |
| `ray_planted.log`, `.json` | the ray plant (seed 5), code 321954dc | 0, every check passes |
| `ray_planted_mut_w0.log`, `_B` | its two controls, code 321954dc | 1 each, as they must |
| `ray_planted*_99ca8e3b.*` | the same three with the first code, before the REF pilot | 0, 1, 1 |
| `ray_planted*_c4496cb1.*` | the same three with the second code, whose floor start sat on the failure bound | 1 each (the plant failed at c = 0) |
| `ray_ref_pilot1_99ca8e3b.log`, `.json` | REF, the pilot, first code: the basis equals #528's, then the floor solve at c = 0 failed | 1 |
| `ray_ref.log`, `.json` | REF (refused, D 242.5459), code 321954dc | 0 |
| `ray_acc.log`, `.json` | ACC (accepted, D 242.5225), code 11c31fbd (the ray mode as 321954dc) | 0 |
| `ray_d232.log`, `.json` | D 232.13, win_d10 (refused), --tensors=1, code 11c31fbd | 0 |
| `ray_classA.log`, `.json` | the class A start (D 249.3927, refused in #603), --tensors=1, code 11c31fbd | 0 |
| `raysum.txt` | `reduced_cubic.py raysum` (code 5f755c56) of the five final JSON files: orders, constants, crossings and next-order estimates | 0 |
| `run_i677.sh`, `exits.txt` | the runner, and every start and exit | |
