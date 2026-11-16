# I921-dh610: the octo-double Jacobian with several tangents per evaluation (Oun), bits and time at D 253

Machine: dh610, Fedora Linux 45, Intel i7-12700 (20 threads, AVX2), 62 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/921
Code: branch `hp/jac-tangents` at c1f07296 (main plus Solver.jacobian_o / newton_o with tangents=n, against multidouble
PR #55's and multishoot PR #44's branches through [patch.crates-io]), worktree `/home/nathan/Source/choptuik-large-d-921`
with its own venv. State: #608's `I608-dh610/restart4_d6/anm_pin3_D253.3382.npz` (eight parts, stored plan).

Scripts, in order, each started as `systemd-run --user --scope bash <script>` from this folder: `build.sh`,
`tests.sh`, `check.sh`.
