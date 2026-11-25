# I1090-mac: form S with a Moebius horizon variable, precision and conditioning against D (the D-uniform route)

Machine: the Mac (Apple silicon, macOS), 1–2 processes at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1090

Code: `solver/inner_large_d/` on branch `wip/large-d-inner` of choptuik-large-d; notes `notes/LARGE_D_INNER.md` there.

| folder / file | what it holds |
|---|---|
| `f64_M6_cont/` | float64 continuation in D of form S (M 6) with the horizon series in t = (1 - z)/(1 + z): one JSON per D, `solve_cont.log` |
| `diag/` | per-order float64 against double-double errors of the affine horizon series, noise amplification per array and per variable |
| `f64_M6_cont_try1/` | the first float64 continuation, which jumped from D 100 to 125 from one point and did not converge there (kept as run) |
| `dd_M10_cont/` | double-double continuation in D of form S (M 10), the Moebius horizon variable, exact forward-mode Jacobians: one JSON per D, `solve_dd_cont.log` |

The seeds of `diag/noise_variable.log` are Track B's D-100 form-S solution (`I1088-mac/Sdd_D100_M8.json`) rescaled to each D.
Commands: in `notes/LARGE_D_INNER.md` §9 on the branch.
