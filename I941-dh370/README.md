# I941-dh370: near_null.py on the order-240, 160 and 135 states at D 229 to 234, with the planted check and its controls

Machine dh370 (Fedora 45, i7-8700, 12 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/941

`run941.sh` (stages `ctl`, `data`, `extra`, `extra2`; units `i941a` to `i941d`; nice 10, three runs of 4 threads at a time): worktree
`~/Source/choptuik-large-d-935` at main 808b1fac, its 4.8.2 `.venv` (multidouble Python package 482c6835),
`hp/near_null.py RAW STATE --k=6 --its=16 --threads=4 --json=NAME.json`, each state on its stored plan (`plan: stored` in every JSON).
Seventeen runs, all exit 0 except the two controls that must fail (`exits_941.txt`), 326 to 527 s each, 0.18 GB.

| names | state | why |
|---|---|---|
| `ctl_planted`, `ctl_planted_mut`, `ctl_sigma_mut` | order 160, D 230 | `--planted=1` (exit 0), `--planted=1 --mutate=scale_block` (exit 1), `--mutate=sigma` (exit 1) |
| `o240_D229.0509`, `_D229.9822`, `_D230.9281`, `_D231.7466` | `I903-win2/ks_chain/leg07_D222.0000_ks240/` | ordered |
| `o160_D229.0000`, `_D230.0000`, `_D231.0000` | `I903-dh610/chain_k160/` | ordered |
| `o135_D230.1312` | `I903-macm3/chain_k135/` | ordered control |
| `o240_D232.0000`, `o135_D229.1312`, `o135_D231.1312` | same chains | added: the order-240 chain's last state, and two more order-135 states (one state gives no fall per unit D) |
| `o160_D232.0000`, `_D233.0000`, `_D234.0000` | `I903-dh610/chain_k160/` | added: the same D as the order-240 chain's last state, and the stall region |

## Analysis

- `analyze941.py FOLDER` prints the six vectors per state, the table of sigma_Delta, sigma_pair and sigma_5 with their ratios, the falls
  per unit D, the order test and the order-135 control (`analysis941.log`). `--selftest` (`selftest941.log`, exit 0) and
  `--selftest --mutate` (`selftest941_mutate.log`, exit 1, swaps the expected sigma_Delta and sigma_pair) check its classification and
  arithmetic on planted records.
- `samebranch941.py RAW` (`samebranch941.log`, exit 0; `--mutate` adds 1e-9 to the order-240 Delta, `samebranch941_mutate.log`, exit 1):
  Delta of the order-240 states against the order-160 chain's Delta(D), within 10 times the order-135 against order-160 difference.

## What the numbers say (`analysis941.log`)

| order | sigma_Delta fall per unit D | sigma_pair fall per unit D | sigma_Delta / sigma_pair |
|---|---|---|---|
| 240 (D 229.05 to 232.0) | 1.51 (log slope 0.412, 0.410, 0.407, 0.405) | 0.997 (flat, 2.9e-10) | 6.1e-5 to 1.8e-5 |
| 160 (D 229 to 234) | 14.9, 13.4, 12.9, 20.7, 19.4 | 15.2 to 15.4, every step | 219 to 304 then 176 |
| 135 (D 229.13 to 231.13) | 1.46, 3.14 | 1.96, 1.99 | 255, 344, 217 |

The order test (order-240 sigma_Delta within 3 times of order 160's at the same D): 1.7 at D 229.05, 14.5 at 229.98, 115 at 230.93, and
1152 at D 232.0 where both chains have a state. The two chains are on the same branch (Delta agrees to 4e-12 to 6e-12).
The harmonic-3 pair is vectors 1 and 2 at orders 160 and 135 and vectors 3 and 4 at order 240 (p1 and m_h at k 3, 0.127 and 0.092);
the Delta mode is vector 3 at orders 160 and 135 (Delta share 0.75 to 0.84) and vector 1 at order 240 (0.88 to 0.91).
sigma_5 and sigma_6 are not converged at order 240 and 135 (relative change over the last two iterations 0.05 to 2), so ratios to sigma_5
are order-of-magnitude only.
