# I100-macm3: lemma 6a(5)'s exact --save-B, checked by reloading

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0), main 5affc10b (lemma6_jump_M.py as at 7a36683). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/100

From solver/proof/ with venv-macm3, 1 thread, nice 10 under caffeinate -i, one after the other (each .cmd has the exact
line; exits.txt each exit):
  lemma6_jump_M.py --M=5 --box=<raw>/I36-macm3/A_M2_6a_M5_sub1e-14.json --rp=0.08 --k=20 --save-B=<raw>/I100-macm3/B_M5_sub1e-14_exact.json
  lemma6_jump_M.py --M=5 --box=<raw>/I36-macm3/A_M2_6a_M5_sub1e-14.json --rp=0.08 --k=20 --load-B=<raw>/I100-macm3/B_M5_sub1e-14_exact.json --mutate=partial

Both runs match the issue's expectations. The save run (03:37:04 to 03:46:13 UTC, 549 s) exits 2 with "G_slow:
invertibility not proved", as in #36, and prints final state radius 1.06e-05 and max radius of B 3.35e-01. The load run
with --mutate=partial (03:46:13 to 03:46:15 UTC, 2 s) exits 0 and prints the same two radii, 1.06e-05 and 3.35e-01, then
"G_slow is 13 x 17: not square ... [MUTATION partial: failure expected]". Before 7a36683 the same load printed 9.94e-05
and 7.80e-01 (#96).
