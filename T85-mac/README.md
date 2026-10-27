# T85-mac: large D 73.27 to 200 in double-double, steps of 1, two layouts side by side (A: last node 0.8, B: 0.85)

Machine: mac (coordinator), 2026-10-27. scan_hp.py at wip/qd-horizon dd0186e (~/Source/choptuik-mac-qd2, ~/venv-qd),
the pinned system (pin 7, --qdh 1) as T75/T80, from T75's pin 7 frontier 73.2657 with its waypoints 70.65, 71.5 and
72.4 as the cubic predictor's history, --nodes to 0.8 (A, x80) or 0.85 (B, x85): T84's jump ladder (folder T84-mac)
showed that in the 0.85 layout single steps of 0.5 to 5 from 73.27 converge, and that the full-system Delta
(Delta_full1, the pinned Delta plus the linearised full-system correction) then agrees with the rational formula to
about 1e-6, while T84's x80 pilot points agree with it as T75's do (5e-8).

Waypoints 74, 75, ..., 200 (dlist.txt), so that both runs land on the same D. tol 1e-19 fixed (no --tol_growth), 6 h,
2 threads each, below normal priority. A point counts when the scan converges it (|F| <= 1e-19).

Written before the run. What is reported: per waypoint, Delta_full1 of A and B and A - B (the cross-check between
layouts, as T75's pin 5 / pin 7 was), the last D of each run, and how the steps fail if they do. The A - B difference
is the uncertainty of Delta_full1 at that D (a spread between two discretisations, not a bound). The formula is not a
reference: these points test it. Expected from T84: A - B near 1e-6 at D 74-78; unknown beyond.

Files: x80.jsonl, x80_attempts.jsonl, x80.log, pin7_x80_D*.npz; the same for x85. Copied into the data repository's
T85-mac/ at each post.

## Outcome (2026-10-27, 17:40 UTC)

Both runs ended on their own (four failed steps in a row). B (0.85) at D 76.48 after 5 points: at 76.40-76.48 its
pinned Delta jumped by 3.6e-3 between two converged points (|F| 1e-25, dDelta_pin +-2e-3), it had left the branch along
the undetermined directions, and every step after that failed with |F| 1e62-1e102. A (0.8) at D 78.12 after 11 points
(last converged 77.8806), its steps shrinking from 1 to 0.005; its Delta_full1 stays within 1e-7 of the rational
formula at every point (ab_table.py; the formula is a plausibility check, not a reference). The waypoints both runs
share: 74, 75, 76, with |A - B| 3.4e-7, 8.3e-7, 2.3e-7. So neither layout maps the branch to D = 200 in double-double;
the points to 78 stand at the 1e-6 level.
