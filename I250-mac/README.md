# I250-mac: the D 30, M 48 no-cut extra pair recounted on the fitted (inner-node) layout, with October's control

Machine: mac (Apple M5, 10 cores, shared). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/250

Code: worktree branch `wip/i252` of the main repository (main 590d88a with #242's `modecount_wind.py` rule cherry-picked;
the circle code is main's `hp/modecount_circle.py`, unchanged). Python /Users/nathan/venv-314/bin/python (hpkernel and
modecount_cx as installed, not rebuilt). Single-threaded, `nice -n 10`, `caffeinate -i`.

## Inputs

- `states/modecount_state_D30.0688_M48_inner015.npz`: #141's M 48 no-cut state on the layout with a node at 0.15
  (raw `I141-mac/states/`, 76fbf9b; |F| 2.4e-26).
- `states/modecount_state_D30.0688_M48_october.npz`: October's M 48 no-cut state, `hp/data/modecount_state_D30.0688_M48.npz`
  of main (2ef5022, 2026-10-22; |F| 9e-18), the background of the count that found the pair.
- `october/data/modecount_D30.0688_M48_october_evals.jsonl`: October's cache, `hp/data/modecount_D30.0688_M48_evals.jsonl`
  of main (2ef5022), copied unchanged (174 lines: the count's 148 and the circle's 26).

## Criteria (written before the runs)

1. **Main circle.** `hp/modecount_circle.py states/modecount_state_D30.0688_M48_inner015.npz 4.267,1.324,0.35
   --fmax=1e-15` (no cut, the state's own M, n0 16 and tol pi/4 as October's circle), own tag `D30.0688_M48_inner015`,
   data in `inner015/data/`. It is read only if every phase step is below pi/4 and there are 0 verification mismatches.
   Winding +1: the pair is present on the fitted layout, and the circle's position is compared with October's 4.267 +
   1.324i. Winding 0: the pair belongs to the old layout's unconverged background.
2. **Positive control on the new layout.** A circle of radius 0.2 at lambda_phys = 1/gamma(D) on the same state, in
   the same run. It must wind +1 with its zero within 1e-3 of lambda_phys; otherwise the main circle is not read.
3. **October's control (the issue's).** The same circle on October's state with a copy of October's cache, tag
   `D30.0688_M48_october`, data in `october/data/`. It must wind +1.
4. **Build check of the control.** Two of October's cached circle points recomputed fresh (not from the cache) on
   October's state must equal the cache in ln|det M| and arg det M to 1e-8 (`scripts/fresh_vs_cache.py`). Its control
   `--mutate=swap` compares each fresh value with the other point's cache entry and must fail (exit 1).
5. **Determinant check of the new state** (`I252-mac/scripts/det_check.py`, the same as #252's): det M changes sign
   between lambda_phys - 0.015 and lambda_phys + 0.015 in both LUs (hpkernel's real one and modecount_cx's complex
   one), and the two agree in ln|det M| to 1e-4 at both points.

modecount_cx: the build of the main checkout (`hp/modecount_cx/build/modecount_cx.cpython-314-darwin.so`, 2026-11-08 16:26,
sha256 3e485ab9a27d6da50135b3fa94d758c922cd080f02d4a07a97e42b0de6136073, the same file #242 uses), copied into the
worktree's build folder, not rebuilt. The first launch (15:22 UTC) imported the crate's source folder instead and every
step exited 1 at once; its logs are in `failed_import/`. Versions: Python 3.14.7, hpkernel 0.1.0 (installed 2026-11-08
16:24), numpy 2.5.4, mpmath 1.3.0.

## Results (2026-11-09, exits in `exits.txt`)

| run | result | verdict |
|---|---|---|
| 5. det check, inner-node state | sign change at lambda_phys in both LUs, LUs 0 apart, pivots 1e-6 ... 3e2 | pass |
| 1. circle 4.267 + 1.324i, R 0.35, inner-node state | winding 0, 16 points, max step 0.055 rad, 0 mismatches | read: the pair is absent |
| 2. lambda_phys circle, R 0.2, inner-node state | winding +1, 24 points, max step 0.363 rad, zero 2.0797477 (estimate 7.7e-8) | pass |
| 3. October's circle on October's state and cache | winding +1, 24 points, max step 0.369 rad, all from the cache (174 lines before and after), zero 4.267421 + 1.319580i | pass |
| 4. fresh vs October's cache, two points | ln\|det\| 8.1e-9 and 1.7e-8 apart, arg 7.9e-9 and 5.4e-8 apart | **fail** (criterion 1e-8) |
| 4. control `--mutate=swap` | 25 and 2.7 apart | fails, as required |

Check 4 fails its own criterion: today's build reproduces October's determinants on October's state to 1.7e-8 in
ln|det M| and 5.4e-8 rad in arg, not to 1e-8. The cause is not identified. It is far below any phase step of a circle
(0.37 rad), and far below #68's offset of 0.04-0.15 between October's state and a re-converged one.
