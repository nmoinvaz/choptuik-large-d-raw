# I1025-win2/kc95_d225: macm3's k_c 87 leg state at D 22.5 regridded to k_c 95, then a hybrid sign scan around lambda_1

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 17:50 UTC, before any regrid or scan of this folder.
Everything here is `../kc95_d22/`'s: the order (quoted there, point 2 of the coordinator's hc of ~17:25 UTC: "first D 22.0, then D 22.5, each as soon as macm3 pushes that state"), the pins, the drivers `kc95_regrid.sh` and `kc95_scan.sh`
(called from that folder with this folder as the third argument), the tools in its `inputs/`, the commands, the acceptance and the thread and memory rules. Only D, the tag and the folder change:

    kc95_regrid.sh 22.5 l1kc95win2d225 kc95_d225      (python -u ell_refine.py l1kc87Lmacm3b 87 l1kc95win2d225 95 1 22.5 <lambda_0 = ell_delta.lam0_at(22.5)> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma; 4 threads, cap 21600 s)
    kc95_scan.sh  22.5 l1kc95win2d225 kc95_d225       (centre = macm3's k_c 87 root at D 22.5 + 0.003 rounded to 0.005, +-0.01 by 0.005 plus a repeat of the centre, four processes of one thread; prediction root + 0.003, bar 0.005)

The D 22.5 regrid waits for macm3's state and record row of D 22.5, for the tag g leap's end (all8.done) and for any other regrid of mine (one at a time); its scan waits for my other scans (the D 22.0 scan's four processes) to end.

## Status
- 2026-11-24 17:50 UTC: folder and README written; the lane for D 22.5 starts after D 22.0's lane is under way and waits for macm3's state (macm3's leg was at D 21.875 at 17:30 UTC, 783 s per point at h 0.03125, about 20 more points to D 22.5).
