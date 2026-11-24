# I1078-win2: gamma at D 3.044375 from the roots of the matched mode determinant D_m (#1083), win2 runs

Machine: win2 (desktop-pc), Windows 11, Core Ultra 7 265K, 20 threads, 95 GB; at most 6 threads of this task, BelowNormal.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1078 (method: #1083, notes/MODE_HORIZON.md).

Code: worktree D:\choptuik-i1078dm, branch wip/i1078-dm from origin/wip/mode-horizon-1083 7c6177e1 (hp kernel sources
equal to main 68b563f9's). Venv C:\Users\nathan\Source\venv-i1078 (new, python -m venv, requirements.txt pins).

Order of the work:
1. build hp (hp/build.sh, fat LTO default, CARGO_BUILD_JOBS=6, multidouble's Python package uninstalled first):
   run_build.sh, build.log, build.times, versions.txt, mem.log.
2. build check: mode_matched.py toy and toy --mutate=shift; four at M' 96 against raw I1083-dh370/four.jsonl.
3. D_m scan in lambda at M' 96, sign changes refined with mode_matched.py root.
4. the same at M' 128 and 160 (HP_DENSE_M_MAX=160), one root at hmax 0.001.
