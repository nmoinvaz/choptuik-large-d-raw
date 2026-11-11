# I470-macm3: lambda(64) at D 55.04 at kf 33 and 35 (does the shift keep growing past kf 31?)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/470.
Code: the worktree ../choptuik-large-d-i271 at 408b4d6, as #455 and #465. Raw output is not committed here while the raw repository's rewrite pause lasts.

Commands (run.sh, caffeinate -is, nice 10, one thread, K = 33 then 35): #465's, with the cut changed:
python3 -u hp/gamma_dd.py <raw>/I470-macm3/gamma_M64_kf<K>.jsonl hp/data/states/up10_D55.0351.npz --threads=1 --polish=4 --Mhi=64 --kf48=<K>

Written before the run (the issue's). lam(64) - lam(32) with its floor check at each cut, or the series gate's refusal with its tails, and the sign pattern stated as kept or broken. #455 and #465's pattern: + at kf = 1 mod 4, - at 3 mod 4;
so kf 33 (= 1 mod 4) predicts +, kf 35 (= 3 mod 4) predicts -. Known: kf 31 gave -1.158e-9 (the largest so far), and the gate refused kf 27 and 29 (centre tails 2.1e-12 and 9.4e-14). The M 32 lam must equal 2.0476841277123925 bit for bit.

## Results

Both exit 1 (floor check ABOVE), kf 33 19:28:13 to 19:55:29, kf 35 to 20:15:41 UTC. M 32 lam bit for bit. The gate refused neither.
  kf 33: lam(64) 2.0476841266944525, lam(64) - lam(32) = -1.018e-09, |F| 4.0e-24 (floor), est -1.208e-15, tails 5.6e-85 and 2.0e-34.   kf 35: lam(64) 2.0476841269974173, -7.150e-10, |F| 5.7e-24, est -1.209e-15, same tails.
At kf 31, 33 and 35 the solved states agree: Delta(64) 1.8242712581939433 and Delta_lo -3.633e-17 in all three, est -1.208e-15, 0 Newton steps and 1 LM step, tails equal; only |F| differs (7.1e-24, 4.0e-24, 5.7e-24).
Yet lam(64) - lam(32) is -1.158e-09, -1.018e-09 and -7.15e-10: the root search scatters by 4.4e-10 on states that are the same to 1e-17 in Delta.
