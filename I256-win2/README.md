# I256-win2: K 39, J 1000 at omega/omega_inf 1.09, 1.10 and 1.11, to test the 1.10 K 45 node

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/256 (recommended by win2 in #202's summary, its task 2).

Command, from `solver/inner_amp/` of `D:\choptuik-large-d` (main checkout at 188853c), Python 3.14.10 (`venv-t177`, python-flint 0.9.0 /
FLINT 3.6.0), Normal priority, no affinity, the three nodes at once beside #228 and #247 (`run_i256.sh`; logs `w<wf>.log`, exits in
`exits.txt`):
`amp_flint_par.py <wf> 39 1000 1280 --procs 3 --fit phys --mf 6:12 --out <this folder>/sigF_w<wf>_K39_J1000_p1280.json`
for wf = 1.09, 1.10, 1.11. #228 keeps priority for memory (coordinator): `mem_watch.sh` only alerts (writes `MEM_ALERT` and exits)
when free memory falls below 22 GB, and then the three nodes are paused or serialized by hand; nothing kills a process.

`compare_256.py` tabulates |sigma_n(K 39) - sigma_n(K 33)| and |sigma_n(K 45) - sigma_n(K 39)|, relative to |sigma_n(K 45)|, at
n = 6, 7, 15 and 16 (and for n = 1 to 16 in a second table), per node, from the 20 stored digits (mpmath, 50 digits): K 33 from
`../T155-win2` (1.09, 1.11) and `../I202-win2` (1.10), K 45, J 1500 from `../I82-win2`. It checks the acceptance: the 1.10
K 39 -> K 45 step is not larger than the larger of the 1.09 and 1.11 steps at those orders, or the orders where it is are named.
`--selftest`: the code reproduces #82's posted K 45 against K 33 rows, and a planted K 39 equal to K 45 gives zero K 39 -> K 45 steps
and a K 39 equal to K 33 gives zero K 33 -> K 39 steps.

## Results (2026-11-09 22:45 UTC)

The three nodes ended with exit 0 (`exits.txt`): w 1.10 after 25 517 s (22:41:31 UTC), w 1.09 after 25 532 s (22:41:46), w 1.11 after 25 556 s
(22:42:10), started 15:36:13 UTC; products about 3010 s, fits about 22 460 s each. `compare_256.py` (`compare_256.log`, exit 1: the 1.10
K 39 -> K 45 step is above the neighbours' at n = 6, 7, 15, 16; selftest ok). Relative steps from the 20 stored digits, relative to
|sigma_n(K 45)|, step1 = K 33 -> K 39, step2 = K 39 -> K 45:

| n | 1.09 step1 | 1.09 step2 | 1.10 step1 | 1.10 step2 | 1.11 step1 | 1.11 step2 |
|---|---|---|---|---|---|---|
| 6 | 0 | 0 | 0 | 9.72e-21 | 0 | 0 |
| 7 | 0 | 6.68e-20 | 0 | 1.2e-18 | 0 | 3.63e-19 |
| 15 | 0 | 2.48e-16 | 0 | 4.03e-16 | 0 | 2.76e-16 |
| 16 | 3.11e-18 | 3.49e-16 | 7.89e-19 | 1.23e-15 | 9.37e-20 | 4.42e-16 |

step1 is exactly 0 for n = 1 to 15 at all three nodes: sigma_n of K 39 equals that of K 33 to all 20 digits (sigma_n depends on orders k up to 2n + 1
only, and the files share J 1000; the precision differs, 960 and 1280 bits). So the K 33 -> K 45 gap at n <= 15 is not a K effect. The 1.10 step2 is above
the larger of the 1.09 and 1.11 steps at n = 6, 7, 15, 16 (ratios inf, 3.3, 1.46, 2.79), the same four orders as #202.

J convergence at the same orders (from the existing files, not a new run): |sigma_n(J 1250) - sigma_n(J 1500)| from #213 (K 45, new firmware) against #82,
and |J 1000 - J 1500| from the K 33 files:

| node, n = 16 | J 1000 against J 1500 | J 1250 against J 1500 | J 1000 against J 1250 |
|---|---|---|---|
| 1.09 | 3.49e-16 | 9.38e-17 | 4.0e-16 |
| 1.10 | 1.23e-15 | 4.89e-17 | 1.19e-15 |
| 1.11 | 4.43e-16 | 5.18e-17 | 4.59e-16 |

At n = 15 (1.10): 4.03e-16, 2.32e-17, 4.26e-16; at n = 6, 7, 8 the J 1250 and J 1500 values are equal to all 20 digits at 1.10.
