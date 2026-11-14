# I794-win2: the series at D 259.52 and 259.57, nearest the real-axis singularity near 259.95

Machine win2 (desktop-pc, 20 threads; 8 beside #603 and #783), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/794.

Scripts (written by the coordinator): `run794.sh` (#776's series command at #603's chain_nsr states D 259.5183 and
259.5702, in the worktree D:/choptuik-i709 at main 3e096e26 with venv-i600, #603's own build), `repro_check794.py`
(#776's check of the series against #603's records, and its control), `report794.py` (bars 2 and 3 on Delta's series,
and the control `--mutate=shiftP`), and `singularity_type.py` of origin/main (#782's estimators, its plants first).

Criteria, fixed before any series was read (#794): (1) each series equals #603's record in all 25 norms and both pivots,
and the control differs (`repro_check794_control.txt` ends `exit 0`); (2) Delta's root test within 5% of |259.95 - D0|;
(3) Delta's nearest stable Pade pole has |Im D*| <= 0.1 and |Re D* - 259.95| <= 0.2 (`report794.txt` ends `exit 0`, and
`report794_shiftP.txt` ends `exit 0`, bar 3 failing at every base with P moved by 1.0); (4) the Dlog estimate of mu on
Delta and on the 24 rows, with its spread and band, reported without a bar (`type794.txt`).
