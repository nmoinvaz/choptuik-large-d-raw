# I911-dh610: hp on multishoot 3.1.0, multidouble 4.7.0 and multisolver 0.1.1, built and bit-checked on dh610

Machine: dh610, Fedora Linux 45, Intel i7-12700 (20 threads, AVX2), 62 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/911
Code: branch `hp/order-by-order` at 0cf9b94a: main plus the bump of hp's and modecount_cx's Cargo.toml and
Cargo.lock (9c2b0840, 7c850c6a) and #914's order-by-order code, which no existing path calls. The first build, at
9c2b0840, failed `hp/modecount_build.sh` on modecount_cx's old pins. Worktree
`/home/nathan/Source/choptuik-large-d-911` with its own venv.
References (extracted from the raw repository's origin/main into `/home/nathan/scratch911/refs`): T81 (`ref`,
`scaled`), anm-mac/jets_inputs (`jets`), and #855's dumps on this machine (I855-dh610: multishoot 3.0.0, multidouble
4.6.0, multisolver 0.1.0) for `xsolve_bits` and `api_bits`.

Scripts, in order, each started as `systemd-run --user --scope bash <script>` from this folder: `build.sh`,
`tests.sh`, `checks.sh`.
