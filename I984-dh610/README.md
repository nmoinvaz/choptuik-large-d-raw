# I984-dh610: base polishes from ks_chain3b's D 242.8630 state at ks 302, 313 and the control 299, with --reseed_qd_bar 1e-15

Machine: dh610 (Fedora desktop, Linux 7.3, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/984

State: `I966-dh370/ks_chain3b/leg00_D237.7132_ks291/anm_pin3_D242.8630.npz` (raw origin/main d3f4a087, blob ff8926fa9393; extracted into `~/scratch967/raw`), ks 291, N 31.
Build: hp's Python from origin/main 4415514e (worktree `~/Source/choptuik-large-d-984`, where `--reseed_qd_bar` exists), the kernel and Python packages of #967's build
(`~/Source/choptuik-large-d-967/.venv`, origin/main d96a09a1; hp/src, Cargo.* and build.sh are identical between the two commits, so the compiled kernel is the same). The
coordinator approved this (hc, 2026-11-19).
Flags: run903e.sh's (`I903-win2/run903e.sh`) with `--steps 0 --keep_plan 0 --save_base 1 --reseed_qd_bar 1e-15 --threads 8`, K = 313 (+22) and 302 (+11) side by
side, then the control 299 (+8), each capped at 2 h (`timeout -s TERM 7200`), nice 10. near_null.py (4 threads) on the state (ks 291) and on every converged base.

| file | what |
|---|---|
| `run984.sh`, `common984.sh`, `gate984.py` | the runs and the verdict of one log |
| `ks<K>.log`, `ks<K>/` | a polish's stdout and output directory |
| `near_null_<name>.log`, `.json` | near_null.py on the state (ks291) and on each converged base |
| `exits_984.txt`, `summary_984.txt` | exits and verdicts |
