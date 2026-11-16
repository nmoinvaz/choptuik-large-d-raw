# I923-dh610: hp on multidouble 4.8.0 and multishoot 3.2.0, the octo Jacobian at two tangents by default, bit-checked

Machine: dh610, Fedora Linux 45, Intel i7-12700 (20 threads, AVX2), 62 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/923
Code: branch `hp/jac-tangents` at d2be15c7 (main 7f88c5bb plus tangents=n, the default of 2 and the released crates),
worktree `/home/nathan/Source/choptuik-large-d-923` with its own venv. References (extracted from the raw repository's
origin/main into `/home/nathan/scratch923/refs`): T81, anm-mac/jets_inputs, and #855's dumps on this machine
(I855-dh610). State for `jac.sh`: #608's `I608-dh610/restart4_d6/anm_pin3_D253.3382.npz`.

Scripts, in order, each started as `systemd-run --user --scope bash <script>` from this folder: `build.sh`,
`tests.sh`, `checks.sh`, `jac.sh`.
