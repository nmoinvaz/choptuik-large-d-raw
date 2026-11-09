# I237-macm3: the onset of the extra zeros between D 50 and 55 narrowed (D 52.04, D 53.79 at M 48), and D 55.04 at M 32, kf 23

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx for 3.14),
main 3e794412. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/237. Beside I232-macm3 (D 50.01 clean, D 55.04 with extras, M 48, kf 23).

Runs (1 thread each, nice 10, caffeinate -is, from the repository root; *.cmd hold the exact lines): (a) D52/count.cmd: hp/modecount_wind.py hp/data/states/up9_D52.0414.npz --M=48 --kf=23 --h0=0.6 --lam=2.050075192515248
--fmax=1e-15 --resolve=last --tag=D52.0414_M48_kf23; (b) D53/: hp/gamma_dd.py <raw>/I237-macm3/D53/gamma.jsonl hp/data/states/up10_D53.7914.npz (its default layout, kf 13 cut from D 35 on; lam_phys is not in
hp/data/gamma_dd.jsonl), then the same count with --lam=<lam of the record> --tag=D53.7914_M48_kf23; (c) D55_M32/count.cmd: hp/data/states/up10_D55.0351.npz --M=32 --kf=23 --lam=2.04768412771239 --tag=D55.0351_M32_kf23.
All with --data=<raw>/I237-macm3/<folder>/data (empty, so every determinant is fresh; no D 52, D 53.79 or D 55 M 32 kf 23 state is in hp/data, hp_data_before.txt). If gamma_dd skips the state (residual above its gate), (b)
stops there and is reported.

Written before the run. Gates: each setup's |F| <= 1e-15 (hp/modecount_common.setup raises above --fmax: a stop for that run, |F| reported, the state it saves moved out of hp/data); gamma_dd's own gate is --fmax 1e-20.
Table: the 8 boxes at each run beside #232's D 50.01 (all 0) and D 55.04 (B0 +2, U0 +1, U +1, full +2), both mismatch counts per edge (all passes and the last pass). Reading rules, fixed now:
  Extras "present" at a run when wind(g) is nonzero in any resolved box, "absent" when 0 in every resolved box. Onset bracket at M 48, kf 23: D 52.04 present: onset in (50.01, 52.04]; D 52.04 absent and D 53.79 present:
  (52.04, 53.79]; both absent: (53.79, 55.04]. Anything else (present at D 52 and absent at D 53.79) is reported as it is and the bracket is not narrowed. D 55.04 at M 32: present or absent by the same rule; absent would mean
  D 55's extras need M 48 as D 61's do (#160, #168). An unresolved edge is "not a count" and its boxes are not read. Not located: this task counts per box and does not track zeros.

(b) gamma_dd on D 53.791398 (D53/gamma.jsonl, exit 0): not skipped, |F| 3.2e-24 in its kf 13 layout, lam_phys = 2.048648769709809 (gamma 0.48812662023156367, formula lam 2.0486490886, one sign change, 7 determinants).
The count then uses --lam=2.048648769709809 (D53/count.cmd).

Results (macm3, main 3e794412, venv-macm3-314 = Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0; awake.log: awake = wall for every run, caffeinate -is; three runs side by side; hp/data back to hp_data_before.txt, the saved states in */hp_data_after/).
  (c) D 55.04 at M 32, kf 23: exit 0 at 08:22:17 UTC, 988 s; setup |F| 4.4e-24 (native M 32, no re-converge, no state saved); 85 evaluations at 11.6 s; wind(g) 0 in all 8 boxes (winding of det M B0 1, U0 0, B1a 1, B1b 1, B1c 0, B1 2,
      U -7, full -12); 14 edges, mismatches 0 in any pass and 0 in the last pass, largest step 0.384 rad. Extras ABSENT at M 32 (they are present at M 48, I232).
  (b) D 53.79: gamma_dd not skipped (|F| 3.2e-24, kf 13 layout), lam_phys 2.048648769709809. Count at M 48, kf 23: exit 0 at 08:59:44 UTC, 3160 s; setup |F| 5.7e-08 in the layout, 5.7e-08 after Newton, 2.5e-20 after LM; 85 evaluations at
      31.5 s; wind(g) 0 in all 8 boxes (winding of det M B0 1, U0 -1, B1a 1, B1b 1, B1c 0, B1 2, U -6, full -10); 14 edges, mismatches 0 and 0, largest step 0.386 rad. Extras ABSENT.
  (a) D 52.04 at M 48, kf 23: exit 0 at 09:06:13 UTC, 3624 s; setup |F| 5.9e-08 in the layout, 5.9e-08 after Newton, 3.8e-19 after LM; 102 evaluations at 30.9 s; wind(g) 0 in all 8 boxes (winding of det M B0 1, U0 0, B1a 1, B1b 1,
      B1c 0, B1 2, U -7, full -12); 14 edges, mismatches 0 and 0, largest step 0.380 rad. Extras ABSENT.
  Onset bracket (rule above): D 52.04 and D 53.79 both absent, so the onset at M 48, kf 23 lies in (53.79, 55.04], narrowed from (50.01, 55.04). D 55.04 at M 32: absent, so D 55's extras need M 48, as D 61's.
  compare_boxes.txt has the seven counts side by side (D 45, 50, 52, 53.8, 55 at M 48, D 55 at M 32, D 61).
