# I113-macm3: lemma 6b1(5) rows 0 and 9, a check of the run-time projection

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0), main ed429084. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/113

From solver/proof/ with venv-macm3, two processes in parallel, nice 10 under caffeinate -i: lemma6b1_cover_M.py row
--M=5 --j=0 and --j=9, --x=<p^ of data/A_M2_box_M5_1e-10.json> --h=1e-18 --tag=_cert, on I37-macm3's ray. Each .cmd has
the exact line, exits.txt each exit and wall time. Predictions from I37-macm3/projection.txt: 2901 and 2117 Lohner steps.
The rows' JSON are copied here as lemma6b1_runs_M5_cert/row_00.json and row_09.json.

Results (macm3, main ed429084; the lemma 6b1 code is unchanged since I37-macm3). Exits and wall times are in exits.txt.
  row 9: exit 0, 463 s, all 17 discs certified, Lam 0.191 to 0.222, box radius 8.5e-17 to 3.6e-16, 1936 Lohner steps
      (predicted 2117, 8.5% below).
  row 0: exit 0, 626 s, all 38 discs certified, Lam 0.173 to 0.187, box radius 2.4e-18 to 1.5e-15, 2576 Lohner steps
      (predicted 2901, 11.2% below).
  Both ran beside #112's ray, three processes at once: 0.23 s per Lohner step after taking 1 s per disc, against row 17's
  0.192 s per step when it ran alone.
