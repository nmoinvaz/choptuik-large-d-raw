# I1098-dh610/ksdown: the downward ks gate at the jump states of D 4000 and D 4628 (#1098)

Machine: dh610 (Fedora, i7-12700), fastmul7 (site_z, hp_z at c21ba40d), 4 threads. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1098

`ks_gate.py --down 1` (wip/large-d-form-s, final version 3b3bfc60, run as hp_z/ks_gate_v2.py) starts at a ks that meets
the bar. It steps ks down while the octo-double residual's change from ks - step to ks stays at most the bar. The
measure is the one the upward gate uses: the change at a ks when the series runs to ks + step. Its control moves Delta
by 1e-40 at the gated ks; that must change the residual by more than the bar.

**D 4000** (mm5's converged jump state, `jump_s_D4000.0000.npz`, sha256 d542ecda, ks 6017, a 9.995, kfreeze 13):

| ks change | residual change |
|---|---|
| 6017 → 6217 | 2.0e-89 |
| 5017 → 6017, five steps | exactly 0.0 each (bitwise-identical residuals) |
| 4817 → 5017 | 7.69e-103 |
| 4717 → 4817 | 5.01e-75 |
| 4617 → 4717 | 2.92e-52 |

- **ks 4717 meets both 1e-64 and 1e-70; 4617 meets neither** (`D4000.log`, `D4000_b.log`, `D4000_d.log`).
- The control at 4717 reads 1.98e-36 and fires (`D4000_d.log`).
- The first two controls read 0.0 (`D4000.log`, `D4000_b.log`). They added the 1e-40 to the octo-double value's second part, whose unit in the last place is about 1e-33, so it was lost to rounding. The control now adds it to the third part.
- Near ks 4700 the series falls about 1e23 to 1e28 per 100 orders. At D 300 (a 8) it falls about 1e16 per 200.

**D 4628**: `D4628.log`, run once its restarted jump (I1098-dh610/ladder/D4628) has converged.

**D 2000's ks 3417**, which was set by hand and not gated: ks_gate.py on its final state (h25, M 48, kfreeze 23) reads
a change of exactly 0.0 at 3417 → 3617 against a bar of 1e-64 (gate2000.log in I1098-dh610/fix6/D2000_M48_6b).
