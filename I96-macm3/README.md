# I96-macm3: the partial-mutation control of lemma 6a(5) on #36's stored B

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0), main 59a3248f. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/96

From solver/proof/ with venv-macm3, 1 thread, nice 10 under caffeinate -i (lemma6a_M5_partial_sub1e-14.cmd has the exact
line; exits.txt the exit, as the issue's command appends it):
  lemma6_jump_M.py --M=5 --box=<raw>/I36-macm3/A_M2_6a_M5_sub1e-14.json --rp=0.08 --k=20 --load-B=<raw>/I36-macm3/B_M5_sub1e-14.json --mutate=partial

Ran 03:21:26 to 03:21:27 UTC, exit 0 ("partial 0" in exits.txt), last line "G_slow is 13 x 17: not square, beta is not
determined by the slow data; lemma 6a NOT established   [MUTATION partial: failure expected]": the control passes.
The reloaded B prints final state radius 9.94e-05 and max radius of B 7.80e-01, where #36's run that saved it printed
1.06e-05 and 3.35e-01: the stored balls keep only their accurate digits (e.g. "[-1.2e+1 +/- 0.221]"), so a loaded B is
wider than the computed one.
