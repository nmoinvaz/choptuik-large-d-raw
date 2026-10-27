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
- qd_leg.sh (qd_leg_pin7.log, qd_leg_pin5.log, pin{5,7}_D*_pinned*_dz.npz, *_fullcorr.jsonl): the quad-double leg,
  both pins at the waypoints 71-73.1, notes 12.4. qd_fullleg.py (fullleg_pin*.jsonl, logs): the full system from the
  polished states.
