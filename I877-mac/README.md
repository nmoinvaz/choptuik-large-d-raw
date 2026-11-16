# I877-mac: a check of the fast-row kernel bound inside fixed_point_M_b.py

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0, mpmath for the reviewer's script), one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/877 (finding F1 of the review #867, proof/A_M_b_review.md). Code:
branch `wip/sa-877`, on top of `wip/sa-878`: the check at b2a451c3, two table rows and one command in
proof/A_lemmas_M.md §2.5 at 1ff5c925.

`exits.txt` has each run's command, its exit status and the status it must have; each log is `<name>.log`, and
`rerun/` holds the 38 logs of `review_867/rerun_runs.sh`.

## The check

`python3 fixed_point_M_b.py --kernel`. The fast rows' bound is

    sup over r ≤ R of r^{-ki} ∫₀^r e^{-a(1/ρ - 1/r)} (ρ/r)^e ρ^{mm} dρ  ≤  R^{pw} / (a + (mm + 1 + e_min) R),   pw = mm + 2 − ki ≥ 1,

and the integral is r^{mm+2} I_n with I_n = ∫₀^∞ e^{−aτ}(1 + rτ)^{−n} dτ, n = mm + 2 + e. The check

- records every case (mm, pw, a, e_min, R) that the module asks `fast_norm` for in the reviewer's five runs at the
  stored zeros: M = 5 at the point, on the complex box, on the sector 0.2, on the sector with k = 40, and M = 3 at
  r₀ = 0.1;
- encloses I_n by its closed form U(1, 2 − n, a/r)/r, Tricomi's U from arb, so the module still imports python-flint
  only;
- requires r^{pw} I_n to lie certainly at or below the bound at r = R, R/2, R/100 and R/10⁴ and at e = e_min and
  e_min + 0.05, the reviewer's sample points, and the enclosures to satisfy 1 = a I_{n−1} + (n − 1) r I_n.

The reviewer's `rv_kernel.py` does the same with mpmath's quadrature, which shares nothing with arb. Before the
check was written the closed form was compared with that quadrature at six points; 22 digits agree.

## Results

| run | what must hold | result |
|---|---|---|
| kernel | no sampled value above the bound; the identity holds | 1417 cases, pw from 1 to 377, mm from 39 to 415; 0 of 11336 values above; the largest is 0.999815 of the bound, at mm = 415, pw = 314, a = 0.18796, e = 1.5, r = R = 0.0049; every identity ball contains 1 (radius at most 2.3×10⁻⁹⁰) |
| kernel_mut_offbyone (exit 3) | the bound with a + (mm + 2 + e)R must fail | 2834 of 11336 values above, the largest 1.006761 of the mutated bound, at mm = 50, pw = 1, a = 0.35355, r = 0.01 |
| rv_kernel (the reviewer's script, unchanged) | the numbers of the review | 1417 cases; 0 of 11336 above; largest 0.999815 at the same case; identity to 2.3×10⁻⁴¹ |
| rv_kernel_mut_offbyone (exit 1) | the numbers of the review | 2834 of 11336 above, largest 1.006761; the five author checks it lists still pass under the mutation, which is finding F1 |
| rerun: the 38 runs of `review_867/rerun_runs.sh` | every exit status as required | 38 runs, 0 with another status; all 38 logs equal the stored ones (`I427-mac/`, `I866-mac/`) apart from wall times and paths |

The two implementations of the test agree in every printed number, with and without the mutation.

## What changed in the module

- `fast_norm`'s formula is unchanged. It writes its cases into `KERNEL_LOG` when that is a dict; it is `None`
  except inside `kernel_check`.
- New: `kernel_integral`, `kernel_check`, the switch `--kernel`, and the constant `ZEROS` (the stored zeros that
  `planted` already used, moved out of that function).
- The mutation is `fast_norm` called with e_min + 1, which is the denominator a + (mm + 2 + e_min)R. No mutated copy
  of the bound exists in the module.

Not changed here: finding F3 of the review (the bound's stated hypotheses in the docstring and in §2.5).

## Recommended tasks

None.
