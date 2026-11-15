# I838-macm3: #749's box near Re 3 at D 61.03 at M = 64: kf 47, then uncut

Machine macm3 (M3 Mac, 6 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/838.

Scripts (the coordinator's): `common.sh` and `job.sh` (#789's, with M = 64), `run_838_pilot.sh` (the kf 47 control
alone, which makes the M 64 state) and `run_838_kf47.sh` (the four R 0.36 circles). Small circles follow, placed from
their zeros; the uncut cut (kf 63) comes after kf 47. Worktree and build as #749 (choptuik-large-d-749 at bd7df22f).

Criteria (#838): the control winds +1 with 0 mismatches and the setup's |F| ≤ 1e-15; every circle 0 mismatches,
windings up to 6; the count with its basis against M = 48's 11 at kf 47; the near-axis zeros against M = 48's.
