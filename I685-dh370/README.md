# I685-dh370: the chain's complex-D singularity from D 252 on, the 24-order series at five of #603's states (the dh370 run of #685)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB. Run at `nice -n 10`, 12 threads, `OPENBLAS_NUM_THREADS=1`, no memory guard.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/685 (recommended by #634, whose 24-order series at D 236.63 and 16-order one at D 245.14 are in I634-mac/).
Code: choptuik-large-d main at aedb403b (a descendant of 2e949de8), worktree `choptuik-large-d-685`, run in the venv of `choptuik-large-d-614` (the 3c35f0c build, multishoot 1.2.2, multidouble 4.2.1);
hp/src, hp/Cargo.*, hp/pyproject.toml, hp/build.sh and hp/python are unchanged between 3c35f0c and aedb403b.
Inputs: #603's states `I603-win2/chain/anm_pin3_D<D>.npz` and records `I603-win2/chain/anm_run.jsonl` of the raw repository at 27a7ab25 (51 states, to D 253.7313), read in place.
The command is #634's (`I634-mac/run_634.sh`, stage n24): `anm_run.py $RAW $R/repro --state S --N 24 --tol_od 1e-60 <#603's flags> --save_jet 2`, here with `--threads 12`.

## Result

Each of the five 24-order series equals #603's record of the step from its base in all 25 norms and both pivots, bit for bit (`repro_check685.log`, from `repro_check685.py`; the control `repro_check685_control.log` compares each with a neighbouring base's record and differs in 0 of 25 norms at all five, as it must).
The planted controls of `jet_singularity.py` at N 24 pass (`planted/planted.log`, exit 0) and `--mutate drop_pole` fails (`planted/planted_mutate_drop_pole.log`, exit 1, P1 FAIL).
`jet_singularity.py summary` was run through `stage_summary685.sh` (it reads only RAW/I634-mac/repro, so a scratch root holds links to I634-mac's series and to this folder's; no code was changed), giving `jet_685.json`, `summary685.log` and, from `table685.py`, `table685.txt`.

| series | exit | wall | norms and pivots equal to the record |
|---|---|---|---|
| D 252.2497 | 0 | 2331 s | 25 of 25, yes |
| D 253.7139 | 0 | 2362 s | 25 of 25, yes |
| D 253.0682 | 0 | 2339 s | 25 of 25, yes |
| D 252.6135 | 0 | 2378 s | 25 of 25, yes |
| D 253.3524 | 0 | 2338 s | 25 of 25, yes |

The singularities are in `table685.txt`: three tracks of D* = D0 + s are seen at three or more bases, and none moves toward the real axis within the data.

## Files

| file | what |
|---|---|
| `run685.sh`, `exits_685.txt`, `repro_D*.log`, `repro/jet_pin3_D*.npz` | the five series (anm_run.py `--save_jet 2`, #603's flags) |
| `repro_check685.py`, `repro_check685.log`, `repro_check685_control.log` | the series against #603's records, and its control |
| `planted/` | `jet_singularity.py planted` and `--mutate drop_pole` |
| `stage_summary685.sh`, `summary685.log`, `jet_685.json` | `jet_singularity.py summary` on the five series and I634-mac's |
| `table685.py`, `table685.txt` | the tables of the report |
