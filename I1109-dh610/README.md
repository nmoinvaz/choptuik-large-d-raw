# I1109-dh610: stage 1c's three roots again with the Rust block 12 (#1109)

Machine: dh610-fedora (Fedora, Linux 7.3, i7-12700, 20 threads, AVX2, 62 GB), runner dh610 (account claude-me2), started 2026-11-28 04:04 UTC by the coordinator (hc from t5). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1109 (comments from 7232733432 on). Written 2026-11-28 04:10 UTC by the clock, before the runs.

## Order (the coordinator's, 2026-11-28 04:04 UTC), after #1102's steps 1 and 2 (ellrs built and gated on this machine)

Three roots at once, each its own `systemd-run --user` unit, nice 10, `OPENBLAS_NUM_THREADS=1 RAYON_NUM_THREADS=2`, `timeout 14400`, from `solver/matter` of the worktree `~/Source/choptuik-ell1fast` (693a4d79), venv `~/Source/venv-i1058`:

```
python d18_secant.py run <R0 jsonl> <R0 npy> 23.0 0.0440 0.0470 r0.jsonl --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2 --pin=90d3e655,d1a3a641
python d18_secant.py run <w01 jsonl> <w01 npy> 23.0 0.0400 0.0500 w01.jsonl --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2
python d18_secant.py run <w10 jsonl> <w10 npy> 23.0 0.0350 0.0550 w10.jsonl --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2
```

Exit 2 (an end not robust, or no sign change): widen that bracket once by 2x about its centre and say so.

Bars (the coordinator's):
1. Control: r0's root within 1e-5 of mm5's refined 0.0455917189 (#1109 comment 7233613794); otherwise stop the other two and report.
2. Report w01's and w10's roots and root - root(r0). For reading: w01 moved Delta by -1.957e-4 and w10 by -1.956e-3 along R0's weak vector; w01 keeps R0's 4179 steps, w10 has 4182.

## Inputs (blobs by `git hash-object --no-filters`, each equal to origin/main's blob of the raw repository, read with `git cat-file blob` into `~/scratch1102/in/`)

| what | blob |
|---|---|
| `I1101-dh170/in/sol_l1kc127k070w2_D23.0000.npy` (R0 state) / `l1kc127k070w2.jsonl` (record) | 90d3e655 / d1a3a641 |
| `I1109-mm5/c/sol_w01_D23.0000.npy` / `.jsonl` | 458d9026 / 3410f1e5 |
| `I1109-mm5/c/sol_w10_D23.0000.npy` / `.jsonl` | 9947a645 / eb52631f |
