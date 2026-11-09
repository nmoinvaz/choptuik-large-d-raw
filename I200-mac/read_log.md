# I200-mac read log

Every source opened through `WebFetch`, with its URL, the part read, and short quotes as the tool returned them (the
tool returns an extraction, with verbatim quotes limited to about 120 characters; they were not byte-compared against
the PDFs). PDFs that came back as binary were extracted with pypdf 7.0.0 from the copy the tool saved, in a scratch
environment. Dates are UTC, all 2026-11-09.

## Q1, results beyond all orders

- R1. **M. Mariño, T. Reis**, *Resurgence for superconductors*, arXiv:1905.09569, https://ar5iv.labs.arxiv.org/html/1905.09569,
  characters 0–147552 (all) in two fetches.
  - Eq. (1.1): Δ² ~ e^{−A/γ}; the first Borel singularity is at A. Gaudin–Yang: c_k ~ −(1/π)(π²)^{−k+1}Γ(k−1) (Eq. 4.6),
    singularity at ζ = π² (Eq. 4.10), "precisely twice the strength of the exponentially small term in the energy gap".
  - Gap: Δ_BCS ≈ 8E_F e^{−π²/(2γ)} (Eq. 2.43); Δ/E_F ≈ (16/π)√(γ/π) e^{−π²/(2γ)} (Eq. 2.54); e_BCS ≈ π²/12 − γ/2 −
    2π² e^{−π²/γ} (Eq. 2.45).
  - "has a non-analytic, exponentially small dependence on the coupling constant"; "should be therefore regarded as a
    non-perturbative effect"; the series is "factorially divergent and non-Borel summable".
  - Abstract: "the Borel singularity is of the renormalon type"; not instanton-driven. Ring diagrams ℐ_ℓ ~ 4^{−ℓ}ℓ!
    (Eq. 4.27), from the logarithmic singularity of the Lindhard function; particle-particle ladders c_n^pp ~ (2π²)^{−n}n!
    (Eq. 4.33).
  - Trans-series Eq. (4.17), C₁ = ±i (Eq. 4.18), which "plays the rôle of a Stokes parameter"; "the choice of sign is
    correlated with the choice of lateral resummation".
  - Introduction: "The Cooper instability has been sometimes linked to the lack of analyticity of the perturbative
    series." No critical temperature or Thouless criterion. Conclusions: "it is natural to conjecture that this
    connection is general"; the series "lacks non-perturbative information".
- R2. **J. Polchinski**, *Effective field theory and the Fermi surface*, hep-th/9210046 (TASI 1992),
  https://ar5iv.labs.arxiv.org/html/hep-th/9210046, all.
  - E∂_E V(E) = N V²(E) + O(V³) (Eq. 28); V(E) = V/(1 + NV ln(E₀/E)) (Eq. 29); E_c = E₁ e^{−1/(λ−μ*)} (Eq. 32).
  - "The gap and the critical temperature are indeed of the form (32), with calculable numerical coefficients"; the RG
    "does not get the O(1) coefficient in the critical temperature".
  - The effective potential "sums up the 'cactus' graphs, the same as in large-N O(N) models and mean field theory".
- Failed: Cooper, PR 104, 1189 (1956), scan at ieeemilestones.ethw.org (404). BCS, PR 108, 1175 (1957): no full text
  surfaced. Both FULL-TEXT-UNREAD.

## Q2 and Q3, mean-field exponents and the one unstable mode

- R3. **T. Hara, T. Koike, S. Adachi**, *Renormalization group and critical behaviour in gravitational collapse*,
  gr-qc/9607010, https://ar5iv.labs.arxiv.org/html/gr-qc/9607010, characters 0–100000 of 216312.
  - RG map Eq. (2), u_i(t,r) ↦ e^{α_i s}u_i(e^{−s}t, e^{−βs}r); R_s on data U(ξ) = u(−1, ξ), Eq. (3); fixed point
    R_s(U*) = U*.
  - Abstract: the results hold for DSS "replacing “fixed point” with “limit cycle”".
  - β_BH = β/κ (Eqs. 21, 27), κ "the unique positive eigenvalue"; Claim 1: "if U∗ has a unique relevant mode, then (S1)
    and (U1) hold with this U∗"; two or more relevant modes give multicritical behaviour.
  - "the analogy not only phenomenologically but also theoretically between the" collapse and phase transitions; no
    mean field, Landau theory, BCS, viscosity. The relevant mode is not tied to a symmetry.
- R4. **A. Larkin, A. Varlamov**, *Fluctuation phenomena in superconductors*, cond-mat/0109177,
  https://ar5iv.labs.arxiv.org/html/cond-mat/0109177, characters 0–200000 of 224656.
  - τ_GL = πħ/[8k_B(T−T_c)] (Eq. 2): the lifetime of fluctuation Cooper pairs diverges at T_c.
  - TDGL, Eq. (99): "−γ_GL(∂/∂t + 2ieφ)Ψ = δℱ/δΨ* + ζ(r,t)", γ_GL = πα/8; ε_p = αT_c(ε + ξ²p²) (Eq. 108), ε = (T −
    T_c)/T_c; propagator L(p, Ω) = (−iγ_GL Ω + ε_p)^{−1} (Eq. 106); τ_p = γ_GL/ε_p.
  - Gi = δT/T_c ~ (T_c/E_F)⁴ (Eq. 1); GL region ξ ~ ε^{−1/2} (ν = 1/2); RG: ν = 3/5 at D = 3, ν = 1/2 + ε/10 near D = 4.
  - Thouless not named in the part read. Sec. 5 (microscopic TDGL) unread.
- R5. **A. Georges, G. Kotliar, W. Krauth, M. J. Rozenberg**, cond-mat/9510091 (RMP 68, 13 (1996), "To appear in
  Reviews of Modern Physics" on the page), https://arxiv.org/abs/cond-mat/9510091 and the ar5iv page (abstract only;
  the body is PostScript): "This mapping is exact in the limit of large lattice coordination (or infinite spatial
  dimensions)."
- R6. **D. Vollhardt**, *Why calculate in infinite dimensions?*, arXiv:2210.06072,
  https://ar5iv.labs.arxiv.org/html/2210.06072, characters 0–100000 of 172147.
  - J = J*/Z (Eq. 11); the fluctuation of the local field is a sum of Z terms over Z (Eq. 12), so it falls like 1/√Z;
    "The Weiss mean-field theory is seen to become exact in the limit of infinite coordination number Z".
  - Fermions: t = t*/√d (Eq. 27), "so that the kinetic energy remains finite for d→∞". ε = 4 − d about Ginzburg–Landau's
    critical dimension. No statement on exponents at d = ∞ in the part read.
- R7. **R. Emparan, C. P. Herzog**, *The large D limit of Einstein's equations*, RMP 92, 045005 (2020), arXiv:2003.11394,
  https://ar5iv.labs.arxiv.org/html/2003.11394, characters 0–300000 of 302723 in four fetches.
  - Sec. I: large D as "mean field-like"; "when the coordination number of a lattice diverges, one recovers a mean field
    theory"; the mean-field intuition applies to "infrared physics, and in particular when the theory is a classical
    one".
  - Sec. III.6: "non-perturbative effects from the far zone must be present in the near-horizon zone", the breakdown is
    "non-perturbative in 1/n", corrections of order n^{−n}.
  - Sec. IV.4.5: "the equations will not be valid when temporal gradients or spatial gradients along the horizon are" of
    order D/r₀; "these theories can only deal with time-dependent variations of the radius of the horizon that are
    small".
  - Sec. V: k_GL = 1 − 1/(2n) + 7/(8n²) + …; the instability because "the sound speed is instead imaginary"; viscous
    entropy production enters at next order in 1/n. Sec. IV.5.1: η = m, s = 4πm.
  - Sec. VII.2 (holographic superconductor): "a WKB style approach", "a zero of the Airy function", a₁ = 2.33811, "about
    a 15% error for n=4 and a 35% error for n=3".
  - Sec. X.1: "the hair condenses just outside the near-horizon zone"; the gains are "meager".
  - Sec. X.3, critical collapse (FULL-TEXT-UNREAD before): "the data are well approximated by" γ ≈ ½(1 − 1/D), "although
    a better fit to the data at larger D" γ ≈ ½(1 − 1/(D+1)), from Sorkin–Oren (2005) and Bland et al. (2005);
    Rozali–Way's solutions are "not self-similar, and it is not a collapse"; "going beyond the scope of the effective
    membrane theory"; "The behavior with D of the echoing period is less clear".

## Q4, holographic superconductors

- R8. **S. A. Hartnoll, C. P. Herzog, G. T. Horowitz**, *Building a holographic superconductor*, arXiv:0803.3295,
  https://ar5iv.labs.arxiv.org/html/0803.3295, all.
  - ⟨𝒪₁⟩ ≈ 9.3 T_c(1−T/T_c)^{1/2} (Eq. 11), ⟨𝒪₂⟩ ≈ 144 T_c²(1−T/T_c)^{1/2} (Eq. 12), "a square root behaviour that is
    typical of second order phase transitions".
  - "Finite temperature continuous symmetry breaking phase transitions are only possible in 2+1 dimensions in the large N
    limit (i.e. the classical gravity limit of our model), where fluctuations are suppressed."
  - T_c from the nonlinear solutions (T_c ≈ 0.226 ρ^{1/2}, 0.118 ρ^{1/2}); footnote 3, "consistent with Landau-Ginzburg
    theory"; 2Δ ≈ 3.54 T_c compared.
- R9. **R. Emparan, K. Tanabe**, *Holographic superconductivity in the large D expansion*, arXiv:1312.1108,
  https://ar5iv.labs.arxiv.org/html/1312.1108, all.
  - n = D − 1; probe limit; m̂ = m/n (Eq. 2.9); 𝖱 = (r/r₀)ⁿ (Eq. 2.16); λ = n/2 + nμ̂_c at criticality (Eq. 2.31).
  - Near zone: hypergeometric, ψ = 𝖱^{iμ̂} ₂F₁(iμ̂+λ̂₊, iμ̂+λ̂₋; 1; 1−𝖱) (Eq. 2.27); far zone: Bessel (Eq. 2.30).
  - Matching gives Ai(−δμ̂) = 0 (Eq. 2.39), a zero-energy bound state in a triangular well (Eqs. 3.13–3.14);
    T/ρ^{1/(n−1)}|_crit = (n/4π)[λ − n/2 + a₁(λ/2 − n/4)^{1/3}]^{−1/(n−1)}, a₁ = 2.33811 (Eq. 2.42); "better than 15%"
    at n = 4, about 35% at n = 3 (App. B).
  - Near-zone BF-type bound m̂²_eff < −1/4 (Eq. 2.23); exponentially small terms in n dropped, corrections O(1/n); "we
    cannot determine the critical exponent at this level of approximation".
  - Sec. 4: backreaction, T_c ∝ (1 − μ̂²/2q̂²) (Eq. 4.12).
- R10. **S. A. Hartnoll, G. T. Horowitz, J. Kruthoff, J. E. Santos**, *Diving into a holographic superconductor*,
  arXiv:2008.12786, https://ar5iv.labs.arxiv.org/html/2008.12786, all.
  - Josephson oscillations and Kasner inversions p_t → −p_t/(2p_t+1) (Eq. 38) inside the hairy black hole;
    c₅ = A sin(B/(1−T/T_c) + C), B ≈ 0.491, C ≈ 1.945 (Eq. 25); c₁/c₂ ≈ 0.796(2)(1−T/T_c)^{1/2}.
  - The number of inversions diverges at temperatures accumulating at T_c; *inferred*: 1 − T_n/T_c ≈ B/(nπ − C), a 1/n
    law, not geometric. "recursive structure", "fractal-like"; BKL and mixmaster mentioned; no DSS, limit cycle or
    critical collapse.

## Q5, discrete scale invariance

- R11. **A. LeClair, J. M. Román, G. Sierra**, *Russian doll renormalization group and superconductivity*,
  cond-mat/0211338, https://ar5iv.labs.arxiv.org/html/cond-mat/0211338, all.
  - V_{jj'} = G ± iΘ (Eq. 2), "Here we add an imaginary part which breaks time reversal".
  - g_{N−1} = g_N + (g_N² + θ_N²)/N, θ unrenormalized (Eq. 14); dg/ds = g² + θ² (Eq. 15); g(s) = θ tan[θs +
    tan⁻¹(g₀/θ)] (Eq. 16); period λ = π/θ (Eq. 17).
  - Δ_n = ω/sinh t_n, t_n = t₀ + nπ/θ (Eq. 10), tan(θt₀) = θ/g (Eq. 11); E_C^{(n)} ∼ −½δN² e^{−2t₀−2nπ/θ} (Eq. 12).
  - θ → 0: Δ₀ ∼ 2ω e^{−1/g}, "recovering the standard BCS result". Cites Bedaque–Hammer–van Kolck and Glazek–Wilson;
    the regime "reduces at one loop to the Kosterlitz-Thouless flow"; "much like a Russian doll".
- R12. **E. Braaten, H.-W. Hammer**, *Universality in few-body systems with large scattering length*, Phys. Rep. 428,
  259 (2006), cond-mat/0410417, https://arxiv.org/abs/cond-mat/0410417 and https://ar5iv.labs.arxiv.org/html/cond-mat/0410417,
  characters 0–200000 of 248219.
  - s₀ cosh(πs₀/2) = (8/√3) sinh(πs₀/6) (Eq. 35); "Its numerical value is s0≈1.00624, so eπ/s0≈22.7"; level ratio
    e^{−2π/s₀} (Eq. 37).
  - Sec. 3.4: "A limit cycle is a family" of Hamiltonians closed under the RG and parameterized by an angle (Eq. 51);
    "one of the signatures of an RG limit cycle is discrete scale invariance"; examples Wilson (1971), Glazek–Wilson,
    LeClair–Román–Sierra: "the gap equation for this model has multiple solutions related by a discrete scaling
    symmetry". No gravity.
- R13. **D. B. Kaplan, J.-W. Lee, D. T. Son, M. A. Stephanov**, *Conformality lost*, arXiv:0905.4752,
  https://ar5iv.labs.arxiv.org/html/0905.4752, all.
  - β = (α − α*) − (g − g*)² (Eq. 2), g± = g* ± √(α − α*) (Eq. 3); m ~ Λ_UV θ(α* − α) exp(−c/√(α* − α)) (Eq. 1);
    Λ_IR/Λ_UV ≃ e^{−π/√(α* − α)} (Eq. 4).
  - 1/r² potential: ν± = −(d−2)/2 ± √(α − α*), α* = −(d−2)²/4 (Eq. 12); "our RG equation actually describes limit cycle
    behavior", scales spaced by exp[−π/√(α* − α)]; it "can explain the Efimov effect".
  - "the loss of conformality can be associated with the violation of the Breitenlohner-Freedman (BF) bound"; no BCS,
    no critical collapse.
- R14. **B. Kol**, *Choptuik scaling and the merger transition*, hep-th/0502033v3, https://arxiv.org/pdf/hep-th/0502033v3
  (pypdf extraction, all 19 pages).
  - Eq. (2.5): ε = ρ^{s±}, s± = ((D−2)/2)(−1 ± i√(8/(D−2) − 1)); "For D ≥ D∗ := 10 we see that s± become purely real".
  - −1/s = γ(1 ± i2π/Δ) (Eq. 3.16); γ = 1/4 (3.19) and 2π/Δ = √((10−D)/(D−2)) (3.20) for D < 10; γ = −1/s₊ =
    ¼(1 + √((D−10)/(D−2))) (3.21) for D ≥ 10.
  - Sorkin–Oren's results "indicate that (3.20) is not a good estimator for the Choptuik ∆".

## Q6, viscosity

- R15. **J. Camps, R. Emparan, N. Haddad**, *Black brane viscosity and the Gregory–Laflamme instability*, JHEP 05 (2010)
  042, arXiv:1003.3636, https://ar5iv.labs.arxiv.org/html/1003.3636, all.
  - η = s/4π, ζ = 2η(1/p − c_s²) (Eq. 1.3), c_s² = −1/(n+1) (Eq. 1.4); "saturate the bounds".
  - Ω = k/√(n+1)·(1 − (n+2)/(n√(n+1))·kr₀) (Eq. 1.5); "Sound waves in the effective fluid are unstable".
  - Large n: Ω̃ = nΩ, k̃ = √n k, Ω̃ = k̃(1 − k̃/(4πT)), "the exact limiting relation valid for all wavenumbers"; k_GL →
    4πT/√n (Eq. 3.11). The viscous fluid equation "does not admit any zero-mode solution", yet the truncated Ω(k)
    "appears to capture the zero-mode". No critical collapse.
- R16. **R. Emparan, K. Izumi, R. Luna, R. Suzuki, K. Tanabe**, *Hydro-elastic complementarity in black branes at large
  D*, JHEP 06 (2016) 117, arXiv:1602.05752, https://ar5iv.labs.arxiv.org/html/1602.05752, characters 0–100000 of
  117569.
  - ∂_tρ + ∂_i(ρv^i) = 0 (Eq. 2.16); ∂_t(ρv^i) + ∂_j(ρv^iv^j + τ^{ij}) = 0 (Eq. 2.17); τ_ij = −ερδ_ij − 2ρ∂_(iv_j) −
    ρ∂_i∂_j lnρ (Eq. 2.18); η = ρ, ζ = (1+ε)η/p (Eq. 2.20); s = 4πρ, T = 1/(4π) (Eq. 2.21), so η/s = 1/(4π).
  - σ^i = σ̂^i/√n (Eq. 2.7); the theory "reconstructs only a region of radial extent ∼1/D above the horizon"; vacuum,
    Maxwell and p-form charges only, no scalar matter; no horizon formation or collapse.
- R17. **M. Rozali, B. Way**, JHEP 11 (2018) 106, arXiv:1807.10283, https://ar5iv.labs.arxiv.org/html/1807.10283, Sec. 3
  to the end (Secs. 1–2.3 read in #172).
  - "we conjecture that this divergence is indicative of horizon formation at finite D"; "While black hole collapse does
    not occur in the large D limit"; "this horizonless large D limit can be joined with the well-developed large D limit
    of black holes"; the time scaling "has not yet appeared in any large D study of black holes".
  - "The metric we have chosen cannot have the continuous or discrete self-similarity exhibited by the finite D critical
    solution"; "These equations are parabolic in character"; "the large D limit does not necessarily commute with the
    long time limit". AdS boson stars: λ = √2 − 1, "suggests that these solutions are linearly stable".
- R18. **I. Amado, D. Areán, A. Jiménez-Alba, K. Landsteiner, L. Melgar, I. Salazar Landea**, *Holographic superfluids
  and the Landau criterion*, JHEP 02 (2014) 063, arXiv:1307.8100, https://ar5iv.labs.arxiv.org/html/1307.8100, all.
  - Eq. (2), v_max = min ε(p)/p; "the imaginary part of the QNMs have to lie all in the lower half plane"; ω(k) = v_s k +
    (b − iΓ)k² (Eq. 3); "we use the determinant method of" [42]; the instability "strongest at finite wavelength".
- R19. **Z.-Y. Yuwen, C. Joana, S.-J. Wang, R.-G. Cai**, *Primordial black hole formation in bulk-viscous cosmology*, PRD
  114, L081309 (2026), arXiv:2606.26532, https://arxiv.org/abs/2606.26532 and https://arxiv.org/html/2606.26532,
  characters 0–100000 of 122393.
  - Eckart bulk viscosity Π = −ϵρ^{1/2}Θ_f, "ϵ is the dimensionless viscosity strength"; ξ ≡ ϵρ^q (Eq. S3), q = 1/2;
    δw = ξH/ρ = ϵ√(8π/3).
  - Fit M_PBH/M× = k|μ−μc|^γ (Eq. 5), Table 3: w = 1/3, ϵ = 0: γ = 0.37 (sinc), 0.28 (Gaussian); ϵ = 0.01: 0.34, 0.26;
    w = 1/5, ϵ = 0: 0.26, 0.23; ϵ = 0.01: 0.26, 0.19. "the γ parameter remains at a similar order of magnitude".
  - Eq. (12): the viscous effect in the critical amplitude, δ_c,0(1+Kϵ). "shear viscosity can be neglected"; Israel–
    Stewart only as an extension (Eq. S51). Cites Choptuik and Evans–Coleman for the scaling law only; no self-similar
    solution, no universality class.
- R20. Abstracts only: Müller–Schäfer arXiv:1710.00136 (matter falling into an existing black hole, viscous
  hydrodynamics; no threshold); Rein–Rendall–Schaeffer gr-qc/9804040, PRD 58, 044007 (1998) ("most of the matter falls
  into the black hole whenever a black hole is formed", "a discontinuity in the mass"); Olabarrieta–Choptuik
  gr-qc/0107076, PRD 65, 024007 (2002) ("the critical behavior in this model is Type I", "unstable, static spacetimes").

## Round 2

- R21. **D. Maison**, *Non-universality of critical behaviour in spherically symmetric gravitational collapse*, PLB
  366, 82 (1996), gr-qc/9504008, https://ar5iv.labs.arxiv.org/html/gr-qc/9504008, all.
  - p = kρ; the Evans–Coleman type "exists only up to a certain maximal value k_max ≈ 0.888"; Table 1: γ = 0.1143
    (k = 0.01), 0.3558 (k = 1/3), 0.8157 (k = 0.888); "the critical index depends rather strongly on the value of k,
    hence it is not universal". One unstable mode assumed, not counted. No viscosity.
- R22. **T. Koike, T. Hara, S. Adachi**, PRL 74, 5170 (1995), gr-qc/9503007, https://ar5iv.labs.arxiv.org/html/gr-qc/9503007,
  all.
  - "β = 1/Re κ" (Eq. 15), κ ≃ 2.81055255, β ≃ 0.35580192; a unique relevant mode assumed; "checked that there are no
    other relevant (or marginal) eigenmodes in the range 0≤Re κ≤15, |Im κ|≤14" (method not stated).
- R23. **C. R. Evans, J. S. Coleman**, PRL 72, 1782 (1994), gr-qc/9402041, https://ar5iv.labs.arxiv.org/html/gr-qc/9402041,
  all.
  - Perfect fluid, p = ρ/3; M_BH ≃ K(η − η_c)^β, β = 0.36 (Eq. 7); "The system is over-determined unless n is taken as an
    eigenvalue of the nonlinear system", n ≃ 1.1485; regularity at ξ = 0, ξ = ∞ and the sonic point. No viscosity,
    no statistical mechanics; the analogies are "intermediate asymptotics" and Guderley's implosion.
- R24. **P. Kovtun, D. T. Son, A. O. Starinets**, PRL 94, 111601 (2005), hep-th/0405231,
  https://arxiv.org/abs/hep-th/0405231 and https://ar5iv.labs.arxiv.org/html/hep-th/0405231, all.
  - η = σ_abs(0)/(16πG) (Eq. 7), σ_abs = a, s = a/4G (Eq. 4); the bound Eq. (15), "saturated by theories with gravity
    duals"; superfluids have finite shear viscosity from the normal component; helium exceeds the bound by about 9.
- R25. **A. Schmitt**, *Introduction to superfluidity*, Lect. Notes Phys. 888 (2015), arXiv:1404.1284,
  https://ar5iv.labs.arxiv.org/html/1404.1284, characters 0–100000 of 244179.
  - Eq. (2), dissipation if ε_p + p·v_s < 0; Eq. (3), v_c = min_p ε_p/p; "it is only the superfluid component that can
    flow through the thin tube"; "only the normal fluid carries entropy"; "A superconductor can be said to break a local
    symmetry spontaneously". No dynamical instability at the critical velocity.
- R26. **S. D. Glazek, K. G. Wilson**, PRL 89, 230401 (2002), hep-th/0203088, abstract: limit cycles "may be common" for
  quantum Hamiltonians that require renormalization; a discrete two-coupling model whose RG changes one coupling.
- R27. **C. Gundlach, D. Hilditch, J. M. Martín-García**, arXiv:2507.07636v1, https://arxiv.org/html/2507.07636v1,
  characters 0–100000 of 317589 (keyword search and Secs. II.5–II.7).
  - II.5: "the critical solution must be a fixed point (CSS) or limit cycle (DSS) in these coordinates".
  - II.6: dimensionful parameters "become irrelevant"; "Examples of dimensionless parameters which do change the
    universality class are" k in P = kρ, the sigma model's κ and probably a conformal coupling; equation-of-state
    changes that "do not affect the limit of high density" keep the class.
  - II.7: "a fixed point of the renormalisation group cannot have a preferred length scale".
  - No hit for viscous, viscosity, dissipat, Israel-Stewart, mean field, Landau, superconduct or Efimov in the part read.
- R28. **F. Marsiglio, K. S. D. Beach, R. J. Gooding**, *The BCS pairing instability in the thermodynamic limit*, Can. J.
  Phys. 90, 889 (2012), arXiv:1203.5122, https://ar5iv.labs.arxiv.org/html/1203.5122, all.
  - Thouless "tracked the BCS instability from above (in temperature) by monitoring the two particle propagator" (Ann.
    Phys. 10, 553 (1960)); g₂ = χ₀/(1 − |U|χ₀) (Eq. 1); "a single pole passes from the lower half-plane to the
    upper-half-plane in complex frequency"; "For the BCS instability we can focus on q=0".
- R29. **R. Emparan, J. Rafecas-Ventosa, B. Way**, *General effective theories of black holes in the large D limit*, JHEP
  04 (2026) 034, arXiv:2512.14186, https://arxiv.org/abs/2512.14186 and https://arxiv.org/html/2512.14186, characters
  0–100000 of 197383.
  - "they form a parabolic system with a well-posed initial value problem"; the near-horizon region "has a thickness of
    order 1/D"; "Time-dependent horizon fluctuations with amplitudes of O(D⁰) lie outside the regime of applicability";
    Rozali–Way cited only for "boson stars or oscillatons". No collapse, no horizon formation, no viscosity.
- R30. Abstracts or records only: Mariño–Reis, *Three roads to the energy gap*, PRB 106, 125142 (2022), arXiv:2010.16174
  (the gap from the Bethe ansatz, from resurgence of the perturbative series, and from the RG; "The three methods lead to
  the same answer"); Chavanis, EPJB 85, 229 (2012), arXiv:1002.0291 (the Nyquist method for self-gravitating systems);
  Silveira, EPL 149, 49001 (2025) (Jeans-type collapse with shear viscosity).
- R31. Wikipedia, *Ginzburg criterion* (a secondary source): "the value of the upper critical dimension comes out to be
  4"; "If the dimension of the space is greater than 4, the mean-field results are good and self-consistent"; cites
  Ginzburg (1961), Amit (1974), Als-Nielsen–Birgeneau (1977), Pathria–Beale (2011), not opened.
- R32. Beekman–Rademaker–van Wezel, arXiv:1909.01820, characters 0–250000 of 269318 (title, Chapters 1–3); Chapter 5
  (Landau theory) not reached by the extraction. FULL-TEXT-UNREAD for the part that matters.
- R33. B. Kol, hep-th/0502033v3: also pp. 3–5 and 14–17 (Table 1, the "Note added", Eqs. (3.13)–(3.21), Table 2).
