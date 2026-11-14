# I772-dh610: #688's u_1^T r by residual block at #735's 0.80 and 0.92 starts

Machine dh610 (Fedora 45, i7-12700, 20 threads; 4 used beside #608's chains), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/772.

Scripts (written by the coordinator): `uf688.py` (I688-dh370's, with hp/ taken from the environment variable HP688,
here dh610's main checkout at a879ccc3 and its .venv, a build after #523), and `run772.sh` (the two starts
`I735-dh370/start/start_080.npz` and `start_092.npz`, taken from origin/main, then `--mutate=shift` at 0.80).

Prediction, written first (#772): u_1^T r is carried by the n3>n4 and horizon>n4 blocks, 0.5 each, and sets the first
step. Bars: the pinned first step within 1% of the base polish's first |dz| (2.52e-01 at 0.80, 1.03e-01 at 0.92, #735);
the route -sigma_1 v_1^T dz_pinned equal to the block sum to 1e-3 (control a); a planted r + beta u_1 returns beta to
1e-10 (control b); `--mutate=shift` fails control a. A failed prediction is reported as failed.
