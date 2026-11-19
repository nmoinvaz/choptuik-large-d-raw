# I983-mac: P7 stage 0, the read-only tests T0a to T0d on the D 40.02 RT root samples' chords

Machine: the Mac (Apple M5, shared), helper session xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/983.
Plan: notes/P7_scope.md §3.4 and §5 (main 4415514e). Nothing is solved here. Every test reads stored states.

## Inputs and code

| item | value |
|---|---|
| samples | RT_FORMULATION.md §14's a, b, c at D 40.020065 on 32 × 121, K 0 and K 7: `I671-win/solves/k0_D40_mutnorows_D40.0201_32x121.npz`, `k7_D40_D40.0201_32x121.npz` (a); `I701-win/solves/k0b_…`, `k7b_…` (b); `I951-win/solves/k0c_…`, `k7c_…` (c) |
| table | `I163-mac/checks/exponents.log` (μ and λ₄ against D) |
| code | `solver/rt/rt_chords.py` on branch `wip/p7-stage0` of choptuik-large-d at 6b9b23f8 (from main 4415514e). It uses `rt_perturb.diff` and `move`, `rt_constraint.omega5`, `rt_mp.RTmp`, `rt_horizon.exponents` and `rt_branch_cheb.py` unchanged |
| interpreter | `/Users/nathan/venv-314/bin/python` (Python 3.14.7, python-flint 0.9.0, numpy 2.5.4, mpmath 1.3.0), `nice -n 10`, one process at a time (the subprocess of T0d runs while its parent waits) |

## Readings, fixed before the first run (2026-11-19 00:05 UTC)

The thresholds are this README's, from the table of P7_scope.md §3.4. Shares and cosines are in the 2-norm of the
unknown vector, as #969's are.

- **Controls (the run exits 1 if one fails).** The K = 0 chords reproduce #969's cosine 0.234 (within 5×10⁻⁴) and
  orthogonal share 0.97 (within 5×10⁻³). rt_sigma's 192-bit max|F| prints 6.91e-31 at c (#951) and 3.36e-18 at c
  moved by #963's random move (seed 977, δ = 10⁻²⁰). `rt_branch_cheb.py --planted` exits 0.
- **T0a.** |cos(a₇ − c₇, b₇ − c₇)| ≥ 1 − 10⁻⁶ means the chords are parallel, and λ₂'s branch is the second K = 0 chord
  (H2). |cos| ≤ 0.99 means they are not parallel, so not (H2). Values in between are undecided.
- **T0b.** For each K = 0 chord (a − c, b − c, b − a), a share along ∂_t z(c) of at least 0.5 means the chord is
  carried by the phase (HP), and a share of at most 0.1 excludes the phase. The Nyquist share reads the same way for
  (HN). Values in between are undecided. A random unit vector's share along a fixed line is about 1/√L = 0.0086 here.
- **T0c.** ρ = g(chord)/g(random), where g is max|ΔΩ₅⁺|/max|Δz|. ρ ≥ 10⁻³ reads (HC) for that chord, and ρ ≤ 10⁻⁸
  reads not (HC). Values in between are undecided. The chord's double-double rounding share, 2⁻¹⁰⁵ max|z|/max|chord|,
  is printed beside it, and ρ near that share is read as a floor.
- **T0d.** For k = ½, 3/2 and 5/2 at sample c's λ₄ and μ, the branch's interpolation error e on N = 121 is placed
  below (N²e < 1.5×10⁻³⁵), above (e > 2.6×10⁻³³) or in the root-level band. The number of k below gives (H4)'s
  predicted count of deep directions, two per k. Against D, the k = ½ placement of each row of #163's table gives the
  D at which the branch enters the band on 32 × 121.
- **Candidate.** (H4) stands if T0b excludes (HP) and (HN), T0c reads not (HC) on both chords, and T0a reads not (H2).
  (H2) holds if T0a reads parallel. (HC) holds if T0c reads (HC) on a chord. Any other combination is reported as
  "none fits".
- **Stage 1.** T1 (the count) is needed unless T0a to T0c leave a single candidate whose count T0d does not predict.
  T2 (the onset at D 30) is needed if (H4) stands.

## Commands

From the code worktree's root, RAW this folder's parent:

```
python solver/rt/rt_chords.py --selftest                     # exit 0
python solver/rt/rt_chords.py --selftest --mutate=f64        # exit 1 (chords from the double parts only)
python solver/rt/rt_chords.py --selftest --mutate=nyq        # exit 1 (the harmonic below Nyquist)
python solver/rt/rt_chords.py --selftest --mutate=null       # exit 1 (the planted null direction removed)
python solver/rt/rt_chords.py RAW --mutate=seed              # exit 1 (T0c's control with seed 978)
python solver/rt/rt_chords.py RAW --out I983-mac/chords.json # the run (logs/run.log)
```

## Result

Not yet run.
