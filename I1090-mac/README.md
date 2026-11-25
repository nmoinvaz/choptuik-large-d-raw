# I1090-mac: form S with a Moebius horizon variable, precision and conditioning against D (the D-uniform route)

Machine: the Mac (Apple silicon, macOS), 1–2 processes at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1090

Code: `solver/inner_large_d/` on branch `wip/large-d-inner` of choptuik-large-d; notes `notes/LARGE_D_INNER.md` there.

| folder / file | what it holds |
|---|---|
| `f64_M6_cont/` | float64 continuation in D of form S (M 6) with the horizon series in t = (1 - z)/(1 + z): one JSON per D, `solve_cont.log` |
| `diag/` | per-order float64 against double-double errors of the affine horizon series, noise amplification per array and per variable |
| `f64_M6_cont_try1/` | the first float64 continuation, which jumped from D 100 to 125 from one point and did not converge there (kept as run) |
| `dd_M10_cont_try1/` | the first dd M 10 run (tol 1e-27, 2 rounds), stopped at D 100 when its split Newton stalled near 2.6e-24 with a difference step below dd resolution |
| `dd_M10_cont_try2..4/`, `dd_Mcont/` | later dd attempts, see below |

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

Restarts of the float64 continuation, appended to  (records ):
```
python3 solve_cont.py S/sol_D186.66_M6_f64.json --M=6 --Ds=186.66,200,225,245.64,263.6,300,350,400,500,... --out=L/f64_M6_cont --noise0=200,245.64,300,400 --accept=1e-9
python3 solve_cont.py S/sol_D400_M6_f64.json --M=6 --a=8 --Ds=400,450,500,600,800,... --out=L/f64_M6_cont --noise_as=1,32 --accept=1e-9   (crashed at D 800 on a non-finite step; driver fixed)
python3 solve_cont.py S/sol_D600_M6_a8.json --M=6 --a=8 --Ds=600,650,700,800,900,1000,1150,1300,1600,2000,2500,3200,4000,5000,6500,8000,10000 --out=L/f64_M6_cont --noise_as=1,32 --accept=1e-9
```
(S/sol_*.json are copies of the records of this folder at those D.) dd runs:  are the M 10
continuations in D from D 100 (stopped or failed: §4 of the note),  the M 8 solve at D 200 from the M 6 one
(stopped: no step along the weak directions). Diagnostics in : noise_variable, affine_orders, noise_at_solution
(per order band and a), f64_vs_dd, cost_vs_D, trackc_at, check_mobius(_dd).
