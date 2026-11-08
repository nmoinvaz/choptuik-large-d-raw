# I97-macm3: lemma 6a(5) at sub-box 1e-14 verbose, at Lohner order 32, and at sub-box 1e-16

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0), main c691ae37. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/97

From solver/proof/ with venv-macm3, three runs in parallel, 1 thread each, nice 10 under caffeinate -i; each line's
exact command is in its .cmd file and its exit and wall time in exits.txt:
  (a) lemma6_jump_M.py --M=5 --box=<raw>/I36-macm3/A_M2_6a_M5_sub1e-14.json --rp=0.08 --k=20 --verbose, to lemma6a_M5_sub1e-14_verbose.*
  (b) the same with LOHNER_ORDER=32, to lemma6a_M5_sub1e-14_lo32.*
  (c) certify_M2.py krawczyk and export6a with --sub=1e-16,1e-24,1e-25, then lemma 6a from that box, to *_sub1e-16.*

Results (macm3, main c691ae37 for the three runs; the module was loaded before the pull to 7a36683, so the B files
are in the old short form). Exits and wall times are in exits.txt.
  (a) 1e-14 verbose: exit 2, 545 s, 604 steps, start box radius 4.30e-08, final state radius 1.06e-05, max radius of B
      3.35e-01, G_slow inverse not proved.
  (b) 1e-14, LOHNER_ORDER=32: exit 2, 981 s, the same 604 steps and the same two radii as (a), G_slow inverse not proved.
  (c) 1e-16 (Krawczyk exit 0, margins +1.000 +1.000 +1.000 +1.000 +0.999 +0.999; export6a exit 0, max radius 4.29e-10):
      lemma 6a exit 2, 552 s, 615 steps, start box radius 4.30e-10, final state radius 1.05e-07, max radius of B
      3.13e-03, |H| <= 1.62e+04, |G_slow^-1| <= 1.28e+03, Lambda 0.4233, rho_6a [39.22052591 +/- 2.60e-9], ok false.
No run gave rho_6a < 1, so the partial control was not run on any of these B (#96 and #100 ran it on the 1e-14 B).
The verbose lines print only the state's max radius, not B's.
