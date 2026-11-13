# I650-macm3: the sigma-model's Delta(eta) at M = 64 at the remaining six couplings

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3), rustc 1.99.1, maturin 1.16.0; worktree ~/Source/choptuik-large-d-b650 at origin/main fdcada23 (matter/sigma_ms, crate sigmams on multishoot and multidouble 4.2.1 per I639-mac's README). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/650 (recommended by #639; assigned by the coordinator's message of 2026-11-13 11:35 UTC, after #656). This folder is in a worktree of the raw repository (~/Source/choptuik-large-d-raw-641), pushed from there. Started 13:26 UTC.

Plan (the issue's): build the kernel with matter/sigma_ms/build.sh, FAST=1 (build_sigma_ms.sh, about 15 min and 5 GB), then chain.py --M 64 --resample_from 48 --etas 5,6,8.5,10,14,20 --extra "--jac mixed --jac_final mixed" --threads 4 --out <this folder>/data, with the six M 48 states of I639-mac/data (sm_eta<eta>_M48.npz; copied into data/ because chain.py reads them from --out) as the seeds. Written before the run (the issue's). Acceptance: at every eta |M64 - M48| <= 3e-11 in Delta, and the M 64 fit's eta_min lies within 2e-6 of M 48's; the task fails otherwise. About 1.5 h at 4 threads plus the build.

Build check (planted.py at M 8 on this build): unmutated PASS (Delta_qd - Delta_dd -4.09e-30, as I639-mac), --mutate gamma FAIL (exit 1, Delta_qd - Delta* -6.2e-12), logs in planted/. Build: exit 0 at 13:30:35 UTC. Production chain (run_650.sh) started 13:31 UTC.

## Results (13:50 UTC; build exit 0 13:30:35, chain M64 exit 0 at 13:47:31 UTC (31 to 47 min: six couplings in about 16 min), analyze650.py's output below; fit_min.py --selftest PASS with its two controls firing)

| eta | Delta at M 48 | Delta at M 64 | M 64 − M 48 | within 3e-11 | |F| at M 64 | source of the M 64 record |
|---|---|---|---|---|---|---|
| 5 | 0.45981784127566648566 | 0.45981784128027755105 | 4.611e-12 | yes | 7.4e-31 | this task |
| 6 | 0.45981079388719681069 | 0.45981079389449469856 | 7.298e-12 | yes | 3.1e-30 | this task |
| 7 | 0.45980936217076921496 | 0.45980936218022274262 | 9.454e-12 | yes | 1.0e-30 | I639-mac |
| 8.5 | 0.45981105877114418127 | 0.45981105878307577261 | 1.193e-11 | yes | 2.1e-30 | this task |
| 10 | 0.45981418368405653112 | 0.45981418369782841373 | 1.377e-11 | yes | 4.7e-30 | this task |
| 14 | 0.45982257284098088035 | 0.45982257285788141574 | 1.69e-11 | yes | 1.4e-30 | this task |
| 20 | 0.45983152655261315838 | 0.45983152657194675766 | 1.933e-11 | yes | 2.7e-30 | this task |
| inf | 0.45986109977073578969 | 0.45986109979581641524 | 2.508e-11 | yes | 2.1e-30 | I639-mac |

acceptance 1 (|M64 - M48| <= 3e-11 at each of the six): PASS
M 48: d4 eta_min 6.9801973, d5 eta_min 6.9801938, d6 eta_min 6.9801938, d7 eta_min 6.9801938; quoted (d6) eta_min 6.9801938, Delta_min 0.4598093617434287853, residual 1.9e-16
M 64: d4 eta_min 6.9801964, d5 eta_min 6.9801929, d6 eta_min 6.9801930, d7 eta_min 6.9801930; quoted (d6) eta_min 6.9801930, Delta_min 0.45980936175284405312, residual 1.9e-16

acceptance 2: eta_min(M 64) − eta_min(M 48) = -8.834e-07 (limit 2e-6): PASS
  degree 4: -8.833e-07
  degree 5: -8.834e-07
  degree 6: -8.834e-07
  degree 7: -8.834e-07
Delta_min(M 64) − Delta_min(M 48) = 9.415e-12
