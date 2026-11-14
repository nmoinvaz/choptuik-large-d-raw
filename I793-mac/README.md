# I793-mac: winding counts recounted with starting samples spaced by edge length (one per 0.25)

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/793
Code: `solver/matter/complex_css.py` and `css_inner_pert.py` of choptuik-large-d, branch wip/xf-793 (the default of
`winding` is one starting sample per 0.25 of edge; `--K=N` keeps N per edge). Originals: `I95-mac/css/` (COMPLEX_CRITICAL
§2), `I376-mac/` and `I770-mac/` (CSS_STABILITY §1.4, §1.6).

| file | what |
|---|---|
| `queue1.sh`, `queue1.log`, `boxes_k0.jsonl` | COMPLEX_CRITICAL 2's boxes A, B, C, S at D = 4, 5, 6, 8, 10, 20, 40, 80, both radii, and the D = 4 controls (plant, nometric), with the new default |
