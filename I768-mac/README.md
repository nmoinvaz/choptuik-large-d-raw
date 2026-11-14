# I768-mac: Kol's correspondence at D = infinity, Emparan-Suzuki's U(1)-symmetric Ricci flow onto Prop. 5(i) (#768)

Machine: mac (Apple M5, the coordinator's Mac), agent xfchecks. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/768

Code: `solver/inner_pert/kol_map.py` of choptuik-large-d, branch wip/i768 (venv-314, sympy), run from
`solver/inner_pert/`.

- `kol_map.log`: `python3 kol_map.py` (13 checks PASS, exit 0).
- `kol_map_mutate_alpha2.log`, `_nocont.log`, `_gauge2.log`: the three mutations (the scalar term doubled; no
  continuation; the gauge velocity doubled), each exit 1.
- `eqcount.py`, `eqnumbers.txt`: the equation numbers cited, counted from the papers' arXiv TeX sources
  (1905.01062v3, hep-th/0502033v3, the latest versions), as (number, label) pairs. The counter reproduces the numbers
  #429 cited from the papers (Kol (2.4), (2.5); ES (4.2), (4.5), (4.22)). The sources themselves are not stored here.
