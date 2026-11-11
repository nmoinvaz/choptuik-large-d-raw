# I485-win2: which change moved the D 30 determinants off October's cache (#442)

Machine win2 (Windows x86-64, Intel Core Ultra 7 265K, AVX2, no AVX-512), issue https://github.com/nmoinvaz/choptuik-large-d/issues/485 (after #482, verdict "code"). 2026-11-10 to 2026-11-11.

## Answer

In 1dcde949's `hp/modecount_cx/src/lib.rs`, `dtau_c`'s complex shift lr + i li. October's cache (ln|det| -940.4586634457893 and -965.1149263751369 at (4.267, 0.974) and (3.9436, 1.1901)) was made with the old form, one `DotAcc` per component. 1dcde949 replaced it with two double-double products and a double-double sum, and today's code gives -940.4586634376807 and -965.1149263918375 (differences 8.1e-9 and 1.7e-8). Putting the old form back
(`patches_effective/olddtau_on_1dcde949.patch`, one loop of `dtau_c`) restores the cache to the bit at both points. The hp kernel (`hp/src`), the multidouble switch (93402cf8), the scaled series (d66b410d) and the arithmetic crate are not involved.

## What ran (check: #250's `fresh_vs_cache.py` at the two points; good = both within 1e-12 of the cache, bad = both within 1e-12 of today's, anything else = other)

1. Old harness (`bisect_run.log`, `bisect_log_old_harness.txt`, `class_<commit>.txt`): e043be2's `modecount_cx` for every commit. 2ef50229 good (the cache to the bit); 7588ebe2, 203670ab, 1dcde949 bad;
   93402cf8, e0c5f54b, 68b9d399, 0a131faf, 6bcd3904, e6c908a2, 154738fa, 4a013224, 0802e86a, fd051d52, e8d84ce7, 2b3b253b and others skipped (that `modecount_cx` does not build on their `hp`). Stopped for that reason.
2. Overlay harness (`harness/step2.sh`, worktree `D:\choptuik-bisect2`, venv `venv-bisect2`, same pinned packages): `hpkernel` built from the commit's own `hp` with maturin (`target-cpu=native`), its multidouble Python package as its `pyproject.toml` names it; `modecount_cx` from 1dcde949 (macm3's overlay)
   with the smallest patch that compiles (`harness/patch_*.py`, effective diffs in `patches_effective/`, none changes arithmetic): 649ec63e, 6bcd3904, d66b410d, 93402cf8 **bad**.
3. The commit's own (old) `modecount_cx` with the patches it needs to compile (`harness/patch_ctxfields.py`, `patch_splitlane.py`, `patch_fieldsolve.py`, `patch_swrap.py`): 0a131faf, 6da4d2f5 (the control, clean rebuild: target directories moved aside), 93402cf8, aafe0cb4 **good, the cache to the bit**.
4. At the same kernel, aafe0cb4: old `modecount_cx` good; 1dcde949's bad; 1dcde949's with `series_scale` = 1 (E1) bad; 1dcde949's with the old `dtau_c` (E2) good.
5. E3: e043be2's own `modecount_cx` with only the `dtau_c` revert, on its own kernel (today's tree): **good, both ln|det| equal the cache to the bit (0.0 difference at both points)** (`class_ov_e043be23.txt`, `step_ov_e043be23.{json,log}`; the first try failed to build for a missing `DotAcc` import in the patch, `build_ov_e043be23_first_failed_import.log`, and the patch now adds the import). So today's code with this one operation put back reproduces October's caches; its diff is `patches_effective/olddtau_on_e043be2.patch`.

File names: `class_ov_<commit>[_tag].txt`, `step_ov_<commit>[_tag].{json,log}` (the two ln|det| values with the cache and the old/today differences), `build_ov_<commit>[_tag].log`. Tags: `_oldcx` the commit's own `modecount_cx`, `_newcx` 1dcde949's unpatched, `_E1_noscale`, `_E2_olddtau`, `_overlay` the first (overlay) run of 93402cf8; `class_ov_aafe0cb4.txt` without a tag is the same run as `_E2_olddtau` (the last one made).
`step_ov_93402cf8.*` is the old `modecount_cx` on 93402cf8 (good); the overlay run of the same commit is `*_93402cf8_overlay*`.

## Controls

- The clean rebuild of the parent 6da4d2f5 (its target directories moved aside) repeats 0a131faf's values to the bit; both equal the cache.
- The same kernel (aafe0cb4) with the old `modecount_cx` is good and with 1dcde949's is bad, and one change of the loop in `dtau_c` toggles it, so the check can fail and the change is the cause.
- `compare_arith/` (`compare_arith.sh`, README, `out/`): `dd.rs`, `dv.rs`, `exact.rs`, `linalg.rs` of 0a131faf and the multidouble crate at 5fb516b are the same code after rustfmt (differences listed there); a planted change of `two_prod` is its control.

## Discrepancies reported, not fixed

- My comment of 18:24 UTC on #485 named 93402cf8 as the first bad commit. It was wrong (the overlay's `modecount_cx` was confounded with the kernel), corrected at 18:54 UTC.
- My message of 19:20 UTC had an invented duration, an unmeasured amplification (1e23) and an unchecked li = 0 claim; corrected at 19:20 UTC.
- The old harness bisect kept running after my first stop (its process tree had a second parent); found and stopped at 19:27 UTC. It touched no result (separate worktree and venv).

## Recommended tasks

See the closing comment on #485: put `dtau_c` back in the `DotAcc` form once macm3's circles end, with the cache reproduction as its check.
