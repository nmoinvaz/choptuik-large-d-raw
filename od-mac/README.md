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

Results so far: the Rust tests 7 of 7 (and qsolve's 8); the build 31 min 11 s, peak 12.7 GB; the bit-identity checks
`ref` 168 of 168 identical (exit 0), `scaled` PASS (0), `jets` 28 of 28 (0), the kappa control 28 of 28 differ (1);
ojet_check at D 128.56 PASS.
