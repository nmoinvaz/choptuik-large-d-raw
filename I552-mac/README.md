# I552-mac: det M's pivots under one ulp of dh at D 61.03, M 48, kf 13 (development test of modecount_pivots.py)

Machine: the Apple M5 Mac (coordinator). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/552

`hp/modecount_pivots.py` (main ecca9c5) on `hp/data/modecount_state_D61.0264_M48_kf13.npz` at lambda = 3.1023 - 0.0068i,
`--M=48 --kf=13 --fmax=1e-14` (this state polishes only to |F| 2.7e-15 in the layout), entry dh[10, 11], with a
modecount_cx built from main 01f2070 plus `cpivots` (thin build, no fat LTO; Rust's floating point does not change with
LTO).

| perturbation | relative size | change of ln\|det\| | pivots moved > 1e-3 | verdict |
|---|---|---|---|---|
| high part +1 ulp | 2^-53 | +28.611 | 22 of 1152 (90% in 6) | localized |
| high part -1 ulp | 2^-53 | +30.238 | 22 (90% in 7) | localized |
| double-double +1 ulp | 2^-106 | 0.000 | 0 | between (printed; "none" in ecca9c5) |
| double-double -1 ulp | 2^-106 | 0.000 | 0 | between (printed; "none" in ecca9c5) |

Checks: planted L U control pass (r 3 moved 3, r 0 moved 0), consistency with mode_det pass, determinism pass.
