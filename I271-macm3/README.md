# I271-macm3: the remaining runs of #271, gamma_dd.py --M48 on the new path (the old-rule control at D 50, D 20, 30, 40 and 58)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/271. Code: branch wip/i271 at 408b4d6, in the worktree
`../choptuik-large-d-i271`. The criteria were written before the runs in `I271-mac/README.md`, and they are not
repeated here. Run (a) is the Mac's (`I271-mac`), and (d) is not among the runs given to macm3.

The runner is `scripts/run_all.sh` (caffeinate -is, nice 10, one thread, one run at a time), which also makes #267's
three runs into `I267-macm3/`. Every exit is in `logs/exits.txt`.

(b) hp/gamma_dd.py <raw>/I271-macm3/gamma_old_rule.jsonl hp/data/states/up8_D50.0075.npz --threads=1 --polish=4 --M48 --mutate=old_rule
(c) hp/gamma_dd.py <raw>/I271-macm3/gamma_dd.jsonl hp/data/states/up2_D20.0437.npz hp/data/states/up6_D30.0688.npz hp/data/states/up7_D40.0201.npz --threads=1 --polish=4 --M48
(e) hp/gamma_dd.py <raw>/I271-macm3/gamma_dd.jsonl hp/data/states/up12_D58.0060.npz --threads=1 --polish=4 --M48

## Results

