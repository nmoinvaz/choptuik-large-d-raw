# I1098-dh170: the fastmul6 kernel built for the Skylake instruction set, and dh170's ladder point (#1098)

Machine: dh170 (Fedora, i7-7700, 8 threads, 31 GB; a #1025 lane runs beside). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1098

- `fastmul6_sky/`: dh610's cross-build of wip/large-d-fastmul6 at e1cd7a84 with -C target-cpu=skylake. The wheel's sha256
  is 9c4d41e97df63f3f867997e28cbf626af8e152525111e61b8b001f455b18ffef, and it has no GFNI instructions. Its AVX-512 code
  sits only in multidouble's runtime-dispatched SIMD backend. It is installed into site_sky by `install_sky.sh`, with
  the Python of f398e829, and checked here. All six checks exit 0 with the same figures as dh610's and mm5's builds:
  - relaxed_build_check: 4.53e-57, control 3.69e-05
  - recip_check: D 300 and D 1000, step-plan change 0, controls 1.72e-36 and 5.06e-37
  - dmat_check: 5.21e-6 and 2.72e-6, controls 1.0
  - taylor_mp_check: 1.1e-124, control 2.36e-31
- The ladder point D 1549 (ladder_point2.sh, kc 230, M 48 tail, kmax 31, KSBAR 1e-70, 6 threads) started after the checks,
  at 19:00 UTC.
- **The D 1549 run's commit field:** ladder_point2.sh passes a hard-coded --commit 478e9d86. The Python it runs is
  f398e829's (hp_y from that commit's archive), and its kernel is the Skylake wheel of e1cd7a84 (d368a0c0's Rust). So its
  records name 478e9d86 where they mean f398e829. f398e829 also makes the inner held solves take chord steps by default
  (--inner_chord 1, e1cd7a84). The points converge to the same 1e-48 tolerance as D 432-1291, though not to the same
  bits. The ladder record will give f398e829. The first run (install_sky.sh) stops at its ks gate on the parse bug, and
  restart1549.sh (unit i1088a-ladder1549) restarts it with the fixed script (8e6779cf), keeping its jump.
