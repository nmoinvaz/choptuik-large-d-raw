# I864-mac: the start sets of lemmas 6a and 6b₁ (M = 3 and M = 5) against the start-value lemma

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0), one process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/864. Code:
`solver/proof/start_cover_lemmas_M.py`, branch `wip/sa-864` on main ecfc1b92: the script at a6710430, the proposed notes (proof/A_lemmas_M.md §6 and §10) at 0fde6a1a.

`run_i864.sh <python> <root of the raw-data clone>` ran everything from `solver/proof/`, in 19 s. `exits.txt` has each
run's command, its exit status and the status it must have: 6 checks exit 0 and 10 mutations exit 1. Each run's log is
`<name>.log`; `cover_M3.log` and `cover_M5.log` hold the full statement of every start set and the reruns.

## The start sets

Read off `lemma6b1_cover_M.py` and `lemma6_jump_M.py`, the same at M = 3 and 5. The stored runs are those
proof/A_lemmas_M.md cites for Theorem A(3) and A(5).

| use | where it is proved | stored run read | M = 3 | M = 5 |
|---|---|---|---|---|
| 1. Lemma 6b₁'s start set at s₀ = ρ₀e^{−3iπ/4}: the old sector lemma (rays within 0.2 of 3π/8, diag) at the covering's centre c and on the complex box c ± (h + 10⁻³), imaginary parts ± 10⁻³ | in the covering's run: `start_data_u` raises unless both fixed points hold and the start point lies in the lemma's radius | `ray.json` (centre, h, the C¹ start set) | `lemma6b1_runs_M3_cert/`: h = 1.1×10⁻⁹, ρ₀ = 262, r₀ = 0.1 | `I38-macm3/`: h = 10⁻¹⁸, ρ₀ = 405, r₀ = 0.07 |
| 2. Lemma 6b₁'s check: the radius g₀ of G₀, where y⁺ is analytic by lemma S(M) (lemma 6b₀) | in a stored run of `lemma6_sector_M.py` over x̂ ± 10⁻⁶; the covering takes g₀ as a constant | `lemmas_M_runs/lemma6_sector_M*_1e-6.json` | R₊ = 0.1², k = 20, N = 53, g₀ = 257 | R₊ = 0.08², k = 20, N = 81, g₀ = 402 |
| 3. Lemma 6a: lemma S and the flat estimate over centre ± 10⁻⁶ | in the 6a run: `lemma6_jump_M.py` exits unless both hold and unless its input box lies inside | the run's JSON, its input box file and its `--x` | `lemma6a_M3_cert.json`, centre x̂ (no `--x`), input `data/A_M_6a_M3_1e-10_in.json` | `I184-macm3/`, centre p̂ (`--x`, `centre_passed.txt`), input `I103-macm3/A_M2_6a_M5_sub1e-18.json` |

Lemma 6a does not use the old sector lemma (the issue's text names it there).

## Results

| test | M = 3 | M = 5 |
|---|---|---|
| 1(a) X_b = c ± h inside the complex box | yes | yes |
| 1(b) diag side condition M W₀ sup\|Im ω/ω∞\| ≤ 3/2 | 0.0115 | 0.0191 |
| 1(c) start point 1/ρ₀ < r₀² | 0.003817 < 0.01 | 0.002469 < 0.0049 |
| 2(a) g₀ ≥ 1/(R₊ sin 0.4) and ρ₀ > g₀ | 257 ≥ 256.79, 262 > 257 | 402 ≥ 401.24, 405 > 402 |
| 2(b) the stored lemma S run holds and X_b lies in x̂ ± 10⁻⁶ (ball in ball) | yes, slack 9.985×10⁻⁷ at A | yes, slack 9.992×10⁻⁷ at ω/ω∞ |
| 3(a) the 6a input box x ± h in centre ± 10⁻⁶ | the certificate's p ± 10⁻¹⁰: slack 9.995×10⁻⁷ at A | p̂ ± 10⁻¹⁸ (the file has no x, so x is the centre): slack 1.000×10⁻⁶ |
| verdict | COVERED | COVERED |
| rerun 1: `start_data_u` at the stored centre | N 53, k 40, contraction 0.5408 at c and 0.5431 on the complex box; 13 of 13 values (all inside the stored balls) and 52 of 52 derivative entries overlap the stored start set | N 105, k 40, contraction 0.3671 and 0.3681; 19 of 19 values (all inside) and 114 of 114 derivative entries overlap |
| rerun 2: lemma S over x̂ ± 10⁻⁶ | contraction 0.8252209105, the stored value | 0.7246665601, the stored value |
| rerun 3: lemma S and the flat estimate at the 6a run's centre | contraction 0.8252; Λ 0.2922808049, the stored value | contraction 0.7247; Λ 0.4233267068, the stored value |

**Mutations** (each must be reported as not covered, exit 1; the same parts fire at M = 3 and 5).

| mutation | reported |
|---|---|
| `widen`: the covering's h and the 6a box's h set to 2×10⁻⁶ | 2(b) and 3(a) |
| `edge`: those h set 9×10⁻¹¹ past the edge | 2(b) and 3(a), slack −9.000×10⁻¹¹ |
| `centre`: the covering's centre and the 6a box moved by 2×10⁻⁶ in ω/ω∞ | 2(b) and 3(a) |
| `g0`: g₀ lowered to 0.75/(R₊ sin 0.4) | 2(a) |
| `rho0`: ρ₀ lowered to 0.9/r₀² | 1(c) and 2(a) |
| `edge0` (null): h set 2×10⁻¹⁰ inside the edge | stays COVERED, slack +2.000×10⁻¹⁰ |

## Does (H0) need a counterpart for the lemmas?

No. Uses 1 and 3 are proved inside the lemma's own run, on sets fixed by the run's arguments, and the scripts raise or
exit unless the fixed point holds and the run's box lies inside. They are part of what (H2), "a complete 6b₁
covering", and (H3), "lemma 6a(M) holds", assert, in the way (H0) is part of every certificate run. Use 2 is the only
one that rests on a stored run, and it is (H1) with X_b in place of X_c: lemma S over x̂ ± 10⁻⁶, which contains X_b.

## Where the notes are sharper than the runs

1. (H1) lists the old sector lemma among what is proved over X₆ = x̂ ± 10⁻⁶. No step of Theorem A(M)'s proof uses that
   run: the covering runs its own old sector lemma at its centre (with r₀ = 0.07 at M = 5, against 0.1 in the stored
   run), and lemma 6a does not use it.
2. Step 3 of the proof takes lemma S and the flat estimate "from H1", over x̂ ± 10⁻⁶. The M = 5 run of lemma 6a
   (`I184-macm3/`) proves them over p̂ ± 10⁻⁶, its own centre. Both boxes contain X_c, and Λ is 0.4233267068 on both.
3. At M = 5 the covering's centre (`ray.json`'s `x`) is p̂ cut at 39 decimals. It differs from the certificate's p̂ by
   4.6×10⁻³⁹ in A, 8.5×10⁻⁴¹ in ω/ω∞ and at most 8.8×10⁻³⁹ (in B₃). The notes call X_b "p̂ ± 10⁻¹⁸". The decimal box
   p̂ ± 10⁻¹⁸ lies in X_b only because arb rounds a ball's radius up to a 30-bit number: the covering's parameter
   ball has radius 10⁻¹⁸ + 2.19×10⁻²⁷. The certificate's Krawczyk sub-box is the ball `arb(0, 1e-18)` around p̂, with
   the same rounded radius, so that ball passes X_b's edge by 4.6×10⁻³⁹ in A. (H2) holds with X_c the decimal box,
   on which the certificate's uniqueness holds a fortiori. The script prints this under "for reference (H2)".

## Recommended tasks

1. **State X_c and X_b exactly at M = 5.** What: in proof/A_lemmas_M.md's summary and §6–7, give X_b as the covering's
   ball (centre `ray.json`'s `x`, radius 10⁻¹⁸ rounded up) and X_c as the decimal box p̂ ± (10⁻¹⁸, 10⁻²⁶, 10⁻²⁷), and
   check that the certificate's zero enclosure K(X) lies in that decimal box. Why: item 3 above; the inclusion
   X_c ⊂ X_b is what step 1 of the proof uses. Acceptance: a script line that prints the inclusion with its slack and
   fails when the covering's radius is replaced by the decimal 10⁻¹⁸. Depends on: #864.
2. **(H1) and step 3's wording.** What: remove the old sector lemma from (H1), or say which step uses it, and let
   step 3 take lemma S from the 6a run's own box. Why: items 1 and 2 above. Acceptance: the hypotheses name only runs
   that a step of the proof consumes; `check_numbers.py --selftest` passes. Depends on: #864.
