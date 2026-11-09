# I196-win2: lemma 6a(5) at p-hat reproduced on win2, with the cross-load of macm3's B

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/196 (reproduces #184, run on macm3 in I184-macm3/).

`run_i196.sh` runs #184's commands on Python 3.14.10 (`venv-t177`, python-flint 0.9.0, FLINT 3.6.0) from `solver/proof/` of
`D:\choptuik-large-d`, one thread, Normal priority, then #184's controls, `review_39/b_float.py` and its `--mutate=w`, then
`--load-B=` of macm3's B (I184-macm3) at p-hat and `I110-win2/b_diff.py` of the two B files. Pass criteria, written before
the run: rho_6a < 1 at p-hat (own B); the cross-load of macm3's B gives rho_6a < 1; `b_float.py` puts the flow at p-hat
within 0.01 of rad(B); `--mutate=coords` fails, `--mutate=partial` fails, `--mutate=swap` fails and `b_float.py
--mutate=w` exceeds 1, as in I184-macm3. Results are added below as the run ends.
