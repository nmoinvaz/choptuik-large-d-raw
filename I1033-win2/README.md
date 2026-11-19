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

## Run 2 stopped, run 3 started separately

`run1033.sh` stopped at run 2 (`cost`, M 320: `ValueError: singular or non-finite pivot at column 642 (NaN)`, a script bug the coordinator will fix; run 2 is not rerun, `cost.jsonl` has M 128 to 256 only). On the coordinator's hc, run 3 alone was started by `run1033_run3.sh` (the run 3 block of `run1033.sh`, the python started directly so the 3 h cap kills its own pid; the report takes `--cost cost.jsonl`, so M 320 and 384 have no cost row). The header of `run1033_run3.sh` says the hc came "~18:40 UTC", a hand-typed guess that is wrong; the launch time is in `exits_1033.txt`.

`run1033_run3.sh` recorded `run3.winpid` 33892, its own forked bash stub and not the python, so its cap check (which wants `tau_map_gain.py ... solve` in the command line) would have killed nothing. The running job was left alone and `gate1033r3.sh` (glue) holds the 3 h cap: it kills the tree of pid 32080 (the venv launcher stub of the solve, child 30900 the main python) at 21:37:05 UTC after checking the command line. If it fires, `exits_1033.txt` says so, and the script's own line `capped 0` is wrong in that case.

## Run 3 stopped for memory, to be rerun from scratch

At 18:53 UTC the coordinator ordered run 3 stopped (win2 at 4.2 GB available and commit 94.6 of 101.5 GB, #1031's rustc 32.9 GB and #1003's K 49 22.3 GB; the M 384 solve would have taken the rest, and #1003 cannot resume). Stopped by hand 3 min after start of its first Newton call: script shells, the python tree by exact pid 32080 (child 30900), and `gate1033r3.sh`. It had written no result (`solve_D3.0475.jsonl` does not exist). Its start checkpoint (|F| 2.25e-22 on 2317 steps, written 18:37 UTC) is kept in `stopped_run3_1854/` so that the rerun starts from scratch. The rerun, then the cost steps, wait for win2-build to report #1031's build finished (about 21:40 UTC).

## The rerun starts at 32e5825d, not 080acfa2 or f53fb5bf (2026-11-19 21:30 UTC)

The coordinator's comment 7022166701 on #1033 (the bot reviews' fixes: checkpoint and result file names carry the map centre s0, checkpoints are bound to their configuration, and `report` fails a failed size or a non-converged identity solve) moves the rerun to `perf/tau-map-lowd` at 32e5825d (the worktree D:/choptuik-i1033 is detached there; the branch was force-updated, origin was f53fb5bf). Nothing of run 3 or the cost steps had started at an older head after the stop above, so nothing is stopped by this. `run1033_v2.sh` (glue, with `rootpid1033.ps1`) runs, in this order, all caps by the exact pid of each command's root python (checked by its command line, no retry):

1. run 0: `selftest` exit 0 and its eight controls (lo parity dps40 inverse gp phase_gp lenient unbound) exit 1 (the first run 0, at 080acfa2, had five controls and passed);
2. run 3, D 3.0475: `solve A_M384 --pairs 1:384,0.4:192,0.5:192`, 3 h cap (exit 0 or 1 goes on, since a map that did not converge is a result);
3. the cost steps into `cost2.jsonl`: M 320 and 384 (cap 1.5 h), the `--mutate plan_m` control (exit 1, no record, cap 10 min), then D 3.7 M 128 to 256 and D 3.0475 M 256 (cap 45 min);
4. run 3's `report` with `--cost cost2.jsonl` (`report_D3.0475.json`).

Run 1 (D 3.7: `check37.jsonl`, `solve37.jsonl`, `report37.json`) and the first run 0 ran at 080acfa2 and are not repeated. `cost.jsonl` (M 128 to 256, from run 2 at 080acfa2) is superseded: `Solver.step_timing()` has held only the LU fill, a copy, in its Jacobian entry since #523, so its seconds per step are not the Newton call's. It stays as it is.
