# I870-mac: the M = 5 boxes with h = 10⁻⁹ and 10⁻¹¹ by the second implementation of the start-value lemma

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0), one process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/870. Code:
`solver/proof/fixed_point_M_b_check.py cert`, unchanged (the runs were made at main ecfc1b92). Branch `wip/sa-870` on main 724d45b9 holds only the proposed sentence for proof/A_lemmas_M.md §2.5, at 05c91a13.

`run_i870.sh <python> <this folder> <h>` ran each box from `solver/proof/`, 266 s and 270 s. `exits.txt` has each run's
command, its exit status and the status it must have: 2 checks exit 0 and 4 mutations exit 3. Each run's log is
`<name>.log`. The method and the criteria are those of `I866-mac/README.md`.

## Results

The two boxes share the centre p̂ and the start ray of the h = 10⁻¹⁰ box (arg ξ = 5π/16, r₀ = 0.0622, N = 132, the
second implementation's own choice as well; k = 130), so the rows at p̂ repeat #866's.

| | `data/A_M2_box_M5_1e-9.json` | `data/A_M2_box_M5_1e-11.json` |
|---|---|---|
| hull half-width | 1.000×10⁻⁹ | 1.000×10⁻¹¹ |
| contraction constant at p̂, on its Cauchy box, over the hull, on its Cauchy box | 0.0886, 0.0888, 0.0886, 0.0888 | 0.0886, 0.0888, 0.0886, 0.0888 |
| sup\|η\| at \|z\| = R in (p, v, c): at p̂, over the hull, on the Cauchy boxes | 1.0×10⁻⁹⁶, 1.3×10⁻³¹, 4.6×10⁻²⁴ | 1.0×10⁻⁹⁶, 1.3×10⁻³³, 4.6×10⁻²⁴ |
| the first implementation's sup\|η\| at p̂ and over the hull | 8.0×10⁻⁹⁶, 1.0×10⁻³⁰ | 8.0×10⁻⁹⁶, 1.0×10⁻³² |
| start values at p̂ | 19 of 19 overlap, all inside the first's; midpoints within 3.0×10⁻⁹⁵ | 19 of 19 overlap, all inside; midpoints within 3.0×10⁻⁹⁵ |
| derivative entries at p̂ | 114 of 114 overlap, all inside | 114 of 114 overlap, all inside |
| derivative entries over the hull | 114 of 114 overlap; radii 7.6×10⁻¹⁰ against 5.4×10⁻¹⁰ | 114 of 114 overlap; radii 7.6×10⁻¹² against 5.4×10⁻¹² |
| values over the hull (not used by the certificate) | 19 of 19 overlap | 19 of 19 overlap |
| second-order jets of Y_N over the hull, 21 directions, orders 0 to 2 | 1197 of 1197 overlap; radii 3.4×10⁻⁹ against 2.0×10⁻⁹ | 1197 of 1197 overlap; radii 3.4×10⁻¹¹ against 2.0×10⁻¹¹ |
| `--mutate=sign` (exit 3) | four contractions hold; 0 of 19 values and 0 of 228 derivative entries overlap | the same |
| `--mutate=radius` (exit 3) | no contraction: row sums 21.5 and 34.3 | the same |

Nothing disagrees with the text: proof/A_M2.md §6.6 states both boxes covered, and they are by the second
implementation as well.

## Recommended tasks

None beyond #869 (the second-derivative columns), which applies to these boxes too.
