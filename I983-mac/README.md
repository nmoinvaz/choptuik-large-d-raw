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
python solver/rt/rt_chords.py RAW --tests e --out I983-mac/extra.json   # outside the readings, code a70ab308 (logs/extra.log)
```

## Result (2026-11-19 00:05 UTC, 10 s on one core)

**By the readings above no single candidate fits. (HP), (HN) and (HC) are excluded, and (H4) and (H2) remain,
because T0a is undecided. T1 is needed.** Every control held, and the seed control failed as it must
(`logs/control_mutate_seed.log`: 6.23e-18 against 3.36e-18, exit 1).

| Test | Measured | Reading |
|---|---|---|
| controls | K = 0 cosine 0.233729 and orthogonal share 0.9723 (#969: 0.234, 0.97). max\|F\| 6.91e-31 at c and 3.36e-18 at the moved state. `rt_branch_cheb.py --planted` exit 0 | ok |
| T0a | \|cos(a₇ − c₇, b₇ − c₇)\| = 0.998730, so 5.0% of b₇ − c₇ is orthogonal to a₇ − c₇. The K = 7 chords are 4.5×10⁻¹⁸ and 4.3×10⁻¹⁸ of max\|z\| | undecided (between 0.99 and 1 − 10⁻⁶) |
| T0b | shares along ∂_t z(c) of 0.024 (a − c), 0.010 (b − c) and 0.016 (b − a). Nyquist shares 7.4×10⁻⁹, 7.2×10⁻⁹ and 9.0×10⁻⁹ | (HP) excluded, (HN) excluded |
| T0c | max\|Ω₅⁺\| at c is 3.5×10⁻¹². g(random) = 1.13×10³. ρ = 3.7×10⁻¹³ (a − c) and 1.1×10⁻¹² (b − c), against chord rounding shares of 1.5×10⁻¹² and 9.1×10⁻¹³ | not (HC) on both chords. ρ sits at the rounding floor, so no change of Ω₅⁺ along the chords is resolved |
| T0d | at sample c (μ 0.129106, λ₄ 21.1275), e(121) = 6.4×10⁻⁴⁷ for k = ½ (N²e 9.4×10⁻⁴³), 2.1×10⁻³⁸ for k = 3/2 (N²e 3.1×10⁻³⁴) and 9.5×10⁻³³ for k = 5/2 | k = ½ below, 3/2 in the band, 5/2 above. (H4)'s count is two deep directions, and four if the k = 3/2 pair reaches the floor |
| T0d against D | the k = ½ branch on N = 121 is above the band through D 20, in the band at D 25 and 30, and below from D 35 | (H4)'s onset on 32 × 121 lies between D 20 and 35 |

**Outside the readings** (`logs/extra.log`, `extra.json`, decided after the run, so this is not a pre-set test):

- The K = 7 chords lie in the K = 0 chords' plane. The out-of-plane share is 2.4×10⁻⁵ for a₇ − c₇ and 6.4×10⁻⁶ for
  the part of b₇ − c₇ orthogonal to it. A random vector's in-plane share would be about √(2/L) = 0.012. The K = 7 rows
  exclude λ₂'s branch (RT_FORMULATION.md §13.2), yet the same plane carries the K = 7 samples' spread, and the
  orthogonal part (5% of 4.3×10⁻¹⁸) is about 8 times the K = 0 chords' size. That argues against (H2), whose second
  direction the rows would remove. It is not a pre-set reading, and T1 still has to decide.
- 92% to 99.5% of each field's part of every chord lies in that field's lowest harmonic: harmonic 0 for ω₁, ω₂ and
  ω₃, wavenumbers ±½ for ω₄. ω₄ carries 50% to 68% of each K = 0 chord and μ under 1%. That is the shape (H4) expects,
  a k = ½ scalar branch with a harmonic-0 response in the metric functions, though it does not prove it.

**Stage 1.** T1 is needed, since two candidates remain and T1 separates them: (H2) predicts one deep direction, (H4)
two, or four if the k = 3/2 pair counts. T2 is needed if T1 reads two or four. T0d puts D 30 inside the band, so a T2
at D 30 alone could not decide. D 20 (above the band, where (H4) predicts no null direction) and D 35 (below it, where
(H4) predicts the null pair) bracket the onset. #423's root-level bound at D 30 on 32 × 121, 1.35×10⁻³¹, is two to four decades
above D 40's, and T2 would also read it.

## T1's code, checked on the Mac (2026-11-19 00:40 UTC)

`rt_sigma.py --save_x` and `rt_xcount.py` on `wip/p7-stage0` at b27f2297, run with `/Users/nathan/venv-qd/bin/python`
and RT_FORMULATION.md 9.9's `MULTIDOUBLE_SITE` (venv-314's multidouble lacks `_dd_dot`). Logs `logs/t1_*.log`.

| check | result |
|---|---|
| `rt_xcount.py --selftest` (planted non-normal J, d = 2 and 4, a pair at 1e-18) | PASS, exit 0 |
| `rt_xcount.py --selftest --mutate=transpose` | FAIL, exit 1: the chords' share falls to 0.05 and 0.08 |
| `rt_sigma.py --planted` against main 4415514e's | identical output, exit 0; `--mutate=shift` still exits 1 |
| `rt_sigma.py --planted --deep 2` and `--deep 4` with `--save_x`, then `rt_xcount.py --expect 2` and `--expect 4` | d = 2 and d = 4 with clean gaps, exit 0; `--expect 4` on the d = 2 file exits 1 |
| `rt_sigma.py cont_32x81_D15.0000 --rough --starts 2`, main against `--save_x` | the same output but the closing "saved" line; `rt_xcount.py` reads the file |
