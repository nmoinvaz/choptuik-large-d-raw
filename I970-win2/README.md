# I970-win2: ks_chain2's step from D 238.1789 at a 0.4657 with --reseed_qd_bar 1e-21, on win2's #962 build

Machine: win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session beside win2b's #903 chain and #945's leg.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/970 (coordinator `nathans-macbook-air-m5-3/t5`).

| | |
|---|---|
| code | worktree `D:\choptuik-i962` of choptuik-large-d, detached at origin/main 290e9d04 (Python only since the 40f4b4a5 build: `git diff 40f4b4a5 290e9d04 -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml` is empty) |
| kernel | venv `C:\Users\nathan\Source\venv-i962`, hpkernel from the #962 build (multidouble 4.9.0, multishoot 3.3.0, `isa avx2 avx2`), Python package multidouble 482c6835 |
| input | `I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D238.1789.npz` of this raw worktree, sha256 f638ad4d6eca0c554f06440d... identical to the live chain folder's |
| run | `run970.sh`: `anm_run.py` with run903e.sh's flags at `--threads 4`, `--ks 291 --keep_plan 0 --D_max 242 --steps 1 --a0 0.4657 --reseed_qd_bar 1e-21`, BelowNormal, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=4` |
| output | `bar21/` (anm_run.log, anm_run.jsonl, states), `bar21.log` (stdout), `exits_970.txt` |
