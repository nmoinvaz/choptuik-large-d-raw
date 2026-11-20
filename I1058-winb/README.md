# I1058-winb: multidouble 5.1.0 Python package on the win laptop (no hp build), and its planted dd_logdet check

Machine: winb, Surface Laptop 4 (i7-1185G7, 4 cores, 8 threads), 31.8 GB, Windows 11. Written 2026-11-20 18:22 UTC. Issue: #1058 (update all machines to the latest multi libs, main 7ca74dd5). The check below was asked for by the coordinator on #1025's lane (hc 2026-11-20, about 18:19 UTC) so that the venv is verified before any share that needs it.

## What this machine does for #1058

No hp build. #1058's table row for winb: multidouble's Python package only (the new venv), since the Windows hp build needs about 30 GB and the laptop has 31.8 GB. So there are no stored-reference checks (highm_check, scaled, jets) here.

## The venv

| item | value |
|---|---|
| path | `C:/Users/nathan/Source/venv-md510` (new; every existing venv untouched) |
| Python | 3.14.10 (`python -m venv`, base `C:/Users/nathan/AppData/Local/Programs/Python/Python314`) |
| requirements | the repo's `requirements.txt` at main 17ae55bf (identical to origin/main's): numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0, maturin 1.16.0; `pip install --no-cache-dir -r`, 40 s |
| multidouble | 5.1.0, `pip install --no-cache-dir -v "multidouble @ git+https://github.com/nmoinvaz/multidouble@8c4360ac0be804d081faeea524e5c1c6e2fffaaa#subdirectory=python"` |
| pip direct_url commit_id | 8c4360ac0be804d081faeea524e5c1c6e2fffaaa (requested_revision the same; `direct_url.json` in this folder) |
| build | 2026-11-20 17:28:49 to 17:30:52 UTC, **123 s** (2.0 min) for the multidouble wheel; whole job 168 s; rustc and cargo 1.95.0, host x86_64-pc-windows-msvc |
| linker | MSVC's `link.exe` first on PATH (Visual Studio 18 Community, vcvars64.bat; `C:/Program Files/Microsoft Visual Studio/18/Community/VC/Tools/MSVC/14.51.36231/bin/HostX64/x64/link.EXE`) |
| priority | BelowNormal |
| import | `multidouble.dd_logdet` and `multidouble.qd_logdet` present |

The build ran before the order to stop it came in; it was not interrupted.

## The planted dd_logdet check (criteria fixed before the run, the coordinator's)

On a planted 200 x 200 matrix A = Q diag(d) Q^T with known det (d known, 3 entries negative), `multidouble.dd_logdet`'s sign and ln|det| must match the exact values (sign -1, ln|det| = sum ln|d_i|) to 1e-12. The control, the same matrix with one row negated, must flip the sign. Run at BelowNormal.

My construction (`check_dd_logdet_1025.py`): seed 1025, Q from a QR of a normal matrix (orthogonality error 1.6e-15), |d_i| log-uniform in [0.9, 1.11], negatives at indices 21, 39, 78, cond(A) 1.23. The range of |d_i| is my choice: the documented float64 rounding of ln|det| is up to n 2^-53 (1 + sum |ln|u_kk||), which for this range is under 5e-13, so the 1e-12 bar is attainable by construction. The exact ln|det| is computed with mpmath at 50 digits.

### Result: PASS (2026-11-20 18:20:10 to 18:20:45 UTC)

| item | value |
|---|---|
| exact sign, exact ln\|det\| | -1, 0.9712404448739763 |
| dd_logdet sign | -1.0 (OK) |
| dd_logdet ln\|det\| | 0.9712404448739694, error -6.88e-15 (bar 1e-12) |
| min, max \|u_kk\| | 0.5238, 11.85 |
| control (row 17 negated): sign, ln\|det\| | +1.0 (flipped, OK), 0.9712404448739694 (difference 0.0) |
| par=True against par=False | same bits |
| qd_logdet (extra) | sign -1.0, ln\|det\| 0.9712404448739694 (error -6.88e-15, equal to dd_logdet's) |
| mpmath det of the stored float64 matrix (extra) | sign -1, ln\|det\| 0.9712404448739688; dd_logdet minus it 6.7e-16 (30 s) |

The 6.9e-15 error against the exact value is the matrix construction (Q is orthogonal to 1.6e-15, A is rounded to float64), not the routine: against the stored matrix the routine is within 7e-16.

## Files

| file | what |
|---|---|
| `README.md` | this file |
| `check_dd_logdet_1025.py`, `check_dd_logdet_1025.log`, `check_dd_logdet_1025.json` | the check, its output and its numbers |
| `run_check_dd_logdet_1025.cmd` | the launcher (BelowNormal) |
| `direct_url.json` | pip's record of the installed package |
| `build_md510_1025.log`, `driver_md510_1025.py`, `build_md510_1025.cmd` | the venv and build job: log with UTC times, driver, launcher |
