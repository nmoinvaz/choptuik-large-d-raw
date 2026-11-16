# I865-mac: lemma S's series control over a parameter box, before and after the fix

Machine: the Mac (coordinator), python-flint 0.9.0. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/865.
Fix: main 26eb48e9 (`lemma_S_M` and `lemma_S` require the centre run's identity checks over a box).

- `box.log`: before the fix, `lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --mutate=series` reports
  "lemma S holds: True", the mutation not caught (exit 3).
- After the fix, the same mutation is caught (exit 0, "holds: False"): `m3box.log` (M = 3, box 1e-6), `m5box.log`
  (M = 5, rp 0.08, box 1e-6), `m5box9.log` (box 1e-9), and at points `m3pt.log`, `m5pt.log`.
- The certificate's runs after the fix, `s3.json`/`s3.log` and `s5.json`/`s5.log` (`--box=1e-6 --Z=0.004489`, exit 0),
  are byte-identical to the code before the fix run on this Mac. `s1.log`: `lemma6_sector.py --box=1e-9`, ALL CHECKS
  PASS: True.
