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
