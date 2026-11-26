# I1098-mm5/ladder/D622/ksgate: the od ks gate on D 622's jump state (#1098)

As for D 1291 (`../../D1291/ksgate/README.md`): the jump loop's ks+200 |dF| is the quad-double residual's change (ks 950: 5.9e-58; ks 1150: an exact 0.0e+00, below that check's resolution), so the ks the loop settled on, **1150**, is confirmed by
`hp/ks_gate.py` (raw/main f398e829, `~/Source/choptuik-fastmul6c`, octo-double residual change from ks to ks + 200), bar **1e-64** (the order's KSBAR), 2 threads, on a copy of the jump state.
Bar, written before the run: the od change from ks 1150 to 1350 is at most 1e-64 (the order's bars: the ks gate passes). If it is not, report and stop D 622.

## Result (2026-11-26 18:30 UTC; `ksgate_1150.log`)

`ks_gate.py` on a copy of the jump state (blob bcad2eed292c59ea8893d42a0b9f5998b08da62f; meta D 622, M 32, kc 200, ks 1150, Moebius a 8), started 18:29:24 UTC, about 1 min, 2 threads:
**ks 1150 -> 1350: octo-double residual change 2.96e-74** (bar 1e-64): the gate passes at ks 1150. The jump loop's own check read 5.9e-58 at ks 950 and an exact 0.0e+00 at ks 1150 (qd resolution).
