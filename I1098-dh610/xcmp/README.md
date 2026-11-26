# I1098-dh610/xcmp: the fastmul5 kernel on dh610 against mm5's build, on one state's octo-double residual

Machine: dh610 (Fedora 45, i7-12700, x86_64, `-C target-cpu=native`). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The kernel is wip/large-d-fastmul5 at f350aa62, which has lane-precision reciprocals and the relaxed horizon products. It was built
into `site_x/` by the low-memory release recipe with 12 jobs, in 38 min 56 s (`build_x_tail.log`).

- `recip_check.log`: `hp/recip_check.py` at D 300 and D 1000 with the bars of I1098-mm5/fastmul5-build. Both PASS, with the same
  digits as mm5's build.
- `dump_residual.log`, `F_D300_base_dh610.npz`: `dump_residual.py`, from I1098-mm5/fix/tools, run on
  I1098-mac-a/budget300_src/D300_full_base.npz (sha256 4c62a1da...) with `HP_EXACT_RECIP=1 HP_HORIZON_RELAXED=1` and kfreeze 13.
  It is compared with mm5's I1098-mm5/fix/F_D300_base_mm5.npz. Both give max |F| 7.991459e-31, the largest difference is 0.0, and
  0 of 4616 parts differ. The aarch64 (NEON) build on macOS and the x86_64 build on Linux agree bit for bit on this residual.
  The two npz files differ as files only in their `kernel` string, which names each machine's path.
