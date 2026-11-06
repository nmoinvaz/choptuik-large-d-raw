# T126-win2: a build of main with the octo-double series (multidouble 4.0.0), for the chain past D ~162

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2; 95.6 GB RAM). Worktree `..\choptuik-t126` at origin/main (hp = a327b97, multidouble "=4.0.0" -- the octo-double jet OJet, its series and solve, octo-double dual Ou; octo-double merged 3ae9e48, notes/OCTO_DOUBLE.md). venv-t126 (Python 3.12, numpy/scipy/maturin, mpmath pinned 1.3.0 for the T81 references). 4 cargo jobs, below normal. choptuik-t115 / venv-t115 left as is (T122 ran there).
Comms entry: 2026-11-06 05:03 UTC cloud to win2 (with the 05:04 ojet_check correction).

This build is the continuation for when T122's quad-double chain ran out (it stopped at D 162.306); the chain would resume with anm_run.py --jet_o 1 on this octo-double build.

1. Build (hp/build.sh, CARGO_BUILD_JOBS=4), log build.log.
2. Checks from choptuik-t126/hp (4 threads): ref (M 48/64/80) vs T81/ref_main.json, scaled vs T81/scaled_main.json, jets vs anm-mac/jets_inputs/jets_inputs.json, jets --mutate=kappa; expected 0,0,0,1. Then ojet_check (octo-double vs quad-double at D 148.74): `ojet_check.py <raw> <raw>/T126-win2/ojet_T113_D148.jsonl --state T113-win/chain/anm_pin3_D148.7434.npz --N 24 --threads 4 --check 0`, log ojet_T113_D148.log; compare d_oq by order with od-mac/ojet_T113_D148.jsonl.
3. Post the build exit/wall/peak, the five exits, ojet_check's order-1 and order-5 errors + the largest relative d_oq difference vs the Mac.
