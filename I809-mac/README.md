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
