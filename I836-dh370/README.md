# I836-dh370: #608's d6 attempt from D 252.6966 at a = 0.0888, rerun with --od_full_drop 1e-2

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/836.

`run836.sh` (written by the coordinator, md5 2680d94c, run unedited by absolute path under user unit `i836`): one step (`--steps 1`)
from `I608-dh610/restart2_d6/anm_pin3_D252.6966.npz` at a = 0.08881784197001252 with #608's restart flags (`--od_accept natural
--od_strong 4 --reseed_start pred`) plus `--od_full_drop 1e-2`; worktree choptuik-large-d-808b at main bd4ada6c, venv-i800.
Output: `drop.log`, `drop/` (the base polish and the predicted state), `exits_836.txt`.

## Results (dh370, 2026-11-15)

Unit `i836`, 10:33:40 to 11:32:42 UTC, exit 0 (`exits_836.txt`, `i836_journal.log`). The base polish converged (max|F| 4.0e-66, Delta
1.68452122064150389 at D 252.696647702, 1 step); the attempt at a = 0.08881784197001252 was accepted at its first try (re-seed ok,
62.6 s) and converged to pinned max|F| 2.2e-62 in 9 octo-double steps, at D 252.78546554377826 (`drop/anm_pin3_D252.7855.npz`,
`drop/anm_run.jsonl`), Delta 1.684507117077615500139346659922563778816 (the eight parts summed exactly).

Iterations: step 1's lam 1 trial was refused by the own test (max|F| 1.02e-30, ratio 1.69) and lam 1/2 accepted (7.6e-47); step 2
accepted at lam 1 (2.55e-31); step 3, where #608's side A was refused, accepted by the full-step drop at lam 1 (max|F| 2.55e-31 to
4.84e-34, 1.9e-3 of the start, ratio 522, so `--od_full_drop 1e-6` would have refused it); steps 4 to 7 accepted by the own test
(ratios 1.3e-5, 1.5e-3, 1.6e-9, 1.9e-15), max|F| 4.85e-34, 1.34e-39, 1.83e-45, 2.22e-62. The first correction moved Delta by -1.69e-17,
and the state's Delta moved 1.69e-17 in all.
