# I1052-dh610: PR #1052's A/B, Broyden's updates between the octo-double corrector's LUs, on dh610

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Pull request https://github.com/nmoinvaz/choptuik-large-d/pull/1052 (branch `perf/od-broyden` 2b883799, base `chore/multishoot-4.0.0` 1c02b15b), the commands of the
coordinator's comment of 20 Nov 2026, 10:22 UTC, queued after the #1050 checks (`../I1050-dh610/`). Both arms of the chain and arc A/B run the PR's scripts (A: `--od_broyden` off, B: `--od_broyden 1`; `--od_times` is the PR's), K1's base arm the base branch's use the same hpkernel, the #1050 build in `~/Source/venv-i1050`
(multishoot 4.0.0, multidouble 5.0.0; PR #1052 changes only `hp/anm_run.py`, `hp/arclength.py`, `hp/octo_corrector.py` and adds `hp/od_broyden_check.py`, `hp/od_broyden_ab.py` and a notes section, nothing under `hp/src` or `hp/python`),
in one session, 10 threads, `nice -n 10`, one run after another.

Worktrees: `~/Source/choptuik-large-d-1052` (perf/od-broyden) and `~/Source/choptuik-large-d-1052base` (chore/multishoot-4.0.0), both detached. Inputs not in the live raw clone were taken from origin/main by `git archive`
(`I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_pin3_D256.{5265,8479}.npz`, `I1008-macm3/run1/arc_002_D259.311977.npz` and `arcjet_002_D259.311977.npz`; `T129-win2/chain/anm_pin3_D180.5246.npz` was there).

Pass criteria, fixed before the runs (the coordinator's): 1. both attempts converge; 2. same D and |Delta_B - Delta_A| <= 1e-30 with all eight parts summed (this is the error); 3. B forms no more LUs in the attempt (in the D chain the count
includes the one LU B defers to the next series). The gain is the attempt's corrector seconds, with a deferred LU charged at A's median LU time.

Order and estimates (caps 3 times each by `timeout` on the exact pid): K1 (base and off arms of `octo_corrector.py planted` at `T129-win2/chain/anm_pin3_D180.5246.npz`, then the bit-for-bit compare; control: k1_base against k2_on must print DIFFER);
K2 (planted with `--broyden 1 --Delta_ref`, pass "(a) PASS", and its controls `--mutate_offset qd` and `--mutate 10`, each must exit 1); the chain A/B at leg 10's flags, two steps c1 and c2, both arms (45-55 min per arm) and `od_broyden_ab.py` on each pair;
the arc A/B (#1008 arc step 4's inputs at `--elim_switch 0`, 75 min per arm) and `od_broyden_ab.py ... --kind arc`. About 6-7.5 h in all. `exits_1052.txt` and `summary_1052.txt` hold the exits and walls.

## Files

| file | what |
|---|---|
| `common1052.sh`, `run1052.sh` | paths and the driver (the commands are in it) |
