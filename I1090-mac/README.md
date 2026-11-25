# I1090-mac: form S with a Moebius horizon variable, precision and conditioning against D (the D-uniform route)

Machine: the Mac (Apple silicon, macOS), 1–2 processes at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1090

Code: `solver/inner_large_d/` on branch `wip/large-d-inner` of choptuik-large-d; notes `notes/LARGE_D_INNER.md` there.

| folder / file | what it holds |
|---|---|
| `f64_M6_cont/` | float64 continuation in D of form S (M 6) with the horizon series in t = (1 - z)/(1 + z): one JSON per D, `solve_cont.log` |
| `diag/` | per-order float64 against double-double errors of the affine horizon series, noise amplification per array and per variable |
| `f64_M6_cont_try1/` | the first float64 continuation, which jumped from D 100 to 125 from one point and did not converge there (kept as run) |
| `dd_M10_cont_try1/` | the first dd M 10 run (tol 1e-27, 2 rounds), stopped at D 100 when its split Newton stalled near 2.6e-24 with a difference step below dd resolution |
| `dd_M10_cont/` | double-double continuation in D of form S (M 10), the Moebius horizon variable, exact forward-mode Jacobians: one JSON per D, `solve_dd_cont.log` |

The seeds of `diag/noise_variable.log` are Track B's D-100 form-S solution (`I1088-mac/Sdd_D100_M8.json`) rescaled to each D.
Commands: in `notes/LARGE_D_INNER.md` §9 on the branch.

Commands as run (from `solver/inner_large_d/` of the branch, nice 10, OMP_NUM_THREADS=1; S = the scratch folder holding
copies of `I1088-mac/Sdd_D100_M8.json` and `Sdd_D100_M10.json`, L = this folder):
```
python3 solve_cont.py S/Sdd_D100_M8.json --M=6 --Ds=100,125,150,200,245.64,263.6,300,400,500,700,1000,1500,2000,3000,5000,10000 --out=L/f64_M6_cont_try1 --noise0=100,150,200,245.64,300,400
python3 solve_cont.py S/Sdd_D100_M8.json --M=6 --Ds=100,110,125,150,175,200,225,245.64,263.6,300,350,400,500,600,800,1000,1300,1600,2000,2500,3200,4000,5000,6500,8000,10000 --out=L/f64_M6_cont --noise0=100,150,200,245.64,300,400
python3 solve_dd_cont.py S/Sdd_D100_M10.json --M=10 --Ds=100,110,125,150,175,200,225,245.64,263.6,300,350,400,500,600,800,1000 --out=L/dd_M10_cont_try1
python3 solve_dd_cont.py S/Sdd_D100_M10.json --M=10 --Ds=100,110,125,150,175,200,225,245.6366177558899,263.6,300,350,400,500,600,800,1000 --out=L/dd_M10_cont --tol=1e-22 --rounds=1 --outer=4
python3 affine_orders.py S/Sdd_D100_M8.json --Ds=100,200,245;  (from hp/) python3 ../solver/inner_large_d/trackc_at.py L/diag/trackc_at.json <the run D>
python3 noise_variable.py S/Sdd_D100_M8.json --Ds=100,150,200,245,300,400 [--mutate=affine]
python3 check_mobius.py S S/Sdd_D100_M8.json [--mutate=Lk];  python3 check_mobius_dd.py S S/Sdd_D100_M8.json --kb=150
```
(the first run used solve_cont.py as committed in b8312af2; the second the version committed in 6e231f5a, which adds
the refinement on failure; the dd run the solve_dd_cont.py of 6e231f5a; each was started before its commit, unchanged)
