# I895-mac: the five newly documented B8 commands, run as written and compared with their stored files

Machine: mac (Apple M5 Mac), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0 with FLINT 3.6.0), one
process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/895. Code: branch `wip/sa-895` on main
4c4bde73, which adds the commands to proof/B8_constants.md §13 and proof/B_chain.md §11.

`check_i895.py <checkout> <python's bin directory>` reads each command from its reproduce block, cuts its comment,
and runs it with bash from `solver/proof`. It compares the result with the stored file as committed, and restores
the file afterwards. A scan appends to its log, so its new records are compared with the stored ones in order. The
atoms run prints, and is compared with the second half of its log. The (H8) run overwrites its log, and is compared
with the stored log without its last line `exit 0`.

| command | stored file | lines or records | largest relative difference |
|---|---|---|---|
| `python3 b8m_atoms.py 4 2e-6 2e-6` | `b8m_atoms_K4.log`, second half | 53 | 0 |
| `nice -n 10 python3 b8m_scan.py 4 73.89,70,66,62,58 --rA=2e-6 --rW=2e-6 --log=b8m_scan_K4_box.log` | `b8m_scan_K4_box.log` | 5 | 0 |
| `for d0 in 1e5 1e6 1e7 1e8 1e9; do python3 b8m_scan.py 4 73.89 --d0=$d0 --rA=2e-6 --rW=2e-6 --log=b8m_scan_K4_d0.log; done` | `b8m_scan_K4_d0.log` | 5 | 0 |
| `python3 b8m_scan.py 4 90 --kappa1=0.7308324141810887 --rA=2e-6 --rW=2e-6 --log=b8m_scan_K4_fixedZ.log` | `b8m_scan_K4_fixedZ.log` | 1 | 0 |
| `python3 b8m_h8.py 4 104.68 --log=b8m_scan_K4_k0.85.log --kappa1=0.85 > b8m_h8_K4_L104.68_k0.85.log` | `b8m_h8_K4_L104.68_k0.85.log` | 12 | 0 |

`check.txt`: CHECK 895: PASS, exit 0. The bound of the issue is 1.7×10⁻¹¹, and the differences are exactly 0 because
the stored files were made by this code on this machine (#890). Wall times are not compared.

The control `--mutate=kappa1` runs the fixedZ command with κ₁ = 0.73 in place of 0.7308324141810887
(`check_mut_kappa1.txt`): the record differs by 5.2×10⁻² and in its `kappa1` field, CHECK 895: FAIL, exit 1.

κ₁ = 0.7308324141810887 is Z cos κ ln n₀ with Z = 0.0085, κ = 0.3 and ln n₀ = 90, in double precision.
