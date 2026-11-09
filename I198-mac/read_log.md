# I198-mac read log

Every source below was opened through the `WebFetch` tool, which returns an extraction of the page (quotes limited to
about 120 characters, not byte-compared against the PDF). Where the tool returned a PDF as binary, the file it saved
was copied into an empty scratch directory and its text extracted with pypdf 7.0.0 (`python -I`, a scratch venv); those
quotes are from that extraction. Quotes are marked as quotes. "Part read" says how much of the page was covered. A
fetch that failed is listed with the reason.

## Q1, the linear cavity

- **L1. M. Pollnau, M. Eichhorn**, *Spectral coherence, Part I: Passive-resonator linewidth, fundamental laser
  linewidth, and Schawlow-Townes approximation*, Prog. Quantum Electron. 72, 100255 (2020),
  DOI 10.1016/j.pquantelec.2020.100255. Records: [KITopen](https://publikationen.bibliothek.kit.edu/1000122140) and
  [Surrey](http://openresearch.surrey.ac.uk/discovery/fulldisplay?&context=L&vid=44SUR_INST:ResearchRepository&docid=alma99822546202346)
  (title, authors, journal, volume, article number, DOI). Full text: the KITopen PDF
  (publikationen.bibliothek.kit.edu/1000122140/84758462), pypdf extraction, Secs. 3.5–3.6 (pp. 22–24) read closely,
  the reference list for [2], [19], [20], [51]–[54].
  - Sec. 3.5, Eq. (99): each emitted mode profile is a Lorentzian, rewritten as a pole pair,
    "1/(δ − i(2ϕ − 2πq)) + 1/(δ + i(2ϕ − 2πq))"; Eq. (100), "Σ 1/(x − q) = π cot(πx)" (citing Remmert); Eq. (101),
    the sum "= (i/2)[cot(ϕ + iδ/2) − cot(ϕ − iδ/2)]"; Eq. (108), the result equals the Airy distribution
    A_emit = (1 − R1R2)/((1 − √(R1R2))² + 4√(R1R2) sin²ϕ), with e^{−δ} = √(R1R2) (Eq. (19), *inferred* from (107)–(108)).
  - "the Airy distribution is nothing else but the sum of the mode profiles of the longitudinal resonator modes".
    Earlier: Koppelmann (Progress in Optics 7) says Bayer-Helms (Z. Angew. Phys. 15 (1963) 330) "showed that the Airy
    distribution can be represented exactly" by a sum of Lorentzians.
  - The sum is over intensities, not fields: "the sum in Eq. (108) is over the intensity mode profiles γq,emit(ν)
    rather than over the electric fields."
  - p. 24, frequency-dependent reflectivity: "Since the photon-decay time also becomes frequency dependent, the FWHM
    linewidth loses its meaning." "each Airy distribution is still the infinite sum of its underlying mode profiles.
    However, the mode profiles are not Lorentzian-shaped anymore" and "the Airy distributions become distorted [2]".
  - Propagation loss, Eqs. (111)–(112): it enters as e^{−α_prop ℓ} per pass, so R1R2 → R1R2 e^{−2α_prop ℓ} in the
    round-trip factor.
  - Not contained: poles off the round-trip lattice, zeros, branch points, or any analytic continuation beyond the
    cot partial fractions; a nonlinear cavity.
- **L2. N. Ismail, C. C. Kores, D. Geskus, M. Pollnau**, Opt. Express 24(15), 16366–16389 (2016),
  DOI 10.1364/OE.24.016366. Bibliographic fields from the search listing of the Optica abstract page (S6) and from
  reference [2] of L1. **FULL-TEXT-UNREAD**: the Optica abstract and full-text pages returned a loading placeholder;
  the scispace PDF returned nothing. Its content is known here only through L1 and L3 (secondary).
- **L3. Wikipedia, *Fabry–Pérot interferometer*** (secondary),
  [en.wikipedia.org](https://en.wikipedia.org/wiki/Fabry%E2%80%93P%C3%A9rot_interferometer), Secs. 3.5, 3.8, 3.9.
  - 3.8, citing Ismail et al.: frequency-dependent reflectivities "can be treated with the same equations as above";
    "the photon decay time τc(ν) and linewidth Δνc(ν) now become local functions of frequency"; "Each Airy
    distribution is the sum of all underlying mode profiles which can be strongly distorted." No functional form of
    R(ν) is given.
  - 3.9, citing Pollnau–Eichhorn: A_circ = 1/((1 − R1R2e^{−αℓ})² + 4R1R2e^{−αℓ} sin²ϕ) as extracted.
- **L4. L. L. Sánchez-Soto, J. J. Monzón, G. Leuchs**, *The many facets of the Fabry-Perot*, Eur. J. Phys. 37, 064001
  (2016), arXiv:1610.06163 (journal-ref and DOI 10.1088/0143-0807/37/6/064001 from the
  [arXiv page](https://arxiv.org/abs/1610.06163)). Full text, [ar5iv](https://ar5iv.labs.arxiv.org/html/1610.06163),
  two fetches.
  - Eq. (2.1), the transmitted amplitude as a sum of round trips, A_in t t′ e^{−iφ}(1 + r² e^{−i2φ} + r⁴ e^{−i4φ} + …);
    Eq. (2.4), T(φ) = (1 − r²) e^{−iφ}/(1 − r² e^{−2iφ}).
  - Sec. 2.2.3, the self-consistent field, Eq. (2.13), A(0) = A(0) r² e^{−i2φ} + t′ A_in, solved in (2.14). The
    transfer function's "poles and zeros provide full information of the response of the system"; they are not
    listed.
  - Sec. 2.2.4, Eq. (2.16): the impulse response is "a train of short pulses separated in time by" 2t_c, with
    e^{−γ_c t_c} = r².
  - Eq. (3.7): "The Airy distribution appears in this way as a sum of Lorentzian profiles of width Γ", centred at
    φ = mπ, with Γ = ln(1/r²).
  - Not contained: losses ("we assume that such a mirror is lossless"), coupled cavities, nonlinear effects.
- **L5. D. M. Marques, J. A. Guggenheim, P. R. T. Munro**, *Angular Airy function: a model of Fabry-Perot etalons
  illuminated by arbitrary beams*, Opt. Express 29(15), 24144–24150 (2021), DOI 10.1364/OE.431362 (from the PDF's own
  header). Full text, [UCL Discovery PDF](https://discovery.ucl.ac.uk/10131370/1/dMarques_angularAiryFunction.pdf),
  pypdf extraction, all 7 pages.
  - Eq. (1): in transmission, A(θ) = √(1−R1)√(1−R2) exp(i2πNh cosθ/λ)/(1 − √R1√R2 exp(i4πNh cosθ/λ)); in reflection
    a ratio of first-degree expressions in the same exponential (a zero and a pole).
  - Eq. (2), the Gaussian angular spectrum, and Eq. (3), Ê_fp(θ, ϕ) = Ê_i(θ, ϕ) A(θ): each plane-wave component gets
    its own round-trip phase 4πNh cosθ/λ.
  - Sec. 3: the asymmetry "occurs because, as the wavelength is reduced from the normal incidence resonant
    wavelength, plane wave components with higher polar angles of propagation enter the filtering condition", while
    on the other side "there are no plane wave components in the beam's angular spectrum which enter the resonance
    condition."
  - Not contained: the analytic structure of the averaged line shape (poles, cuts), a closed form of the integral,
    a law for the amplitude of the m-th round trip. Its refs. [10] (La Penna et al., Opt. Commun. 162, 267 (1999)),
    [12] (Nichelatti–Salvetti, Appl. Opt. 34, 4703 (1995)) and [13] (Lee–Hahn–Lee, JOSA A 19, 973 (2002)) were not
    opened.
- **Failed.** The UCL Discovery "pp" mirror of L5 (403); the Optica pages of L2 (loading placeholder).

## Q2, nonlinear cavities

- **N1. T. Hansson, S. Wabnitz**, *Frequency comb generation beyond the Lugiato–Lefever equation: multi-stability and
  super cavity solitons*, JOSA B 32(7), 1259–1266 (2015), DOI 10.1364/JOSAB.32.001259 (the DOI from the related-DOI
  field of the [arXiv page](https://arxiv.org/abs/1503.03274); volume, issue and pages from the Chalmers record). Full text, [ar5iv](https://ar5iv.arxiv.org/html/1503.03274),
  two fetches, Secs. II–V.
  - Eqs. (1)–(2), the Ikeda map: "E^{m+1}(t,0) = √θ E_in + √(1−θ) e^{iφ₀} E^m(t,L)" and a damped NLS in z.
  - Eq. (4), the fixed point: "E = ρe^{iφ}E + √θ E_in", with φ = δ₀ − γL_eff|E|², so the stationary field is the
    round-trip geometric sum with an intensity-dependent ratio, E = √θ E_in/(1 − ρe^{iφ(|E|²)}) (*inferred*, solving
    (4)). Eq. (5): 1/[(1−ρ)² + 4ρ sin²(φ/2)] = |E|²/(θ|E_in|²), the Airy function of the nonlinear phase. "Either one or
    three stationary states are possibile when the rotation (phase-shift) is assumed small"; further "excited" states
    at |E|² ≈ (δ₀ + 2πn)/(γL).
  - Sec. IV: the round-trip matrix "c^{m+1} = √(1−θ)[W⁻¹(0)R(ϕ)W(L)]c^m ≡ Qc^m"; "The Ikeda map has an instability
    whenever the modulus of an eigenvalue of Q is larger than unity"; Eq. (11), "q± = √(1−θ)(p ± √(p²−1))" with
    "p = cos(ϕ)cosh(μL) − [γ|E0|² + (β2/2)ω²] sin(ϕ) sinh(μL)/μ"; the ordinary MI "has its origin in the q+ eigenvalue,
    while the latter comes from the q− eigenvalue and gives rise to a period doubling instability."
  - The LLE is the round-trip average of the map, valid for small per-pass nonlinear phase and detuning; it misses the
    excited states and the period-doubling instability.
  - Not contained: Newton or continuation for the fixed points (they are found from (5) and a geometric construction),
    harmonic balance.
- **N2. M. Conforti, A. Mussot, A. Kudlinski, S. Trillo**, *Modulational instability in dispersion oscillating fiber
  ring cavities*, arXiv:1405.6041; the [arXiv page](https://arxiv.org/abs/1405.6041) gives no journal-ref but the
  related DOI 10.1364/OL.39.004200 (Opt. Lett. 39, 4200 (2014)). Full text, [ar5iv](https://ar5iv.arxiv.org/html/1405.6041).
  - The perturbation obeys "d ε/dz = M(z) ε" (2×2); the round-trip matrix is "the 2×2 fundamental matrix solution
    evaluated at z=Λ"; its eigenvalues λ are the Floquet multipliers, unstable when "|λ|>1", with gain ln|λ|/Λ. For
    piecewise-constant dispersion: "We have MI if |Δ|>(1+W)", Δ the Floquet discriminant, W = e^{−2αΛ} the Wronskian.
  - A period-two state: "the pulse train is reproduced identical after two round-trips".
  - Not contained: harmonic balance, Hill's method, continuation.
- **N3. P. Parra-Rivas, E. Knobloch, L. Gelens, D. Gomila**, *Origin, bifurcation structure and stability of localized
  states in Kerr dispersive optical cavities*, arXiv:2010.03375 (no journal-ref on the
  [arXiv page](https://arxiv.org/abs/2010.03375); IMA J. Appl. Math. per the search listing, *(unverified)*). Full text, [ar5iv](https://ar5iv.labs.arxiv.org/html/2010.03375), characters 0–193242 in two
  fetches.
  - Eq. (1), the LLE "∂tA = −(1+iΔ)A + iν∂x²A + i|A|²A + S". Stationary states by "numerical path continuation
    algorithms" with "a predictor-corrector approach" (citing Allgower–Georg and Doedel et al.); stability from
    "Lψ = σψ", "computing the eigenvalues of the Jacobian matrix obtained from L after spatial discretization".
  - Sec. 7: breathers from "a supercritical Hopf bifurcation (H)"; the cycle "undergoes a period-doubling bifurcation
    (PD)", then "period-2", "period-4" and temporal chaos; the attractor ends in "a boundary crisis (BC)" with "the
    infinite-dimensional saddle corresponding to the unstable spike".
  - Not contained: continuation of the periodic orbits or their Floquet multipliers, software, a scaling law at the
    saddle.
- **N4. D. Gomila, M. A. Matías, P. Colet**, *Excitability mediated by localized structures*, arXiv:nlin/0411047,
  journal-ref PRL 94, 063905 (2005), DOI 10.1103/PhysRevLett.94.063905 (from the
  [arXiv page](https://arxiv.org/abs/nlin/0411047)). Full text, [ar5iv](https://ar5iv.labs.arxiv.org/html/nlin/0411047).
  - Eq. (1), the 2D LLE. "The unstable branch (the so-called lower or middle branch) has a single unstable
    direction." Near the saddle-loop bifurcation the period obeys T ∝ −(1/λ₁) ln(θ_c − θ), λ₁ "the unstable
    eigenvalue of the saddle point", λ₁ = 0.17713581; predicted slope 1/λ₁ ≈ 5.65 against 5.60 from simulations.
  - The eigenvalues come from a "semi-analytical stability analysis" of an earlier JOSA B paper, not described here.
- **N5. Y. K. Chembo, C. R. Menyuk**, *Spatiotemporal Lugiato–Lefever formalism for Kerr-comb generation in
  whispering-gallery-mode resonators*, arXiv:1210.8210, related DOI 10.1103/PhysRevA.87.053852. Abstract only
  ([arXiv](https://arxiv.org/abs/1210.8210)): "a variant of the Lugiato-Lefever equation" that is "significantly more
  suitable than the modal expansion approach" for wide combs. The modal expansion is Chembo–Yu, PRA 82, 033801 (2010)
  (records only, S14).
- **N6. C. Maitland, M. Conforti, A. Mussot, F. Biancalana**, *Stationary states and instabilities of a Möbius fibre
  resonator*, Phys. Rev. Research 2, 043195 (2020), DOI 10.1103/PhysRevResearch.2.043195, arXiv:2004.14095 (journal-ref
  from the arXiv page). Full text, ar5iv.
  - Eq. (1): each loop's output feeds the other, A₁^{m+1}(0) = √θ A_in + √(1−θ)e^{−iδ₂}A₂^m(1), and symmetrically.
    Stationary states are one-round-trip fixed points. The 4×4 Floquet matrix W has eigenvalues in pairs ±λ₁, ±λ₂.
    Period-two and period-four trains appear in simulations; "A detailed analysis of parametric instabilities of the
    Möbius resonator and they period doubling is outside the scope of this paper."
  - Not contained: a half-period map composed with the swap, a symmetry reduction of the Floquet problem.
- **Records only** (bibliographic fields from search listings or library records, content not read): K. Ikeda, Opt.
  Commun. 30(2), 257–261 (1979) (bdt.semi.ac.cn record); K. Ikeda, H. Daido, O. Akimoto, PRL 45, 709–712 (1980);
  L. A. Lugiato, R. Lefever, PRL 58, 2209–2211 (1987), DOI 10.1103/PhysRevLett.58.2209; S. Coen, M. Haelterman, PRL 79,
  4139–4142 (1997), DOI 10.1103/PhysRevLett.79.4139; M. Haelterman, S. Trillo, S. Wabnitz, Opt. Commun. 91, 401–407
  (1992); F. S. Felber, J. H. Marburger, PRA 17, 335–342 (1978); Y. K. Chembo, N. Yu, PRA 82, 033801 (2010).
- **Failed.** scilit (403) for Ikeda 1979; the Czech library record of Felber–Marburger (bot check); the Kyoto PDF of
  PRL 50, 713 (empty).

## Q3, Fratini et al.

- **F1. F. Fratini, E. Mascarenhas, L. Safari, J-Ph. Poizat, D. Valente, A. Auffèves, D. Gerace, M. F. Santos**, *A
  Fabry-Perot interferometer with quantum mirrors: nonlinear light transport and rectification*, PRL 113, 243601
  (2014), arXiv:1410.5972, INSPIRE recid 3025790 (title, authors, journal, DOI from the INSPIRE record). Full text with
  the supplement, [ar5iv](https://ar5iv.labs.arxiv.org/html/1410.5972).
  - Eq. (1), the power-dependent reflectance of one emitter, R = γ²/(γ² + 4δω² + 4pγ²), with reflected phase
    θ = arctan(2δω/γ) − π. Eq. (2), T = 1/(F₁ + F₂ sin²(2μ + θ₊)).
  - (S.2), the round-trip sum with the complex ratio √(R₁R₂) e^{2ikL} e^{i(θ₁+θ₂)}. (S.7), the powers at the emitters,
    p₁ = |t^{inc}(0) + t^{intr}(0)|², p₂ = |t^{intr}(L)|², "appear both at the right- and the left-hand sides", solved
    numerically: a geometric sum whose ratio depends on the field it sums.
  - Rectification from two different emitters, figure of merit Eq. (4).
  - Not contained: multiple solutions, bistability, a stability analysis or time evolution of the stationary state.
- **F2. F. Fratini, R. Ghobadi**, *Full-quantum light diode*, PRA 93, 023818 (2016), arXiv:1510.01968 (INSPIRE). Full
  text, ar5iv. Master equation for the two emitters with the light traced out, Bloch–Langevin equations for nine
  operators, steady state with the Mathematica package QUANTUM. No round-trip sum, no bistability, no stability
  analysis. Against the semiclassical model of F1, "the quantumness reduces the nonlinearity of the system".
- **F3. E. Mascarenhas, M. F. Santos, A. Auffèves, D. Gerace**, *A quantum rectifier in a one-dimensional photonic
  channel*, PRA 93, 043821 (2016), arXiv:1510.01472 (INSPIRE). Full text, ar5iv. Quantum stochastic (input–output)
  master equation; "the Fabry-Perot approach overestimates the diode efficiency", always below 70%. No round-trip
  sum, no bistability, no stability analysis.
- **F4. N. Almeida, T. Werlang, D. Valente**, *Mach-Zehnder interferometer with quantum beamsplitters*, JOSA B 36,
  3357 (2019), arXiv:1902.10181 (INSPIRE). Full text, ar5iv. Single-excitation Schrödinger equation with a
  Wigner–Weisskopf approximation, closed-form photodetection probabilities, a transfer-matrix limit. No geometric
  series, no self-consistent stationary state.
- **F5. Abstracts only** ([arXiv](https://arxiv.org/abs/1611.05050) and the like): Roy, PRA 96, 033838 (2017),
  arXiv:1611.05050 (a two-level and a Λ atom coupled asymmetrically; "critical intensity" for maximum nonreciprocity);
  Dai, Roulet, Le, Scarani, PRA 92, 063848 (2015), arXiv:1510.04494 (full quantum treatment; rectification "a purely
  multi-photon effect", up to 70%); Manasi, Roy, PRA 98, 023802 (2018), arXiv:1712.04474 (quantum Langevin equations
  for driven spin chains); Zheng et al., arXiv:1605.01135 (coupled microcavities; the abstract mentions "the unstable
  output field intensity caused by optical bistability"). None mentions a round-trip sum or a self-consistent
  geometric series.
- **F6. Fratini's own publication list**, [sites.google.com/site/filippofratiniwebsite](https://sites.google.com/site/filippofratiniwebsite/home/physics),
  and his INSPIRE records (I3): after 2014 the line continues only in F2, in an optical transistor with a quantum dot
  in a photonic wire (PRB 97, 201106(R) (2018), arXiv:1705.04056; OSA QIM 2017, QT2B.2), which were not opened.
