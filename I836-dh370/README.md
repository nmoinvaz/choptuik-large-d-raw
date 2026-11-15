# I836-dh370: #608's d6 attempt from D 252.6966 at a = 0.0888, rerun with --od_full_drop 1e-2

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/836.

`run836.sh` (written by the coordinator, md5 2680d94c, run unedited by absolute path under user unit `i836`): one step (`--steps 1`)
from `I608-dh610/restart2_d6/anm_pin3_D252.6966.npz` at a = 0.08881784197001252 with #608's restart flags (`--od_accept natural
--od_strong 4 --reseed_start pred`) plus `--od_full_drop 1e-2`; worktree choptuik-large-d-808b at main bd4ada6c, venv-i800.
Output: `drop.log`, `drop/` (the base polish and the predicted state), `exits_836.txt`.
