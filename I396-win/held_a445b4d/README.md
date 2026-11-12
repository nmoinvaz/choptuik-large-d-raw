# held_a445b4d: plan_print.py at the faulty commit a445b4dd, on unsolved states (win)

Made by main a445b4dd (`hp: plan_print.py prints a computed plan to the bit and tests its steps`), which leaves the resampled M 48 and M 64 states unsolved (|F| 1.6e-11): its Newton diverges and it lacks setup's Levenberg-Marquardt fallback; its layout check passed anyway (the coordinator's message `choptuik-large-d/2026-11-12/131047Z-coordinator-081b.md`). **Do not use these plans as plans of solved states.** They are kept as a cross-OS comparison of the same unsolved start on two machines (the coordinator's message `132423Z-coordinator-64fa.md`); the Mac's two hashes there are 9a2ee2fa8617a74e... (M 48) and 8ee2918bf799f9a8... (M 64).

Machine win (Surface Laptop 4), worktree `choptuik-i396` at a445b4dd, venv-t151's hpkernel (a build before #523), 3 threads per run at BelowNormal, both runs started together at 13:11 UTC on 2026-11-12 and finished within a minute (14 s and 26 s of compute). Commands: `i396_plan_M48.cmd` and `i396_plan_M64.cmd` (`plan_print.py data/states/up6_D30.0688.npz --M=<M> --kf=none --threads=3 --json=...`).

| run | exit | \|F\| | plan sha256 | control (64 ulps up) | largest step truncation | layout check |
|---|---|---|---|---|---|
| M 48 (`plan_win_M48.*`) | 0 | 1.63e-11 | dccace2ea9209d001bc63a500681feadd2f2c870ead626d1bc9e554fdebac01f | differs (pass) | 4.2e-32 | pass (unsound at this \|F\|) |
| M 64 (`plan_win_M64.*`) | 0 | 1.68e-11 | 414e07cab249c46b2f63fba3994ea702e92ad3f1ebdc89e84657d645a43b6aae | differs (pass) | 7.8e-32 | pass (unsound at this \|F\|) |

The logs also carry `RuntimeWarning: overflow encountered in square` (hpkernel/driver.py:149) and, at M 64, "centre series at x = 0.3: truncation inf".
