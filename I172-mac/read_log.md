# I172-mac read log

Every source below was opened on 2026-11-08 through the `WebFetch` tool, which returns an extraction of the page (quotes
limited to about 120 characters, not byte-compared against the PDF). Quotes are marked as quotes and are as the tool
returned them. "Part read" says how much of the page the extraction covered. A fetch that failed is listed with the
reason, so the channel can be retried.

## Critical collapse and discrete self-similarity

- **R2. C. Gundlach**, *Understanding critical collapse of a scalar field*, PRD 55, 695 (1997), gr-qc/9604019,
  DOI 10.1103/PhysRevD.55.695. [abs](https://arxiv.org/abs/gr-qc/9604019) (abstract, journal-ref and DOI fields) and
  [ar5iv](https://ar5iv.labs.arxiv.org/html/gr-qc/9604019), characters 0–100000 of 130156.
  - Sec. II.3: κ = 0 requires that "a and g, as well as ξ0, are composed only of even frequency terms in τ, and X± only
    of odd frequency terms." "This reflection-type symmetry is compatible with the field equations."
  - Sec. II.3: "I have expanded all periodic fields in Fourier components of τ, truncating the expansion at some
    relatively small number of components."; "the Fourier series converges rapidly" because "the solution is smooth".
  - No decay law of the coefficients, no closed-form time profile, no strip of analyticity in τ.
- **R3. J. M. Martín-García, C. Gundlach**, *Global structure of Choptuik's critical solution in scalar field collapse*,
  PRD 68, 024011 (2003), gr-qc/0304070 (bibliographic fields verified in notes/REF_CHECK.md §1).
  [ar5iv](https://ar5iv.labs.arxiv.org/html/gr-qc/0304070), characters 0–100000 of 143647, two fetches.
  - Sec. IV.1.1: the metric fields are even, "their Fourier transform only contains even k modes"; the matter fields U
    and V only odd k.
  - Sec. IV.2, before Eq. (59): "Therefore the high frequency behaviour of our fields Z is similar to that of the
    function" Σ_k e^{−a|k|} e^{4πikτ/Δ} = sinh a/(cosh a − cos(4πτ/Δ)) (Eq. (59)), which "has periodic sharp peaks of
    width aΔ/(4π) and height 2/a for small a."
  - Sec. IV.2: "the decay exponent a ranges from 0.28 for f_c at the center to 2.04 for U_p at the past lightcone";
    the phases of the high modes "tend to a linear dependence on k at a given point x"; "this exponential decay is the
    best numerical evidence we have in support of the analytical character of the Choptuik spacetime"; "We have not
    found an explanation for this behavior, but it seems to be of dynamical origin."
  - Eq. (59) is offered as a similarity, not fitted. It is a sum over all k with real ratio e^{−a}, with no first
    harmonic in the numerator and no phase parameter.
- **R4. R. H. Price, J. Pullin**, gr-qc/9601009. [ar5iv](https://ar5iv.labs.arxiv.org/html/gr-qc/9601009), full
  extraction. Flat-space pieces "Y = A sin[ω(ρ − αu)]" (Eqs. (24)–(25)), "y = e^{ρ−τ} F̃(τ)" (Eq. (38)) with F̃ only
  periodic, Eq. (43) f(η) = 𝒜 η ln η sin(ω ln η + δ̄), and "If, in fact, we take F~ to be a sinusoidal oscillation of
  amplitude unity". One frequency only; no harmonic series, no rational, arctan or artanh form. This settles the
  *(unverified)* line of notes/EEG_PROFILE.md §5.
- **R5. M. Reiterer, E. Trubowitz**, CMP 368, 143 (2019), arXiv:1203.3766 (verified in notes/LIT_REVIEW.md §3).
  [arXiv PDF](https://arxiv.org/pdf/1203.3766) came back as binary (failed); then
  [ar5iv](https://ar5iv.labs.arxiv.org/html/1203.3766), characters 0–100000 of 118188.
  - Sec. 1.1: "We represent the ωi as combined Fourier-Chebyshev series"; "Each ωi is 2π periodic or antiperiodic in τ,
    all are 4π periodic."; coefficients "𝒪((κ1)^−|m|(κ2)^−|n|)" "in the high frequency limit |m|+|n|→∞, with κ1,κ2>1";
    "We use κ1=65/64 and κ2=5/4."
  - Sec. 3: the antiperiodic class has "v_mn = 0 for all even m". No closed-form time profile.
- **R6. C. Ecker, F. Ecker, D. Grumiller, T. Jechtl**, SciPost Phys. 20, 176 (2026), arXiv:2602.10185 (verified in
  notes/REF_CHECK.md §1). [HTML v2](https://arxiv.org/html/2602.10185v2), characters 0–100000 of 214015.
  Fourier series in τ (Sec. 3.2, Eq. (24); Sec. 4.1, Eq. (59)); "whenever Z is an even function in τ we have
  Ẑ_{2l+1}(x)=0"; "We find Nτ=512 to be sufficient for D≳3.2". No decay law of the coefficients and no closed-form
  profile in the part read. Appendix C.3 ("Fourier approximation") and Fig. 22 ("Power spectra of converged initial
  data") lie past the part read (FULL-TEXT-UNREAD).

## Large D

- **R7. S.-H. Lai, W.-Y. Wen**, arXiv:2610.04960 (verified in notes/LIT_REVIEW.md §1).
  [HTML](https://arxiv.org/html/2610.04960), full extraction. Eq. (4), β(τ) = cos(2πτ) + sin(6πτ)/15.9476: "As a toy
  model, we use the explicit unit-period example of Ref. [12]"; the conclusions hold for any periodic β with isolated
  simple zeros, vanishing mean and half-period antisymmetry. No geometric or rational profile.
- **R8. R. Emparan, R. Suzuki, K. Tanabe**, *Evolution and end point of the black string instability: large D
  solution*, arXiv:1506.06772. [ar5iv](https://ar5iv.labs.arxiv.org/html/1506.06772), full extraction. Effective
  equations (11)–(12); static non-uniform strings, Eq. (17); the only analytic profile is the Gaussian blob, Eq. (22),
  "m(z) ≃ L/√(2π) e^(−z²/2)"; a small deformation is "approximately sinusoidal". No Fourier series with geometric
  coefficients and no rational function of cos. The journal (PRL 115, 091101 (2015)) is not on the page fetched.
- **R12. M. Rozali, B. Way**, JHEP 11 (2018) 106, arXiv:1807.10283 (verified in notes/REF_CHECK.md §1).
  [ar5iv](https://ar5iv.arxiv.org/html/1807.10283), Sec. 2.3. Eq. (10):
  "\varphi_{0}=\tanh^{-1}(\epsilon\,e^{-\omega^{2}r^{2}/2}\sin(\omega\tau-\tau_{0}))" and
  "\delta_{0}=\frac{\epsilon^{2}\,e^{-\omega^{2}r^{2}}\cos^{2}(\omega\tau-\tau_{0})}{1-\epsilon^{2}\,e^{-\omega^{2}r^{2}}\sin^{2}(\omega\tau-\tau_{0})}".
  No explicit ∂τφ₀, no harmonic expansion; "Since this oscillation is a single frequency, this solution describes the
  large D version of an oscillaton."

## Echoes in other fields

- **R1. A. Testa, P. Pani**, *An analytical template for gravitational-wave echoes: signal characterization and
  prospects of detection with current and future interferometers*, arXiv:1806.04253.
  [ar5iv](https://ar5iv.arxiv.org/html/1806.04253), characters 0–100000 of 121374. Eq. (10),
  "𝒦(ω) = 𝒯_BH ℛ e^{−2iωx₀} / (1 − ℛ_BH ℛ e^{−2iωx₀})"; Appendix A, Eq. (37), the sum
  "[1 + Σ_{n=1}^∞ (ℛℛ_BH e^{2iωd})^n]" and its closed form; Eq. (38), the n-th echo
  "𝒦_n(ω) = (𝒯_BH ℛ)(ℛ_BH ℛ)^{n−1} e^{−2iωx₀}"; Eq. (28), "A_echo(t) ∝ |ℛℛ_BH|^{t/2d}". The poles of 𝒦 are the
  object's quasinormal modes. The ratio ℛ, 𝒯 and Υ depend on ω, so 𝒦 is not periodic in ω; no real part of 𝒦 is
  taken; no arctan.

## Identities

- **R9. DLMF §1.15** ([dlmf.nist.gov/1.15](https://dlmf.nist.gov/1.15)). Eq. 1.15.12, "P(r,θ) = (1 − r²)/(1 − 2r cos θ
  + r²) = Σ_{n=−∞}^{∞} r^{|n|} e^{inθ}, 0 ≤ r < 1" (§1.15(iii), "Poisson Kernel"); Abel means 1.15.18 and 1.15.20;
  the conjugate Poisson integral on the line, 1.15.40. No named conjugate Poisson kernel for the circle.
- **R10. DLMF §18.12** ([dlmf.nist.gov/18.12](https://dlmf.nist.gov/18.12)). Eqs. 18.12.7, "(1 − z²)/(1 − 2xz + z²)
  = 1 + 2 Σ Tₙ(x) zⁿ"; 18.12.8, "(1 − xz)/(1 − 2xz + z²) = Σ Tₙ(x) zⁿ"; 18.12.9, "−ln(1 − 2xz + z²) = 2 Σ (Tₙ(x)/n)
  zⁿ"; 18.12.10, "1/(1 − 2xz + z²) = Σ Uₙ(x) zⁿ", all for |z| < 1. With x = cos θ these are the geometric Fourier
  series (the substitution Tₙ(cos θ) = cos nθ is not on this page).
- **R11. DLMF §4.24** ([dlmf.nist.gov/4.24](https://dlmf.nist.gov/4.24)). Eq. 4.24.3, "arctan z = z − z³/3 + z⁵/5 −
  z⁷/7 + ⋯", "|z|≤1, z≠±i" (§4.24(i) Power Series).
- **R13 (failed).** The course copy of the G&R series tables,
  [utf.mff.cuni.cz FourierSeries.pdf](https://utf.mff.cuni.cz/vyuka/NOFY126/2023/materialy/FourierSeries.pdf): a
  scanned PDF, no text came through. G&R's entry numbers 1.447 and 1.448 rest on search summaries only
  *(unverified)*.

## Failed fetches (breathers in optics)

- Dudley, Genty, Dias, Kibler, Akhmediev, *Modulation instability, Akhmediev Breathers and continuous wave
  supercontinuum generation*, arXiv:0910.1930: the [abs page](https://arxiv.org/abs/0910.1930) gave the title, authors,
  abstract and the related DOI 10.1364/OE.17.021497; the abstract does not state an analytic spectrum. The
  [PDF](https://www.arxiv.org/pdf/0910.1930) came back as binary, the
  [Optica full text](https://opg.optica.org/oe/fulltext.cfm?uri=oe-17-24-21497) as a loading placeholder.
- [hal-00582946 NA2011.pdf](https://hal.archives-ouvertes.fr/hal-00582946/file/NA2011.pdf): bot protection (Anubis).
- [PMC3376454](https://pmc.ncbi.nlm.nih.gov/articles/PMC3376454): browser verification screen.
