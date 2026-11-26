# I1098-dh610/fastmul6_build: the fastmul6 kernel on dh610 and its checks (#1098)

Machine: dh610 (Fedora 45, i7-12700, x86_64). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The kernel is wip/large-d-fastmul6 at d368a0c0: fastmul5 plus the d/dtheta matrices' f64 remainders on the quad- and
octo-double lanes (HP_EXACT_DMAT, on by default). It was built from `rebuild_y.sh` (in `../fix/`) into `site_y`, with
its own copy of hp in `hp_y`. The low-memory recipe with 8 jobs took 82 min 36 s beside other runs (`build_tail.log`).
The checks ran from hp_y with fastmul6's later Python: the fixed taylor_mp_check (f1b3cb8b) and the release criterion
(dcd93f55). All exit 0 (`exit_codes.txt`), with the same digits as mm5's build (I1098-mm5/fastmul6-build):

| check | result |
|---|---|
| recip_check D 300, D 1000 | step-plan change 0 (bar 1e-44); control 1.72e-36, 5.06e-37 (must exceed 1e-40) |
| dmat_check D 300 | the remainders move F by 4.92e-35; the two mechanisms agree to 5.21e-6 of it; control (2c) 1.0 |
| dmat_check D 1000 | 2.141e-34; 2.72e-6; control 1.0 |
| taylor_mp_check D 300 | 1.1e-124 with hi + lo + c on both sides (bar 1e-60); control 2.36e-31 |
