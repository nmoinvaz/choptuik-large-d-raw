# I482-win2: x86-64 check of the D 30 determinant cache (platform or code)

Machine win2 (Windows x86-64, Intel Core Ultra 7 265K, no AVX-512), issue https://github.com/nmoinvaz/choptuik-large-d/issues/482 (a check for #442, #250's check 4).
Checkout `D:\choptuik-i482`, a worktree detached at main e043be2; venv-t126 (Python 3.12.8); one thread, below-normal priority, beside #461's crawlJ.
Results follow in this README, with `fresh_vs_cache.log` / `.json` and the `--mutate=swap` control `fresh_vs_cache_mutate_swap.log` / `.json`.

## Result (2026-11-11 02:53 to 02:54 UTC): "code"

Build (`cd hp && bash modecount_build.sh`, venv-t126 active, `CARGO_BUILD_JOBS=1`, `nice -n 10`, 2 min 17 s, offline) printed
`modecount_cx ok D:\choptuik-i482\hp\modecount_cx\build\modecount_cx.cp312-win_amd64.pyd` (`-C target-cpu=native` on this CPU, which has AVX2 and no AVX-512).
The check (`fresh_vs_cache.py`, one thread, below-normal priority, 32 s) exited 1: it prints its two differences, both above its own tolerance of 1e-8. The control with
`--mutate=swap` exited 1 as it must (differences 24.66 in ln|det| and 2.73 in arg). `exits.txt` has the exits and times.

| point (re, im) | quantity | win2 (fresh) | macm3 (fresh) | October's cache | win2 - macm3 | win2 - October |
|---|---|---|---|---|---|---|
| 4.267, 0.9740000000000001 | ln\|det\| | -940.4586634376807 | -940.4586634376807 | -940.4586634457893 | 0 | +8.1086e-9 |
| 4.267, 0.9740000000000001 | arg | -0.0488120116698596 | | -0.04881201953426029 | | +7.8644e-9 |
| 3.94364216362105, 1.1900607986722187 | ln\|det\| | -965.1149263918375 | -965.1149263918375 | -965.1149263751369 | 0 | -1.67006e-8 |
| 3.94364216362105, 1.1900607986722187 | arg | -2.782800043880229 | | -2.782799989380578 | | -5.4500e-8 |

Verdict by the issue's definitions: "platform" would be win2 within 1e-12 of the cache (it is 8.1e-9 and 1.7e-8 away); "code" is win2 within 1e-12 of macm3 (it is equal to macm3 in every printed digit,
difference 0 at both points). **Verdict: code.** x86-64 with AVX2 on Windows and arm64 NEON on macOS give the same ln|det| to the last digit, and both differ from October's cache by the same 8.1e-9 and 1.7e-8.
The macm3 arg values were not in the issue, so the arg columns are compared with October's only.

Files: `fresh_vs_cache.log` / `.json`, `fresh_vs_cache_mutate_swap.log` / `.json`, `exits.txt`.
