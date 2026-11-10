# I267-macm3: the series gate of gamma_dd.py --Mhi on the planted state (refused, the control without the gate, the override)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/267. Code: branch wip/i271 at 408b4d6, in the worktree
`../choptuik-large-d-i271`. The criteria were written before the runs in `I267-mac/README.md`. The planted state
`states/up6_D30.0688_kc100.npz` is copied from `I267-mac/states/` (`state_sha256.txt`, both lines equal).

The runner is `../I271-macm3/scripts/run_all.sh`, after #271's runs. Every exit is in `logs/exits.txt`.

(b) hp/gamma_dd.py <raw>/I267-macm3/gamma_planted.jsonl <raw>/I267-macm3/states/up6_D30.0688_kc100.npz --threads=1 --polish=4 --M48
(c) the same with --mutate=no_tail_gate, into gamma_no_gate.jsonl
(d) the same as (b) with --series_override, into gamma_override.jsonl

## Results

First attempt (gamma_planted.jsonl, gamma_no_gate.jsonl, gamma_override.jsonl; 05:02:42 to 05:03:32 UTC): all three exit 0 with no M 48 record. With
--polish=4 the planted state's M 32 residual ends at 1.2e-20, above --fmax 1e-20, so it is skipped before the gate. The gate was not tested.

Second attempt (coordinator, 05:06 UTC, chosen after seeing the first): the same three with --fmax=1e-19, into gamma_planted_fmax.jsonl,
gamma_no_gate_fmax.jsonl and gamma_override_fmax.jsonl (`../I271-macm3/scripts/run_second.sh`). The criteria of I267-mac/README.md are unchanged.

