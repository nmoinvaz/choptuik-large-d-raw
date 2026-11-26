# I1098-dh610/fastmul7_build: fastmul7's build on dh610 and its checks (#1098)

Part of `../`. Machine: dh610 (Fedora, i7-12700). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

fastmul7 is fastmul6 with horizon_mob's B_0 split exact for the matrix applied (form_s.rs, c21ba40d on
wip/large-d-fastmul7). `rebuild_z.sh c21ba40d` built it into hp_z/ and site_z/ with target-cpu=native and the
low-memory recipe (4 jobs, nice 19). It started at 18:51:10 UTC and was built at 20:17:24 UTC (`build_z.log`). The wheel's
sha256 is b3523a077542456904d4f918728200c49a26ab69874e91e5924393fd094d76bd. The checks ran after it, each log here,
with exit codes in `exit_codes.txt`:

| check | result | exit |
|---|---|---|
| recip_check D 300, D 1000 | step-plan change 0.0, controls 5.06e-37 and 1.72e-36 | 0, 0 |
| dmat_check D 300, D 1000 | 5.21e-6 and 2.72e-6, controls 1.0 | 0, 0 |
| taylor_mp_check D 300 | 1.1e-124, control 2.36e-31 | 0 |
| split check (`split300.log`) | Moebius a 8 ks 800 against mpmath 4.65e-70, bar 1e-100 | 1 |
| split scan (`split300_scan.log`, `split_scan_z.sh`) | Moebius a 8 ks 1600 against mpmath 9.74e-129, bar 1e-100 | 0 |

- **The split check** (horizon_mp_check.py at D 300's u h21 state) compares the kernel's Moebius values at x_l with
  mpmath's u series summed to order 1100. That reference converges (its last ten terms are at most 3.4e-215), and the
  kernel's u sum at ks 506 matches it to 9.7e-108.
  - At a 8 and ks 800 the Moebius values were 4.65e-70 off, against a bar of 1e-100.
  - Both controls fired: the old split (mutate 57) reads 1.7e-60, and m_h + 1e-30 reads 4.62e-28.
- **The scan** settles what the 4.65e-70 is. At a 8 the gap falls with ks: 4.65e-70 (ks 800), 1.86e-86 (1000),
  8.77e-103 (1200), 4.31e-119 (1400), 9.74e-129 (1600).
  - At a 4 it is 9.96e-129 already at ks 800 and at ks 1200, the same floor as a 8 at ks 1600.
  - So the 4.65e-70 is the Moebius series' truncation at a 8 and ks 800, not arithmetic. The bar of 1e-100 had assumed
    rounding alone.
  - With the truncation below the floor, the kernel's Moebius values agree with mpmath to 9.7e-129. The old split's
    control still reads 1.7e-60. So fastmul7 removes the 1.7e-60 offset and leaves no other term above 1e-128 here.
- The relaxed_build_check of mm5's list is not among these checks.
- **The standing check of the Moebius horizon, for this and later builds** (`split300_mpmob.log`, `mpmob_test.sh full`):
  horizon_mp_check.py from wip/large-d-form-s 5b31dedf, with `--mp_mob 1`. It writes horizon_mob's recursion again in
  mpmath (150 digits, the kernel's matrices read exactly, exact solves). Its comparison of record is the kernel's
  Moebius sum against mpmath's at the same a and ks, the arithmetic alone. The truncation is a separate line that does
  not gate. At D 300's u h21 state, a 8, ks 800:
  - the arithmetic: 9.744e-129 (p, m, c: 8.4e-129, 9.74e-129, 1.92e-130), bar 1e-100: PASS, exit 0;
  - the truncation (mpmath's Moebius sum against its converged u sum): 4.647e-70, the same figure the first split check
    read, so that figure was all truncation;
  - the controls against mpmath's Moebius sum: m_h + 1e-30 reads 4.62e-28, and the old split (--ctl_mutate 57) reads
    1.7e-60, above its bar of 1e-80;
  - the mpmath Moebius sum to ks 800 took 606 s, and the whole check about 35 min.
  - `mpmob_test_60.log` is the short test of the same code at ks 60 (the arithmetic 9.74e-129, the truncation 1.27e-8),
    run first.
