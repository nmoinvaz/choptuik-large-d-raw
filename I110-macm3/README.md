# I110-macm3: lemma 6a(5) with the other machine's B

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT 3.6.0, Python 3.13.3, macOS-26.3.1-arm64-arm-64bit-Mach-O), main c282ab8a.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/110 (macm3's half; win2's is in I110-win2/).

From solver/proof/, 1 thread, nice 10 under caffeinate -i (each .cmd has the exact line, exits.txt each exit):
  lemma6_jump_M.py --M=5 --box=<raw>/I103-macm3/A_M2_6a_M5_sub1e-18.json --rp=0.08 --k=20 --load-B=<raw>/I104-win2/B_M5_sub1e-18.json
      --json=<raw>/I110-macm3/lemma6a_loadB_win2.json        (the issue's command, plus --json as the coordinator asked)
  An addition, not in the issue: the same with --load-B=<raw>/I103-macm3/B_M5_sub1e-18.json (macm3's own B), to lemma6a_loadB_macm3.*.
  reload_inflation.py (also an addition) measures how much --load-B inflates each stored radius; its output is reload_inflation.log.
The two box files (I103-macm3 and I104-win2) are byte-identical (cmp).

Results. rho_6a balls, Lambda [0.4233267068 +/- 6.91e-12] in every macm3 row:
  win2's B on macm3: exit 0, 1 s, rho_6a [0.2181093597 +/- 3.59e-11] < 1, |H| <= 6.78e+01, |G_slow^-1| <= 5.48e+00.
  macm3's B on macm3, reloaded (addition): exit 0, 1 s, rho_6a [0.2309898805 +/- 3.09e-11].
  For comparison (other folders): macm3's B in memory (#103) [0.2309898799 +/- 4.42e-13]; win2's B in memory (#104)
  [0.2181093594 +/- 4.74e-11]; win2 loading macm3's B (I110-win2) [0.2309898806 +/- 4.01e-11].
  H_max and Gslow_inv_max, stored as doubles, agree to every digit between the machines for the same B.
  Reloading inflates every radius: 760 balls per file, relative +9.3e-10 to +5.5e-9, median 1.9e-9, on both machines' B.
