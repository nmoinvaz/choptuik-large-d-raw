# I957-dh370: hp-level check of series_o's tangent_from (PR #956), one build, all four steps pass with main's comparison

Machine dh370 (Fedora 45, i7-8700, 12 threads, 31 GB, 8 GB zram swap). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/957

## Build

Worktree `~/Source/choptuik-large-d-957` at the head of PR #956's branch `perf/series-tangent-from` as the issue named it, 954eadcb (detached; on 2026-11-18 06:42 UTC `origin/perf/series-tangent-from` is 7ef16af6, whose tangent commit b7374d3a is the same change of the same size on a newer base: the hunks of `jet_by_order_check.py`, `prec_tests.rs` and `Cargo.toml` have the same patch ids as 954eadcb's, those of `python.rs` and `anm_run.py` differ by context, and 7ef16af6 adds a `--series_split` commit; this build and every result are of 954eadcb), fresh `.venv`
(Python 3.14.10 by `python3.14 -m venv` and `pip install -r requirements.txt`, no uv on this machine; `pip uninstall multidouble` found nothing).
`build957.sh` (unit `i957b`): `hp/build.sh` with `CARGO_BUILD_JOBS=6`, nice 10, and the low-memory recipe the coordinator ordered
(`CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`, the same bits as fat LTO per AGENTS.md), multishoot patched to 4e36b912 by
`hp/Cargo.toml`. 2026-11-18 04:15:28 to 04:48:47 UTC, exit 0, 33 min 19 s, peak RSS 24 080 876 kB (`/usr/bin/time -v`, `build.log`), system used
memory peaked at 27.4 GB (04:20:28, `mem.log`), swap 9 MB. The memory watcher only logs and alerts (the coordinator's rule: no guard that kills), no alert fired.
Two earlier starts were stopped by me after 1 min each (04:13:04, a watcher that could stop the unit; 04:14:29, fat LTO before the recipe was ordered).
Import: `hpkernel avx2 multidouble avx2` (`isa.log`), the .so holds multidouble 4.8.2 and multishoot 3.2.0 at checkout 4e36b91, the Python package is multidouble 482c6835.

## Steps (R = the raw clone's push worktree, ST = `I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz`, ST2 = `.../anm_pin3_D232.0000.npz`, 10 threads, nice 10)

| step | command (from `hp/`) | exit | result |
|---|---|---|---|
| 1 | `cargo test --release --lib oseries_ -- --nocapture --test-threads=1` (`cargo_test_oseries.log`) | 0 | 2 passed in 456 s after a 9 min compile. `oseries_by_order_bitwise`: 0 rows differ in octo-double (serial and threaded), quad-double, double-double, control 9600. `oseries_tangent_accuracy`: from 1 and from 3, 0 rows differ below the order, moved orders within 4.0e-130 and 1.5e-130 in octo-double (bound 2.4e-122), 6.9e-64 and 5.3e-64 in quad-double (1.6e-58), 2.1e-31 and 1.9e-31 in double-double (1.3e-26); control, the kept series not moved: 1.001e0 |
| 2 | default path, `jet_by_order_check.py R ST --N 24 --threads 10 --Np 6` | 1 under the old comparison (`jbo_default.log`), 0 under main's (`jbo_default2.log`) | old: 24 of 24 orders the same bits, but with the planted change order 5 differed (757 entries, `diff_pr.log`): the planted change drives orders 5 and 6 past double range in both forms and the inf and NaN payload bits differ (the coordinator's reading, main 9bff3a1e). New: jets 1680.2 s, by order 721.3 s, ratio 2.33; no order differs, none with the planted change; both controls fire (orders 1 to 6 differ) |
| 3 | `--tangent_from 1` on ST (`jbo_tangent1.log/.json`) | 0 | formed twice 720.8 s, moved from order 1 431.6 s, ratio 1.67; z_1 the same bits; max ρ 6.55e-35 both forms (bound 6.71e-32); control 1.16e+29 (fires); max\|z_k − z'_k\|/max\|z_k\| 0 at order 1, 2.7e-52 at order 2, 6.3e-49 to 1.0e-46 at orders 3 to 24 |
| 3 | `--tangent_from 1` on ST2, D 232.0 (`jbo_tangent1_D232.*`) | 0 | 720.0 s and 430.8 s, ratio 1.67; z_1 the same bits; max ρ 1.38e-36 both (bound 1.41e-33); control 2.74e+29; rel 0 at order 1, 7.0e-51 at order 2, 6.5e-48 to 6.7e-46 at orders 3 to 24 |
| 4 | `--tangent_from 3` on ST (`jbo_tangent3.*`) | 0 | 720.6 s and 435.0 s, ratio 1.66; z_1..z_3 the same bits; max ρ 6.55e-35 both (bound 6.71e-32); control 3.52e+29; rel 0 at orders 1 to 3, 9.9e-50 to 3.2e-48 at orders 4 to 24 |

Per-order ρ_k of the moved series equals the twice-formed series' at every moved order, bit for bit (max |ρ_moved/ρ_twice − 1| = 0, `summary957.log`): ρ_k is
read from the leading parts and looks like the state's own residual floor (6e-35 at D 229.0509) that both forms share (not tested), so the ρ test separates only gross errors
(the control's 1e29), and the differences between the forms are in the last column (rel, 1e-46 and below, rounding amplified by the Jacobian's condition, not a pass criterion).

## What was run and stopped, and the check that changed

- `jbo_default_main.log`: the same default command on the main build of this machine (`~/Source/choptuik-large-d-935`, 808b1fac, multishoot 3.2.0), the coordinator's
  control for step 2; stopped at 1994 s on the coordinator's word (dh610 had reproduced the failure on plain main), no result. `checks957b.sh` is the chain
  that started it (its `diff_main` and later steps never ran).
- `diff957.py` and `diff_pr.log/.json`: the size of the step 2 failure on the PR build (order 5: 757 entries differ in all eight parts, rel nan).
- `nan957.py` (a diagnostic of the nan entries) was dropped on the coordinator's word before it ran and moved to the Trash.
- `jet_by_order_check957.py` is the PR branch's `hp/jet_by_order_check.py` (it has `--tangent_from`; main's has not) with main 9bff3a1e's `same_words` and `differ`
  put in unchanged (finite words compared bit for bit, non-finite ones by place only), run from `hp/` of the build under test. `selftest_differ957.log`:
  payload-only differences pass, a moved non-finite place and one finite ulp fail. `jbo_tangent1.log` is the run with this script (the first run, 10 min with
  the old comparison, was stopped by me, `exits_957.txt`).
- `checks957.sh` (steps 1 and 2 with the old comparison, stopped at the first failure), `checks957c.sh` (diff_pr, then the first start of step 3), `checks957d.sh` (the
  runs of steps 3, 4 and the step 2 rerun with the new script).

## Controls

| control | result |
|---|---|
| step 3 and 4's control `JET_MUT_TANGENT_KEEP` (28) | fires in all three runs, ρ 1.16e+29, 2.74e+29, 3.52e+29 |
| `summary957.py --mutate` (the moved series' ρ times 2^11) | all three runs fail, exit 1 (`summary957_mutate.log`) |
| step 2 controls (kept intermediate dropped; the planted change in the order-by-order form only) | orders 1 to 6 differ in both |
| `differ` of `jet_by_order_check957.py` | `selftest_differ957.log` |
| `diff957.py`'s controls (the jets against itself differs nowhere, the change in one form differs at every order) | ok in `diff_pr.log` |

## Files

`build957.sh` `build.log` `mem.log` `isa.log` `exits_957.txt`; `checks957.sh` `checks957b.sh` `checks957c.sh` `checks957d.sh`; `cargo_test_oseries.log`;
`jbo_default.*` `jbo_default2.*` `jbo_default_main.log` `jbo_tangent1.*` `jbo_tangent1_D232.*` `jbo_tangent3.*` (each `.log` and `.json`); `diff957.py` `diff_pr.*`;
`jet_by_order_check957.py` `selftest_differ957.log`; `summary957.py` `summary957.log` `summary957_mutate.log`.
