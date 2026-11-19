# I1033-win2: the tau-mapped grid at low D, measured (hp/tau_map_gain.py)

win2, https://github.com/nmoinvaz/choptuik-large-d/issues/1033

Runs 0-3 of notes/LOW_D_SPEEDUP.md, "Step 5, the measurement", "Runs" (coordinator, 2026-11-19), 8 threads at BelowNormal priority beside #1003.

- Code: worktree D:/choptuik-i1033, branch perf/tau-map-lowd (draft PR #1037) at 080acfa2, run from its hp/.
- hpkernel (read-only, the existing low-D venv, not rebuilt): `hpkernel.__file__` = C:\Users\nathan\Source\venv-i600\Lib\site-packages\hpkernel\__init__.py
  built as hpkernel-0.1.0 from main fc697f3a (fat LTO, worktree D:/choptuik-i600, #600; wheel D:/choptuik-i600/hp/dist/hpkernel-0.1.0-cp314-cp314-win_amd64.whl), `_hpkernel` .pyd sha256 4ede9afec7ffb40e93c321270ddc9614d644473e1b74834e9406a98f7571f90d
- Python 3.14.10 (venv-i600): numpy 2.5.4, mpmath 1.3.0, scipy 1.18.1, multidouble (Python package) 0.1.0.
- Inputs: RAW/T82-win/states (D 3.0475), RAW/T100-win2/states (D 3.044375), hp/data/lowD_states/highm15_D3.7000_M*.npz (D 3.7).
- Differences from the note: python of that venv for python3, no nice (priority set at launch), D:/ paths, output in run1033.log and exit codes in exits_1033.txt (launcher run1033.sh, glue only).
- Run 3 solve capped at 3 h by exact pid; no run 4 (the coordinator decides).

Files: check37.jsonl, solve37.jsonl, report37.json (run 1); cost.jsonl (run 2); solve_D3.0475.jsonl, report_D3.0475.json (run 3); states/ (per-call checkpoints).
