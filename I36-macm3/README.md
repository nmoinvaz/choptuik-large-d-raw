# I36-macm3: lemma 6a(5) on the M = 5 certificate state box

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0), main dc3b2d0b. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/36 (commands in its first comment).

From solver/proof/ with venv-macm3, 1 thread, nice 10 under caffeinate -i (lemma6a_M5_cert.cmd has the exact line,
exits.txt how it ended; stopped after 6 h):
  lemma6_jump_M.py --M=5 --box=data/A_M2_6a_M5_1e-10.json --json=<raw>/I36-macm3/lemma6a_M5_cert.json

Ended with exit 1 after 20 s (01:23:25 to 01:23:45 UTC). The log's one line is "lemma S or the flat estimate failed"
(lemma6_jump_M.py line 160, before the backward integration), so no JSON was written. Stopped there, as the issue says.

The first run (the first comment's command, default --rp 0.1) is kept as lemma6a_M5_cert_rp0.1.log and .cmd. The
coordinator's comment of 2026-11-08 01:56 UTC corrected the command to --rp=0.08 --k=20 with --save-B, and added the
control --mutate=partial on the stored B, which must return 0 (3 if it wrongly passes):
  lemma6_jump_M.py --M=5 --box=data/A_M2_6a_M5_1e-10.json --rp=0.08 --k=20 --save-B=<raw>/I36-macm3/B_M5.json --json=<raw>/I36-macm3/lemma6a_M5_cert.json
  lemma6_jump_M.py --M=5 --box=data/A_M2_6a_M5_1e-10.json --rp=0.08 --k=20 --load-B=<raw>/I36-macm3/B_M5.json --mutate=partial
to lemma6a_M5_cert.log and lemma6a_M5_partial.log (each .cmd has the exact line); the main run stops after 6 h.

The corrected run ended with exit 2 after 150 s (01:57:02 to 01:59:32 UTC): lemma S and the flat estimate closed
(contraction 0.7247, Lambda 0.4233), then "backward integration failed (step size underflow at t =
0.41552823781967163)", t the real leg's parameter (xi = 0.3 + (0.067 - 0.3) t, so xi = 0.2032). No B_M5.json and no
JSON were written, so the --mutate=partial control, which loads that B, was not run. Stopped there.

Coordinator's comment of 2026-11-08 02:18 UTC: Krawczyk on a sub-box of the certificate box, export of the state box at
xi1 from it, lemma 6a from that box; first --sub=1e-12,1e-20,1e-21 (files *_sub1e-12.*), then, as its integration
underflowed, --sub=1e-14,1e-22,1e-23 (*_sub1e-14.*). Each step's exact line is in its .cmd, exits in exits.txt.
  sub1e-12: krawczyk exit 0 (margins +1.000 +1.000 +0.999 +0.999 +0.999 +0.999); export exit 0 (max radius 4.29e-06);
            lemma 6a exit 2 after 367 s, start box radius 4.30e-06, "step size underflow at t = 0.9076055632904172"
            (xi = 0.0885).
  sub1e-14: krawczyk exit 0 (margins all +1.000); export exit 0 (max radius 4.29e-08); lemma 6a exit 2 after 475 s,
            start box radius 4.30e-08: the backward integration completed (604 steps, final state radius 1.06e-05,
            max radius of B 3.35e-01, stored as B_M5_sub1e-14.json), then "G_slow: invertibility not proved; lemma 6a
            NOT established". No rho_6a and no JSON. The --mutate=partial control was not run (it runs only if lemma
            6a passes).
