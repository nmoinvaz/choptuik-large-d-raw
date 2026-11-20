# I1025-win2d: a new venv with multidouble 5.1.0 (dd_logdet, qd_logdet) for the #1025 share, and its planted dd_logdet check on win2

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task: the coordinator's hc of 2026-11-20 (read 17:27 UTC): a preparation job so that win2's share of #1025's l = 1 multiplet work can start as soon as xfkappa sends it. This folder holds the setup, the install log and the check; nothing of the share itself.

## Setup (written 2026-11-20 17:28 UTC, before any install)

| | |
|---|---|
| venv | **new**: `C:\Users\nathan\Source\venv-md510` (a name that did not exist), made with `python -m venv` from `C:\Users\nathan\AppData\Local\Programs\Python\Python314\python.exe` (Python 3.14.10; uv is not installed on win2). Every existing venv is left alone (venv-md482, venv-md491, venv-i600, venv-i962, venv-i1034 and the others) |
| requirements | the repo's `requirements.txt` at origin/main 1926c1c3 (sha256 prefix 9a539138a26f1a91, equal to my main checkout's; copied here): numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0, maturin 1.16.0. `pip install -r requirements.txt` first |
| multidouble | `pip install --no-cache-dir "multidouble @ git+https://github.com/nmoinvaz/multidouble@8c4360ac0be804d081faeea524e5c1c6e2fffaaa#subdirectory=python"` (release 5.1.0 with `dd_logdet` and `qd_logdet`, per the coordinator), built by maturin with rustc/cargo 1.96.0, `link.exe` of MSVC 14.51.36231 (`C:\Program Files\Microsoft Visual Studio\18\Community\VC\Tools\MSVC\14.51.36231\bin\Hostx64\x64`) put **first** on PATH (Git Bash's `/usr/bin/link` is GNU coreutils' and must not be found first). BelowNormal. Wall time recorded in `build.times`; cap 5400 s by the exact root pid (command line checked for `pip`; the estimate is 30 min, times 3) |
| record | `versions.txt`: pip's `direct_url.json` commit of the installed multidouble, `pip list`, `multidouble.__file__`, its version and ISA, rustc/cargo/link.exe versions |
| the check, fixed now (the coordinator's) | a planted 200 x 200 matrix with known det: `A = Q diag(d) Q^T` with Q orthogonal (seeded QR of a Gaussian matrix) and d known with **3 entries negative**. `multidouble.dd_logdet`'s **sign must be -1** and **ln|det| must equal sum ln|d_i| to 1e-12**. The control: the same matrix with **one row negated**, whose sign must flip (+1) (ln|det| unchanged). Run at BelowNormal from the new venv. I also compare, as information (not in the coordinator's criteria), with ln|det| of the matrix as stored (python-flint ball determinant at 300 bits of the double entries), because forming A in floating point moves its det from the planted one by rounding |
| not done | nothing of #1025's share; no existing venv, worktree or job touched |

## Readings fixed before the run

1. The install exits 0 and `pip`'s `direct_url.json` for multidouble names commit **8c4360ac0be804d081faeea524e5c1c6e2fffaaa**; `dd_logdet` and `qd_logdet` import.
2. The check: sign -1 and |ln|det|(dd_logdet) - sum ln|d_i|| <= 1e-12; the row-negated control returns sign +1. If the sign is right but ln|det| is off by more than 1e-12, that is reported with its size and where it comes from (the stored matrix's own det, flint) and nothing is loosened. A control that does not flip the sign stops the work.
3. The reply to the coordinator: the venv path, pip's `direct_url` commit, the check's numbers and the build time.

## Addendum 17:31 UTC, after the install and before the check ran

The install ended 17:30:22 UTC (exit 0, multidouble build 72 s; see Result). The API read from the installed package: \`dd_logdet(ah, al, par=False)\` returns \`(sign, ln|det A|, min |u_kk|, max |u_kk|)\`; **ln|det A| is a float64 sum of ln|u_kk|** and carries float64 rounding of about n 2^-53 (1 + sum |ln|u_kk||) (its doc), so the 1e-12 bar is about 100 times that bound here. \`logdet_check.py\` (this folder) adds, fixed now and before it runs:
- the planted matrix: n = 200, seed 20261120, Q = the Q of \`np.linalg.qr\` of a Gaussian matrix, d_i = s_i exp(u_i) with u_i uniform in [-0.7, 0.7] (magnitudes between 0.5 and 2.01) and s_i = -1 at 3 random positions (seeded), +1 elsewhere; A = Q diag(d) Q^T in float64, passed as (A, zeros). The planted exact value sum ln|d_i| is summed in mpmath at 50 digits from the d_i as stored.
- criteria (the coordinator's): sign -1 and |ln|det| - sum ln|d_i|| <= 1e-12. Control: row 0 negated, sign must be +1 and ln|det| equal to the unnegated one within 1e-12.
- information, no criterion: ln|det| and sign of the matrix **as stored** by python-flint (arb_mat at 600 bits, entries exact), the difference of dd_logdet from it (expected near the float64 bound above), the difference of the planted value from it (the rounding in forming A in float64, including Q's departure from orthogonality, expected about 1e-14), \`par=True\` against \`par=False\` (documented to give the same bits), and qd_logdet's sign and ln|det| on the same matrix (a0 = A, others zeros).
- the check can fail: \`--mutate=lnd\` scales d_0 by 1 + 1e-9 in the expected value only, which must make the ln|det| check fail (exit 1), and the row-negated control above is the sign check's control.
- exit 0 only if all criteria hold; run once at BelowNormal from venv-md510 (\`OPENBLAS_NUM_THREADS=1\`). A failure is reported with its numbers; nothing is loosened.

## Result

Not yet run.
