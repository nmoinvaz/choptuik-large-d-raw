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

## Files

- `run_build.sh` (launched by `run_build.cmd` through WMI at BelowNormal): venv, `hp/build.sh`; `build.log`, `build.times`,
  `versions.txt` (hpkernel import, crates, .pyd sha256, pip list), `mem.log` (free RAM and rustc working set every 2 min),
  `exits_1078.txt`.
- `chain1078.py` (launched by `run_chain.cmd`): every later step, each as `<step>.log`, one line per step in
  `steps_1078.txt`, exit codes in `exit_codes.txt`; `four.jsonl` and `four_compare.txt` (against raw I1083-dh370/four.jsonl);
  `scan_m96.jsonl` (the D_m scan); `4_root_*`/`5_root_*` (bracket roots, `hp/mode_matched_bracket.py`); `scan_<tag>.jsonl`,
  `root_<tag>.jsonl` (M' 128, M' 160, hmax 0.001).
- `push1078.sh`: copies this folder into the push worktree D:\choptuik-raw-i1078p and pushes from there.

## Status

- Build: exit 0, 17:35:49 to 22:25:29 UTC 24 Nov (17388 s), fat LTO, 6 jobs, BelowNormal; rustc peak working set
  36.1 GB (2-min samples), free RAM never below 3.88 GB. hpkernel avx2, multidouble avx2 (Python package 8c4360ac),
  crates multidouble 5.1.0, multishoot 4.1.0, multisolver 0.2.2; `_hpkernel.cp314-win_amd64.pyd` sha256 900de2be...
- Checks: `toy` exit 0, `toy --mutate=shift` exit 1, `mode_matched_bracket.py selftest` exit 0 and `--mutate=shift` exit 1.
- `four` at M' 96: exit 0 (line residual 4.4e-13, pivot ratio 5.2e-8), about 295 s per determinant at 6 threads; sign,
  ln|D_m|, pmin and pmax bit-identical to dh370's four.jsonl at all four rates (`four_compare.txt`).
