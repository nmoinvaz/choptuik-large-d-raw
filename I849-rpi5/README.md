# I849-rpi5: the lemmas around Theorem A(M = 3)'s point certificate reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/849. Script (the coordinator's): `run849.sh`, the rigorous commands of
proof/A_lemmas_M.md section 10 at M = 3 from `solver/proof/` of the worktree `~/Source/choptuik-large-d-849`, with the
controls. Each command has its log here and its exit code and wall time in `exits_849.txt`; the lines marked ctrl must
fail. `env.txt` records the commit and the versions.

- `lemma6b1_runs_M3_rpi5/`: lemma 6b1's covering on the certificate's box p̂ ± 1.1e-9, every row computed here (tag
  `_rpi5`; the stored x86 rows are `_cert`). `lemma6b1_check_M3_rpi5.json`: its check C1-C8.
- `lemmas_M_runs/`: the step (i) tables and lemma S runs this machine wrote.
- `diff_against_stored.txt`: which stored x86 outputs in `lemmas_M_runs/` this machine's runs changed.

Added by the rpi5 runner (the coordinator approved it on #849):

- `run849.sh` started the three covering row jobs together with the C¹ ray run, so they exited 1 (`row_run` needs
  `ray.json`, which the ray run writes at its end). `run849_rows_b.sh` ran the same row commands after `cover_ray`
  exited, then the check and control commands again; its logs and `exits_849.txt` lines end `_b`. The script's own
  `cover_check` and `cover_check_drop11_0` lines (exit 3, "no run") stay as they were.
- `lemma6b1_check_M3_rpi5_b.json` is the check of the rerun. `lemma6b1_runs_M3_rpi5/` holds all twelve rows and the ray.
- `diff_sizes.py`, `diff_sizes.txt`: the size of each change against the stored x86 files (read from the worktree
  and `git show HEAD:`), without the timings. `lemmas_M_runs/mutations_M.json` was copied by hand, since `run849.sh` omits it.
