# I1088-mm5: form-S direct solves at large D on the Mac mini M5 Pro (#1088)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1088

Setup of the machine, hp's release build of `wip/large-d-form-s` and its selftests. Code: worktree
`~/Source/choptuik-formsq`, detached at origin/wip/large-d-form-s 1ccd32ab (the head at 2026-11-26 02:25 UTC).
Python: uv's 3.14 in `~/venv-314`, from requirements.txt. Rust: stable by rustup.

## Expected results (written 2026-11-26 02:28 UTC, before any selftest ran)

| check | command (from the worktree, `~/venv-314` active) | expected |
|---|---|---|
| build | `CARGO_PROFILE_RELEASE_STRIP=false nice -n 10 hp/build.sh` (multidouble's Python package uninstalled first) | exit 0; the last line `hpkernel <isa> multidouble <isa>` with a NEON isa; wall about 31 min and 24 GB peak (AGENTS.md; macm3 took 31.1 min, #1058) |
| import | `python -c "import hpkernel; print(hpkernel.__file__)"` | a path in `~/venv-314/lib/python3.14/site-packages/hpkernel/`, not the worktree's `hp/python` source |
| floor stop | `python hp/floor_stop_check.py` | exit 0; `dd steps 2 (floor True), qd steps 1 (chord [True], reform [False]), Jacobians formed 2, converged True: PASS` |
| floor stop, control | `python hp/floor_stop_check.py --mutate=nofloor` | exit 1; `FAIL`, with eight dd steps at the floor (#1088, 2026-11-26 00:04 UTC post) |
| floor stop, stale J | `python hp/floor_stop_check.py --stale` | exit 0; the qd stage takes 2 steps, the first a chord step with reform |
| form S | `python hp/form_s.py check hp/data/states/up2_D20.0437.npz` | exit 0; converged in 3 steps; Delta_S 2.1111402926144795056; Delta_S - Delta_A about -2.03e-17 (dh610: -2.03e-17); form S at the form-A state \|F\| about 8.4e-12 |
| form S, control | the same with `--mutate flux` | the control fires. On dh610 the form-S residual at the form-A state jumps from 8.4e-12 to 1.7e-2, Newton takes no step (lam 0, proposed dDelta +2.96e-2), `NOT converged`, and Delta_S - Delta_A prints 0.0 because no step was accepted. Here it must show a residual and a proposed dDelta far above the clean run's. A control that reproduces the clean run's 8.4e-12 fails |

- The stored double-double states are in the code repository's `hp/data/states/`, not in this repository.
- `form_s.py check` always exits 0; its verdict is in the printed lines. The tolerance of a bit-identity claim
  (AGENTS.md: every ISA gives the same bits) is the printed Delta_S digits against dh610's, as far as the stored log
  shows them.
- Files here: `build.log` (the build's output with `/usr/bin/time -l`), `build_time.txt`, `mem_samples.log`
  (resident memory of the build's processes every 20 s), `uninstall.log`, and the selftests' logs.

## Results (2026-11-26 02:48 UTC)

| check | exit | result | against the expectation |
|---|---|---|---|
| build | 0 | 02:26:51 to 02:47:32 UTC, **1240.7 s (20.7 min)** wall (`/usr/bin/time -l`: 1231 s user, 27.6 s sys); peak resident **24.81 GB (23.1 GiB)** by `/usr/bin/time -l`, 23.98 GB in the 20 s samples (02:35:12 UTC); last line `hpkernel neon multidouble neon` | shorter than the expected 31 min; memory as expected |
| import | 0 | `/Users/nathan/venv-314/lib/python3.14/site-packages/hpkernel/__init__.py` (`import_path.txt`) | as expected |
| floor stop | 0 | `dd steps 2 (floor True), qd steps 1 (chord [True], reform [False]), Jacobians formed 2, converged True: PASS` | as expected |
| floor stop, `--mutate=nofloor` | 1 | `dd steps 8 (floor False) ... FAIL` | as expected: the control fires |
| floor stop, `--stale` | 0 | `dd steps 2, qd steps 2 (chord [True, False], reform [True, False]), Jacobians formed 3: PASS` | as expected |
| `form_s.py check` up2_D20.0437 | 0 | converged in 3 steps; Delta_S 2.1111402926144795056; Delta_S - Delta_A **-2.03e-17**; - delta_all -6.81e-17 | as expected, and every printed digit equals dh610's `out/check.log` (the iterations' \|F\|, \|dz\| and dDelta too) |
| the same, `--mutate flux` | 0 | form S at the form-A state \|F\| **1.73e-02** (clean 8.39e-12); Newton's proposed step has \|dz\| 5.95e+06 and dDelta +2.958e-02, every trial is rejected (lam 0), so `NOT converged` and Delta_S - Delta_A prints **0.0** | the control fires on the residual and the proposed dDelta, like dh610's `out/check_flux.log`. It does **not** move the printed Delta: no step is accepted. 35 panic lines (`form_s.rs:226`, "the slaving LU of a Taylor step: singular or non-finite pivot at column 0 (NaN)") come from rejected trials, and the process still exits 0 |

- The dd selftests and the check use the stored state `hp/data/states/up2_D20.0437.npz` of the code repository
  (M 32, K 8, ks 100). No double-double state of the raw repository was needed.
- The build is of 1ccd32ab (wip/large-d-form-s, 2026-11-26 02:20 UTC head at the time) on Rust 1.100.0 with multidouble
  5.1.0, multishoot 4.1.0 and multisolver 0.2.2 from crates.io, and multidouble's Python package at 8c4360ac. Versions of
  everything are in `versions.txt`.
- Not run: `highm_check.py ref`, `scaled` and `jets` (the stored-reference bit checks), which the order did not ask for.
- Exit codes: `selftest_exit_codes.txt`. Logs: `build.log`, `floor_stop*.log`, `form_s_check*.log`.
