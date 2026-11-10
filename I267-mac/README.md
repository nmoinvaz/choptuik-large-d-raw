# I267-mac: the series gate of gamma_dd.py --Mhi, its planted state and its control

Machine: mac (Apple M5, 10 cores, shared with other sessions; one process at a time, 1 thread, nice 10, caffeinate).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/267 (from #254's recommended task 4).
Code: `hp/gamma_dd.py` on the branch wip/i271 of the main repository, commit 408b4d6 (#267's change on top of #271's
2e72818). The runner is `../I271-mac/scripts/run.sh` with this folder's logs; every exit is in `logs/exits.txt`.

## The change

Every `--Mhi` record holds both series' truncation (`modecount_common.series_tail`: centre at the first node, horizon at
the last) at the resampled start (`tails_start`) and at the solution (`tails`). A state where either exceeds
SERIES_TAIL (1e-15) is refused there: the record says `refused` with the reason, has no lam, and the exit is 1.
`--series_override` accepts it and records `override`. `--mutate=no_tail_gate` removes the check.

## The planted state

`states/up6_D30.0688_kc100.npz` (`scripts/plant.py`): D 30's saved state, `hp/data/states/up6_D30.0688.npz` (M 32, no
cut), with its centre series order lowered from kc 414 to 100. `scripts/tails_kc.py` measures both series on the M 32
layout and on the double-double M 48 start for several kc (`logs/tails_kc.log`). At kc 100 the M 32 layout passes and
the M 48 start's centre series does not.

## Pass and fail criteria (written before the runs)

(a) **The records carry the tails.** Every `--Mhi` record of this task and of I271-mac (`gamma_dd.jsonl`) has
`tails_start` and, unless refused at the start, `tails`, each with the centre and the horizon series.

(b) **The planted state is refused.** `gamma_dd.py --polish=4 --M48` on it gives an M48 record with `refused` (at the
start), no lam, and exit 1.

(c) **The control accepts it.** The same with `--mutate=no_tail_gate` gives no `refused` and a located lam(48). Its
exit is 0 unless its floor check (#271) fires, which is reported separately. If it is refused, the gate's control
failed.

(d) **The override** (if time allows): the same with `--series_override` gives `override` with the reason and a lam.

## Results

Not run: the subagent's session ended at about 02:10 UTC on 2026-11-10 (coordinator's note). The runs are made on
macm3 (folder I267-macm3).
