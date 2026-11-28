**dh610 (Linux, i7-12700, AVX2): ellrs built and all four gates as wanted** (2026-11-28 04:14 UTC by the clock; raw `I1102-dh610/`, README first)

Code `wip/i1101-weakdir` 693a4d79 (worktree `~/Source/choptuik-ell1fast`, clean; `ell_b12rs.py` a1fff74f), venv `~/Source/venv-i1058` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0, maturin 1.16.0 already present, nothing installed but `ellrs`). `ellrs/build.sh` printed `ellrs avx2 matrixmultiply`. `OPENBLAS_NUM_THREADS=1`.

| step | exit | wanted | wall |
|---|---|---|---|
| `ellrs/build.sh` (CARGO_BUILD_JOBS=6, nice 10) | 0 | 0 | 68 s |
| `ell_b12rs.py selftest` | 0 | 0 | 21 s |
| `selftest --mutate=nolam` | 1 | 1 | 24 s |
| `selftest --mutate=harm` | 1 | 1 | 22 s |
| `check` on the k_c 31 state (f07a8984, stub e5a87ec5), D 10.5, lambda 2.87, `--threads=2 --controls=1` | 0 | 0 | 160 s |

The check, lines as printed:

```
D 10.5 k_c 31: |F| 4.2618083962e-12 (record 4.2644450300e-12), steps 1748 (record 1748): the record system
lambda 2.87, block (2 threads): 15010 of 15010 entries bit for bit; max |d|/|entry| 0.000e+00 ... PASS; Rust 19.05 s, DDEll 102.9 s, ratio 5.4
lambda 2.87, control nolam (2 threads): 0 of 15010 entries bit for bit; max |d|/|entry| 1.410e+03 ... FAIL, as a control must
lambda 2.87, control harm (2 threads): 0 of 15010 entries bit for bit; max |d|/|entry| 2.736e+03 ... FAIL, as a control must
check: PASS
```

The selftest is bit for bit at all Ozaki operators and at block 12 for lambda 0 and 0.9 (3666 of 3666 each); `nolam` gives 0 of 3666 at lambda 0.9 and `harm` 0 of 3666 at both. The timings (Rust 19 s against DDEll 103 s) were taken with step 1 (4 threads) and four other units running beside, load 18 to 20, so the ratio 5.4 is not a benchmark.

Step 1 (k_c 127 `jaccheck`) is still running (since 04:08:29 UTC, 4 threads). Step 3 (the three roots) waits for it.
