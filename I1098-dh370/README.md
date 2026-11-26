# I1098-dh370: the fastmul6 build attempt on dh370 (#1098)

Machine: dh370 (Fedora 45, i7-8700, 12 threads, 31 GB, 8 GB swap; a #1025 lane holds about 6 GB). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1098

- `fastmul6_build/`: the release build of wip/large-d-fastmul6 at e1cd7a84 (`rebuild_y.sh`: the low-memory recipe with 3
  jobs). Started at 16:51:41 UTC and stopped by hand at 16:59:45 UTC, before the #1025 lane could run short of memory.
  Eight minutes into the hpkernel crate its rustc was at 25.0 GB, and available memory fell to 1.7 GB with swap at
  3.2 GB (`mem.log`, every 30 s). The ladder queue behind it (`after_y.sh`: D 622, 747 and 896 by ladder_point2.sh) was
  stopped with it and never ran.
- dh610's fastmul6 wheel (target-cpu=native on an i7-12700) cannot serve here. objdump finds 60 gf2p8affineqb (GFNI)
  instructions in it, which the i7-8700 lacks.
- The D 2828 release on the old kernel (I1088-dh370's rls2828) was stopped at 16:50 UTC on the coordinator's order.
  Its h5, h7 and h9-step states are kept on dh370 in out/rls2828/.
- `fastmul6_sky/`: dh610's Skylake cross-build of fastmul6 (e1cd7a84; wheel sha256 9c4d41e9..., no GFNI; its AVX-512
  code sits only in multidouble's runtime-dispatched SIMD backend), installed into site_sky with the Python of f398e829
  by `install_sky.sh`. All six checks exit 0 with the same figures as dh610's and mm5's builds. The ladder point D 896
  (ladder_point2.sh, kc 200, M 48 tail, kmax 23, KSBAR 1e-64, 6 threads) started after the checks, at 18:58 UTC.
- **The D 896 run's commit field:** ladder_point2.sh (blob ed177006 for the first try, 8e6779cf for the restart at 19:05
  UTC after the ks-gate parse fix) passes a hard-coded --commit 478e9d86. The Python it runs is f398e829's (hp_y from
  that commit's archive), and its kernel is the Skylake wheel of e1cd7a84 (d368a0c0's Rust). So its records name
  478e9d86 where they mean f398e829. f398e829 also makes the inner held solves take chord steps by default
  (--inner_chord 1, e1cd7a84). The points converge to the same 1e-48 tolerance as D 432-1291, though not to the same
  bits. The ladder record will give f398e829.
