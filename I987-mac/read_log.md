# Read log, issue #987 (2026-11-19, UTC)

Every URL came from a WebSearch result. The fetches went through Claude Code's WebFetch, by a web-fetch subagent.

| item | URL | outcome |
|---|---|---|
| Costin–Tanveer, Ann. IHP C 24 (2007) 795–823, arXiv:math/0608290 | https://arxiv.org/pdf/math/0608290 | HTTP 200, PDF saved by the tool (sha256 prefix 15cefc8d3ab6ed9c), arXiv:math/0608290v1 [math.AP] 11 Aug 2006, 41 pages |
| Costin–Tanveer, Navier–Stokes, arXiv:math/0612063 | https://arxiv.org/pdf/math/0612063 | HTTP 200, PDF saved by the tool (sha256 prefix b82740c2bf9eaf50), arXiv:math/0612063v2 [math.AP] 20 Dec 2006, 30 pages |
| Xie–Tanveer, ARMA 166 (2003) 219–286 | https://portal.mardi4nfdi.de/wiki/Publication:1566401 | HTTP 200, a stub with the title only, no full-text link |
| the same | https://link.springer.com/article/10.1007/s00205-002-0235-4 | 303 to a Springer sign-in page (idp.springer.com), not followed |
| the same | https://www.researchgate.net/publication/226967448_Rigorous_Results_in_Steady_Finger_Selection_in_Viscous_Fingering | HTTP 403 |

**Extraction.** WebFetch returned both PDFs as compressed binary. Each copy was put in its own empty directory and
extracted with pypdf 7.1.1 (with fontTools) in a scratch venv (`python -I`), one text file per paper with page
markers: 2014 lines (math/0608290) and 1734 lines (math/0612063). The math survived extraction well enough to read
the statements. Every numbered statement and the main proofs were read. The estimate lemmas' proofs were skimmed for
further hypotheses (grep for assume, require, suppose, condition, restrict), and none was found beyond those recorded
in LIT_REVIEW.md §6.1.

**Xie–Tanveer.** Not reached. No arXiv or author-hosted copy surfaced in two searches. A search tool's summary of the
Springer abstract (a secondary source) says that analytic symmetric finger solutions exist for small surface tension
if and only if a Stokes constant for a relatively simple nonlinear differential equation is zero.
