# I792-dh610: the series at D 259.55 and 259.59, nearest the real-axis singularity near 259.95

Machine dh610 (Fedora 45, i7-12700; 4 threads beside #608's chains), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/792.

Scripts (written by the coordinator): `run792.sh` (#776's series command at #603's chain_nsr states D 259.5502 and
259.5901, in dh610's main checkout a879ccc3 and .venv; the bases and #603's records from origin/main), `repro_check792.py`
(#776's check of the series against #603's records, and its control), `report792.py` (bars 2 and 3 on Delta's series,
and the control `--mutate=shiftP`), and `singularity_type.py` of origin/main (#782's estimators, its plants first).

Criteria, fixed before any series was read (#792): (1) each series equals #603's record in all 25 norms and both pivots,
and the control differs (`repro_check792_control.txt` ends `exit 0`); (2) Delta's root test within 5% of |259.95 - D0|;
(3) Delta's nearest stable Pade pole has |Im D*| <= 0.1 and |Re D* - 259.95| <= 0.2 (`report792.txt` ends `exit 0`, and
`report792_shiftP.txt` ends `exit 0`, bar 3 failing at every base with P moved by 1.0); (4) the Dlog estimate of mu on
Delta and on the 24 rows, with its spread and band, reported without a bar (`type792.txt`).
