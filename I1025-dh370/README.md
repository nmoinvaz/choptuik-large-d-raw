# I1025-dh370: the l = 1 multiplet's k_c 63 leap from D 18.5 to D 20 and its hybrid scans on dh370 (#1025)

Machine dh370-fedora (Fedora, i7-8700, 12 threads, 31 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025 (the coordinator's #1025-lane order, hc 2026-11-22 ~03:00 UTC).

Task: the leap of xfkappa's k_c 63 states (raw `I1025-mac/d18/sol_l1kc63Wm1025_D18.437500.npy` and `_D18.500000.npy`, record lines `l1kc63Wm1025.jsonl`) from D 18.5 to D 20 at h 0.0625 with winb's flags (the header of raw `I1025-win/leap_kc63.log`: `ell_leap.py l1kc63W1025 1 63 ... --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold`), 6 threads, nice 10, 12 h cap; then the hybrid scans (`I1025-mac/d18/d18_hybsign.py`) at D 19, 19.5 and 20 over lambda 1.40 to 1.80 at 0.01.
Code: worktree `~/Source/choptuik-large-d-1025` at origin/wip/ell1-highD 48c36355 (`solver/matter/ell_leap.py` blob 1eb873e4, the pin of xfkappa's lane); python from `~/Source/choptuik-large-d-1058b/.venv` (multidouble 5.1.0 with `dd_logdet`, hpkernel isa avx2).
The command, quoted before the run (`run1025leap.sh`):

    cd ~/Source/choptuik-large-d-1025/solver/matter && nice -n 10 timeout 43200 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 \
      ~/Source/choptuik-large-d-1058b/.venv/bin/python -u ell_leap.py l1kc63dh370 1 63 \
      <raw>/I1025-mac/d18/sol_l1kc63Wm1025_D18.437500.npy 18.4375 <raw>/I1025-mac/d18/sol_l1kc63Wm1025_D18.500000.npy 18.5 20 0.0625 \
      --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold

`ell_leap.py` writes `data/l1kc63dh370.jsonl` and `data/sol_l1kc63dh370_D<D>.npy` into the worktree's `solver/matter/data/`; `run1025leap.sh` mirrors them into `kc63_leap/` every 5 minutes and at the end.
Files: `kc63_leap/` (records, states, log, `summary_leap.txt`).

Takeover: the leap was started by `choptuik-dh370-me2` (hc t1j, 2026-11-22 03:06 UTC), which hit its usage limit at about 03:52 UTC. The runner session that took over at 06:23 UTC did not touch the leap's processes. Its watcher (`wait1025.sh` fired on the fold-watch line at D 18.625) was not re-read in between; no step failed or ended in that time.
