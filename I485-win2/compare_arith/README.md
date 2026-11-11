# I485-win2/compare_arith: the double-double sources before and after 93402cf8

Machine win2, issue https://github.com/nmoinvaz/choptuik-large-d/issues/485. `compare_arith.sh` compares `hp/src/{dd,dv,exact,linalg,v8,qd,qv}.rs` of 0a131faf
(the last kernel with its own arithmetic) with the multidouble crate's `src/` at 5fb516b (the pin of 93402cf8), both formatted with rustfmt and the crate's
`rustfmt.toml`, and prints how many lines differ. Run as `bash compare_arith.sh /d/choptuik-large-d <multidouble checkout at 5fb516b> out` (here
`~/.cargo/git/checkouts/multidouble-2ee9e3c95fe1538e/5fb516b`). Results (`out/*.diff`, the formatted copies in `out/old` and `out/new`):

| file | differing lines | what they are |
|---|---|---|
| dd.rs | 2 | `TWO_PI.hi` written as `std::f64::consts::TAU` (the same double, 6.283185307179586) |
| dv.rs | 0 | |
| exact.rs | 0 | |
| linalg.rs | 37 | `ld % 8 == 0` as `ld.is_multiple_of(8)` in three asserts; `solve_lanes` and `solve_lanes_hi` moved to hp's trait `field::FieldSolve` |
| v8.rs | 461 | new backends (sse2, neon, portable) and their doc, the cfg of each backend gets `not(feature = "portable")`; the AVX2 module (old lines 150 to 329) has no hunk |
| qd.rs, qv.rs | 22, 20 | not used by the solver or by `modecount_cx` at these commits |

Control: the script also plants a change of `two_prod` (`a.mul_add(b, -p)` as `(a * b) - p`) in a copy of dd.rs and requires that the planted copy differs.
So the rounding of the double-double sum, product, the `DotAcc` accumulation (dv.rs) and the LU (linalg.rs) did not change in 93402cf8, and neither did the
AVX2 vector backend that win2 runs. `Lane for DV` is also the same text in the crate's `dual.rs` and in hp's old `lane.rs`.
