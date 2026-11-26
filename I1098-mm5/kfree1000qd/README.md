# I1098-mm5/kfree1000qd: D 1000 p1 harmonics 15-31, qq Jacobian, qd residual (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The release of `../kfree1000qq/` restarted on the coordinator's order (2026-11-26 08:57 UTC): the release's residual runs in
quad-double (`--res qd`), since the serial octo-double residual costs about 920 s per inner trial at D 1000 and the
quad-double floor sits far below the 1e-48 tolerance (the jump agent's advice, as in rls2000d: solved in qd, checked in od).
The final record's end check is in octo-double (release_ls: `chk = "od" if res == "qd"`); its `F_check_precision` must read od.
`../kfree1000qq/README.md` records the stop of the previous run; `../kfree1000/README.md` the first.

- Input: `input/release_ls_h13_D1000.0000.npz`, git blob 22bb10b98cd4726c5d0ebd09cbd710423329fa57 (the same file as in
  kfree1000, verified with `git hash-object`), from `I1088-dh610/rls1000h13q/`: D 1000, M 32, ks 1517, kc 200, kfreeze 13, Moebius
  horizon (hmob 8). Its Delta is 1.654240854145891738985793904266682194993; its record's quad-double check is 5.4e-43, its
  Hamiltonian check's a rows 7.8e-25, Track C 1.654240854245 +- 7.8e-10.
- Code: worktree `~/Source/choptuik-1098` at the head of wip/large-d-form-s, 0706d878 (Python only: form_s.py's
  release_joint and its hand-over of a qd or dd inner solve that stops unconverged, which does not touch qq; and hp/src/python.rs's M = 48
  instances, which the installed 1ccd32ab kernel build does not have and an M = 32 run does not use; no rebuild), on the
  1ccd32ab kernel build as before.
- Command, from `~/Source/choptuik-1098/hp`, `~/venv-314`'s python, nice 10, detached under `timeout 8h`, 9 threads:

      python -u form_s.py release_ls <the input here> <this folder> --harm 15,17,19,21,23,25,27,29,31 --kmax 31 \
        --jac qd --res qd --tol 1e-48 --tol_h 1e-44 --threads 9 --outer 6 --commit 0706d878 \
        --jac_by 15:qq,17:qq,19:qq,21:qq,23:qq,25:qq,27:qq,29:qq,31:qq > rls.log

## Bars and what to expect (written 2026-11-26 08:57 UTC, before the run)

| item | bar or expectation |
|---|---|
| released | each harmonic ends with `released` (harmonic step below --tol_h 1e-44, or target \|F\| below --tol 1e-48) within 6 outer steps. `direct_s.jsonl` is written when harmonic 31 is released |
| record | `F_solve_precision` qd, **`F_check_precision` od** (it must read od), the Hamiltonian check |
| stop and report | an outer step past 3x the first outer step's time; a harmonic that ends at the outer floor stop without being released; an exception; the 8 h timeout |
| time | the first outer step's time is reported; the quad-double residual is several times cheaper than the octo-double one (D 300 qq outer step: 87 s with od), so the 20 min per qq outer step estimated for od should fall to a few minutes |
| Jacobian modes | all qq from the start. At D 300 h15's qq outer 1 step was 9.70e-10, and h25-h31 were released at outer 0 by the residual criterion |
| Delta's change | D 300: h15 -4.8083e-17, h17 +4.9397e-18, h19 -3.0887e-19, h21 +3.7004e-21, h23 -4.9622e-24, total -4.34487e-17. The h13 release moved Delta by +2.75e-14 at D 300 and +3.74e-14 at D 1000, so h15 is expected near 1e-16 here, within a factor of a few (a guess from one ratio, not a check) |
| Hamiltonian check | the final record's a rows. D 300's reads 1.06e-20 against 2.8e-22 for its h13 record; the D 1000 h13 record reads 7.8e-25 |

Delta's change per harmonic is computed by `diff_delta.py` on the log's digits (mpmath), never by hand.
