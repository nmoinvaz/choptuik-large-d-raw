# I70-macm3: mode counts at D 45.05 and 61.03, M 48 with the cut (jobs 7 and 6 of modecount_local.sh)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT 3.6.0,
hpkernel 0.1.0 neon), main e04d6f17. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/70

From the repository root with the venv's bin first on PATH, the two jobs in parallel, 1 thread each, nice 10, caffeinate -is, --data in data/ (empty
at the start): job 7 = python3 hp/modecount_wind.py hp/data/states/up7_D45.0507.npz --M=48 --kf=13 --h0=0.6 --lam=2.056738610147195 --fmax=1e-15
--tag=D45.0507_M48_kf13; job 6 = python3 hp/modecount_wind.py hp/data/seeds/local/up23_D61.0264.npz --M=48 --kf=13 --h0=0.6 --lam=2.043532530673195
--fmax=1e-15 --tag=D61.0264_M48_kf13. Before the run: job 7 has no saved M 48 kf13 state (it re-converges from the M 32 state), job 6 resumes from the
saved hp/data/modecount_state_D61.0264_M48_kf13.npz (tracked, |F| 2.7118e-15). setup saves re-converged states into hp/data, so the files the run
creates or changes are copied to hp_data_after/ and the tracked ones restored. Each .cmd has the exact line, exits.txt the exits, awake.log the awake time.
Stop conditions: a setup that raises on |F| > 1e-15 stops that job (|F| reported); wind(g) not 0 in any box is a finding.

Results (macm3, main e04d6f17). Awake time equals wall time in both jobs (awake.log).
  job 7, D 45.05, M 48 with the cut: exit 0, 2648 s. setup: |F| 3.3e-09 in the layout, 6.9e-13 after Newton, 2.0e-18 after Levenberg-Marquardt (below the
    1e-15 gate); 81 new determinants (data/modecount_D45.0507_M48_kf13_evals.jsonl, 25.7 s each). wind(g) is 0 in all 8 boxes (printed as +0.000000 or
    -0.000000), no extra zero. winding of det M: B0 1, U0 0, B1a 1, B1b 1, B1c 0, B1 2, U -7, full -12, as the expected zeros and candidate poles give.
    boxes_D45_M48_vs_M32.txt: the 8 boxes equal October's D 45 M 32 count (hp/data/modecount_D45.0507_M32.log, cut by default at D >= 35).
  job 6, D 61.03, M 48 with the cut: exit 1, 401 s. setup resumed from the saved hp/data/modecount_state_D61.0264_M48_kf13.npz (|F| 2.7118e-15): |F| 2.7e-15 in
    the layout, 2.7e-15 after Newton, 2.7e-15 after Levenberg-Marquardt, then RuntimeError "background not converged in this layout: |F| = 2.7e-15 > 1e-15
    (M = 48)"; no count. The state moved by at most 3.2e-11 and its stored |F| went from 2.7118e-15 to 2.6721e-15 (job6_state_after_vs_october.txt). October's
    task 6 (hp/data/modecount_queue.log, the cloud) stopped the same way: 1.3e-06 after Newton, 2.7e-15 after Levenberg-Marquardt, the same RuntimeError.
  hp/data: job 7 created modecount_state_D45.0507_M48_kf13.npz (moved to hp_data_after_job7/); job 6 rewrote the tracked D 61 state (copied to
  hp_data_after_job6/ with October's, then restored). hp/data is clean. Job 3 (D = 4) is not run here.
