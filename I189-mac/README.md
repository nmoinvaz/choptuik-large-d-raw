# I189-mac: independent review of Theorem A(5)'s trusted integration code, with CAPD as a second validated integrator

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), /Users/nathan/venv-qd (Python 3.13.15, python-flint 0.9.0 with
FLINT 3.6.0, mpmath 1.3.0 with the pure-Python backend, numpy 2.5.4). CAPD 6.1.0 at commit
37057e5899bccaa6cd5701057b7e6ea5e232ef8b, built with -DCAPD_ENABLE_MULTIPRECISION=ON -DCAPD_INTERVAL_TYPE=NATIVE (filib
needs x86 SSE), against MPFR 4.2.2 and GMP 6.3.0 (Homebrew), Apple clang 21.0.0. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/189. Code: solver/proof/review_189/ on branch wip/i189. At most 2
processes, nice 10.

Contents (filled in as the runs land; exits.txt has each run's exit and wall time):

- inputs/: the CAPD inputs written by review_189/export_inputs.py from the stored files (start6b1.txt from
  I38-macm3/lemma6b1_runs_M5_cert/ray.json sets["0"]; path6b1.txt with the 17 ray legs and row 17's 10 disc times;
  start6a_*.txt, the hull of y and sigma(y) at xi1 = 0.3 from I103-macm3/A_M2_6a_M5_sub1e-18.json).
- b1_*.log: capd_m5 c0 (multiprecision C^0 doubleton) on lemma 6b1(5)'s ray and row 17's arc; cmp_b1_*.log/json:
  compare.py b1 against ray.json starts and I39-mac/disc_inputs/row_17.json.
- a_*.log: capd_m5 c1 (double C^1 doubleton) on lemma 6a(5)'s backward flow; cmp_a_*.log/json: compare.py a against
  I103-macm3/B_M5_sub1e-18.json (and I184-macm3's B when it lands).
- mut_*.log: the mutations (sign of [[C E] P], the coefficient 2 of -(2 + s) Q scaled, a perturbed start), in capd_m5
  and in the original (review_189/orig_mut.py).
- scripts/: the shell scripts that ran everything.
