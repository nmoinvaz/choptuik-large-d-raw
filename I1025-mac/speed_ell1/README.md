# I1025-mac/speed_ell1: the fast l = 1 mode matrix, the fast double-double block 12 and the Brent refinement, checked on the Mac

Machine: the Mac (Apple M5, macOS 27), venv-1025dd (numpy 2.5.4, scipy 1.18.1, multidouble with dd_logdet), one BLAS
and one rayon thread per process, nice 10, beside other users' jobs. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025

Code: branch wip/ell1-speed of choptuik-large-d, solver/matter/ell_fastm.py, ell_fastdd.py, d18_secant.py, and the
note solver/matter/SPEED_ELL1.md, which reads these files. Commits per run below; dss_ell.py, ell_ddm.py and ddnp.py
equal 505d8399 in all of them.

## Inputs (read in place from this repository; blobs by git hash-object --no-filters)
| state | stub | from |
|---|---|---|
| sol_l1kc31r1025_D10.5000.npy f07a8984 | l1kc31r1025.jsonl e5a87ec5 | I1025-mac/out/ |
| sol_l1kc55F1025_D18.125000.npy 88ccda5c | l1kc55F1025.jsonl 0fb77df8 | I1025-mac/out/ (the pins of I1025-mac/d18/lane_d18m.sh) |
| sol_l1kc103dh610d22125_D22.1250.npy 7c8d7ad2 | l1kc103dh610d22125.jsonl 1e903b8b | I1025-dh610/kc103_d22125/ |
Every run printed "the record system" (d18_hybsign.py's residual and step check) before using its state.

## runs/
- `sec55/`: d18_secant.py (0f2e8267), k_c 55, D 18.125, bracket (1.77, 1.78), tol 1e-6, fast M (jac), ell_ddm's block 12:
  root 1.7733011670, bracket [1.7733011508, 1.7733016508], 6 evaluations, 1057 s.
- `sec55cs/`: the same with --mm=cs --b12=ddm (d18_hybsign.py's evaluation; d8b0cf67): root 1.7732997423, bracket
  [1.7732990863, 1.7732999430], 6 evaluations, 2378 s. Its ends equal the scan records
  (I1025-mac/d18/d18125k55_scan_1025.jsonl) to all printed digits.
- `sec103/`: d18_secant.py (d8b0cf67), k_c 103, D 22.125, the ends 0.485 and 0.490 only (--maxev=2, a timing estimate),
  fast M and ell_fastdd's block 12: signs - and + as dh610's scan, ln|det| off its records by 2.7e-5 and 1.5e-3;
  1316 s and 563 s.
- `repro/`: d18_hybsign.py (blob e089207a) at 1.77 on the k_c 55 state: ln|det| -1617.4278109138, the scan record.

## checks/
The ell_fastm, ell_fastdd and d18_secant checks and controls (exit codes in final_selftests.log), the block-12 error
split (b12split55.log), and the timing runs. Their reading is in SPEED_ELL1.md.

## scripts/
The scratch scripts behind checks/ (time103.py, bench103.py, bench103b.py, b12split.py, prof_*.py, mb*.py). They
import the branch's solver/matter by an absolute path on the Mac.
