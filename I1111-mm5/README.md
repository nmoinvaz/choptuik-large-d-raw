# I1111-mm5: the l = 1 mode determinant in double-double at D 16, k_c 55 (#1111 stage 1)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1111 ("l = 1 at D 16: the mode determinant in double-double, and a root without the decaying-mode ladder"; its body is the record). Stage 1 only.

Coordinator's order (2026-11-28 01:30 UTC), the follow-on of #1109's stage 1 (ended 01:28 UTC; its table is on #1109): in the `~/Source/choptuik-1109` worktree, `git checkout --detach` **49664990** (`wip/i1101-weakdir`: "ell_ddm: det --kappa, the double-double mode matrix on another kappa's RK4 steps (#1111)"), `solver/matter/ell_ddm.py` blob 64c4337f490771c98e6deccfd0371a45ea4599f2, `~/venv-314/bin/python`, run from `solver/matter`.

**States** (`in/`, read with `git show origin/main:<path>` and blob-checked with `git hash-object --no-filters`): K35 `I1101-mac-weakdir/B/sol_l1kc55k035m_D16.0000.npy` (**9a05efa5993c9b01ceddd7c79a8601551b78bc99**, record `B/l1kc55k035m.jsonl`) and chord-all `I1101-mac-weakdir/B/seg/sol_all_D16.0000.npy` (**5bd737d7f9e8a4f1ff2986dfcb104c1aba1aa228**, map `sol_all_D16.0000.map.json`), both on K35's 5124-step map.

**Commands**, three runs at once, one thread each (OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=VECLIB_MAXIMUM_THREADS=1), `nice -n 10`, each under `timeout 14400`, logs and JSONL in this folder:

```
python3 ell_ddm.py det K35STATE 16 55 2.238 --kappa 0.35 --out ddet_k35.jsonl
python3 ell_ddm.py det ALLSTATE 16 55 2.238 --kappa 0.35 --out ddet_all.jsonl
python3 ell_ddm.py det K35STATE 16 55 2.238 --kappa 0.35 --out ddet_k35_hionly.jsonl --mutate=hionly
```

Stop rule (the order): a run that prints other than **5124 RK4 steps** is stopped and reported.

## Bars, written before the runs (#1111's stage 1 acceptance; the order's four verdicts)

1. Each run prints 5124 RK4 steps, and its five LU variants agree in sign.
2. **Control that must fail:** the `hionly` run's ln|det| differs from `ddet_k35`'s by more than the spread over its five variants. If it does not, double-double adds nothing here and bars 3-4 mean nothing.
3. ln|det| of the two states within **0.1** of each other: float64 blocks 0-11 cause the sensitivity.
4. Their difference within **10% of 0.81**: the sensitivity is the discrete operator's.
5. Anything else is reported as is. For reference (the issue): the float64 ln|det| of K35 at lambda 2.238 is -1590.66295 by `mode_matrix_fast` and -1589.20688 by `DSSEll.mode_matrix`.

Reported: each run's double-double ln|det|, its spread over the five variants, the signs, the float64 ln|det|, the seconds, and the verdicts of bars 1-4. Posted on #1111, pushed here, reported to the coordinator. Estimate (the issue): about 1 h per run, three in parallel.
