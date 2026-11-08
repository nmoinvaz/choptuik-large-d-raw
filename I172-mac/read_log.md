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

## Second round (2026-11-08, after 20:20 UTC)

Correction to R8: the arXiv journal-ref of Emparan–Suzuki–Tanabe is Phys. Rev. Lett. 115, 091102 (2015), DOI
10.1103/PhysRevLett.115.091102 ([abs](https://arxiv.org/abs/1506.06772)), not 091101 as first written above.

### Critical collapse and large D

- **R23. E. W. Hirschmann, D. M. Eardley**, *Universal scaling and echoing in gravitational collapse of a complex
  scalar field*, PRD 51, 4198 (1995), gr-qc/9412066 ([abs](https://arxiv.org/abs/gr-qc/9412066), abstract and
  journal-ref). The collapse is "continuously self-similar". The [ar5iv](https://ar5iv.labs.arxiv.org/html/gr-qc/9412066)
  conversion failed ("Conversion to HTML had a Fatal error"), so the body is FULL-TEXT-UNREAD.
- **R24. C. Ecker, F. Ecker, D. Grumiller**, PRL 136, 191401 (2026), arXiv:2601.14358.
  [HTML v1](https://arxiv.org/html/2601.14358v1). Eq. (21) "β⁡(τ)=cos⁡(2πτ)+sin⁡(6πτ)/A", "A≈15.9476"; "the frequencies
  of higher modes are odd integer multiples of the fundamental frequency" (from finite-D numerics, their ref. 25);
  dψ₀/dτ = β/√(1+β²); no closed form of ψ₀ for the example; no harmonic decay law, geometric series, rational form or
  arctan.
- **R25. C.-H. Wu**, *Quantum critical collapse in the large D limit*, arXiv:2610.20705.
  [HTML](https://arxiv.org/html/2610.20705), characters 0–200000 of 209108. β(T) is "a smooth periodic function" (Sec.
  4.1), "Any smooth periodic β⁡(T) gives a leading-order DSS solution"; Eq. (103), β(T+Δ/2) = −β(T). No explicit
  profile.
- **R31. C.-H. Wu**, *Quantum fate of the Choptuik naked singularity*, arXiv:2606.17135, Phys. Rev. D 114, 044092
  (2026) (arXiv journal-ref). [abs](https://arxiv.org/abs/2606.17135), abstract only: 2+1 and 3+1 exterior models; no
  echo profile.
- **R28. C. Gundlach, D. Hilditch, J. M. Martín-García**, arXiv:2507.07636 (verified in notes/REF_CHECK.md §1).
  [HTML v1](https://arxiv.org/html/2507.07636v1), characters 0–200000 of 317589. "where Freg(τ), Fsing(τ) and H(τ) are
  periodic with period Δ" (Sec. III.3); "The scalar field itself is smooth with respect to τ"; no Fourier decay, no
  analyticity strip in τ, no closed-form profile, no large-D profile in the part read.
- **R33. C. Ecker, F. Ecker, D. Grumiller**, arXiv:2611.07007v1 (INSPIRE recid 3223940; title and authors match).
  [HTML v1](https://arxiv.org/html/2611.07007v1). Eq. (16) "β̃(θ) = A∗ Re[ e^{iθ} / (1 + q e^{i(2θ+δ)}) ]"; (S58)
  "β̃(θ) = A∗ Σ_{n≥0} (−q)^n cos[(2n+1)θ + nδ] = A∗ (cos θ + q cos(θ+δ)) / (1 + 2q cos(2θ+δ) + q²)"; after Eq. (16),
  "with successive mode amplitudes exponentially suppressed as e^{-αn}, where α = −ln q ≈ 2.90." The tool found no
  reciprocal-of-ellipse form, no linear equation in θ, no antiderivative (arctan appears only in the phase definition
  (S57)), no citation for the geometric model, and no mention of the Poisson kernel. This agrees with #165.
- **R32. G. Fodor**, *A review on radiation of oscillons and oscillatons*, arXiv:1911.03340 (cites Rozali–Way per
  INSPIRE). [ar5iv](https://ar5iv.labs.arxiv.org/html/1911.03340), characters 0–100000 and 190000–290000 of 291274.
  Sine-Gordon breather as a small-amplitude series, Eq. (2.15), with "at higher order in the expansion cos(3ωt),
  cos(5ωt)… modes also arise"; the expansion "is not convergent". Oscillon harmonics in Sec. 2.8.3, Eqs. (2.97)–(2.100),
  with polynomial (not geometric) coefficients. Rozali–Way's large-D oscillaton is not discussed in the parts read
  (characters 100000–190000 unread).

### Echoes and breathers in other fields

- **R15–R16. J. O. Smith III**, *Physical Audio Signal Processing* (W3K Publishing, 2010), online at CCRMA.
  [Feedback Comb Filters](https://ccrma.stanford.edu/~jos/pasp/Feedback_Comb_Filters.html): "y(n) = b\_0 x(n) - a\_M
  y(n-M)"; variant "y(n) = b\_M x(n-M) - a\_M y(n-M)"; the filter is "a computational physical model of a series of
  echoes, exponentially decaying and uniformly spaced in time", e.g. a plane wave between two parallel walls.
  [Amplitude Response](https://ccrma.stanford.edu/~jos/pasp/Feedback_Comb_Filter_Amplitude.html): "H(z) =
  \frac{1}{1-g\,z^{-M}}", "G(\omega) \isdef \abs{H(\ejo)} = \frac{1}{\abs{1 - g e^{-j\omega M}}}"; "g>0 produces
  resonant peaks at" ω_k = 2πk/M, "while for g<0, the peaks occur midway between these values."
- **R19. Wikipedia, *Fabry–Pérot interferometer*** ([page](https://en.wikipedia.org/wiki/Fabry%E2%80%93P%C3%A9rot_interferometer)),
  a secondary source. Transmitted field by round-trip decay: E_trans,1 = −E_inc t1 t2 e^(−iφ), E_trans,m+1 =
  E_trans,m r1 r2 e^(−i2φ), hence E_trans/E_inc = −t1 t2 e^(−iφ)/(1 − r1 r2 e^(−i2φ)), cited there to O. Svelto,
  *Principles of Lasers*, 5th ed. (2010), ch. 4.5.1 *(unverified)*; the circulating field cited to Siegman, *Lasers*
  (1986), ch. 11.3 *(unverified)*; the Airy distribution cited to Ismail, Kores, Geskus, Pollnau, Opt. Express 24(15),
  16366–16389 (2016) (fields from a search listing; the Optica page returned a loading placeholder, *(unverified)*).
  The tool flagged that the page's printed A_circ denominator, (1 − R1R2)² + 4R1R2 sin²φ, disagrees with
  |1 − r1 r2 e^(−i2φ)|⁻², which gives (1 − √(R1R2))² + 4√(R1R2) sin²φ (a Wikipedia transcription issue, not ours).
- **R20. F. Fratini, E. Mascarenhas, L. Safari, J-Ph. Poizat, D. Valente, A. Auffèves, D. Gerace, M. F. Santos**,
  *A Fabry-Perot interferometer with quantum mirrors: nonlinear light transport and rectification*, PRL 113, 243601
  (2014), arXiv:1410.5972 ([abs](https://arxiv.org/abs/1410.5972) for the journal-ref;
  [ar5iv](https://ar5iv.labs.arxiv.org/html/1410.5972) for the text). Supplemental Eq. (S.2), the round-trip sum
  "√T1√T2 + √T1√R2√R1√T2 e^{2ikL}e^{i(θ1+θ2)} + ..." and its closed form with denominator
  "1-\sqrt{R_{1}R_{2}}e^{2ikL}e^{i(\theta_{1}+\theta_{2})}", a complex round-trip ratio.
- **R22. N. Lu, J. Cuevas-Maraver, P. G. Kevrekidis**, *PT-symmetric sine-Gordon breathers*, J. Phys. A 47, 455101
  (2014), arXiv:1406.3082 ([abs](https://arxiv.org/abs/1406.3082); [ar5iv](https://ar5iv.labs.arxiv.org/html/1406.3082)).
  Eq. (2): b_e = 4 arctan[σ cos(at)/(a cosh σx)], b_o = 4 arctan[σ sin(at)/(a cosh σx)], σ = √(1−a²); Appendix
  Eq. (17), a numerical Fourier expansion in time with k_m = 15; no coefficients tabulated.
- **R29. Z. Mark, A. Zimmerman, S. M. Du, Y. Chen**, *A recipe for echoes from exotic compact objects*, PRD 96, 084002
  (2017), arXiv:1706.06155 ([abs](https://arxiv.org/abs/1706.06155); [ar5iv](https://ar5iv.arxiv.org/html/1706.06155),
  characters 0–100000 of 137091). Eq. (20), 𝒦̃(ω) = 𝒯̃_BH ℛ̃ e^{−2iωx₀}/(1 − ℛ̃_BH ℛ̃ e^{−2iωx₀}); Eq. (29), the same as
  a sum over echoes with (ℛ̃_BH ℛ̃)^(n−1) e^{−2i(n−1)ωx₀}; "each echo decays less than the previous and has a slightly
  lower frequency". No real part of 𝒦̃ and no arctan.
- **R30.** Testa–Pani: arXiv journal-ref "Phys. Rev. D 98, 044018 (2018)", related DOI 10.1103/PhysRevD.98.044018
  ([abs](https://arxiv.org/abs/1806.04253)).
- **Failed:** [arXiv:2312.01320](https://arxiv.org/abs/2312.01320) (HTML 404, abstract only); the KIT record
  1000122140 is a different Pollnau paper (Prog. Quantum Electron. 72, 100255 (2020)).

### Identities

- **R17. The hippopede.** [MacTutor](https://mathshistory.st-andrews.ac.uk/Curves/Hippopede/) returned 404.
  [A. Coffman, Lemniscates](https://users.pfw.edu/CoffmanA/pov/spiric.html): "This curve is also called an 'elliptic
  lemniscate of Booth,' and it is the image of an ellipse under inversion with respect to its center."
  [MathWorld, Hippopede](https://mathworld.wolfram.com/Hippopede.html) (E. W. Weisstein): r² = 4b(a − b sin²θ),
  reference Lawrence, *A Catalog of Special Plane Curves* (Dover, 1972), pp. 144–146; no inversion statement there.
- **R34. V. Ryazanov**, *The Stieltjes integrals in the theory of harmonic functions*, arXiv:1711.02717
  ([ar5iv](https://ar5iv.labs.arxiv.org/html/1711.02717)). Eq. (3.1), "the Poisson kernel is the 2π−periodic function"
  P_r(Θ) = (1−r²)/(1−2r cos Θ+r²); Eq. (4.1), "the conjugate Poisson kernel is the 2π−periodic function" Q_r(Θ) =
  2r sin Θ/(1−2r cos Θ+r²). No sine series of Q_r given. Journal not shown.
- **R26. J. F. Geer**, *Rational trigonometric approximations using Fourier series partial sums*, ICASE Report 93-68,
  NASA CR-191535, 1 Sep 1993 ([NTRS record](https://ntrs.nasa.gov/citations/19940017095)). Abstract: each
  approximation "is the quotient of a trigonometric polynomial of degree N" and one of degree M, with "an appropriate
  number of the Fourier coefficients of S(sub N,M) agree with those of f". Journal version J. Sci. Comput., DOI
  10.1007/BF02091779, from a search listing *(unverified)*.
- **R27 (failed).** Koepf and Nana Chiadjeu, *Algorithmic approach for formal Fourier series*, Math. Comput. Sci. 9
  (2015) 365–389 (search listing; the [Springer page](https://link.springer.com/article/10.1007/s11786-014-0215-8)
  redirected to a login, *(unverified)*). Benoit, Brisebarre, Salvy, arXiv:2604.26944
  ([HTML](https://arxiv.org/html/2604.26944), three fetches): the extraction stopped in Sec. 7.2 each time, so their
  account of Koepf–Nana Chiadjeu and Sec. 9.4 "Fourier expansions" were not reached.

## Identity check (this folder)

`identity_check.py` checks four identities used in the addendum at 30 digits on 41 points: the derivative of
Rozali–Way's oscillaton at fixed r is 2√q times form B at δ = 0; the derivative of the sine-Gordon breather at x = 0 is
2√q times form B at δ = π; the Fabry–Pérot transmitted field is Eq. (16)'s complex function with w = −r1r2 and θ = −φ;
form B in terms of P_q and Q_q. `identity_check.log` (exit 0, deviations ≤ 6e-31) and `identity_check_mutate.log`
(sign of q or w flipped, deviations 0.65–1.09, exit 1).
