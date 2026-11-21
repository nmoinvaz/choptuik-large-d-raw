# I1025-win/d18ref120: the full dd M's sign at lambda 1.20 on D 18's and D 18.0625's states, k_c 63 (winb)

Written before the run, 2026-11-21 16:20 UTC by my clock (substituted from `date -u` when pushed).

## Order

The coordinator (hc, about 16:10 UTC), after the D 18.125 scan: xfkappa's sign-convention check (#1025 comment 7065503193) finds no global flip. But the hybrid's sign at the reference lambda 1.20 flips between D 18 and D 18.0625, read as a root crossing 1.20 unless the hybrid is wrong there. Test it with the full dd M: `ell_ddm.py det` at lambda 1.20 on D 18's state (`I1025-win/out/sol_l1kc63W1025_D18.000000.npy`) and on D 18.0625's (`I1025-mac/d18/sol_l1kc63Wm1025_D18.062500.npy`), two processes, 6 h caps, the same variants and noise as before. Readings in the README first. Post on #1025. (The folder name is my choice; the order names none.)

## Inputs (raw origin/main by `git show`, `git hash-object --no-filters`; `prep_ref120_inputs_1025.log`)

| item | raw path | blob |
|---|---|---|
| D 18 state | `I1025-win/out/sol_l1kc63W1025_D18.000000.npy` (the same blob at `I1025-mac/d18/`) | 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21 |
| D 18.0625 state | `I1025-mac/d18/sol_l1kc63Wm1025_D18.062500.npy` | f2307f0e8ffb4621b61f74450a920c652981d973 |
| D 18 record (system check) | `I1025-win/out/l1kc63W1025.jsonl`, the D 18.0 line: F 2.630345255831752e-10, 2552 steps | c33039dfa38b495486fb3ef7da77077d43db775a |
| D 18.0625 record (system check) | `I1025-mac/d18/l1kc63Wm1025.jsonl`, the D 18.0625 line: F 2.6753918623791614e-10, 2540 steps | 08f4dbf367edba55814e5cf989ccd32a9a5dbe67 |
| hybrid reference signs | `I1025-mac/d18/d18_refsign_1025.jsonl` (xfkappa; noise robust, 1e-15, 2 seeds) | 3e2d8b4e8f72943983fab091730629464b04e854 |
| signtest.py (system check only) | `I1025-mac/signtest.py` | 179ea09681b0a75f7cefdff98984b48051b3f085 |

The hybrid at lambda 1.20 (xfkappa, the Mac): D 18, sign -1, ln|det| -1929.5742472863 (float64 -1, -1929.6400022400); D 18.0625, sign +1, ln|det| -1923.7847417121 (float64 +1, -1923.7237560476). Both noise robust. The other states in his table: D 17.75 minus, 18.125 plus, 18.1875 plus, 18.25 plus, 18.5 minus; the flip between D 18 and D 18.0625 is the one tested here.

## Commands

The dd check of #1025 as win2 ran it at D 18 (comment 7060027218): `ell_ddm.py det STATE D 63 LAM --noise 1e-24,1e-20,1e-16` (5 exact variants; noise on the dd propagator entries, 2 seeds). Mine, from `solver/matter` of the worktree `C:/Users/nathan/Source/choptuik-i1025d` at wip/ell1-highD 48c36355 (the worktree of the D 17.75 and D 18.5 dd checks), PY `venv-md510`, BelowNormal, 4 threads per process:

```
python -u ell_ddm.py det <D 18 state> 18.0 63 1.2 --noise 1e-24,1e-20,1e-16 --out rows/ell_ddm_D18_lam1.2.jsonl
python -u ell_ddm.py det <D 18.0625 state> 18.0625 63 1.2 --noise 1e-24,1e-20,1e-16 --out rows/ell_ddm_D18.0625_lam1.2.jsonl
```

Two processes in parallel, each capped at 6 h (21600 s) and killed at the cap by the exact pid of the process the driver started (`taskkill /PID <pid> /T /F`; tested on dummy children, `ref120_driver_selftest.log`). `ell_ddm._setup` fixes Ks 30, u0 0.04, kappa 0.7 (the records'); `det` checks no record, so the system check is done by `signtest.py ... syscheck`, below.

Checks made now. `ell_ddm.py selftest` PASS (exit 0) and `selftest --mutate=slices` FAIL (exit 1, Ozaki product 3.0e-14 against 1e-28), as wanted (`rows/selftest_ddm.log`, `rows/selftest_ddm_mutate_slices.log`). System check (`smoke_syscheck_D18.log`, `smoke_syscheck_D18.0625.log`, `make_stubs_ref120_1025.log`; the stubs are the record lines plus a placeholder lam): D 18 rebuilds F 2.6297953945896373e-10 against 2.630345255831752e-10 and 2552 steps against 2552: same true. D 18.0625 rebuilds F 2.6781029735399767e-10 against 2.6753918623791614e-10 and 2540 steps against 2540: same true.

## Readings, fixed now (the coordinator's, hc about 16:10 UTC)

- dd equal to the hybrid at both (D 18 minus, D 18.0625 plus) **confirms a root crossing 1.20 between them**.
- dd differing from the hybrid at either means a **structured hybrid error at that reference, and the crossing reading is void**.

A dd sign counts if its 5 exact variants agree and 1e-24 noise leaves it unchanged (both seeds), as in every dd check of this task; 1e-20 and 1e-16 are information. If a dd sign does not count at either state, neither reading applies and that is reported (the order does not say this case; I apply the rule of the earlier dd checks). The dd ln|det| is printed beside the hybrid's, as information. `read_ref120_1025.py` reads the two records (six planted cases as wanted: crossing confirmed, a differing dd sign at D 18, at D 18.0625 and at both, a disagreeing variant, a noise flip).

## Run

`ref120_driver_1025.py` (launcher `start_ref120_1025.cmd`, BelowNormal) waits for the D 18.125 scan driver (`d18mid_driver_1025.py`) to end, checks the pins, runs the two processes, and reads. It starts by itself when the scan ends (expected about 17:05 UTC: the scan was at 11 of 13 and 11 of 14 points at 16:18). Output: `ref120_w.log`, `rows/dd_*_lam1.2.log`, `rows/ell_ddm_*_lam1.2.jsonl`, `rows/ref120_reading.log`, `rows/ref120_samples.csv` (every 60 s each python's cpu, working set, private bytes and peaks, and the laptop's memory and load). Estimate from the D 18.5 dd (5920 s and 5950 s): about 1.7 h, so done about 18:50 UTC.

## Status

Not started (16:20 UTC).
