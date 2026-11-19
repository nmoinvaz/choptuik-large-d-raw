# I992-mac: lemma 6b1's M = 1 disc certificates, a second implementation (P2 item 2(b)): logs and records

Machine: the Mac (Apple M5, shared), helper session xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/992.
Code: `solver/proof/review_p2c/p2c_disc.py`, `p2c_disc_compare.py`, `p2c_disc_11_1_growth.py` on branch `wip/p2-6b1b` of
choptuik-large-d (written up in `notes/P2_remaining.md` section 4), `/Users/nathan/venv-314/bin/python`, python-flint
0.9.0, FLINT 3.6.0, nice 10, one process. These files were made in `solver/proof/review_p2c/` and moved here from the
branch before its merge (2026-11-19). Two were renamed without ':' or ',' (cd933da6), and the stale first runs are
labelled `_devel`.

- `p2c_disc_checkint.log`: the integrator against the stored ray boxes, current code (PASS, deviations 9.6e-24 to
  1.3e-20). The equation check prints to the console.
- `p2c_disc_0-0_11-0.jsonl`: discs (0, 0) and (11, 0) during development (section 4.2's fixes).
- `p2c_disc_ray.log`, `.jsonl`: the 12 start-ray discs with the current code, 12 certified; the records equal the
  k = 0 records of `p2c_disc_all.jsonl` apart from timings.
- `p2c_disc_ray_devel.log`, `.jsonl`, `p2c_disc_checkint_devel.log`: the first runs, made before section 4.2's
  development fixes (the series cap of 10, the weight orientation): 0 of 12 discs certified, and integrator
  deviations up to 1.7e-9. They were filed as `p2c_disc_ray.*` and `p2c_disc_checkint.log` and are superseded.
- `p2c_disc_all.log`, `.jsonl`: all 178 at the protocol's inputs (4 x stored box radius + 1e-15): 177 certified,
  (11, 1) Lambda 1.494.
- `p2c_disc_diag_11_1.log`, `p2c_disc_diag_11_1_infl0..3.jsonl`: disc (11, 1) at 0 to 3 x the stored radius.
- `p2c_disc_all_infl2.log`, `.jsonl`: all 178 at 2 x the stored radius + 1e-15: 178 certified.
- `p2c_disc_11-0_r16.jsonl`, `p2c_disc_K1_toolarge.log`: control K1, disc (11, 0) at radius 16: not certified.
- `p2c_disc_ray_mut_sign.jsonl`, `p2c_disc_K2_sign.log`: control K2, the sign mutation: 0 of 12.
- `p2c_disc_compare.log`: the comparison with the stored margins (section 4.3).
- `p2c_disc_11_1_growth.log`: disc (11, 1)'s bound against its input box (section 4.4).
