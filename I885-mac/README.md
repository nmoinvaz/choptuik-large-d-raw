# I885-mac: the B8 chain rerun with b8_formal's constants at the working precision, and why lemma LC's matrix moves

Machine: mac (Apple M5 Mac), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0 with FLINT 3.6.0), one
process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/885. Code: branch `wip/sa-885` on main
26178871, where `solver/proof/b8_formal.py` sets the precision to 256 bits before it makes W₀, A\* and ω\*/ω∞.

## The rerun

`run_i885.sh <python> <output directory>` ran the 17 commands of proof/B8_constants.md §13 and proof/B_chain.md §11
that depend on those constants, from `solver/proof/`. `b8m_scan.py` and `b8m_lc.py` append to their `--log`, so every
output went to the output directory under the stored file's name, and no stored file was touched. `exits.txt` has each
run's exit status: all 17 are 0. `compare_i885.py` then compared each output with the stored file of the same name,
leaf by leaf. Its table is `compare.txt`.

| verdict of proof/B_chain.md | stored | rerun |
|---|---|---|
| (H8) closes at L₀ = 73.89, with the box and with the offset d₀ = 10⁷ | yes | yes, numbers within 5.1×10⁻¹⁶ |
| B5(2), `b5_jump_d0_1e7.json` | | within 1.2×10⁻¹⁶ |
| the IFT, n₀ = e^89.75, `b7_ift.json` | e^89.75 | the same in every number |
| lemma LC, `b8m_lc_K4.log` | closes | closes, numbers within 3.9×10⁻¹⁵ |
| its contraction constant, `b8m_lc.py --lipcheck` | θ = 0.7355 | θ = 0.7355 |
| lemma J, `b8m_lcj.json` | θ = 0.17593 | the same in every number |
| the mutations `JD`, `rho2L` with `--mutlc`, `d0`, `kernel` | caught | caught |

Three differences are not in the last digits.

- **The Lipschitz matrix `b8m_lc_lip.json`.** 515 of its 1600 entries move by more than 10⁻⁹, by factors 0.733 to
  1.018. All are below 6.1×10⁻⁶³. The 416 entries of 10⁻⁶⁰ or more move by at most 2.2×10⁻¹¹. See below.
- **The scan record at L₀ = 62** of `b8m_scan_K4_box.log`: 67 iterations against the stored 70, and its two last
  relative changes differ by 1%. The code of main, unchanged, gives 67 as well (`I879-mac/`, the run as written), so
  the stored record predates the current code. It also lacks the field `d0`, as do the stored records at the other
  L₀ and in `b8m_scan_K4_k0.85.log`. It closes in every version.
- **The mutated run** `b8m_lc_K4_mut_rho2L.log`: its last relative change differs by 4×10⁻³ and two constants by
  9×10⁻⁴. It is the record of a mutated certificate, which `b8m_lc_numcheck.py --mutlc` must catch, and does.

## Why entries of the Lipschitz matrix move

An entry is a secant, (M(η) − M(0))/η with η = 10⁻⁶, of two evaluations at 256 bits. Where the bound does not depend on
the perturbed input, the two evaluations are of one number, and the entry is their rounding difference divided by η.
`experiments/` has the two runs that test this, on main's code:

| | entries that are noise | entries of 10⁻⁶⁰ or more | θ |
|---|---|---|---|
| stored, η = 10⁻⁶, 256 bits | 1108 of 1600, at most 2.3×10⁻⁶⁹ | 416 | 0.7355 |
| `--eta=1e-3` (`lip_eta1e-3.json`) | 1108 shrink to within 1% of 10⁻³ of their value | move by at most 9.2×10⁻⁵ | 0.7355 |
| 320 bits (`lc_at_prec.py 320`, `lip_prec320.json`) | 1100 shrink to within a factor 4 of 2⁻⁶⁴, median 5.421×10⁻²⁰ | move by at most 1.6×10⁻⁹ | 0.7355 |

So the noise entries scale as 1/η and as 2⁻ᵖ with the precision p. Of the 1184 entries below 10⁻⁶⁰, 32 do not move in
either experiment and are genuine small bounds, and the rest carry noise. Of the 515 entries that the code change
moves, 490 are pure noise and 25 are a small bound plus noise. All 1184 together add at most 2.3×10⁻⁶⁰ to a weighted
row sum of θ, whose weights lie between 1 and 38.
