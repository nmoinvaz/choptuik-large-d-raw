# I1025-mac/ellcond: the conditioning of the l = 1 solve at D 19.75, k_c 87, and where the Linux and macOS states differ

Coordinator (hc t5) on the Mac, 2026-11-23. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025.
Code: choptuik-large-d branch `wip/ell-cond`, `solver/matter/ell_cond.py`. States from raw: A = dh170's Linux k_c 87
D 19.75 state (blob 352107a8), B = macm3's macOS state of the same source (blob 5825f5d0).

| file | what |
|---|---|
| `plant.log`, `plant.json` | control: B = A + 1e-6 v_min; reads 1.000000e-06 on v_min, others 2e-18: PASS |
| `real.log`, `real.json` | J's 8 smallest singular values 2.3e-16 to 8.1e-16 (sigma_max 12.2); B - A (7.90e-6, Delta +1.41e-6) has components of about 1e-12 along those 8 and 7.90e-6 outside them; |J dz| 1.45e-11 against |F(B) - F(A)| 1.34e-11 |

Reading: the states differ along weak directions (|J dz| / |dz| about 1.8e-6), not along the floor (null) directions;
the residual still tells the two apart at 1.3e-11, above the 1e-12 rounding noise between builds.
