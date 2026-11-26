# I1099-mac: hp with multidouble's recip_parts against 33eeff5c's own, bit for bit

Machine: this Mac (Apple M5, 10 cores, 32 GB, macOS 27.0.1), dev-o1 builds, nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1099

Builds: `wip/hp-recip-md` eaa6f150 (hp's `recip_parts` replaced by multidouble's `recip::recip_parts`, PR
nmoinvaz/multidouble#188 at 862157a) and its base `wip/large-d-form-s` a3e6ca3b (33eeff5c's Rust, the reciprocals
of record). The PR's later commits to f47a403 change docs and tests only.

States: recip_check's D 300 (`I1088-dh610/out/rls300/release_ls_h13_D300.0000.npz`, blob e5a3b5f8) and D 1000
(`I1088-dh610/rls1000h13q/release_ls_h13_D1000.0000.npz`, blob 22bb10b9).

- `recip_md.log`: `recip_check.py` on both states with the new build: PASS, the same lines as mm5's fastmul5 build
  (raw `I1098-mm5/fastmul5-build/recip300.log`, `recip1000.log`).
- `recip_bits.py`: the octo-double residual (HP_EXACT_RECIP=1, kfreeze 13) at both states, with the state's steps and
  with every step halved, saved per build (`recip_md.npz`, `recip_base.npz`); `compare.log`: 0 differing words.
- Control (`recip_bits_ctl.py`, `compare_control.log`): the new build with HP_EXACT_RECIP=0 against the base's exact
  reciprocals must differ: about 3500 words differ in each array.
