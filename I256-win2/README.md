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
