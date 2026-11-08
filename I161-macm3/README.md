# I161-macm3: win2's amplitude run (#140) repeated on macm3, hashed

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python 3.13.3, python-flint 0.9.0, FLINT 3.6.0), main e04d6f17
(solver/inner_amp is unchanged since win2's checkout d9fab0b: `git diff d9fab0b HEAD -- solver/inner_amp` is empty). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/161

From solver/inner_amp/ with the venv's bin first on PATH, nice 10, caffeinate -is (amp.cmd): python3 -u amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12
--out <raw>/I161-macm3/amp_macm3.json. win2's JSONs are I140-win2/amp_copy{1,2,3}.json and I146-win2/round1/amp_copy{1,2,3}.json (25 rounds, all one hash).

Written before the run. compare_amp.py reuses #140's canon() (I140-win2/compare.py: SHA-256 of the JSON after dropping the timing keys sec, seconds, timing, order_times and keys
ending _s, time, times) and prints macm3's hash against win2's six copies.
  Pass: the hash equals win2's (I146-win2/README.md: amplitude 1.10 K 15 J 750 640 bits = fd6b5ef2f90d4f55 in 16 hex), or the first differing entry (a sigma string) is named.
  Control (must change the hash): macm3's JSON with the last digit of the last sigma string (sigma_str[-1][1]) changed. The script exits 1 if the control hashes like the original, so that the
  comparison could not fail. The control of the rest, #140's own, is I140-win2/compare.py --selftest (exit 0).
  The lemma 6a(5) JSON and B are not rerun here: the issue gives no command for them and the coordinator's message names the amplitude only. Their macm3 files exist
  (I103-macm3, I110-macm3) and their difference from win2's is #110's (748 of 760 radii differ in B, compared by #111's rule, not by hash).

Results (macm3, main e04d6f17). Awake time equals wall time (awake.log: no sleep since 2026-11-07 22:39 PST).
  amp_macm3.json: 296 s wall, 296 s awake (15:31:12 to 15:36:08 UTC; products 60.4 s, fit setup 6.9 s, fits 234.7 s; win2's copy took 609 s). Exit status not captured (exits.txt).
  compare_amp.txt (compare_amp.py exit 0): macm3's hash fd6b5ef2f90d4f559a1a1ab68a7e85fe7c9b8538cc7e50ac41d2fb5510eb47d8 EQUALS win2's six copies (I140 copy1 to 3, I146 round1 copy1 to 3),
  and the 16-hex hash fd6b5ef2f90d4f55 of the 25 rounds of #146. Dropped keys: order_times, seconds, timing. The changed-digit control (last digit of sigma_str[-1][1],
  ...638 -> ...631) gives 520426f8... and differs. #140's selftest ok. The same code and library on both: python-flint 0.9.0 and FLINT 3.6.0 (win2 Python 3.12.8, macm3 3.13.3).
  What differs: CPU (Intel Core Ultra 7 265K, x86-64, against Apple M3, arm64), OS, compiler and the GMP assembly kernels. So the hash checks that the arb arithmetic of win2 and
  macm3 gives the same bits on this path, and it shares the FLINT 3.6.0 source and the Python driver, so it is not a check of those.
