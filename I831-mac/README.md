# I831-mac: reseed's import-time precision, and the octo-double path's bits across BLAS threads

Machine: the Apple M5 Mac (`mac`), agent xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/831.

Code: branch `wip/xf-831` from main 75f94140: 83fd181f (reseed, its importers, `hp/import_precision.py`) and the
step_bits commit (`hp/step_bits.py`). Build: main 3c35f0c's hpkernel (i599/site2). 3 threads, nice 10.

## Part 1: reseed set 50 digits when imported

reseed.py ran `mp.mp.dps = 50` at module level. It now sets `DPS = 50` under its main guard. `Reseeder` keeps D as
given: an mpf is not rounded to the caller's precision, and a string is parsed at 60 digits or more.

Three scripts had relied on the import and now set 50 themselves:
- `octo_corrector.py` sets it under its main guard, and parses D_str with `D_of` at 60 digits or more.
- `reseed_hist.py` sets it in main.
- `reseed_start_check.py` sets it under its main guard.

reduced_cubic's restore (#828) and chain_dM's comment about the import went.

`import_precision.py` has three parts:
- **(A)** Static. A module another module imports must not set the precision at import, directly or through a
  module-level import. The direct setters found at 75f94140 are in KNOWN, reseed excepted.
- **(B)** Dynamic. Each importer of reseed must keep its precision across reseed's import.
- **(C)** Reseeder must keep D_str's digits at 15.

| run | (A) | (B) | (C) | exit |
|---|---|---|---|---|
| `import_precision_before_old` (the check run from the 828 worktree, reseed before #831) | FAIL: reseed sets it, anm_run through it | FAIL: 7 of 12 importers changed (reduced_cubic 140 -> 50, horizon_radius 60 -> 50, octo_corrector, crawl_probe, proj_shift, reseed_hist, step_spread 15 -> 50) | FAIL: \|D - D_str\| 5.72e-15 | 1 |
| `import_precision_before` (`--root` the 828 worktree, C from the fixed code) | FAIL | FAIL | pass | 1 |
| `import_precision` (wip/xf-831) | pass | pass: all 12 kept | pass: 0.0 | 0 |
| `import_precision_selftest` | the planted setter and its module-level importer listed, nothing else | the planted lazy importer listed | | 0 |

octo_corrector's `digits` check passes and its `--mutate 2` fails, as do reseed's `projlog` and `--mutate=silent`.

**Scope.** (A) found 55 library modules that set the precision at import, through 33 direct setters other than
reseed, most of them in solver/ (proof, review and planted code). They are in KNOWN, which makes the check fail on any
new one. Moving them all is outside the coordinator's scope for #831, though the issue's literal acceptance says no
module.

## Part 2: no octo-double call uses BLAS

The kernels link only libSystem (`otool -L` of `_hpkernel` and `_multidouble`). Their rayon loops write disjoint
elements (map-collect, chunked updates) and have no parallel reductions (multishoot 1.2.2, multidouble 4.2.1).

| run | dps | stored-step check | residual, solve, second LU's step (sha256, 16 hex) | |
|---|---|---|---|---|
| `stepbits.log`: OPENBLAS 1, unset, 1, unset | 140 | 3.118e-89 | da94c506523c493c, d56d3fe149515769, 7ff0680103741b62 | all four the same |
| `stepbits2.log`: the old reseed imported after reduced_cubic, before Real (#828's probe) | **50** | **3.622e-35** | da94c506523c493c, **fe8d101dccd0f753**, 7ff0680103741b62 | the solve differs |
| `stepbits2.log`: the fixed reseed, the same order | 140 | 3.118e-89 | the same as the first | same |
| `step_bits.log`: blas1, blasN, reseed_first, kernel1 | 140 | 3.118e-89 | the same in all four | exit 0 |
| `step_bits_dps50.log`: `--mutate=dps50` (50 digits where reseed was imported) | 50 | 3.622e-35 | the solve differs | exit 1 |

**#828's discrepancy 2 was part 1's bug, not BLAS.** Its probe imported reseed after reduced_cubic and before
building Real, so the check's 140-digit conversions ran at 50 digits. The residual and the LU are the same bits.
Only the solve, whose right-hand side passes through mpmath, differs. The path gives the same bits at 1 and at all
OpenBLAS threads, and at 1 and 3 kernel threads. stepbits2's first launch had the imports in the wrong order (reseed
first, then reduced_cubic, which set 140 again) and was stopped and rerun.

## Recommended tasks

1. **The import check in CI.** Run `hp/import_precision.py --selftest` and its (A) in CI (static, no build), and
   (B) and (C) where hpkernel is built. Acceptance (can fail): CI fails on a branch that adds `mp.mp.dps = 50` at
   module level to a module another imports.
2. **The 33 known direct setters.** Decide which to move under main guards. Those in solver/proof and its reviews
   back certified results, so moving them needs each certificate rerun. Acceptance (can fail): KNOWN shrinks, and
   each moved module's own checks give the same output before and after.
