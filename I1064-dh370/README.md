# I1064-dh370: the (a5) control on dh370's machine and build (#1064): leg 14's step 18 base restarted with --base_polish 0 --keep_plan 1 --save_jet 2

Machine dh370-fedora (Fedora, 12 threads, hpkernel isa avx2), issue https://github.com/nmoinvaz/choptuik-large-d/issues/1064 (the coordinator's hc of 2026-11-21 ~19:58 UTC, after dh610's comment 7068400617).

`run1064a5.sh` takes dh610's (a5) command (`I1064-dh610/front_D262.7908/a5_basepolish0/`, raw 94ddff79: leg 14's arguments plus `--base_polish 0 --steps 1 --ks 293 --keep_plan 1 --save_jet 2 --save_base 1`) with `--threads 4`, `nice -n 10`,
from `I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.7908.npz`, code `~/Source/choptuik-large-d-966g/hp` (299728b7: 1aa4a4fb + --reseed_o_bar + the ks_chain --keep_plan option), python and hpkernel from `~/Source/choptuik-large-d-961/.venv` (40f4b4a5 build),
beside the running chain. Its jet is compared (dh610's `jetdiff1064.py`, `jetbits1064.py`, `jetstats1064.py`) with the chain's own `jet_pin3_D262.7908.npz` and with dh610's `jet_a5_basepolish0.npz`.
Results of `run1064a5.sh` (a5_restart/): `summary_a5.txt` (first), `a5_restart.log`, `jetdiff_*.txt`, `jetbits_*.txt`, `jetstats_*.txt`, `row0check_*.txt`, `jet_a5_dh370.npz`.

`run1064a5nb.sh` (the coordinator's second order, hc 2026-11-21 ~20:25 UTC): the same (a5) command with the BLAS variables unset as in the chain's environment, output `a5_noblas/` (`summary_a5.txt`, `a5_noblas.log`, `jet_a5_noblas.npz`, `jetdiff_*`, `jetbits_*`, `jetstats_*`). Reading, fixed before: equal to the in-chain jet to 1e-40 means the BLAS thread setting is the cause; equal to the (a5) of `a5_restart/` bit for bit means the cause is the in-chain state; anything else is reported as found.
