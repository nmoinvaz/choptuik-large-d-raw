# I809-mac: matter/CSS.md 6's winding counts of det M (kappa = 1) recounted with starting samples spaced by edge length

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/809
Code: `solver/matter/css_count.py`, `css_locate.py` and `css_pert.py` of choptuik-large-d, branch wip/xf-809 (the
winding starts from one sample per 0.25 of edge; `--K=N` keeps N per edge, 12 before). Originals:
`solver/matter/data/css_count_k1.jsonl` and `css_locate_k1.jsonl` (D = 10, 20, 40); the D = 4 counts of CSS.md 6 have no
record there. Backgrounds: `solver/matter/data/css_bg_k1.jsonl`.

| file | what |
|---|---|
| `queue1.sh`, `queue1.log`, `counts.jsonl`, `locate.jsonl` | the selftest, then every count of CSS.md 6 (css_count.py: 7 quoted boxes and the 3 boxes CSS.md 6 infers to hold exactly two; css_locate.py: 5 boxes), new default |
| `queue2.sh`, `queue2.log`, `diag.jsonl` | the D = 4 resonance-line box (counted 4, quoted 3): the old start (--K=12), the box cut into four in Re with each zero refined at R = 0.6 x_h, the bottom edge moved to Im 1.52 |
| `edge_zero.log` | the zero next to that box's bottom edge, by secant at R = 0.85 and 0.6 x_h |

## Results (kappa = 1, R = 0.85 x_h unless marked)

`css_count.py selftest`: the planted box 0.2 < Re < 2, |Im| < 6 with F = exp(pi lam^2) times three zeros counts 3 with
the new default and -5 with 12 starting samples per edge (the four right-edge intervals far from the zeros lose 2 turns
each). PASS, control fires.

| D | box | tool | quoted | new default |
|---|---|---|---|---|
| 4 | 0.2 < Re < 2.5, \|Im\| < 1.5 | css_count | 1 (lambda = 1) | 1 (232 determinants) |
| 4 | 2.5 < Re < 5, \|Im\| < 0.5 | css_count | 1 (lambda_phys = 3.786) | 1 (64) |
| 4 | 2.5 < Re < 5, 0.5 < Im < 1.5 | css_locate | 1, 2.532 + 1.486i, to 2.521 + 1.510i at 0.6 x_h | 1, 2.5319827 + 1.4858277i, to 2.5209637 + 1.5101844i |
| 4 | 2.5 < Re < 5, -1.5 < Im < -0.5 | css_locate | 1 (the conjugate) | 1, the conjugate to 1e-13 |
| 4 | 0.2 < Re < 5, 1.5 < Im < 2.5 | css_locate | **3** | **4** (also 4 with --K=12) |
| 10 | 0.2 < Re < 4.5, \|Im\| < 3 | css_count | 4 | 4 (460) |
| 10 | the same, R = 0.6 x_h | css_count | 4 | 4 (484) |
| 10 | 0.2 < Re < 4.5, \|Im\| < 2 | css_count | 2 | 2 (240) |
| 10 | 0.2 < Re < 4.5, 0.05 < Im < 3 | css_locate | 1, 3.3226 + 2.5045i, runs to 1 at 0.6 x_h | 1, 3.3225788 + 2.5045180i, runs to 1 |
| 20 | 0.2 < Re < 6, \|Im\| < 3 | css_count | 4 | 4 (456) |
| 20 | 0.2 < Re < 6, 0.05 < Im < 3 | css_locate | 1, 4.8288 + 2.9969i, runs to 1 at 0.6 x_h | 1, 4.8287572 + 2.9968513i, runs to 1 |
| 40 | 0.2 < Re < 5, \|Im\| < 2.5 | css_count | 2 | 2 (336) |
| 4 | 0.2 < Re < 5, \|Im\| < 1.2 | css_count | 2 (inferred from the located zeros) | 2 (220) |
| 10 | 0.2 < Re < 4.5, \|Im\| < 2.4 | css_count | 2 (inferred) | 2 (328) |
| 20 | 0.2 < Re < 6, \|Im\| < 2.9 | css_count | 2 (inferred) | 2 (404) |

**The one discrepancy.** The D = 4 box 0.2 < Re < 5, 1.5 < Im < 2.5 holds 4 zeros of det M: 1.7246631 + 1.6329116i,
3.2528484 + 1.5734640i, 4.0372394 + 1.5145361i and, from the zero sum of the piece 3.8 < Re < 5, one near 4.78 + 1.53i.
The three refined ones move by 2.5e-2, 2.5e-2 and 2.0e-2 at R = 0.6 x_h: artefacts on the resonance line Im 1.537. The
pieces 0.2-1.4, 1.4-2.6, 2.6-3.8, 3.8-5 wind 0, 1, 1, 2. The zero at 4.0372 + 1.5145i is 0.0145 inside the bottom edge,
and with the edge at Im 1.52 the box counts 3. The 12-per-edge start counts 4 on today's code and background, which
are those of the commit that quoted 3 (4ae034b3), and the 3 has no record, so its source is not reproduced.
