# I880-mac: the M = 5 box run and its Krawczyk test from the second implementation's C² start data

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0), one process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/880. Code:
`solver/proof/fixed_point_M_b_check.py` (new commands `box2` and `kraw`, and `assemble_b`), branch `wip/sa-880` on
main 1f3cda09: the harness at 34822736, the notes (proof/A_lemmas_M.md §2.5) at 86aa468b. `certify_M2.py` and `fixed_point_M_b.py`
are not changed by this issue.

`exits.txt` has each run's command and exit status. Files: `pilot.log`, `pilot.json` (30 steps);
`A_M2_box_M5_1e-10_b.json` (the new box file, in the stored file's format), `box2_M5_1e-10_b.log` and `.runlog` (the
run's output and `box2_run`'s own log); `kraw_M5_1e-10_b.log`; `box2_M5_1e-10_b_mut_sign.log`, `.runlog` and
`A_M2_box_M5_1e-10_b_mut_sign.json.ckpt` (the mutated run, stopped).

## What ran

`box2` calls `certify_M2.box2_run` with the stored run's chart, h = 10⁻¹⁰ and w = (10⁻¹⁸, 10⁻¹⁹), after replacing
`certify_M2.start_data2`, for that call, by `assemble_b`: the values at p̂, the first-derivative columns and the 21
second-derivative columns built from `fixed_point_M_b.py` (the assembly that #869 compared entry by entry). The
integrator, the path and the Krawczyk test are the certificate's own.

## Results

| | from the second implementation's start data | the stored run (`data/A_M2_box_M5_1e-10.json`) |
|---|---|---|
| start data | N = 132, k = 130, contraction constants 0.0886, 0.0888, 0.0886, 0.0888; bound of D²η 7.7×10⁻²⁰ | N = 132, k = 40; bound of D²η 9.96×10⁻¹⁹ |
| steps on the ray, the arc, the real axis | 2118, 863, 101 | 2118, 863, 101 |
| run time | 3334 s (2178, 947 and 111 s on the legs, 83 s for the start data) | 2269 s |
| radii at ξ₁: state box, V0, W, V(X) | 4.29×10⁻⁴, 1.10×10¹, 3.51×10²², 6.47×10⁸ | 4.29×10⁻⁴, 1.29×10¹, 3.47×10²², 6.47×10⁸ |
| Krawczyk on the whole box: K(X) ⊂ int X | yes; margins 0.996, 0.998, 0.889, 0.889, 0.912, 0.911 | yes; 0.996, 0.998, 0.889, 0.889, 0.912, 0.911 |
| zero's enclosure on the whole box, radius in A, ω/ω∞, B₃, C₃, B₅, C₅ | 3.66×10⁻¹³, 1.74×10⁻¹³, 1.00×10⁻¹³, 1.02×10⁻¹⁴, 1.03×10⁻¹⁴, 1.82×10⁻¹⁵ | 3.67×10⁻¹³, 1.74×10⁻¹³, 1.00×10⁻¹³, 1.02×10⁻¹⁴, 1.03×10⁻¹⁴, 1.83×10⁻¹⁵ |
| Krawczyk on the sub-box ±(10⁻¹⁸, 10⁻²⁶, 10⁻²⁷) | yes; margins 1.000, 1.000, 0.986, 0.986, 0.951, 0.951 | yes; 1.000, 1.000, 0.980, 0.980, 0.932, 0.932 |
| zero's enclosure on the sub-box, radius in A | 5.07×10⁻²³ | 6.08×10⁻²⁴ |

The two enclosures of the zero overlap in every parameter, on the whole box and on the sub-box. So the certificate
passes from the second implementation's start data, with the stored margins on the run's whole box. On the sub-box
the inner margins are slightly larger and the enclosure of the zero in the outer coordinates is 8 times wider; both
runs pass.

## The sign mutation, and a mistake in how it was run

The mutation: the second implementation's start data with the sign of [G P] flipped (values and both sets of
columns), then the same run. Criterion written before the runs: it must not pass the Krawczyk test, and a failed
run counts.

What happened. The mutated start data are accepted (four contractions hold for the other system, 0.0879 to 0.0881).
The ray takes 3248 steps (2118 clean) and ends with a state radius of 7.9×10⁻⁸ (2.0×10⁻¹⁰ clean). On the arc the step
size falls from 5×10⁻⁵ to 9×10⁻⁷, and after 52550 arc steps (863 clean) the run was at arc parameter 0.327 with W
radius 3.4×10⁵. It was stopped by hand (SIGTERM, exit 143) after 49339 s.

So the mutation yields no box file and no certificate. Its Krawczyk test was never reached, and the run counts as
"did not pass" only by the wording of the criterion. No stop rule had been written for it: it was started in the
background without a step cap and left for 13.7 hours of one core. A background run now gets a step or time cap
before it is left.

A cleaner control is to follow as a comment on the issue and a file here: the scale mutation ([G P] times
1 + 10⁻⁹) with `box2_run`'s own step cap of 6200, which should finish in the normal step count and then fail the
Krawczyk test.

## Recommended tasks

None beyond that control.
