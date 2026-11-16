# I922-mac: the review of the σ-model kernel's band solver smdriver.newton_band, its reruns, mutations and Newton checks

Machine: mac (Apple M5 Mac). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/922. Code: branch
`wip/sa-922`, scripts `matter/sigma_ms/review_922/`, note `matter/SIGMA_BAND_review.md`. The kernel module is the
build of #652 (`I652-mac/README.md`), run with python 3.14 and `PYTHONPATH` at that build's site directory, one
process with 2 threads at nice 10, every run under a time cap (`gtimeout`). Local paths are removed from the copies
here. Inputs: the stored states and records of `I845-mac/`, `I913-mac/`, `I915-mac/`, `I916-mac/` and `I917-mac/`.

## Result

A state that `newton_band` returns as converged is a root of the kernel's system: one Newton step whose Jacobian is
built from the residual alone leaves #913's D 10.5 state at max |F| = 1.17e-31 with Delta moved by 9.6e-22, and all
75 stored converged states of the band solver's runs have max |F| < 1e-28 on their plan. Four of the reviewer's
seven mutations of `newton_band` pass the planted test unchanged.

| check | criterion, written before the run | result | verdict |
|---|---|---|---|
| K1, Newton step, Jacobian by central differences of the residual (h = 2^-33) | max \|F\| <= 1e-30, Delta moves <= 1e-20 | 1.302e-31, +9.618e-22 | OK |
| K1 again, Jacobian from two step sizes | the same | 1.171e-31, +9.618e-22 | OK |
| K2, `Solver.jacobian`, start hi | the same | 1.079e-31, +9.618e-22 | OK |
| K2, start up | the same | 1.202e-31, +1.661e-23 | OK |
| K2, start march | the same | 1.109e-31, +8.769e-21 | OK, at 0.88 of the bound |
| K3, the two Jacobians | a difference above 1e-15 is a finding | 1.78e-14 at h = 2^-33; 1.20e-21 from two step sizes, over all 3521^2 entries | OK: truncation (K3b) |
| K3b, 41 columns at three step sizes | extrapolated columns equal `Solver.jacobian`'s to 1e-18 | 6.08e-22, ratio 4.00 per halving | OK |
| K4, x = J^-T e_Delta | -x.F equals the step's dDelta to 1e-3 | equal in the digits printed; \|x\|_1 = 8.674e9, \|x\|_2 = 6.360e8 | OK |
| R3, `planted_band.py` and its four mutations | exits 0, 1, 1, 1, 1; the stored numbers | so; all 32 entries equal | OK |
| R4, `sonly`, named on the issue beforehand | the planted test fails | exit 1 (A: max \|z - z*\| 5.45e-14) | OK |
| R4, `noshort`, `none` | exit 0 | exit 0 | OK |
| R4, `loose`, `nochord` | reported | exit 1 (A) | noticed |
| R4, `nodamp`, `nofloor`, `noheld`, `anyB` | reported | exit 0 | not noticed (finding F1) |
| R6, the residual at every stored state | max \|F\| < 1e-28 and equal to the record's to 1e-3 | 75 judged of 77, largest 9.646e-29, all bit-equal | OK |
| R6's control | exit 1 | exit 1, 75 of 75 fail at 1.0e-23 | OK, after the control was corrected |

## Files

| file | what |
|---|---|
| `exits.txt` | every run's exit status, what it had to be, its seconds and its command |
| `planted/clean.*`, `planted/mut_*.*` | R3: `planted_band.py` and its mutations `noband`, `easy`, `root`, `gamma` |
| `mut/*.txt`, `mut/*.json` | R4: `rv_band_mut.py --mutate NAME`, the planted test on a mutated copy of `newton_band` |
| `newton/hi_fd.*` | K1, K2, K3 at `I913-mac/out/sm_hi_D10.5_M32.npz` with one step size (608 s) |
| `newton/hi_fd2.*` | the same with the Jacobian from two step sizes, and K4 (1047 s) |
| `newton/fdcol.*` | K3b: 41 columns at h = 2^-33, 2^-32, 2^-31 |
| `newton/hi.*`, `up.*`, `march.*` | K2 and K4 at the three starts of #913 |
| `states/all.*` | R6: one row per state file |
| `states/mut_state.*` | R6's control, 1e-20 added to the low part of the first unknown |
| `states/mut_state_noop.*` | the control's first version, which added it to the high part and changed nothing (exit 0) |

## What went wrong on the way

- R6's control exited 0 at first: 1e-20 added to the high part of a double-double value is rounded away. Corrected to
  the low part, it fails at all 75 states.
- K3 exceeded the reviewer's mark of 1e-15 (1.78e-14 in one entry). K3b shows it is the truncation of the central
  difference, and the run with two step sizes brings it to 1.20e-21.
- The mutation named on the issue beforehand was `sonly`. `loose` was run first in its place, and `sonly` after the
  other runs. Both fail the planted test, as expected of them.

## Recommended tasks

1. **A planted toy on which the band solver's refinements are needed.**
   What: a second toy for `planted_band.py` whose band has reduced singular values over at least six decades, a
   start whose Newton band step has more than 99% of its squared length in directions that hold less than 5% of
   B^2, and resolved rows curved enough that a band step of Newton's full length is rejected. Its controls are the
   mutations `nodamp`, `nofloor`, `noheld` and `anyB` of `review_922/rv_band_mut.py`.
   Why: finding F1. These four pass the present test, and no band trial was rejected in any stored run, so nothing
   would notice a later change to the damping, the floor, the held-back step or the acceptance rule.
   Acceptance, each can fail: the unmutated function exits 0 on the new toy; each of the four mutations exits 1; the
   clean run rejects at least one band trial (a halving). If the floor cannot be made to matter in a toy of f64
   singular vectors, the note says so and `nofloor` is listed as not testable.
   Decision it informs: whether SIGMA_DSS section 11 can say the planted test covers the two refinements.
   Depends on: #922. Estimate: half a day, the Mac, one process.
2. **The width of Delta along the kernel's chains.**
   What: `review_922/rv_newton.py --state FILE` (K2 and K4, 45 s each) at every stored state of #916's and #917's
   chains from D 9 to 11, and a table of \|x\|_1, \|x\|_2 and \|x\|_1 max \|F\| against D.
   Why: finding F2. \|x\|_1 max \|F\| is the first-order error bar of Delta at a converged state, 8.7e9 max \|F\| at
   D 10.5, and it is not known whether it grows with D.
   Acceptance, each can fail: \|x\|_1 max \|F\| <= 5e-16 at every point, the 16th digit of the chain tables; -x.F
   equals the Newton step's dDelta to 1e-3 at every point; the three starts at D 10.5 give the same \|x\|_1 to three
   digits (they do here, 8.674e9).
   Decision it informs: how many digits of the chain tables the band fixes, and the error bar to quote in section 11.
   Depends on: #922. Estimate: one hour, the Mac, 2 threads.
3. **Text of SIGMA_DSS section 11 and of the docstring** (the coordinator's edits; findings F2 to F6 of the note).
   Section 11: name "about 3e-23" as a spread and give the bound beside it; "its largest Delta component is 0.059"
   is start B's first band step, 0.071 at the solution; "3% of B per iteration" is 2.4%; one sentence on what the
   planted test covers. Docstring: the acceptance rule also accepts S up to its value before the step; the radius
   changes only after a limited step and doubles only without a halving.
