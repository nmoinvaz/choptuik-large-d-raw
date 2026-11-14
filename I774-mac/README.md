# I774-mac: the full system's Delta on the exact freeze projector, re-polished from win's pre-#523 states

Machine: the coordinator's Mac (Apple M5), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/774.
Worktree `choptuik-large-d-774` (branch `wip/i774` at main 3e096e26), `/Users/nathan/venv-314` (Python 3.14),
nice 10, 4 threads, `OPENBLAS_NUM_THREADS=1`, one job at a time (`run_774.py`, which logs each job's start, end, exit
code, wall and CPU seconds to `logs/run_774.log`).

## The two builds

| build | hpkernel | `_hpkernel` .so SHA-256 (first 16) | freeze projector |
|---|---|---|---|
| E | main 3c35f0c's build (multishoot 1.2.2, multidouble 4.2.1), session scratchpad `site2`, loaded with `PYTHONPATH` | 13b27ce3f9b60464 | exact (#523) |
| R | venv-314's installed build of 2026-11-09 | 8d271187fc694058 | rounded, as win's venv-t151 of #725-#769 |

Both run the same Python (the worktree's `hp/` at main 3e096e26; its `hp/` differs from #742's 5249c432 only in files
outside the od path, and #752 reproduced #742's lines with it) and the same multidouble Python package (main's pin
f092018d). R reproduced #742's predictions bit for bit and its log lines in #752 (raw `I752-mac/`, 77a5564b). Each
job's log starts with the hpkernel file its interpreter loads, and `run_774.py` refuses a job whose build loads the
other kernel.

## Plan, written before the runs (2026-11-14 15:48 UTC)

Every job is `anm_run.py RAW I774-mac/<job> --state <state> <flags> --steps 0 --save_base 1 --threads 4`, so it is the
base polish only, and the polished state is saved as `<job>/base_pin<k>_D<D>.npz` (eight parts). Flags
(`run_774.py --list`):

- Full system, #727's and #742's: #682's flags with `--corrector od --tol_od 1e-60 --reseed_o 3 --elim_switch 0`.
- Held, T138-win2's chain (`--kfreeze 3 --held_fit data/held_fit.json`, unchanged on main since T138's 31da699) with
  its quad-double corrector swapped for `--corrector od --tol_od 1e-60 --reseed_o 3`, as #727 swapped cont3's, and
  the default switch, which is T138's.

| job | build | state | what it gives |
|---|---|---|---|
| `C_X2c` | R | `I727-win/states/X2_on_cont3plan.npz` | **control, run first**: #727's X2c job from its start (3 Newton steps on win) |
| `E_117` | E | `I742-win/L/anm_pin13_D117.0000.npz` | D 117 on the exact projector; its first lines must equal #752's `I752-mac/logs/AB_main.log` |
| `E_113` | E | `I742-win/P/base_pin13_D113.0000.npz` | D 113 |
| `E_120` | E | `I742-win/M/anm_pin13_D120.0000.npz` | D 120 |
| `E_cont3` | E | `I682-win/cont3/anm_pin13_D99.8750.npz` | cont3 at D 99.875 |
| `E_X2c` | E | `I727-win/X2c/base_pin13_D99.8750.npz` | X2c at D 99.875 (cont3's plan, so it must agree with `E_cont3`) |
| `H_R113`, `H_R117`, `H_R120` | R | `T138-win2/chain/anm_pin3_D<D>.0000.npz` | the held states polished to 1e-60 on the rounded projector (pilot `H_R117` first) |
| `H_E113`, `H_E117`, `H_E120` | E | the same | the held states on the exact projector |

The held jobs are not in #774's list. They are here because #742's Delta_held is T138's quad-double chain (tol_qd
1e-28, pre-#523 build), so Delta_full - Delta_held "on the exact projector" needs the held side polished on it too.

**Delta of a state** is the exact sum of the last entry of its parts (Python `fractions.Fraction`, exact; `cmp_774.py`),
printed to 40 digits. This shares nothing with #739's reading (`I739-win/cmp_739.py`, arb at 600 bits), and
`cmp_774.py` first reproduces #742's 40-digit Delta at D 113, 117 and 120 and X2c's 60 digits from the stored
states, exiting 1 on a mismatch.

**Pass criteria, fixed now (#774's acceptance):**

1. Control: `C_X2c`'s polished Delta equals X2c's stored Delta (`I727-win/X2c/base_pin13_D99.8750.npz`) to 1e-50,
   and its log lines equal #727's `logs/X2c.log`. `cmp_774.py --mutate 1e-48` adds 1e-48 to the control's Delta and
   must fail. If the control fails, nothing on build E is run until the cause is known.
2. Each re-polish on build E converges: the corrector says converged, final octo-double max|F| at most 1e-60.
3. Each shift Delta_E - Delta_stored is reported with its kind: "measured" when both the stored state (on build R) and
   the E polish are converged roots of their systems at most 1e-60; cont3's stored state is quad-double, and #727's
   pilot2 showed its od polish on the rounded build takes no Newton step (Delta unchanged), so its kind says so.
4. Discrepancy bars: a shift above 1e-3 of #742's Delta_full - Delta_held at that D (4.37e-16, 4.95e-16 and
   5.32e-16 at D 113, 117 and 120) flags the notes' statements resting on #742's table, and a shift above 1e-25 at
   D 99.875 flags those resting on #725-#769's D 99.875 values (HELD_HARMONICS 4.4).
5. Table: Delta_full - Delta_held at D 113, 117 and 120 with both sides on the exact projector (E jobs), beside
   #742's (both from the stored states) and beside the rounded pair polished to 1e-60 (stored full, `H_R`).

**Expectation, written now and not a criterion:** #752's `AB_main.log` (build E, D 117) moved Delta by +1.57e-20 in
its first step, so the shifts at D 113-120 are about 1e-20, far below bar 4, and the shift at D 99.875 is probably
above 1e-25 (HELD_HARMONICS 4.4 records -2.76e-23 at D 73 between the builds), which would flag 4.4's D 99.875 values.

**Not done:** states other than these, any continuation step, any flag change beyond the corrector swap of the held
jobs. If a held polish stalls on build R with the default switch, I stop the held jobs and report.
