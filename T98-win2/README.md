# T98-win2: the hp double-double kernel built on win2 (Core Ultra 7 265K), its bit-identity and control checks

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores: 8 P + 12 E, no SMT; AVX2, no AVX-512; 95.6 GB RAM; on AC). Below-normal priority, run beside the J 1500 hedge pair (nothing of T98 is on the hedge's memory guard).
Comms entry: 2026-11-02 10:22 UTC cloud to win2.
Toolchain: cargo 1.96.0, rustc 1.96.0 (host x86_64-pc-windows-msvc, LLVM 22.1.2). venv-hp: Python 3.12.8, numpy 2.5.4, scipy 1.18.1, maturin 1.16.0.
Worktree: `git worktree --detach` at origin/main 0f0e20c (`..\choptuik-t98`); the amp checkout is left alone (the J 1500 runs still import from it). multidouble commit 00c6dfd89a432cc15c4efc56060fbb30f5518ab1 (release tag 1.8.0), from hp/pyproject.toml.

hp_build/ holds each command's log (`> file 2>&1`, pushed at each post):
- build.log (step 1); cargo_test.log (step 2); controls.log, block.log, converge.log (step 3);
- ref_vs_win.log, ref_vs_mac.log, ref_save.log (step 4); scaled_vs_mac.log (step 5); profile_M320_t4.log, profile_M320_t8.log (step 6).
Artifacts: ref_win2.json (step 4, the kernel's outputs at the seven resolutions), profile_M320.jsonl (step 6).
