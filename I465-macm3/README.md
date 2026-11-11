# I465-macm3: lambda(64) at D 55.04 at kf 27, 29 and 31 (does the sign pattern with kf mod 4 of #455 hold?)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/465.
Code: the worktree ../choptuik-large-d-i271 at 408b4d6, as #455 and #291. Raw output is not committed here while the raw repository's rewrite pause lasts.

Commands (run.sh, caffeinate -is, nice 10, one thread, K = 27, 29, 31 one after another): #455's, with the cut changed:
python3 -u hp/gamma_dd.py <raw>/I465-macm3/gamma_M64_kf<K>.jsonl hp/data/states/up10_D55.0351.npz --threads=1 --polish=4 --Mhi=64 --kf48=<K>

Written before the run (the issue's). Acceptance: lam(64) - lam(32) with its floor check at each cut, and the sign pattern stated as kept or broken. #455's pattern: + at kf 13, 17, 21, 25 (kf = 1 mod 4) and - at 15, 19, 23 (kf = 3 mod 4), rms 3.1e-10.
So the pattern predicts: kf 27 (= 3 mod 4) negative, kf 29 (= 1 mod 4) positive, kf 31 (= 3 mod 4) negative. A series gate refusal or a solve above the floor is reported with its tails and est, and the next K runs. The M 32 lam must equal 2.0476841277123925 bit for bit.

## Results

All three exit 1 (kf 27 17:16:42 to 17:53:08, kf 29 to 18:22:53, kf 31 to 18:51:53 UTC; the Mac was shared with 5 other jobs). M 32 lam equals 2.0476841277123925 bit for bit in all three.
  kf 27: series gate REFUSED at the solution (centre 2.1e-12, ratio 0.932; horizon 3.1e-23), |F(64)| 1.8e-20 (lm), est -2.2e-14 ABOVE, no lam.   kf 29: REFUSED (centre 9.4e-14, ratio 0.910; horizon 4.1e-25), |F| 3.4e-21 (lm), est +2.35e-14 ABOVE, no lam.
  kf 31: lam(64) 2.047684126554028, lam(64) - lam(32) = -1.158e-09, |F| 7.1e-24 (floor), est -1.21e-15 ABOVE, tails 5.6e-85 and 2.0e-34, not refused.
