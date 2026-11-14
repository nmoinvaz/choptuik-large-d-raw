# I786-dh610: the rows of the n3>n4 block that carry the re-noded starts' residual

Machine dh610 (Fedora 45, i7-12700; 4 threads beside #608's chains), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/786.

Scripts (written by the coordinator): `uf786.py` (I772-dh610's `uf688.py` with `--rows=BLOCK`) and `run786.sh` (at
#735's `start_080.npz` and `start_092.npz` from origin/main, in #772's build, main a879ccc3).

Criteria, fixed before the run (#786): the rows of n3>n4 with |r| above 1e-60 listed with their field (p, m, a, c, the
block's M-row quarters), grid index, r, u_1 and share of the block's u_1^T r, the shares summing to 1 to 1e-10
relative; r's largest harmonics per field; the control, r set to 1e-36 at the block's row of largest |u_1| alone, lists
that row alone with share 1. #688's controls a and b must stay ok. Each log ends `check: pass`.
