# I477-macm3: the series gate on every stored state behind a mode count, circle or moment result

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/477.
Raw output is not committed here while the raw repository's rewrite pause lasts.

Method. The setup's gate is modecount_common.series_tail against SERIES_TAIL = 1e-15 (#265); hp/series_truncation.py measures it on a stored state "as saved" (its layout, its cut), with no solve and no count, in seconds per state. Command (run_gate.sh, caffeinate -is, nice 10, one thread):
python3 -u hp/series_truncation.py <raw>/I477-macm3/gate_all.jsonl <the states of unique_states_f.txt>
States: every modecount_state_*.npz and lowD_D4 / lowDn_D4 state under the raw I-folders (hp_data_after, states, data_*) and the tracked hp/data (modecount_state_*, lowD_states/lowD*_D4*, states/up*): 396 files found (candidates_all.txt), 361 unique by sha256 (candidates_sha.txt), of which 106 are behind mode counts (unique_states_f.txt: 49 modecount states, 53 M 32 seeds up*, 4 low-D D 4 states); the rest are low-D high-M gamma states (lowDhm, d4hm, highm, lowDmac, t45plan, lowDv, lowDw; failed and ckpt states), not behind a mode count.
A first launch was killed by hand after it began on a lowDhm M 320 state (gate_all_aborted_lowDhm.log). tabulate.py builds table.md from gate_all.jsonl, candidates_sha.txt and the I<n> folder names.
Controls (written before the run, from the issue): lowD_D4.0000_M48.npz and the D 45 kf 21 state without the node must come out refused; lowDn_D4.0000_M48.npz must pass; the third refused state of #441's list (a gamma_dd --Mhi=64 D 55.04 solution) is not a stored state, so the first two I68 D 30 M 64 states of the gate's own selftest stand in. series_truncation.py --selftest (selftest.log) passes 3/3 and --mutate=half fails it, 1/3, exit 1 (selftest_mutate_half.log).

## Results
See the closing summary of the issue. 106 unique states: 6 refused, 100 pass. table.md is the whole table.
