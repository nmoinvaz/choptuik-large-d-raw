# I1098-mm5/kfree1000qq: D 1000 p1 harmonics 15-31 released with the qq Jacobian from the start (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The release of `../kfree1000/` restarted on the coordinator's order (2026-11-26 08:55 UTC): the quad-double Jacobian's
inner trials took about 920 s each at D 1000 and floored at D 300 for every harmonic, so every harmonic here starts with the
"qq" Jacobian (quad-double, solved in quad-double). `../kfree1000/README.md` records the stop and keeps the stopped log.

- Input: `input/release_ls_h13_D1000.0000.npz`, git blob 22bb10b98cd4726c5d0ebd09cbd710423329fa57 (the same file as in
  kfree1000, verified with `git hash-object`), from `I1088-dh610/rls1000h13q/`: D 1000, M 32, ks 1517, kc 200, kfreeze 13, Moebius
  horizon (hmob 8). Its Delta is 1.654240854145891738985793904266682194993; its record's quad-double check is 5.4e-43, its
  Hamiltonian check's a rows 7.8e-25, Track C 1.654240854245 +- 7.8e-10.
- Code: worktree `~/Source/choptuik-1098` at 992c86c3 on the 1ccd32ab kernel build, as in kfree300.
- Command, from `~/Source/choptuik-1098/hp`, `~/venv-314`'s python, nice 10, detached under `timeout 8h`, 9 threads:

      python -u form_s.py release_ls <the input here> <this folder> --harm 15,17,19,21,23,25,27,29,31 --kmax 31 \
        --jac qd --res od --tol 1e-48 --tol_h 1e-44 --threads 9 --outer 6 --commit 992c86c3 \
        --jac_by 15:qq,17:qq,19:qq,21:qq,23:qq,25:qq,27:qq,29:qq,31:qq > rls.log

## Bars and what to expect (written 2026-11-26 08:55 UTC, before the run)

| item | bar or expectation |
|---|---|
| released | each harmonic ends with `released` (harmonic step below --tol_h 1e-44, or target \|F\| below --tol 1e-48) within 6 outer steps. `direct_s.jsonl` is written when harmonic 31 is released |
| stop and report | an outer step past 3x the first qq step's time; a harmonic that ends at the outer floor stop (at qq there is no next mode) without being released; an exception; the 8 h timeout |
| time | at D 300 a qq outer step took 87 s (one trial) and the release step 17 s; the serial residual's cost at D 1000 is about 14x (the stopped run's trials), so about 20 min per qq outer step and about 45 min per harmonic (outer 0 and 1 with a trial, outer 2 the release), about 4.5 h in all |
| Jacobian modes | all qq from the start. At D 300 h15's qq outer 1 step was 9.70e-10 against the qd Jacobian's 5.05e-13, and h25-h31 were released at outer 0 by the residual criterion |
| Delta's change | D 300: h15 -4.8083e-17, h17 +4.9397e-18, h19 -3.0887e-19, h21 +3.7004e-21, h23 -4.9622e-24, total -4.34487e-17. The h13 release moved Delta by +2.75e-14 at D 300 and +3.74e-14 at D 1000, so h15 is expected near 1e-16 here, within a factor of a few (a guess from one ratio, not a check) |
| Hamiltonian check | the final record's a rows. D 300's reads 1.06e-20 against 2.8e-22 for its h13 record; the D 1000 h13 record reads 7.8e-25 |

Delta's change per harmonic is computed by `diff_delta.py` on the log's digits (mpmath), never by hand.
