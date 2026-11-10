# I282-macm3: the lam_phys circle at D 55.04, M 64, kf 23 at R 0.05, with (node/) and without (nonode/) the centre node at 0.15

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main bfe5fd54 (origin/main d2a75f4 differs in no file of hp/ that these runs read).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/282. Beside #271's script and I280, I285, I286.

Commands (node/circle.cmd and nonode/circle.cmd, caffeinate -is, nice 10, one thread each, both at once): the issue's (a) and (b) as written.
States, copied into hp/data before the start so that each setup loads its saved state (state_sha256.txt): (a)
I275-macm3/hp_data_after/modecount_state_D55.0351_M64_kf23_ct1e-150.npz (this machine, #275); (b) I252-mac/states/modecount_state_D55.0351_M64_kf23.npz
(the M5 Mac, #252). A Newton or LM line in a log means the state was refitted, and is reported. Both caches start empty, so every determinant is new.

Written before the run. Stop, per circle: setup |F| above 1e-15, (a) without a node at 0.15, or (b) with one. Acceptance: both circles wind +1 with
estimates below 3e-6. Report: each zero's miss from 2.04768412771239 with its estimate, against #275's 1.095e-5 and #252's 2.3e-5. The factor between
the two misses is called resolved only if the misses differ by more than the sum of the two estimates. Estimates are ranges, not bounds.

## Results

Both exit 0 (nonode 05:33:35 UTC, node 05:36:09 UTC; started 04:40 UTC, awake under caffeinate). Both states loaded with no Newton or LM line and
are unchanged (sha256 as before); they are in hp_data_after/ and hp/data is back without them. 30 determinants each.
  (a) node (nodes 0.15, 0.3 ... 0.7, |F| 3.6e-20): winding +1, 28 points, max step 0.351, 0 mismatches, 0 alias bisections; zero
      2.0476801581 +0.0000020922i, estimate 5.2e-06; miss from 2.04768412771239: 4.49e-06 (Re -3.97e-06, Im +2.09e-06).
  (b) no node (innermost 0.3, |F| 2.1e-20): winding +1, 28 points, max step 0.351, 0 mismatches, 0 alias bisections; zero
      2.0476818248 +0.0000045415i, estimate 8.6e-06; miss 5.09e-06 (Re -2.30e-06, Im +4.54e-06).
Acceptance: both wind +1; both estimates (5.2e-06, 8.6e-06) are above 3e-6, so it fails. By the rule written before the run the misses differ by
6.0e-07, far less than the sum of the estimates (1.4e-05): the factor between them (1.13) is not resolved.
