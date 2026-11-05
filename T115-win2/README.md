# T115-win2: hp on multidouble 3.2.0 with split Cauchy sums: bit-identity checks, jet timing, and T107's D 3.0425 plan traced

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores: 8 P + 12 E, no SMT, AVX2; 95.6 GB RAM; on AC). Worktree `..\choptuik-t115` at perf/md32 aeea2d1 ("hp: multidouble 3.2.0, Cauchy sums with a borrowed accumulator" = main + multidouble 3.2.0 + hp's Cauchy sums split over lane vectors with a borrowed accumulator). venv-t115 (Python 3.12, numpy/scipy/maturin, mpmath pinned 1.3.0 for the T81 bit-identity references). All cores, below normal priority. The current T106 build (choptuik-t106 / venv-t106) is left untouched.
Comms entry: 2026-11-05 22:09 UTC cloud to win2.

1. Build perf/md32 via `hp/build.sh` (pip uninstall -y multidouble first), log in `hp_build/build.log`.
2. Bit-identity + jet checks on the new build (4 threads each): ref (M 48/64/80) vs T81/ref_main.json, scaled vs T81/scaled_main.json, jets vs anm-mac/jets_inputs/jets_inputs.json, and jets --mutate=kappa. Expected exits 0, 0, 0, 1.
3. jet_scale.py timing on both builds, --threads 1,4,8,12,20: jet_scale_old.log (venv-t106), jet_scale_new.log (venv-t115).
4. Retrace T107's leg_M320c D 3.0425 plan on the new build with HP_PLAN_TRACE=500; cap 2 h after the base summary.
