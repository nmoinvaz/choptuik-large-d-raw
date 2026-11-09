# I221-mac read log

Every source below was opened on 2026-11-09. Where `WebFetch` returned a PDF as binary, the copy it saved was moved into
an empty scratch directory and its text extracted page by page with macOS PDFKit (a 15-line Swift script kept in a
separate directory); those quotes are from that extraction, whose equations are partly garbled (ligatures and
fraction bars are lost), so equations were reconstructed from the extraction and are marked as such. One page that
`WebFetch` could not open (MDPI, HTTP 403) was read as text through Claude in Chrome. Quotes are marked as quotes.

## The two named sources

- **R1. M. Pollnau, M. Eichhorn**, *Spectral coherence, Part I: Passive-resonator linewidth, fundamental laser
  linewidth, and Schawlow-Townes approximation*, Prog. Quantum Electron. 72, 100255 (2020),
  doi:10.1016/j.pquantelec.2020.100255. KITopen record https://publikationen.bibliothek.kit.edu/1000122140 (title,
  authors, journal, volume, article number, DOI, KITopen DOI 10.5445/IR/1000122140, "published online 11.08.2020" per
  the record); PDF https://publikationen.bibliothek.kit.edu/1000122140/84758462 (67 pages, sha256 9814177f…797d9;
  running footer "Progress in Quantum Electronics 72 (2020) 100255", "Available online 9 March 2020"). **Read in full**
  (pp. 1–67), Secs. 2–4 (pp. 3–30) and 6–10 (pp. 47–65) closely, Sec. 5 and Sec. 8 for structure only.
  - Sec. 3.1, Eq. (53): Ecirc/Elaun = 1/(1 − r1r2 e^{−αprop ℓ} e^{−i2ϕ}); Eq. (56), the generic Airy distribution;
    Eq. (62), its integral over one free spectral range, (1/π)∫Acirc dϕ = 1/(1 − R1R2 e^{−2αprop ℓ}); Eq. (63), the
    fraction of the FSR where Acirc ≥ 1, "from ΔνFSR/2 for R1R2 = 0 to ΔνFSR/3 for R1R2 → 1".
  - Sec. 3.4, Eq. (91): Erefl/Einc = (r1 − r2e^{−αprop ℓ}e^{−i2ϕ})/(1 − r1r2e^{−αprop ℓ}e^{−i2ϕ}) (reconstructed);
    Eq. (94): at resonance it vanishes for R1 = R2 and αprop = 0, the back-emitted field "destructively interferes
    with the electric field Erefl,1 initially back-reflected".
  - Sec. 3.5, Eqs. (98)–(108): the emitted mode profile in phase variables is 2δ/(δ² + (2ϕ − 2πq)²), split as
    "1/(δ − i(2ϕ − 2πq)) + 1/(δ + i(2ϕ − 2πq))" (reconstructed), with δ = δout/2, "which can be a general function of
    frequency"; Eq. (100), Σ 1/(x − q) = π cot(πx) [Remmert]; Eq. (101), the sum "(i/2)[cot(ϕ + iδ/2) − cot(ϕ − iδ/2)]";
    Eq. (107), (1 − e^{−2δ})/((1 − e^{−δ})² + 4e^{−δ}sin²ϕ); Eq. (108), the result is Aemit. "the Airy distribution
    is nothing else but the sum of the mode profiles of the longitudinal resonator modes". "the sum in Eq. (108) is
    over the intensity mode profiles γq,emit(ν) rather than over the electric fields", because "all optical modes are
    orthogonal with each other". Fig. 14: 31 mode profiles summed numerically against the Airy distribution.
  - p. 24, frequency-dependent reflectivity: "the FWHM linewidth loses its meaning", "the mode profiles are not
    Lonretzian-shaped anymore" (sic), "the Airy distributions become distorted [2]". Sec. 3.6: the q = 0 mode is
    included in the sum, so there is no cut-off wavelength.
  - Sec. 4.2, Eq. (113): Lorentzian finesse Fc = 2π/(−ln(R1R2e^{−2αprop ℓ})); Eq. (114): Δνc = ΔνFSR at
    R1R2e^{−2αprop ℓ} = e^{−2π} ≈ 0.001867, R1 = R2 ≈ 4.32%. Sec. 4.3, Eqs. (115)–(119): ΔνAiry from an arcsin;
    Eq. (117): ΔνAiry/Δνc; Eq. (118): ΔνAiry = ΔνFSR at R1R2 = 17 − 12√2 ≈ 0.02944, "R1 = R2 ≈ 17.2%". Fig. 12
    caption: ratios 1.001, 1.022, 1.132, 1.717 at R1 = R2 = 0.9, 0.6, 0.32, 0.172. Fig. 19 caption: "When the minimum of
    the Airy distribution crosses half its maximum ... the linewidth instantaneously jumps to infinity." p. 28: "we
    are operating numerous laser resonators whose passive Airy linewidth ΔνAiry is undefined".
  - Sec. 5.3, Eq. (128): energy conservation for a field generated inside the resonator requires
    cos(Δϕem) = √(R1R2); Eq. (130): θ = π/2, emission "90° in lead".
  - Sec. 6.2: Blaquière (1962) "by comparison with the theory of fission in a nuclear reactor in a subcritical,
    critical, or supercritical state" derived half the maser linewidth; Gordon (1964): "in a steady-state oscillator,
    including a cw laser, the gain is always smaller than the losses".
  - Sec. 7.1, Eq. (142): 1/τL = 1/τc − cg; Eq. (143): ΔνL = |1/τL|/(2π); Eq. (146): "Λ := 1/(1 − cgτc)", the
    spectral-coherence factor. Fig. 34: five regimes; at cgτc = 1, "Λ, τL, QL → ∞ and ΔνL = 0"; for cgτc > 1,
    "Λ < 0, τL < 0, QL < 0, but ΔνL > 0", "temporally unsustainable" (Sec. 7.3).
  - Sec. 7.4, Eqs. (155)–(156): in cw, Rdecay − Rst = Rsp > 0, so "in a cw-lasing mode the gain due to stimulated
    emission is smaller than the losses". Eq. (163): Λ = φ/φvac + 1 for an ideal four-level laser.
  - Sec. 7.5, Eqs. (167)–(178): the four approximations (i)–(iv) take Eq. (154) to the Schawlow–Townes Eq. (138);
    without the "+1" the approximation diverges at Pout → 0, "a 'zero-photon catastrophe'".
  - Sec. 2.2: "The relevant issues will be discussed in part II of this paper." Sec. 10: the factor-of-two reduction
    near threshold, "We have already obtained a possible semi-classical answer ... and will discuss it in part II".
  - References [18] Svelto, 5th ed., "pp. 142–146. Ch. 4.5.1"; [19] the same book, "pp. 169–171. Ch. 5.3".
  - Not contained (whole-text search of the extraction): the word "pole" (only in "dipole"), "branch", "singular",
    "eigenvalue" (only in the title of their ref. [7]); zeros of a line shape other than Eq. (94); a functional form of a
    frequency-dependent reflectivity; complex frequency ("complex plane" occurs once, in Sec. 5.1(e) on the
    Kramers–Kronig relations); a growth-rate law near threshold or a build-up time.
- **R2. N. Ismail, C. C. Kores, D. Geskus, M. Pollnau**, *Fabry-Pérot resonator: spectral line shapes, generic and
  related Airy distributions, linewidths, finesses, and performance at low or frequency-dependent reflectivity*,
  Opt. Express 24(15), 16366–16389 (2016), doi:10.1364/OE.24.016366. Full text: the published version deposited in
  KTH DiVA, https://kth.diva-portal.org/smash/get/diva2:948682/FULLTEXT01.pdf (25 pages: a DiVA cover and journal
  pp. 16366–16389; sha256 bad4caea…a280e4; header "Vol. 24, No. 15 / 25 Jul 2016 / OPTICS EXPRESS 16366",
  "Received 15 Apr 2016; ... published 12 Jul 2016"), reached through Unpaywall. **Read in full.**
  - Abstract and Sec. 1: the Airy linewidth and finesse "break down at a mirror-reflectivity product equaling
    (0.172)2"; the frequency-dependent case gives "deformed mode profiles that can be analytically determined".
  - Secs. 2–4 are the αprop = 0 versions of R1's Secs. 2–4 (Eqs. (1)–(53), Appendices A–C), with the same
    decomposition, Eq. (42), from Appendix C's cot sum [Remmert].
  - Sec. 5: "Now we consider the mirror reflectivities as general functions of frequency, Ri(ν), such that the
    photon-decay time τc(ν) of Eq. (3) becomes a function of frequency"; "Δνc turns into a local function of
    frequency, thereby losing its meaning as the FWHM linewidth"; each mode profile is computed from Eqs. (15) and (41)
    with τc(ν). The example: identical multilayer mirrors, reflectivity "symmetric around its maximum value of 98% at
    300 THz", shown in Fig. 9 (no formula in the text); lengths 999.808 µm and 999.924 µm. In the asymmetric case the
    nearest mode profile and the Airy distribution "become strongly asymmetric", with a main peak of FWHM 7.2 GHz
    against 118.7 GHz for a constant τc. Numerical sums of 6 × 10⁶ mode profiles; the truncation error follows
    "ϵ(M) = εM −1", Kahan summation suggested. Approximating each mode by a Lorentzian with its own width gives an
    error that "would never decrease to zero ... but would converge to a constant value".
  - Not contained: a closed form for Ri(ν), complex frequency, poles, zeros, branch points, a nonlinear or active
    cavity.

## Later work and citing works

- **R3. V. Vujnović, N. Kralj, M. Karuža**, *A pole-based approach to composite linear optical cavities with internal
  dielectric reflectors*, Photonics 13(8), 721 (2026), doi:10.3390/photonics13080721 (OpenAlex record: authors,
  volume, issue, article number; cites R2). Read through Claude in Chrome at
  https://www.mdpi.com/2304-6732/13/8/721, Sections 1–6 and Fig. captions (characters 0–50000 of 80809; Appendices
  A–D and the reference list not read).
  - Abstract: they "identify cavity poles as zeros of the reduced denominator in the complex-frequency plane"; for a
    weak reflector "the resulting mode pulling and linewidth change are, respectively, governed by the imaginary and
    real parts of a single complex quantity formed by the coherent sum of two mirror-side scattering paths".
  - Eqs. (23)–(25): t(ω) = t1t3e^{ik(L1+L2)}/𝒟(ω), poles at 𝒟 = 0, Im ω < 0. Eq. (29): one-pole form
    t ∝ 1/(ω − ω̃⁽⁰⁾ − Σ(ω)), "the optical self-energy". Eqs. (39)–(41): δω̃ = i(c/2L)ζ, δω = −(c/2L)Im ζ,
    δκ = −(c/L)Re ζ. Eq. (54): the three-mirror denominator 1 + r1r2e^{2ikL1} + r2r3e^{2ikL2} + r1r3e^{2ik(L1+L2)}.
    Sec. 5.3: pole trajectories by continuation in a swept parameter, Eq. (56) dω̃/ds = −∂sD/∂ωD, which "applies to a
    simple pole"; the non-simple case is in Appendix D (not read).
  - Not contained in the part read: zeros of the response, branch points, a profile with non-geometric harmonics.
- **R4. M. Eichhorn**, *The influence of resonator outcoupling and losses on the photon statistics of the LASER*,
  Appl. Phys. B 128(10) (2022), doi:10.1007/s00340-022-07897-6. Abstract only (OpenAlex): a master-equation extension
  for the beam-splitter effect of output couplers; Poisson statistics are not general.
- **R5.** Abstracts only (OpenAlex): He, Lu, Zhao, Opt. Express 27(13), 17876 (2019), the reflection Airy distribution
  and a loss measurement; Atvars, JOSA B 38(10), 3116 (2021), analytic resonance formulas for FP and WGM resonators;
  Zhou, Fu, Chen, Tsai, Jun, JLT 43(3), 1007–1016 (OpenAlex year 2024), the analytic (Hilbert-transform) spectrum of
  an FP interferometer with arbitrary reflectivities.
- **R6. Pollnau's own later records** (OpenAlex abstracts): Pollnau, Opt. Lett. 43, 5033 (2018), counter-propagating
  modes ±q are independent modes; Kores, Ismail, Bernhardi, Laurell, Pollnau, IEEE Photonics J. (2018), the
  distributed phase shift in DFB resonators accumulates incompletely, so the resonance shifts to shorter wavelengths;
  the same authors, CLEO/Europe 2019, DFB resonators with a continuously distributed phase shift; Yeung, Pollnau, SPIE
  (2020), a recursive circulating-field method for exact fields in Bragg mirrors and DFB structures; Pollnau, ICTON
  2019, *The laser linewidth – fairy tales and physical evidence*; Pollnau, Ismail, *Novel aspects of the Fabry-Pérot
  resonator*, a book chapter (2018), no abstract in the record and not opened.
- **R7. Ismail, Kores, Geskus, Pollnau**, SPIE 10090, 1009011 (2017), doi:10.1117/12.2252740, *Mode profiles and
  Airy distributions of Fabry-Pérot resonators with frequency-dependent mirror reflectivity*. Record only (search
  listings); the SPIE page returned nothing.

## Failed fetches

- scispace (typeset.io) PDF of R2: empty. Optica `fulltext.cfm` and `viewmedia.cfm` for R2: loading placeholder.
  KTH DiVA record page: an Anubis bot check (the FULLTEXT01.pdf link worked). SPIE page of R7: empty. sciencegate:
  DNS failure. MDPI through `WebFetch`: HTTP 403 (read through Chrome instead). The Springer chapter of R6: not
  opened; the only copy that surfaced was a university proxy mirror, which was not used.
