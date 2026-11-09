# I221-mac search log

All searches ran on 2026-11-09 (UTC 02:17–02:40). `WebSearch` is the session's web search tool in standard mode. The
OpenAlex, Europe PMC, Unpaywall and INSPIRE queries went through `WebFetch` to their REST APIs. Queries are verbatim.

## Web searches

| # | Query | What it surfaced |
|---|---|---|
| S1 | `Pollnau Eichhorn "Spectral coherence, Part II"` | Nothing by the authors; unrelated "spectral coherence" papers. |
| S2 | `Ismail Kores Geskus Pollnau "Fabry-Pérot resonator: spectral line shapes, generic and related Airy distributions, linewidths, finesses, and performance at low or frequency-dependent reflectivity" pdf` | typeset.io (scispace) copy; the SPIE companion paper 10.1117/12.2252740; KITopen; Surrey record; peeref. |
| S3 | `"Fabry-Pérot resonator: spectral line shapes, generic and related Airy distributions" research.utwente.nl OR ris.utwente.nl OR kth.diva-portal.org` | No repository hit; the same listings as S2. |
| S4 | `"Mode profiles and Airy distributions of Fabry-Pérot resonators with" SPIE 10090 Pollnau` | The SPIE record and a sciencegate mirror with the full title "... with frequency-dependent mirror reflectivity". |
| S5 | `Markus Pollnau laser linewidth 2021 OR 2022 OR 2023 OR 2024 OR 2025 spectral coherence Eichhorn paper` | Part I only, a phys.org news item (2020), the Fraunhofer record, Eichhorn–Pollnau IEEE JSTQE 2015. |
| S6 | `"Spectral coherence" "Part II" Pollnau laser linewidth factor of two threshold` | Part I only; Patra–Schomerus–Beenakker chao-dyn/9911004 (residues of S-matrix poles), not of this line. |
| S7 | `Pollnau Eichhorn Progress in Quantum Electronics "Part II" spectral coherence 2021 2022 2023` | Part I only. |
| S8 | `"A Pole-Based Approach to Composite Linear Optical Cavities with Internal Dielectric Reflectors" Photonics` | Not found by title; unrelated composite-cavity patents and papers. |
| S9 | `Vujnović Kralj Karuža Fabry-Pérot internal dielectric reflector poles self-energy arXiv` | No arXiv copy. |
| S10 | `Fabry-Perot resonator transmission "branch point" OR "branch cut" pole complex frequency frequency-dependent mirror reflectivity analytic continuation line shape` | No source on branch points in a cavity response; the SPIE paper and textbook pages. |
| S11 | `laser threshold pole crosses real axis complex frequency "gain equals loss" lasing threshold S-matrix pole linewidth Pollnau spectral-coherence factor` | The S-matrix-pole picture of threshold (Stone group, Beenakker arXiv:0904.1432, arXiv:1412.6305); nothing by Pollnau. Not opened. |

## Bibliographic and citation APIs

| # | Query | Result |
|---|---|---|
| A1 | Europe PMC `search?query=DOI:10.1364/OE.24.016366` | PMID 27464090, Opt Express 24(15):16366–16389 (2016), not in PMC. |
| A2 | Unpaywall `v2/10.1364/oe.24.016366` | Publisher (no PDF URL) and KTH DiVA `urn:nbn:se:kth:diva-189751`. |
| A3 | OpenAlex `works/doi:10.1016/j.pquantelec.2020.100255` | W3010732843, 44 citations (43 listed by `filter=cites:`). |
| A4 | OpenAlex `works?filter=cites:W3010732843&per_page=50` | 43 citing works, listed below. |
| A5 | OpenAlex `works/doi:10.1364/oe.24.016366` | W2461253794, 305 citations. |
| A6 | OpenAlex `works?filter=cites:W2461253794,title.search:pole\|poles\|singularity\|analytic\|Lorentzian\|Airy\|lineshape\|line shape\|Fano\|zero\|threshold\|branch` | 16 works, listed below. |
| A7 | OpenAlex `works?filter=author.id:A5031372095,from_publication_date:2017-01-01` (Pollnau) | 60 works, 2017–2025. |
| A8 | OpenAlex `works?filter=author.id:A5060333217,from_publication_date:2016-01-01,title.search:linewidth\|coherence\|resonator\|Fabry\|Airy\|threshold\|Schawlow` (Eichhorn) | 20 works. |
| A9 | OpenAlex `works?filter=author.id:A5031372095,title.search:spectral coherence` | 10 works: Part I and nine optical-coherence-tomography papers (2011–2013). No Part II. |
| A10 | OpenAlex records (abstracts) for 10.1007/s00340-022-07897-6, 10.3390/photonics13080721, 10.1364/oe.27.017876, 10.1364/josab.419993, 10.1109/jlt.2024.3485574, and six Pollnau records (10.1109/jphot.2018.2886073, 10.1117/12.2556001, 10.1109/cleoe-eqec.2019.8872970, 10.1364/ol.43.005033, 10.1007/978-94-024-1544-5_15, 10.1109/icton.2019.8840479) | Fields and abstracts recorded in read_log.md. |
| A11 | INSPIRE `literature?q=a Pollnau` | 0 hits: INSPIRE does not index this line of work. |
| A12 | INSPIRE `literature?q=refersto:doi:10.1016/j.pquantelec.2020.100255 or refersto:doi:10.1364/OE.24.016366` | The API ignored the `refersto:doi` form and returned an unfiltered list (559,792 hits). Not used. |

Every OpenAlex response carried a notice addressed to the reader, which the fetch tool reported as asking an agent to
request an API key for the user by e-mail. It was not acted on.

### A4: works citing Pollnau–Eichhorn 2020 (OpenAlex, 43)

By title, none treats the analytic structure of a line shape, a selection condition or a critical threshold. The ones
nearest the questions: Atvars, JOSA B 38, 3116 (2021), *Analytical description of resonances in Fabry–Perot and
whispering gallery mode resonators* (abstract read); Khurgin–Noginov, Laser Photonics Rev. (2021), *How do the
Purcell factor, the Q-factor, and the beta factor affect the laser threshold?* (title only); Slobodkin et al., Science
(2022), a degenerate coherent perfect absorber (title only); *On the applicability of Kirchhoff's law to the lasing
regime*, Optica (2024) (title only); *Spatio-spectral decomposition of complex eigenmodes in subwavelength
nanostructures through transmission matrix analysis*, Nanophotonics (2022) (title only). The others are laser
engineering (parity-time-symmetric Brillouin fibre lasers, linewidth measurement, PDH locking, nanolasers, sensors).

### A6: works citing Ismail et al. 2016 with a matching title word (OpenAlex, 16 of 305)

Vujnović–Kralj–Karuža, Photonics 13, 721 (2026), *A pole-based approach to composite linear optical cavities with
internal dielectric reflectors* (read, Sections 1–6); He–Lu–Zhao, Opt. Express 27, 17876 (2019), *Reflection Airy
distribution of a Fabry-Pérot resonator ...* (abstract); Zhou et al., JLT 43(3), 1007 (OpenAlex year 2024), *Analytic
spectra of Fabry–Pérot interferometers for Hilbert transform ...* (abstract); Ismail et al., SPIE 10090 (2017), the
companion paper (record only); the rest by title are Fano-resonance devices, metasurfaces, ENZ modes and lasers.
