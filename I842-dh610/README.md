# I842-dh610: the arclength chain around the fold at D 259.8875, from #603's chain_nsr state (cross-machine to I842-mac/pilot3)

Machine dh610 (Fedora 45, i7-12700, 20 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/842.
Code: `hp/arclength.py` and `anm_run.py --arclength` at main 44275d99, worktree `choptuik-large-d-842`, run with #855's
venv (hpkernel from the 7e4cfd03 build; main differs from it only in multidouble 4.6.0's clu_pivots, which the chain path
does not use). Launcher `run842.sh` (the coordinator's one-line command of 2026-11-16, 9 threads, nice 10), log
`chain.log`, exits in `exits_842.txt`, output `chain/`. Step 0 repeats I842-mac/pilot3 (xfkappa's pilot, the Mac).
