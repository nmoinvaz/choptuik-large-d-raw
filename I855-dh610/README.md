# I855-dh610: hp on multidouble 4.5.0, multishoot 3.0.0 and multisolver 0.1.0, built and bit-checked on dh610

Machine: dh610, Fedora Linux 45, Intel i7-12700 (20 threads, AVX2), 62 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/855
Code: branch `hp/multishoot-3` at 7e4cfd03, worktree `/home/nathan/Source/choptuik-large-d-855` with its own venv.
References (extracted from the raw repository's origin/main into `/home/nathan/scratch855/refs`, the clone left as it is):
T81 (`ref`, `scaled`), anm-mac/jets_inputs (`jets`), I523-mac/c3 and I614-dh370 (`xsolve_bits`, `api_bits`, the chain step).

Scripts, in order, each started as `systemd-run --user --scope bash <script>` from this folder: `build.sh`,
`tests.sh`, `checks.sh`, `pivots.sh` (the worktree moved to branch hp/clu-pivots, multidouble 4.6.0's clu_pivots in
modecount_cx, which is rebuilt and checked again), then `timing.sh` once #608's chains have ended.
