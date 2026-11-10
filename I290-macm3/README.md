# I290-macm3: lam_phys at D 61.03, M 48 by gamma_dd's root search at the cuts kf 13, 21, 23, 25 and 27

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/290. Beside I282, I285 and I286.

Code: the worktree ../choptuik-large-d-i271 at 408b4d6, not main 831d873. Main could not be pulled (SSH to GitHub is down on this Mac and git over
HTTPS is not allowed). The GitHub API's comparison 408b4d6...831d873 lists no file under hp/ except two CSVs in hp/data, so hp/gamma_dd.py and what
it imports are the same in both.

Commands (run.sh, caffeinate -is, nice 10, one thread, one cut after another): the issue's, for K in 13 21 23 25 27:
python3 -u hp/gamma_dd.py <raw>/I290-macm3/gamma_kf$K.jsonl hp/data/seeds/local/up23_D61.0264.npz --threads=1 --polish=4 --M48 --kf48=$K

Written before the run (the issue's rules). A run whose floor check fires or whose M 48 solve stops above --fmax is reported with its |F| and est,
and the next cut runs. Table: lam(48) against kf with |F(48)|, est, the floor verdict and both tails. Each circle's zero (kf 23 2.0435328121,
kf 25 2.043535 +0.000004i, kf 27 2.043502736 -0.000013053i) is compared with the root at its cut, within the circle's own estimate or not.
Each record's M 32 lam must equal 2.043532530673195 bit for bit. The root's resolution is find_lam's, not a bound.

## Results

