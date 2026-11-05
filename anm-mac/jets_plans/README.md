# anm-mac/jets_plans: the jets bit-identity reference with its plans, and its checks on the Mac

Machine: the Mac (Apple M5, NEON), the build of main at bfaa03d (venv-qds), hp/highm_check.py jets at main 0ab955c+.

- `compare_200.log`: this build against `anm-mac/release210/jets_200.json`, on its own plans: 28 of 28 bit-identical.
- `jets_plans.json` (`save.log`): the 28 hashes and the three plans (M 32, 48, 64) they were made on.
- `kappa.log`: the control, `--mutate=kappa` against jets_plans.json on its plans: 28 of 28 differ, exit 1.
