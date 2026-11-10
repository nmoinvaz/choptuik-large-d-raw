# I445-macm3: the 8 M 40 circles that #252 left on the M 64 states (D 61: 3, D 55: 5), under #252's restated lambda_phys gate

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/445 (was #274).

Inputs, from I252-mac (the M5 Mac): states/modecount_state_D61.0264_M64_kf23.npz and states/modecount_state_D55.0351_M64_kf23.npz (sha256 in state_sha256.txt), and the caches D61/circles and D55/circles
(determinants of the lambda_phys circle, the M 48 circles and the first M 40 circles). Each process has its own copy of a cache (d61/data, d55a/data, d55b/data), so that three processes never write one file.
The command of I252-mac/scripts/run_v2.sh does not run here as written (it names the M5 Mac's python and worktree), so run_445.sh is its equivalent with this machine's paths and options kept
(--kf=23 --n0=20 --fmax=1e-15, the state file as the seed, --tag and --data).

The circles (R as I252 gave them): D 61, in process d61: 1.98 +1.20i (R 0.3, the circle that was stopped), 1.83 +0.49i (R 0.3), 0.032 +3.086i (R 0.2).
D 55, processes d55a: 0.24271 +0.92524i, 0.09923 +4.48036i, 0.34863 +2.61221i (R 0.2); d55b: 0.36031 +2.16089i, 0.59532 +5.03932i (R 0.2). (0.477308 +1.453280i was run by I252.)

Written before the runs (#252's restated gate, scripts/gate_phys_v2.py): in each process the lambda_phys circle (R 0.2) is replayed from its cache (no new determinants), then gated: winding +1, every step below pi/4, 0 verification mismatches, its zero within 3 x
its own estimate and within 1e-3 of lambda_phys (D 61: 2.043532530673195, D 55: 2.04768412771239). A failure stops that D's circles and is reported. Reading (#252, criteria 4 and 5): a winding +1 is reported with the located zero and the measured
position noise (the control's distance from lambda_phys, 5.4e-4 at D 61 and 2.3e-5 at D 55 in #252) beside the circle's own estimate; "keeps its lambda" is within 0.01 of the M 40 position. A winding 0 means no zero in that disc. Estimates are ranges, not bounds.

## Results

