# I36-macm3: lemma 6a(5) on the M = 5 certificate state box

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint
0.9.0), main dc3b2d0b. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/36 (commands in its first comment).

From solver/proof/ with venv-macm3, 1 thread, nice 10 under caffeinate -i (lemma6a_M5_cert.cmd has the exact line,
exits.txt how it ended; stopped after 6 h):
  lemma6_jump_M.py --M=5 --box=data/A_M2_6a_M5_1e-10.json --json=<raw>/I36-macm3/lemma6a_M5_cert.json

Ended with exit 1 after 20 s (01:23:25 to 01:23:45 UTC). The log's one line is "lemma S or the flat estimate failed"
(lemma6_jump_M.py line 160, before the backward integration), so no JSON was written. Stopped there, as the issue says.
