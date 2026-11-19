# I1019-mac: B5(1), an independent check (P2 item 5), starting with whether its data cover (H8)'s certified delta

Machine: the Mac (Apple M5, shared), helper session xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1019.
Code: choptuik-large-d main c39ed13e (branch `wip/p2-b5`), `/Users/nathan/venv-314/bin/python`, python-flint 0.9.0,
nice 10, one process.

## delta/: the first question (2026-11-19)

- `b5_jump_stored_delta.log`: `python3 b5_jump.py` as stored, which reads (H8)'s delta from `b8m_h8_K4_L73.89.log` at full
  precision; identical to the repository's `b5_jump.log`: x_Phi = (39784.4, 38775.8), C_E = 2.532366e+33.
- `h8_rounded_up.log`, `b5_jump_rounded_up.log`: the same with B8_constants.md 8.3's rounded-up delta
  (8.3e-5, 79.04, 3.232, 6.464) given by `--h8log`: x_Phi = (39789.7, 38781.0), C_E = 2.532706e+33.
- `b5_threshold_superposition.log`: `b5_threshold.leading_data_bound` with its DELTA0 (0, 76.56, 3.23125, 6.46251),
  with the leading coefficients rounded up (0, 76.5602, 3.231259, 6.462517), and with (H8)'s rounded-up delta.

## b5/: B5(1) recomputed (protocol: notes/P2_remaining.md 6.1 at 5e09a010)

Code: `solver/proof/review_p2c/p2c_b5.py` on `wip/p2-b5` at 6487a5f7, mpmath (256 bits).
- Stage A, `logs/model.log`, `phiz.log`, `phiz_mut_G0.log`: Lemma 1 against B8's reduced system, section 1.3's Phi_z
  against the total derivative, Lemma 2's G0 against the eps -> 0 limit; K2 (G0's C B0 P/(2z) term dropped) must fail.
- Stage B, `logs/residual*.log`: Lemma 3 from the eps-expansion on the inner series; K1 as the protocol wrote it
  (`offsol`) and the off-solution control K1b (`offphi`).
- `logs/exits.txt`: every run's exit code.
- Stage C, `run_c.sh` (code 5f58c30b), `logs/sector_*.log`, `p2c_b5_*.json`: the sector constants on 3073 cells (at the
  box centre and over the box), L, the Perron norm and the certified super-solutions; the controls K3 (Phi <- C x 1.5,
  the protocol's), its x 2 supplement and Phi <- P x 2 (B5_inner.md 6's own mutation). The box run was repeated at
  d3d9cdef after its centre-only checks were made centre-only (`exits_c.txt` lists both; the numbers are the same).
