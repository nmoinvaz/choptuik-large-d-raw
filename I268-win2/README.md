# I268-win2: the octo-double load check of anm_run.py on the I19-win2 crawl states

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/268 (second part; the coordinator's comment of 2026-11-10 00:19 UTC).

For each state of `../I19-win2/crawl/` that has a row in `hp/data/delta_all.csv` (D 214.6, 214.7, 214.8, 214.9, 215.0, 215.025, 215.03125;
the last file is named `anm_pin3_D215.0312.npz`): `anm_run.py` with the crawl's own options (`--kfreeze 3 --held_fit data/held_fit.json
--N 24 --eps 1e-14 --h_max 0.1 --D_max 220 --corrector od --tol_od 1e-40 --qd_it 12 --od_junk 4 --jet_o 1 --reseed 2 --reseed_q 1
--save_pred 1`, `../I19-win2/README.md`), `--state` = that state and `--steps 0`, so that only the load check runs: the octo-double polish
of the start state from its eight stored parts, with `--reseed 2` inside ElimO, which prints the Newton iterations, the converged line with
Delta and its correction, and the double-double |F| of the first two parts. `--threads 8` instead of the crawl's 18 (beside #228).

Where: the worktree `D:\choptuik-t126` (the project's move to D: took the old `..\choptuik-t126` with it; its `.git` file points to the old
location, so git does not work there, but its `hp/*.py` are identical to e743608, which ran #19 (README of I19-win2), and to c691ae3, which
added `hp/data/delta_all.csv`), venv-t126 (Python 3.12.8, hpkernel 0.1.0, multidouble 0.1.0, numpy 2.5.4). Normal priority.
`run_i268.sh` runs the seven states one after the other (logs `load_D<D>.log`, exits in `exits.txt`). `compare_268.py` parses the
crawl log's block of each accepted state and this folder's log and compares: the converged line (|F| and the Delta with its correction),
the "octo-double Newton" line (steps, max|F|, double-double |F| of the first two parts); `--selftest`.
