# I793-mac: winding counts recounted with starting samples spaced by edge length (one per 0.25)

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/793
Code: `solver/matter/complex_css.py` and `css_inner_pert.py` of choptuik-large-d, branch wip/xf-793 (the default of
`winding` is one starting sample per 0.25 of edge; `--K=N` keeps N per edge). Originals: `I95-mac/css/` (COMPLEX_CRITICAL
§2), `I376-mac/` and `I770-mac/` (CSS_STABILITY §1.4, §1.6).

| file | what |
|---|---|
| `queue1.sh`, `queue1.log`, `boxes_k0.jsonl` | COMPLEX_CRITICAL 2's boxes A, B, C, S at D = 4, 5, 6, 8, 10, 20, 40, 80, both radii, and the D = 4 controls (plant, nometric), with the new default |
| `queue2.sh`, `queue2.log`, `locate_k0.jsonl` | COMPLEX_CRITICAL 2's strip S cut into sub-boxes of width 0.5 (`complex_css.py locate`), each zero refined at R = 0.6 x_h, with the new default |
| `chain.sh` | runs queues 2 and 3 after queue 1, one at a time |
| `queue3.sh`, `queue3.log`, `inner_counts.jsonl` | CSS_STABILITY 1.4 (kappa 0) and 1.6 (kappa 1) recounted with the new default, W also with K = 6 |

## Results

### COMPLEX_CRITICAL 2 (complex_css.py boxes), new default against I95-mac/css/boxes_k0.jsonl

| D | A | B | C | S (0.85, 0.6) | all 8 match | determinants (new, old) | seconds (new, old) |
|---|---|---|---|---|---|---|---|
| 4 | 0 | 2 | 1 | 6, 6 | yes | 1378, 1092 | 361, 242 |
| 5 | 0 | 2 | 1 | 5, 5 | yes | 1368, 1072 | 435, 265 |
| 6 | 0 | 2 | 1 | 4, 4 | yes | 1348, 1042 | 364, 291 |
| 8 | 0 | 2 | 1 | 3, 3 | yes | 1234, 976 | 348, 305 |
| 10 | 0 | 2 | 1 | 2, 2 | yes | 1202, 936 | 449, 283 |
| 20 | 0 | 2 | 1 | 1, 0 | yes | 1280, 852 | 777, 276 |
| 40 | 0 | 2 | 1 | 0, 0 | yes | 1296, 820 | 1580, 400 |
| 80 | 0 | 2 | 1 | 0, 0 | yes | 1328, 852 | 1810, 640 |

D = 4 controls (R = 0.85 x_h): plant 1 + 3i in C: 2; nometric B: 0, C: 0 (quoted 2; 0, 0).

The seconds include a shared machine's load (load average up to 102 during D = 40 and 80); they are not a cost
comparison.

### COMPLEX_CRITICAL 2's strip sub-boxes (complex_css.py locate, width 0.5)

| D | 4 | 5 | 6 | 8 | 10 | 20 | 40 | 80 |
|---|---|---|---|---|---|---|---|---|
| sum of sub-box windings (quoted) | 6 (6) | 5 (5) | 4 (4) | 3 (3) | 2 (2) | 1 (1) | 0 (0) | 0 (0) |
| located (quoted) | 6 (6) | 5 (5) | 5 (5) | 3 (3) | 2 (2) | 1 (1) | 0 | 0 |
| displacement at 0.6 x_h | 9e-4 to 1.3e-2 | 1e-2 to 3.3e-2 | 3.1e-2 to 4.8 | 3.9e-2 to 0.14 | 0.18, 4.1 | 4.9 | — | — |

### CSS_STABILITY 1.4 and 1.6 (css_inner_pert.py count, settings A and B)

| box | kappa 0 (A, B) | quoted | kappa 1 (A, B) | quoted |
|---|---|---|---|---|
| A | 0, 0 | 0, 0 | 0, 0 | 0, 0 |
| B | 2, 2 | 2, 2 | 2, 2 | 2, 2 |
| C | 1, 1 | 1, 1 | 0, 0 | 0, 0 |
| S | 0, 0 | 0, 0 | 0, 0 | 0, 0 |
| plant in C (kappa 0, 1 + 6i) / in B (kappa 1, 3 + 1i), setting A | 2 | 2 | 3 | 3 |
| nometric, B, setting A | 0 | 0 | 1 | 1 |
| strip 5 < Re < 8, lower / upper, setting A | | | 0 / 1 | 0 / 1 |
| artefact box 6.5 < Re < 8, 2.95 < Im < 4.61, setting B | | | 0 | 0 |
| locate's plant at 2.3 + 6.1i | | | found at A and B, displacement 0 | the same |
| **W, new default** | | | **4, 2** (538, 494 determinants) | 4, 2 (K = 24) |
| **W, K = 6 (the control)** | | | **0, 0** (344, 304) | 0, 0 |

Every quoted count recounts to its quoted number; none is a discrepancy.

## Not recounted

- COMPLEX_CRITICAL 3 (the real DSS's imaginary sector, `hp/modecount_*`) and its D = 60 row: another counter, outside
  #793's scope.
- `css_pert.py winding` (used by `css_count.py`, matter/CSS.md 6): its own routine, with K = 12 per edge.
