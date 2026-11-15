# I817-dh610: the strong-row chord at #713's planted start s0_D252 (D 252.6135), without and with the drop

Machine dh610 (Fedora 45, i7-12700, 20 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/817.

Script (written by the coordinator): `run817.sh`. It runs `octo_corrector.py planted` from #713's start with #777's rerun
flags (`--switch 0 --reseed_o 3 --reseed_start pred --qd 0`) plus `--strong 4`, as two arms side by side at 2 threads
each: `strong4` and `strong4_drop` (`--full_drop 1e-6`). Worktree `choptuik-large-d-817` at main 390d1db9, the main
checkout's .venv (#606's build, after #523's exact projector).

Criteria (#817): pinned max|F| below 1e-40 within 12 steps, with Delta within 1e-30 of the root #816 finds (mac752, on
the Mac). Otherwise the log names where it stops: the first point's projection, the chord stalling, or the Newton steps
after it. The runs do not wait for #816; only the judging does.
