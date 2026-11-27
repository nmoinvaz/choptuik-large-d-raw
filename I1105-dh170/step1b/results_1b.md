| run | u0 | \|F\| | steps | psi-constraint | Delta | re-solve s | root (lam_lin) | lam_brent | final bracket | evals |
|---|---|---|---|---|---|---|---|---|---|---|
| U30 | 0.03 | 2.5624e-10 | 2778 | 1.845997e-04 | 1.001713513723048 | 2474 | - | - | not read: status nonrobust, robust [True, True], signs [-1.0, 1.0] | - |
| U40 | 0.04 | 1.7851e-10 | 2565 | 1.848253e-04 | 1.0017134267209413 | 2354 | 2.244901715 | 2.244901714 | (2.2449017139438805, 2.2449017639438806), width 5.00e-08 | 9 |
| U50 | 0.05 | 1.8882e-10 | 2400 | 1.848210e-04 | 1.0017132544654048 | 2301 | 2.244909506 | 2.244909505 | (2.244909505429695, 2.2449095972613335), width 9.18e-08 | 8 |

- root(U40) = 2.244901715; against P4's re-root of the record at u0 0.04 (2.2440428096): +8.589e-04 (information)
- T3: T3 not formed (not read: status nonrobust, robust [True, True], signs [-1.0, 1.0])
- T5 = root(U50) - root(U40) = +7.7915e-06: |T5| <= 1e-4: as predicted
- predictions for information: T3 about -1.5e-5 (u0^-9.7), a linear law about -4e-4; T5 about +9e-7
