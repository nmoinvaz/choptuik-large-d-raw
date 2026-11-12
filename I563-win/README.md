# I563-win: near_null.py on the stored plan by default, one run at crawlJ's D 242.3642 state

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/563 (the coordinator's message `choptuik-large-d/2026-11-12/111444Z-coordinator-5e89.md`). Worktree `choptuik-i563` at main d020d584 (`hp: near_null.py factors the state's stored plan by default`; `hp/src`, `Cargo.toml` and `pyproject.toml` are unchanged since 14dc3863, so venv-t151's hpkernel is the build), 2 threads at BelowNormal beside #587's 3, under `I462-win/run_capped.py` with a cap of 14400 s.

`i563_nn_default.cmd`: `near_null.py <raw> I461-win2/crawlJ/anm_pin3_D242.3642.npz --threads=2 --json=<raw>/I563-win/nn_default.json`, with no `--keep_plan`, so the default applies. The state is #461's crawlJ state at D 242.3642; this raw clone lacked it, so it was copied (untouched, not pushed from here) from the up-to-date raw worktree, sha256 identical. Output: `nn_default.json`, `nn_default.log`, `nn_default.exit`.

**What it decides (the coordinator's).** The default took the stored plan: the json's `plan` is "stored", sigma_1..sigma_4 print as 2.551e-27, 2.530e-27, 4.392e-26 and 7.930e-26, and the pinned step line prints max 8.118e-38, norm 5.049e-37, Delta +9.965e-40, all as #501's `s07_keep`. A step of about 9.4e-15 would mean the default did not take the stored plan, and fails. (The issue's own acceptance names both of #501's starts and both plans; this run is the one at crawlJ's D 242.3642 state that the coordinator assigned.)

## Result

**The check passes.** The default run (`nn_default.*`) started 11:16:05 UTC and ended 11:23:42 UTC (7.6 min; the octo-double LU took 208 s), exit code 0, no Traceback, `check: pass`. The expected 2 h was an overestimate for this machine. It ran beside #587.

| quantity | #563 default run | #501 `s07_keep` | the coordinator's value |
|---|---|---|---|
| json `plan` | **stored** | stored | "stored" |
| sigma_1 | 2.551e-27 | 2.551e-27 | 2.551e-27 |
| sigma_2 | 2.530e-27 | 2.530e-27 | 2.530e-27 |
| sigma_3 | 4.392e-26 | 4.392e-26 | 4.392e-26 |
| sigma_4 | 7.930e-26 | 7.930e-26 | 7.930e-26 |
| pinned step max | **8.118e-38** | 8.118e-38 | 8.118e-38 |
| pinned step norm | **5.049e-37** | 5.049e-37 | 5.049e-37 |
| pinned step Delta | **+9.965e-40** | +9.965e-40 | +9.965e-40 |
| `\|\|J v_1\|\| / sigma_1` | 0.999424 | 0.999424 | |

The pinned step line is identical to #501's, including V^T dz (+1.01e-38 -1.51e-38 +2.50e-39 +6.92e-40) and the share on span(V) (0.0363). The step is 5.0e-37, not about 9.4e-15, so the default took the stored plan.

**Against #501's `s07_keep` run** (the Mac; `ref_501_near_null_s07_keep.{json,log}` are copies from the raw repository): the logs are line-for-line the same except the timings (LU 208 s here, 802 s there) and the convergence figure of sigma_3 (8e-16 here, 5e-16 there, a quantity at rounding level). `cmp_json.py` (`compare_json_vs_501.txt`): the two jsons have the same structure and the same non-numeric fields; of 575 numbers 129 differ, the largest relative differences being 6.5e-15 in the V^T dz entries of the step, 4.7e-15 in those of the pinned step, and 1e-16 in the sigma_i, which is double-precision rounding between two machines. Control (`control_json_mutated.txt`): sigma_1 changed by 1e-6 relative, and the comparison reports exactly that one number.

**Control: the check can fail** (`nn_keep0.*`, the same command with `--keep_plan=0`, 11:24:30 to 11:32:25 UTC, exit 0): json `plan` "new"; the pinned step is max 1.248e-15, norm 9.378e-15, Delta +9.228e-17 (the 9.4e-15 of the re-made plan) and its share on span(V) is 1.0000; sigma_1..sigma_4 print the same, 2.551e-27, 2.530e-27, 4.392e-26 and 7.930e-26, as the issue says ("sigma is the same on both plans"). So the step line separates the two plans, and the default run is on the stored one.

**What this run does not cover.** The issue's own acceptance names both of #501's starts and both plans; this run is the one the coordinator assigned, at crawlJ's D 242.3642 state with the default plan, with the `--keep_plan=0` control on the same state.
