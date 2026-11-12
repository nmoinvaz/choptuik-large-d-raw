# I396-win: hp's computed node and segment plans at M 48 and 64 on Windows (win), for the diff with the Mac's

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/396 (the coordinator's messages `choptuik-large-d/2026-11-12/131002Z-coordinator-2bc9.md`, `131047Z-coordinator-081b.md` and `132423Z-coordinator-64fa.md`). venv-t151's hpkernel (a build before #523: `Solver.plan` is unchanged by it, the coordinator says), python-flint 0.9.0, Python 3.10. Nothing is built. Each run is 3 threads at BelowNormal under `I462-win/run_capped.py` with a cap of 7200 s; the two runs of a set start together (6 busy threads).

**The runs of main 179afc4c** (`hp: plan_print.py solves the resampled state before planning it`; worktree `choptuik-i396b`), started 13:25:13 UTC on 2026-11-12: `i396_plan_M48.cmd` and `i396_plan_M64.cmd`, `python -u plan_print.py data/states/up6_D30.0688.npz --M=<48|64> --kf=none --threads=3 --json=<raw>/I396-win/plan_win_M<M>.json`, `--fmax` at its default 1e-15, with the log `plan_win_M<M>.log` and the exit code `plan_win_M<M>.exit`. Each run resamples the state to M tau points, fits the nodes and re-converges (Newton, then Levenberg-Marquardt where Newton stops above `--fmax`; a state above it is refused) in a fresh temp cache (`tempfile.mkdtemp`, so nothing cached on win is read and the two parallel runs do not share one), prints the plan to the bit (the nodes and every segment's x points as hex floats, the plan's sha256), tests every planned Taylor step once and as two half steps against the target 1e-32, and runs its built-in control (a plan made again with the tolerance 64 ulps up must have a different hash). It exits 1 when its layout check or the control fails.

**`held_a445b4d/`** holds the first two runs, made by the faulty commit a445b4dd on unsolved states (|F| 1.6e-11), kept as a cross-OS comparison with the Mac's runs of the same commit; see its README. They are not plans of solved states.

**What it decides (the coordinator's).** Post each run's plan sha256, |F| and truncation line, with the exits, on #396; the coordinator diffs the JSONs with the Mac's.

## Result (main 179afc4c)

Both runs ended with exit 0 and no Traceback: M 48 at 13:29:42 UTC (269 s of compute), M 64 at 13:28:47 UTC (213 s), from 13:25:13 UTC. Both pass the layout check and the built-in control (the plan made again with the tolerance 64 ulps up has another hash: 94478b3e3cdf8b4b... at M 48, 5f13060a23af51ca... at M 64).

| run | exit | \|F\| | plan sha256 | largest step truncation (target 1e-32; meets it within 100 times) | layout check |
|---|---|---|---|---|---|
| M 48 (`plan_win_M48.*`) | 0 | 9.01e-18 (Newton stops at 1.6e-11, Levenberg-Marquardt takes it down) | 1afd6f2399792eb12167cef9fa07bde22e3b62ed1c803c1ff84ad58bab2eff0f | 4.6e-32, meets it | pass |
| M 64 (`plan_win_M64.*`) | 0 | 2.34e-26 (Newton stops at 1.7e-11, Levenberg-Marquardt takes it down) | 9fe18b9e83771c40980aa6fce3991dbf006d768fbaf5e996ff34b84542a9387b | 8.3e-32, meets it | pass |

Segments (largest step truncation, then the end of the segment against the next node): M 48 has 4 segments (4.6e-32, 3.7e-32, 3.8e-32, 3.7e-32; 1.9e-21, 1.7e-21, 1.0e-20, 9.0e-18, the last bounded by |F|), M 64 has 5 (5.9e-32, 4.3e-32, 6.5e-32, 5.4e-32, 8.3e-32; 1.7e-31, 1.5e-31, 1.1e-31, 4.3e-29, 2.3e-26). The M 64 log also prints "centre series at x = 0.3: truncation inf" and the `RuntimeWarning: overflow encountered in square` that Newton's first step on the resampled state prints; the runs of the faulty commit in `held_a445b4d/` print the same lines.

**Against the Mac's values, as the coordinator quoted them** (the Mac's plan hashes at 179afc4 are not on GitHub yet, so no plan diff is made here): |F| at M 48 is 9.01e-18 here and 9.0e-18 there (equal); |F| at M 64 is 2.34e-26 here and 1.7e-26 there, which differ, so the Levenberg-Marquardt solutions are not the same to that precision and the plans can differ for that reason alone.

**Control: win against win** (`plan_win_M48_rerun.*`, `plan_win_M64_rerun.*`, the same two commands, `i396_plan_M<M>_rerun.cmd`, 13:30 to 13:34:32 UTC, exit 0): the second runs have the same plan sha256 and |F| as the first, and all 16 fields of each json are equal (the nodes, every segment's x points as hex floats, |F|, the hashes, the segments' truncations). So a plan hash on win is reproducible run to run, and a hash difference against the Mac is not run-to-run noise of this machine.

**The faulty commit a445b4dd** (`held_a445b4d/`, its own README): the hashes there are dccace2ea9209d00... (M 48) and 414e07cab249c46b... (M 64), against the Mac's 9a2ee2fa8617a74e... and 8ee2918bf799f9a8... at the same unsolved start.
