# I1096-mac: relaxed products in form S's Moebius horizon series, checks and timings

Machine: this Mac (Apple M5, 10 cores, 32 GB, macOS 27.0.1), shared with other sessions; runs at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1096

Code: choptuik-large-d branch `wip/large-d-fastmul` (hp's `form_s.rs` with `Solver.set_horizon_relaxed`,
`Solver.horizon_s` and `hp/form_s_relaxed.py`), on multidouble's branch `feat/series-mullow` (`series::mullow`,
`series::Relaxed`, `Lane::block_mul`). hp built with the `dev-o1` profile (opt-level 1) unless a file says otherwise.

States (inputs, not copied here), raw-data repository at e0fb6211f, git blobs (`git hash-object --no-filters`):

| D | file | blob | ks |
|---|---|---|---|
| 2000 | `I1088-dh610/L2000/lastnode_D2000.0000_step.npz` | 392276089bb4a24974e8359adad661a2a0bb72ba | 2618 |
| 10^4 | `I1088-dh610/L10000q/lastnode_D10000.0000_step0.npz` | f95c8269b4a2595f422ae6c919f20359615ef861 | 13018 |
| 2x10^4 | `I1088-mm5/L20000/guess_D20000.0000.npz` | 1f63b72bbfb3d3fde0d94450031af328064b3aec | 11416 |

Bars, written before the first run (form_s_relaxed.py check), relative to max |h| of the horizon block (p, m, c at
the last node): |h_relaxed - h_naive| <= 1e-28 (double-double), 1e-58 (quad-double), 1e-110 (octo-double). Control:
relaxed with the first square of the product c U left out (mutate 55) must miss the same bar.

- `check.jsonl`, `check_*.log`: the checks, one line per state and precision.
- `time.jsonl`, `time_*.log`: wall seconds, term by term against relaxed.

## Amendment 1 (2026-11-26 06:45 UTC, after the D 2000 check, before the D 10^4 and 2x10^4 checks)

At D 2000 the quad-double bar was missed: |h_relaxed - h_naive| = 3.6e-57 against 1e-58. The term-by-term quad-double
sums themselves err by 3.7e-57 against the octo-double ones there, and the relaxed ones by 1.5e-58, so the bar lay below
the precision's floor at that state. That verdict stays as it is. From here on, in double- and quad-double the bar is
also met when |h_relaxed - h_od| <= 2 |h_naive - h_od| (the relaxed sums as accurate as the term-by-term ones, against
octo-double), and the control must miss both. At D 2000 the double-double relaxed sums gave the term-by-term bits and
the control did not fire: double-double squares start at order 2 x 513 = 1026, and the series is below 1e-46 from about
0.56 n = 1120 on, so the squares touch only orders that do not reach double-double's rounding. That check is vacuous at
D 2000; at D 10^4 and 2x10^4 the squares reach the orders that matter.
