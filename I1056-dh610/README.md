# I1056-dh610: bit check of PR #1056 (hp on multishoot 4.1.0, multidouble 5.1.0 and multisolver 0.2.2) against the venv-i1050 build and the stored references

Machine: dh610 (Fedora 45, i7-12700, 20 threads, 62 GB), runner session claude-me2. PR: https://github.com/nmoinvaz/choptuik-large-d/pull/1056 (branch `chore/multishoot-4.1.0`, head e208e136; the coordinator's first message named 8e7aa415, its amendment names e208e136).
Queued by the coordinator after PR #1054's D 251.88 pair. Nothing here is started until that pair has ended and is posted.

What the PR changes in `hp/` (1c02b15b to e208e136): `Cargo.toml`, `Cargo.lock` (multishoot 4.0.0 to 4.1.0, multidouble 5.0.0 to 5.1.0, multisolver 0.2.1 to 0.2.2), the `fastmul_bench` and `modecount_cx` manifests and lock, `pyproject.toml`
(multidouble's Python package from commit 482c6835, tag 4.8.2, to 8c4360ac, release 5.1.0) and `border_cost.py` (a script, from main's #1049). No `hp/src`.
The reference build is `~/Source/venv-i1050` (worktree `~/Source/choptuik-large-d-1050` at 1c02b15b, multidouble 5.0.0 / multishoot 4.0.0 / multisolver 0.2.1, Python package at 482c6835). Main 08699de5 has the same `hp/src` and Cargo pins; `run1056.sh` checks that first
(`git diff --stat 1c02b15b 08699de5 -- hp/src hp/Cargo.toml hp/Cargo.lock` must be empty; its control, the same diff to e208e136 over the two Cargo files, must not be).

Steps (the coordinator's, in order; `run1056.sh`, one at a time at nice 10, each under timeout, from `hp/` of the worktree `~/Source/choptuik-large-d-1056`, `OMP_NUM_THREADS=1`):
1. a worktree at e208e136, a new venv `~/Source/venv-i1056` (uv, Python 3.14), `PIP_NO_CACHE_DIR=1 python -m pip uninstall -y multidouble`, `hp/build.sh` (with `PIP_NO_CACHE_DIR=1`; the unit's memory peak is read from systemd right after the build;
   est. 26-50 min, 24-29 GB), then pip's `direct_url.json` of multidouble in venv-i1056 (and in venv-i1050), which must name 8c4360ac;
2. with venv-i1050's python: `highm_check.py ref --save=REF.json --Ms=48,64,80`, `scaled --save=SC.json`, `jets --save=JETS.json` (the last also writes `JETS_inputs.npz`);
3. with venv-i1056's python: the same three with `--compare=` against those files, and `jets --compare=JETS.json --mutate=kappa` (must fail, exit 1);
4. with venv-i1056's python against the stored references: `ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80`, `scaled --compare=$RAW/T81/scaled_main.json`, `jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json`; added (not asked): the same jets compare with `--mutate=kappa`,
   so that the stored-inputs path has a control that can fail;
5. the Python helpers (`od_axpy`, `od_add_dd` of the multidouble package, which `highm_check` does not reach): `octo_corrector.py planted $RAW T129-win2/chain/anm_pin3_D180.5246.npz --threads 10 --accept natural --qd 0` (#1052's K1 command) with venv-i1050, then venv-i1056
   (est. 4 min each), compared by `cmp_planted.py` (every line equal except the wall seconds: every per-step max|F|, |dz|, dDelta, pivot and the final Delta; its `--mutate` control must exit 1), plus the final states' eight parts bit for bit (added);
   and the same on venv-i1056 with `--mutate_offset qd`, which must exit 1.
Pass: 0 differing rows in every compare, every kappa control fails, pip's direct_url names 8c4360ac, the planted logs are equal, and `--mutate_offset qd` exits 1. `exits_1056.txt` and `summary_1056.txt` hold the exits, walls and row counts.

## Files

| file | what |
|---|---|
| `common1056.sh`, `run1056.sh`, `cmp_planted.py`, `compare1050.py` | paths, the driver, the planted-log comparator with its control, a copy of the row comparator (not used by the driver) |
| `exits_1056.txt`, `summary_1056.txt`, `memlog_1056.log` | exits with times, the one-line result of every step, the alert-only memory log (no alert) |
| `build1056.log`, `venv.log`, `build` facts in the summary | the build (1555 s, unit memory peak 27 678 MiB), the pip direct_url of both venvs (8c4360ac in venv-i1056, 482c6835 in venv-i1050) |
| `REF.json`, `SC.json`, `JETS.json`, `JETS_inputs.npz` | the references saved with venv-i1050 |
| `save_*.log`, `cmp_*.log`, `stored_*.log` | the highm_check runs (steps 2, 3 and 4) |
| `planted_i1050.*`, `planted_i1056.*`, `planted_i1056_mut_offset_qd.*` | step 5's octo_corrector.py planted runs (log, json, final state npz) |
| `cmp_planted.txt`, `cmp_planted_control.txt`, `cmp_planted_offset.txt`, `cmp_planted_npz.txt` | the comparisons: venv-i1050 against venv-i1056 (identical), the comparator's `--mutate` control (differs), the offset-qd run against the base (differs, as it must), the final states bit for bit |

## Results (17:32 UTC, 20 Nov)

Every step passes: exits as expected, 0 differing rows in every compare, both kappa controls fail, pip's direct_url names 8c4360ac, the planted logs equal in every printed digit (and the final states bit for bit), `--mutate_offset qd` exits 1.
The unit ran 16:14:25 to 17:30:08 UTC (1 h 15 min, 4 h 30 min CPU), journal memory peak 27 GB, no memory alert.
