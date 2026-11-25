# I1025-win2/kc95_d225: macm3's k_c 87 leg state at D 22.5 regridded to k_c 95, then a hybrid sign scan around lambda_1

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 17:44 UTC, before any regrid or scan of this folder.
Everything here is `../kc95_d22/`'s: the order (quoted there, point 2 of the coordinator's hc of ~17:25 UTC: "first D 22.0, then D 22.5, each as soon as macm3 pushes that state"), the pins, the drivers `kc95_regrid.sh` and `kc95_scan.sh`
(called from that folder with this folder as the third argument), the tools in its `inputs/`, the commands, the acceptance and the thread and memory rules. Only D, the tag and the folder change:

    kc95_regrid.sh 22.5 l1kc95win2d225 kc95_d225      (python -u ell_refine.py l1kc87Lmacm3b 87 l1kc95win2d225 95 1 22.5 <lambda_0 = ell_delta.lam0_at(22.5)> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma; 4 threads, cap 21600 s)
    kc95_scan.sh  22.5 l1kc95win2d225 kc95_d225       (centre = macm3's k_c 87 root at D 22.5 + 0.003 rounded to 0.005, +-0.01 by 0.005 plus a repeat of the centre, four processes of one thread; prediction root + 0.003, bar 0.005)

The D 22.5 regrid waits for macm3's state and record row of D 22.5, for the tag g leap's end (all8.done) and for any other regrid of mine (one at a time); its scan waits for my other scans (the D 22.0 scan's four processes) to end.

## Status
- 2026-11-24 17:44 UTC: folder and README written; the lane for D 22.5 starts after D 22.0's lane is under way and waits for macm3's state (macm3's leg was at D 21.875 at 17:30 UTC, 783 s per point at h 0.03125, about 20 more points to D 22.5).

## D 22.5 lane released (the coordinator's hc, 25 Nov ~06:00 UTC; written 2026-11-25 05:56 UTC, before the regrid)
Order (verbatim): "both. Start the k_c 95 regrid at D 22.5 now on the 4 free threads, beside the running scan. Priority after that: the D 22.28125 low scan first, then the D 22.5 scan." (A reply to my question after macm3's part b2 reached D 22.5: "which first, D 22.5 or the low scan".)
- Source: macm3's part b2 k_c 87 state at D 22.5 (`I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.500000.npy`, blob 78956b39, committed 2026-11-24 21:04 -08:00) and its record row (|F| 3.8020e-10, 2863 steps, constraint 8.304e-3, Delta 1.159825168294, h 0.03125, 1928 s), fetched by `fetch_macm3.py --path=I1025-macm3/kc87_leg2/b2 --tag=l1kc87Lmacm3b2`, accepted by `kc87_syscheck_1025.py` (controls 1 1) before the regrid.
- Regrid: `kc95_regrid.sh 22.5 l1kc95win2d225 kc95_d225` with `SRC_TAG=l1kc87Lmacm3b2 SRC_PATH=I1025-macm3/kc87_leg2/b2 COMMIT_GATE_GB=off`: `ell_refine.py l1kc87Lmacm3b2 87 l1kc95win2d225 95 1 22.5 <lambda_0 = ell_delta.lam0_at(22.5)> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, 4 threads, BelowNormal, cap 21600 s; accepted only by `kc95_syscheck_1025.py` (controls 1 1; the k_c 87 check refuses). Pins, procedure and drivers as `../kc95_d22/README.md`.
- Scan: not yet started. Priority: after the D 22.28125 low scan (`../kc87_d2228125_low/`), which itself starts after the k_c 95 low scan of D 22.25 (~07:15 UTC). The scan needs macm3's k_c 87 root at D 22.5 (not yet in `roots87.txt` at 05:55 UTC; macm3 scans every multiple of 0.125) and the offset of the prediction from that root: both to be taken from the coordinator and macm3's reading; the scan driver is started by hand after those.
- 2026-11-25 05:50 UTC: the regrid driver started through `cim_start.ps1` (`SRC_TAG=l1kc87Lmacm3b2 SRC_PATH=I1025-macm3/kc87_leg2/b2 COMMIT_GATE_GB=off`). Source fetched (state blob 78956b39, record file blob 40d927af with 17 rows) and accepted (selftest 0, controls 1 1). The regrid started at 05:50:41 UTC, root pid 48888, cap 21600 s (11:50 UTC at the latest), committed memory 71.1 GB. Last two k_c 95 regrids of this kind took 7894 s and 7668 s: exit expected ~08:00 UTC.
