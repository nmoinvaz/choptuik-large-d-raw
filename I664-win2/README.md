# I664-win2: natural-test A/B on #603's class B refusals (D 236.13, 238.54, 240.12, 249.87)

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads per run. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/664 (queued by the coordinator on the agent-msg channel, messages 1794557834560-0 and 1794558079369-0, 2026-11-13; after #644).
Code: worktree `D:\choptuik-i664` at origin/main 141d9d48 ("newton_od: |dz| to 3 digits and a line per refused trial at verbose 1", #666; printing only, not the iteration); venv-i600 (the #600 build, hpkernel `_hpkernel.cp314-win_amd64.pyd` sha256 4ede9afe..., the kernel #603 runs on). #603's chain is read in place (the bases `I603-win2/chain/anm_pin3_D<base>.npz`) and left running.
Runs (`run_664.sh`, 8 in all, one after the other, own first for each attempt): `anm_run.py ... --steps 1 --a0 <a> --od_accept own|natural` from the base of the refused attempt, #603's other flags:

| attempt | base state | a0 (full precision: D of the refused attempt's target state minus D of its base, from the states' meta) |
|---|---|---|
| 236.13 -> 237.13 | D236.1312 | 1.0 |
| 238.54 -> 239.51 | D238.5375 | 0.9765625 |
| 240.12 -> 240.89 | D240.1244 | 0.762939453125 |
| 249.87 -> 250.47 | D249.8696 | 0.5960464477539062 |

(`hp/data/corrector_attempts.csv` on main rounds a to 6 digits: 1, 0.976562, 0.762939, 0.596046.) Outputs `<attempt>_own/`, `<attempt>_natural/`, logs `<attempt>_own.log`, `<attempt>_natural.log`, starts and exits in `exits_664.txt`.

Acceptance (#664): each `own` run repeats #603's log lines for that attempt; each `natural` run is reported as converged or refused, with its trial lines; where natural converges, its Delta matches #603's state at the same D_str to 1e-40, or the task fails; with a different D_str, report both.

Results follow when the runs end.
