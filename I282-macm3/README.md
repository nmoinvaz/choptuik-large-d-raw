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

