# I1098-mm5/kfree1000: D 1000's p1 horizon harmonics 15-31 released (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Order of coordinator t5 (2026-11-26): the same release as I1098-mm5/kfree300, at D 1000. p1's horizon harmonics 15-31 are
held at zero in the full system of record (harmonics 1-13 free); this run releases them one by one (`form_s.py release_ls
--harm 15,17,...,31 --kmax 31`) and records Delta's change for each.

- Input: `input/release_ls_h13_D1000.0000.npz`, git blob 22bb10b98cd4726c5d0ebd09cbd710423329fa57 (verified with
  `git hash-object`), from `I1088-dh610/rls1000h13q/` of this repository: D 1000, M 32, 5 nodes, ks 1517, kc 200, kfreeze 13,
  solved, Moebius horizon (hmob 8). Its Delta is 1.654240854145891738985793904266682194993; its record: quad-double check
  5.4e-43, Hamiltonian check a rows up to 7.8e-25, Track C 1.654240854245 +- 7.8e-10.
- Code: worktree `~/Source/choptuik-1098` at 992c86c3 (wip/large-d-form-s) on the 1ccd32ab kernel build, as in kfree300.
- Command, from `~/Source/choptuik-1098/hp`, `~/venv-314`'s python, nice 10, detached under `timeout 8h`, 9 threads (the
  L50000 solve keeps its own 9):

      python -u form_s.py release_ls <the input here> <this folder> --harm 15,17,19,21,23,25,27,29,31 --kmax 31 \
        --jac qd --res od --tol 1e-48 --tol_h 1e-44 --threads 9 --outer 6 --commit 992c86c3 > rls.log

## Bars and what to expect (written 2026-11-26 08:06 UTC, before the run)

| item | bar or expectation |
|---|---|
| released | each harmonic ends with `released` (harmonic step below --tol_h 1e-44, or target \|F\| below --tol 1e-48) within 6 outer steps. `direct_s.jsonl` is written when harmonic 31 is released |
| stop and report | a harmonic that ends at the outer floor stop without being released; an exception; an outer step 3x past its predicted end; the 8 h timeout |
| time | about 3x D 300's time per outer step (ks 1517 against 306); D 300 took 4 min per harmonic (3 outer steps), so about 12 min per harmonic and 2 h in all |
| Jacobian modes | at D 300 every harmonic's quad-double Jacobian floored at the first outer step and the harmonic went on with the "qq" Jacobian (released in 2 more outer steps); h25-h31 were released at outer 0 by the residual criterion |
| Delta's change | D 300: h15 -4.8083e-17, h17 +4.9397e-18, h19 -3.0887e-19, h21 +3.7004e-21, h23 -4.9622e-24, total -4.34487e-17. The h13 release moved Delta by +2.75e-14 at D 300 and +3.74e-14 at D 1000 (1.4x), so h15 is expected near 1e-16 here, within a factor of a few. A guess from one ratio, not a check |
| Hamiltonian check | the final record's a rows. D 300's reads 1.06e-20 against 2.8e-22 for its h13 record; the D 1000 h13 record reads 7.8e-25. Reported either way |

Delta's change per harmonic is computed by `diff_delta.py` on the log's digits (mpmath), never by hand.

## Stopped (2026-11-26 08:55:25 UTC)

Stopped by hand, with SIGTERM to the `timeout` pid 16875 (python 16876), after 48 min, on the coordinator's order: h15 outer 0
with the quad-double Jacobian took about 920 s per inner trial (D 300: 65 s; the serial octo-double residual scales as ks^2,
1517 against 306), and neither trial flagged a floor, so the halving would have run up to 6 tries (about 1.5 h) before
the "qq" Jacobian, which released every harmonic at D 300. The projection for all nine harmonics was about 15 h, over the 8 h
timeout. No outer step was accepted: `rls.log` holds only

    h15 outer 0 (qd Jacobian) starts 08:07:01 UTC
    h15 outer 0: target |F| 1.27e-42, harmonic-15 step 1.10e-10 (204 s)
    h15 outer 0 trial lam 1: inner NOT converged in 3 steps (|F| 1.71e-38), target |F| 1.71e-38 against 1.27e-42 (1160 s)
    h15 outer 0 trial lam 0.5: inner NOT converged in 3 steps (|F| 2.08e-38), target |F| 2.08e-38 against 1.27e-42 (2082 s)

The run continues in `../kfree1000qq/` from the same input state with `--jac_by 15:qq,...,31:qq`. This folder keeps the log.
