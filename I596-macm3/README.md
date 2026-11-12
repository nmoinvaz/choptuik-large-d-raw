# I596-macm3: the root search at D 55.04 and M 64 on the exact determinant of the double-double matrix (gamma_dd.py --ball=320), five brackets

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314. Code: the git worktree ~/Source/choptuik-large-d-b596 at main 742bb879 (hp/gamma_dd.py with --ball), the modecount_cx built there on 2026-11-12 12:53 UTC with hp/modecount_build.sh (1 min 34 s, build.log; hp/modecount_cx and hp/src unchanged since ecca9c53), the Python hpkernel of 2026-11-09. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/596 (recommended by macm3 in #590's closing summary; the coordinator's message of 2026-11-12 12:44 UTC).

Runs (common.sh run(), chainA.sh and chainB.sh, one thread per run, two at a time, nice 10, caffeinate -is): #590's seven commands with --ball=320 added: python3 -u hp/gamma_dd.py <raw>/gamma_D55_NAME.jsonl hp/data/states/up10_D55.0351.npz --threads=1 --polish=4 --Mhi=64 --kf48=33 --bracket=A,B --xtol=1e-16 --ball=320 (state sha256 945714e9bda3700d...), brackets b1 to b5, b1r (must equal b1 bit for bit) and none (no sign change, lam null). Chain A: b1, b3, b5; chain B: b2, b4, b1r, none.

Written before the run (the issue's). Controls: b1r = b1 bit for bit and none gives lam null. The spread of lambda(64) over b1 to b5 beside #590's 1.345e-9: the verdict is "the LU's noise" if it is below 1e-11, otherwise both are reported. lambda(32) on the exact determinant against #590's double-double lambda(32) (2.047684127712392 to 2.0476841277123925): they must agree within #590's lambda(32) spread (4.4e-16) or the difference is reported.

## Results


(2026-11-12 15:17 UTC, macm3) All seven runs finished (exits.txt), the last at 15:16:45 UTC (started 12:54:17 UTC; M 32 141 to 164 s, M 64 2087 to 3186 s per run on the exact determinant, about 117 s per ball determinant). Every one exits 1, bracketed or not, for the M 64 floor check ABOVE (est -1.2075e-15), as in #590 and #470; none is told apart by lam null (n_signchanges 0).
| bracket | λ(32) | λ(64) | n_det (M 32) | M 64 floor check (est) | exit | #590 double-double λ(64) |
|---|---|---|---|---|---|---|
| b1 | 2.047684127712392 | 2.047684128675301 | 6 | ABOVE (-1.208e-15) | 1 | 2.0476841275012796 |
| b2 | 2.047684127712392 | 2.0476841274458297 | 7 | ABOVE (-1.208e-15) | 1 | 2.0476841280061455 |
| b3 | 2.0476841277123925 | 2.0476841275291844 | 7 | ABOVE (-1.208e-15) | 1 | 2.047684127567935 |
| b4 | 2.047684127712392 | 2.047684127440434 | 6 | ABOVE (-1.208e-15) | 1 | 2.0476841269633494 |
| b5 | 2.047684127712392 | 2.047684127195844 | 6 | ABOVE (-1.208e-15) | 1 | 2.0476841283086755 |
| b1r | 2.047684127712392 | 2.047684128675301 | 6 | ABOVE (-1.208e-15) | 1 | 2.0476841275012796 |
| none | None | None | 2 | - | 1 | - |

Spread over b1 to b5 on the exact determinant: λ(32) 4.441e-16 (min 2.047684127712392, max 2.0476841277123925); λ(64) 1.479e-09 (min 2.047684127195844, max 2.047684128675301). #590 (double-double LU): λ(32) 4.441e-16, λ(64) 1.345e-09.
λ(32) exact against #590's double-double: differences ['+0.00e+00', '+0.00e+00', '+0.00e+00', '+0.00e+00', '+0.00e+00'].
λ(64) exact minus the DD value, per bracket: ['+1.174e-09', '-5.603e-10', '-3.875e-11', '+4.771e-10', '-1.113e-09']; mean of exact λ(64) 2.0476841276573188, DD mean 2.047684127669477.
Control b1r vs b1: λ(32) bit for bit equal, λ(64) bit for bit equal. Control none: exit 1, lam None, n_signchanges 0.
seconds M32/M64: [(141, 2272), (159, 2740), (164, 3071), (144, 3186), (147, 2087)]

Verdict (the issue's): the spread of lambda(64) over b1 to b5 on the exact determinant is 1.479e-9, not below 1e-11, so it is NOT the double-double LU's noise; both are reported: 1.479e-9 (exact, this task) beside 1.345e-9 (double-double LU, #590). lambda(32) on the exact determinant equals #590's in all five brackets (difference 0 to the last bit), within #590's lambda(32) spread of 4.4e-16. Controls: b1r equals b1 in lambda(32) and lambda(64) bit for bit; none exits 1 with lam null.
