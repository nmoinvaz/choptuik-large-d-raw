# I461-win2: the fixed re-seed (main d9e7f78) on Windows, then the crawl past D 215.03 with it

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/461 (follows from #446).

Worktree `D:\choptuik-i446`, detached at d9e7f78, made from `D:\choptuik-large-d` (whose own checkout stays at 188853c). Interpreter `venv-t126`
(Python 3.12.8; its `hpkernel` is `_hpkernel.cp312-win_amd64.pyd` built 2026-11-05 22:51 local, avx2, with the octo-double `Solver` entries; multidouble
Python package f092018). The newest commit touching `hp/src` on main is 1bad14f (M = 40 in the binding), after that build; the coordinator ruled at
08:20 UTC that it changes nothing for M = 32 and that part A runs with the venv as it is. `import reseed` from the worktree's `hp/` works.

Part A (`run_i461_a.sh`, 4 threads, the six runs one after the other): logs `A_<n>_*.log`, exits `exits.txt`.

## Part A result (2026-11-10 08:26 UTC)

Part A ran 2026-11-10 08:21:41 to 08:26:31 UTC (`exits.txt`), six runs one after the other at 4 threads beside #296's 18. `verdict_461_a.py` (`--selftest` ok:
required verdicts pass, a must-PASS that FAILs, a control that PASSes, an exit code that disagrees with the verdict and a missing log each give the
expected exit), output in `verdict_461_a_result.txt`, exit 0: **part A passes, all six as required**.

| run | must | win2 | on the M5 Mac |
|---|---|---|---|
| checkq d6 D 215.0 | PASS | PASS, u0 residual 8.78e-32 (64 s) | 8.78e-32 |
| the same, `--sweeps 1` (control) | FAIL | FAIL, stops at 1.21e-06 (12 s) | 1.21e-06 |
| checkq d6 D 209.0 | PASS | PASS, 1.07e-32 (66 s) | 1.08e-32 |
| checkq the crawl's D 215.0344 prediction | PASS | PASS, 6.89e-32 (64 s) | not run there |
| truthq d6 D 214.5 | PASS | PASS, error left 5.62e-63 in m_h, 1.14e-64 in a_h (68 s) | 5.6e-63, 1.1e-64 |
| the same, `--sweeps 1` (control) | FAIL | FAIL, error left 1.20e-32 in m_h, 1.83e-32 in a_h (16 s) | 1.2e-32 |

Every number agrees with the Mac's to the digits the issue gives, except the D 209.0 residual, 1.07e-32 against 1.08e-32, a last-digit difference at the
quad-double floor (the limit is 1e-24). The build: worktree `D:\choptuik-i446` at d9e7f78, `venv-t126`, `hpkernel` `_hpkernel.cp312-win_amd64.pyd` built
2026-11-05 22:51 local, multidouble Python package f092018. Logs `A_*.log` print every rung (the first pass at u 0.3 reads NOT converged and the repeated
block steps bring it to the floor).
