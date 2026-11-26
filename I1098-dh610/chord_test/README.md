# I1098-dh610/chord_test: release_ls's inner chord steps against fresh Jacobians (#1098)

Machine: dh610 (Fedora 45, i7-12700; oversubscribed at the time). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The runs are D 300's tail h15 (then h17) from fastmul6's D300_mob6 state (I1098-mm5/fix6), on site_y with hp_y2's
form_s.py at e1cd7a84. `c1/` has --inner_chord 1, `c0/` has --inner_chord 0. Each uses 2 threads, side by side
(`../fix/chord_test.sh`).

| run | h15 outer 0's trial | inner steps | Delta after h15 outer 0 |
|---|---|---|---|
| c1 | 1270 s | 7 (chord) | 1.678171015400871496347123798664126021128 |
| c0 | 1427 s | 4 (fresh) | 1.678171015400871496347123798664126021128 |

The Delta values are the same to all 40 printed digits. The chord steps save 11% here. Both runs were stopped in h17
(16:42 UTC).
