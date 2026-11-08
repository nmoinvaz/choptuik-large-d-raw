# I38-macm3: lemma 6b1(5), all rows and the covering check on p^ +- 1e-18

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0), main 1d335c25. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/38

From solver/proof/ with venv-macm3, nice 10 under caffeinate -i, on I37-macm3's _cert ray (lemma6b1_runs_M5_cert/ray.json),
--M=5 --x=<p^ of data/A_M2_box_M5_1e-10.json> --h=1e-18 --tag=_cert. Rows 17 (I37), 0 and 9 (I113) are certified. The other
15 rows run as five parallel rows processes (rows_a to rows_e: rows 1,10,15 / 2,12,16 / 3,11,13 / 4,5,14 / 6,7,8), each
.cmd with the exact line. Then check (--json), check --drop=9,5 (must fail) and mutate --j=0 (must certify no disc). Each
exit and wall time is in exits.txt. lemma6b1_runs_M5_cert/ is copied here at each push.

Results (macm3, main ed429084; the lemma 6b1 code is unchanged since I37-macm3). Exits and wall times are in exits.txt.
  rows_a to rows_e: all exit 0, 2099 to 2174 s, no failing disc (0 "ok False" in the five logs).
  check: exit 0, "LEMMA 6b_1 CHECK: PASS", 366 tiles glued (1188 polar rectangles, 957 links); lemma6b1_check_M5_cert.json.
  check --drop=9,5: exit 3 (must fail), "LEMMA 6b_1 CHECK: FAIL (3 failures: tile (9, 6): agreement point not in the meeting
      set; tile (10, 4): meeting set not connected; point (|u| = 165.24, arg = phi_9,5) not covered without tile (9, 5))".
  mutate --j=0: exit 0, 530 s, 0 of 38 discs of row 0 certified (must be 0).
  The run directory lemma6b1_runs_M5_cert/ holds ray.json and row_00.json to row_17.json (18 rows, 366 discs, all ok).
  Totals: 37129 Lohner steps over the 18 rows (projection 40168), 12123 s of row process time plus the ray's 484 s;
  rows_table.md has the per-row figures from check.log.
