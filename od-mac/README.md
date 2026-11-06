# od-mac: the Taylor series in octo-double (notes/OCTO_DOUBLE.md), its checks on the Mac

Machine: the Mac (Apple M5, NEON), from 2026-11-06 01:00 UTC, a subagent of the coordinator session. The kernel is
built from the worktree `choptuik-od` (branch `feat/od-jets` of the code repository) on multidouble 4.0.0, in a
scratch venv (Python 3.13), with `CARGO_PROFILE_RELEASE_STRIP=false`.

- `osolve_tests.log`: `cargo test --release --lib osolve_` (the Rust tests of hp/src/osolve.rs).
- `build.log`: hp/build.sh under `/usr/bin/time -l` (the release build's time and peak memory).
- `highm_*.log`: the bit-identity checks of the existing paths (`highm_check.py ref`, `scaled`, `jets`, and `jets
  --mutate=kappa`, the control).
- `ojet_check_D128.jsonl`, `.log`: `hp/ojet_check.py` at `anm-mac/pred_q/A2/anm_pin3_D128.5559.npz` (N 8, with its
  criteria and controls).
- `ojet_T113_D148.jsonl`, `.log`: the same with `--check 0 --N 24` at `T113-win/chain/anm_pin3_D148.7434.npz`, T113's
  last saved state, the two series' difference by order.

- `pilot_jet_o.log`, `pilot_jet_q.log`, `pilot_jet_q24.log`, `pilot_jet_q8_h225.log`: the first `--jet_o` pilot (N 8 at
  a_max 0.2246, failed) and the runs that located the cause, the truncation at N 8 (notes/OCTO_DOUBLE.md 3). The N 8
  runs were stopped after their first attempt.
- `pilot2_jet_o.log`, `pilot2_jet_q.log`: the second pilot (N 8, h_max 0.0125), passed, and its quad-double A/B; states
  in `pilot2_jet_o/`, `pilot2_jet_q/`.

Results (code at 38ff408, notes/OCTO_DOUBLE.md 3): the Rust tests 7 of 7 (and qsolve's 8); the build 31 min 11 s, peak
12.7 GB; the bit-identity checks `ref` 168 of 168 identical (exit 0), `scaled` PASS (0), `jets` 28 of 28 (0), the kappa
control 28 of 28 differ (1); ojet_check at D 128.56 PASS; at D 148.74 the quad-double series' relative error is 6.7e-13
at order 1 and 1e-6 to 1.2e-5 at orders 4-9; the `--jet_o` pilot converged to 1.2e-44 at D 128.568.
