# I1088-dh370: Track A of #1088 on dh370, the full system's weakest singular values at three chain states

Machine: dh370 (Fedora 45, i7-8700, 12 threads), the venv of `~/Source/choptuik-large-d-1082` (hpkernel at a9975061,
main's kernel), 6 threads at nice 10, systemd user units `i1088a-wsv` and `i1088a-wsv2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1088
The runs ran in `~/Source/choptuik-large-d-1088a/work/` (code of `wip/large-d-jump` fetched as a tarball), and their
files were copied here from the Mac, which pushed this folder.

- `weak_sv/`: `weak_sv.py` (from `I1088-mac-a/probes/`, its path to hp/ edited) on the order-293 chain's states at D
  245.5586, 254.5903 and 263.5987 (`I966-dh370/ks_chain3b/`), kfreeze 13, 10 directions, 6 iterations
  (`run_wsv.sh`); `weak_sv2.py` deflates the weakest six to resolve the Delta mode (`run_wsv2.sh`, logs added when
  done).

Form S jumps (#1088, `hp/form_s.py jump` on branch `wip/large-d-form-s`, the kernel built on dh370 by the low-memory
release recipe from 38943f4f, `~/Source/choptuik-large-d-1088a/fs`), each in its own folder with `run.log` (start, end,
the command), `jump.log` and `jump_s.jsonl` (one record per Newton step), via `run_jump.sh`:
- `j300_junk10/`: D 300 with the 10 weakest no-Delta directions frozen; stopped by hand after step 0.
- `j300_held/`: D 300 with p1's harmonics 5-13 held at the guess's values; converged, the state `jump_s_D300.0000.npz`
  (form S's layout, eight parts).
- `j1000_held_d2/`: D 1000 (degree 2, ks 989, kc 200, Delta Track C's 1.654240854245): step 0 found no trial; stopped by
  hand after it.
- `mixed/`: speed probes at D 300 from the held state `j300_held/` (`mixed.py`, `run_mixed.sh`): the octo-double
  Jacobian with 1 and 2 tangents (`tangents.log`), and the iteration with an f64 Jacobian formed once at the guess and
  the octo-double residual (`mixed.log`) with its control, J times 1.01 (`mixed_scale101.log`).
- `rebuild_mob.sh`: the release build of `wip/large-d-form-s` with the Moebius horizon (6244fbff).
- `mixed2/`: the coordinator's run on this machine (from /home/nathan/Source/t5-mixed2/, `mixed2.py`, `run.sh`,
  `run3.sh`): Newton on the held system at D 300 from the guess with the octo-double residual and the Jacobian
  re-formed at every step in double-double (`dd.log`, control `dd_scale101.log`), f64 (`f64_fresh.log`) or quad-double
  (`qd_fresh.log`), and one octo-double Jacobian as a chord (`od_chord.log`); copied while `run3.sh` runs.
- `after_mob.sh`: the D 1000 held jump with the Moebius horizon, queued after `rebuild_mob.sh`.
- `j1000_held_mob/`: D 1000 held, the Moebius horizon (a 8, ks 1517, kc 200), the quad-double Jacobian, the octo-double
  residual to 1e-40; Delta 1.654240853943893145 and the full system's first-order dDelta (`jump.log`, the state).
- `after_mob_lean.sh`: D 1000 again the lean way (double-double solve, Delta-bound stop, quad-double check), queued after
  a rebuild with the z recurrence.
- `j1000_lean/`: D 1000 held the lean way on the build with the z recurrence (ae0b5453): the double-double Jacobian
  and residual stopped by Delta's first-order bound, one quad-double check, the discretization report and the
  Hamiltonian check; the plan and held values of j1000_held_mob.
- `run_zcheck.sh`: the z-recurrence check at D 1000 and the D 2000 guess (out/zcheck/zcheck.log, copied when done).
