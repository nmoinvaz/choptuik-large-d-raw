# I994-mac: the l = 1 multiplet's inner selection and growth rate at D = infinity, M = 1 and M = 3 (logs)

Machine: Mac (Apple silicon), helper session xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/994

Code: branch `wip/ell1-dinf` of choptuik-large-d at aff9c2fa. `solver/inner_stokes/inner_ell.py` holds the M = 1 zero,
`solver/inner_stokes/nested_ell.py` the M = 3 zero, and `solver/inner_pert/ell_lam.py` the growth rate (on
`first_order_jet.py` with `ELL`). Each log starts with its command and the UTC time and ends with the exit code. The
`inner_ell` and `nested_ell` commands run from `solver/inner_stokes`, the `ell_lam` ones from `solver/inner_pert`.

| log | what it checks |
|---|---|
| `sym.log` | the solver's equations against the psi system (sympy, l symbolic), with a control that must be nonzero |
| `checklin_M{1,3}_l{0,1,2}.log` | the flat jump against 2 pi i K'(i nu w + l) times the flat fast solution |
| `zero_l0_planted.log`, `zero_l0_mutate_grav.log` | the planted l = 0 M = 1 zero, and l = 0 with the gravity weight of l = 1 (must fail) |
| `zero_l1_first.log`, `zero_l1_second*.log`, `zero_l1_third*.log` | the l = 1 M = 1 zeros at three xi1 each |
| `zero_l1_delta*.log`, `zero_l1_rtol1e-13.log`, `zero_l1_margin14.log` | the first l = 1 zero with the ray angle, rtol and r0 margin changed |
| `zero_l1_mutate_grav.log` | l = 1 with the unweighted gravity (must fail) |
| `scan_l1.log` | the M = 1 ratio on a grid A 2..80, w/w_inf 1..5, with its local minima refined |
| `m3_l0_planted.log`, `m3_l1_pilot.log`, `m3_l1_zero.log` | the M = 3 zeros: l = 0 planted, then the l = 1 pilot (stopped by hand at its noise floor) and the l = 1 zero at three xi1 |
| `lam_ident*.log`, `lam_cross*.log`, `lam_modes*.log` | the jet model at ELL = 0 against the base commit, at ELL = 1 against inner_ell, and the exact modes lambda = 0 and 1, each with its mutation |
| `lam_l0_planted.log`, `lam_scan_l1.log`, `lam_l1_M1.log` | lambda* at M = 1: l = 0 planted, the l = 1 scan of the deflated determinant, and the l = 1 root at three xi1 |
| `lam3_l0_planted.log`, `lam3_l1.log`, `lam3_l1_rtol1e-13.log` | lambda* at M = 3: l = 0 planted, and l = 1 at three xi1 at two rtols |
