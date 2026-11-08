# I125-macm3: lemma 6b1(5) C1 ray at h = 1e-16 and 1e-17, a test of the radius-floor model

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0,
FLINT 3.6.0), main db617735. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/125

From solver/proof/ with venv-macm3, two rays in parallel, 1 thread each, nice 10 under caffeinate -i: lemma6b1_cover_M.py ray
--M=5 --c1 --x=<p^ of data/A_M2_box_M5_1e-10.json> --h=1e-16 --tag=_c1h16 and --h=1e-17 --tag=_c1h17 (each .cmd has the exact
line, exits.txt each exit). predictions.txt holds the model's predictions, written before the rays ran. The run directories are
copied here as lemma6b1_runs_M5_c1h16/ and _c1h17/.

Results (macm3, main db617735; the lemma 6b1 code is unchanged since I37-macm3). Exits and wall times are in exits.txt.
  ray --c1 at h = 1e-16 and 1e-17: both exit 0, 2506 s wall each, 17 segments, 2520 Lohner steps, equal at every h. Of that wall
  time 1949 s was the Mac asleep (a clamshell sleep at 22:05 PST and maintenance sleeps to 22:39 PST), 557 s awake, against
  517 s for #118's rays; pmset_sleep.log has the windows.
  radius_over_h_vs_model.txt: measured radius over h against predictions.txt (written before the rays ran).
  Rows 1, 6, 9, 11, h = 1e-16 and 1e-17: all eight within 10% of the prediction, from -8.7% (row 6, 1e-17) to +0.5%.
  Over all 16 segment ends after the start the largest deviation is 11.6%, three ends at h = 1e-17 (|u| 325, 298, 272) between
  -10.7% and -11.6%, the model too high where the floor is still building.
  pmset_sleep.py and pmset_sleep.log: how much of each macm3 run's window was the Mac asleep, T139 to I125.
