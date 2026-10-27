# T84-mac: large D toward D = 200, pilot: the pinned continuation with the last node moved toward the horizon

Machine: mac (coordinator). scan_hp.py at wip/qd-horizon dd0186e (~/Source/choptuik-mac-qd2, ~/venv-qd), T80's settings
(comms.txt, T75 and T80 entries), from T75's pin 7 frontier D 73.2657 with its three newest states as history, and
--nodes 0.3,0.4,0.5,0.6,0.7,0.85 (x85) or ...,0.7,0.8 (x80): the horizon series is matched at u0 = 0.15 or 0.2, inside
the radius of about 0.22 that notes/QUAD_DOUBLE.md 12.2 estimates for generic horizon data; with u0 = 0.3, T80 failed
every step from this start (raw/T80, folder T80).

Pass criteria, fixed before the run (T80's pilot rule): within the hour, at least 3 converged points and a median step
in D of at least 0.002 (T75's last steps were 0.0013-0.0018), each point with F_full <= 1e-19 and |dDelta_pin| <=
1e-10. Reported either way: the re-converged start's Delta in the new layout against T75's Delta_full1 at 73.2657.

Files: x85.jsonl, x85_attempts.jsonl, x85.log, pin7_x85_D*.npz; the same for x80. dlist.txt: waypoints 73.30 to 200.00.

## The quad-double Newton on these states (2026-10-27 afternoon; qd_*.py, their logs and jsonl)

- qd_deflated.py: newton_qd with deflation (w 24, 'all' then 'full'), with the junk frozen ('junk'), and plain
  ('control'), on pin7_x85_D73.2707 and pin7_x80_D73.2707: none converges (stalls at 4.7e-14 / 1.8e-14 / 3.2e-17 on
  x85, 4.6e-16 / 8.1e-17 on x80), the step halving with lam 1/2.
- qd_kfreeze.py: the same with p1's harmonics above 7 zeroed and kfreeze 7, on T75's 0.7-layout frontier and on x80:
  stalls (3e-6 at lam 1/32; 1.9e-11 halving).
- qd_weak.py: the quad-double Jacobian's weakest directions at x85 by inverse iteration on the LU: twelve with sigma
  1e-29..1e-24 are p1's harmonics 13, 11, 9, 7, 5, 3 (cos/sin pairs; Delta content 1e-5..1e-2). The two listed with
  sigma 2e-22 and 5e-22 and Delta content 0.6-0.8 are f64 Rayleigh-Ritz noise (qd_jvcheck.py: |J v| = 1.4 along one
  of them, equal to the finite difference), withdrawn.
- qd_scan1d.py: |F(z + t v)| along that direction is linear in |t| (slope 1.4): not weak.
- qd_lucheck.py (f64, inconclusive by cancellation) and qd_ludump.py + qd_luexact.py (python-flint, 320 bits): the LU's
  plain and transposed solves and the Newton step satisfy their equations to 9e-36, 2e-29 and 2e-33 relative, i.e.
  to the quad-double roundoff of |J| |x| (|x| 1.5e29 for a unit right-hand side, so sigma_min(J) is about 1e-29).
  The LU and the Jacobian (finite differences, qd_jvcheck.py) are right; the system is what is singular.
