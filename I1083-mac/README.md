# I1083-mac: the matched mode determinant at D 3.044375 and 3.15 (sonic valley, match_node), Mac runs

Machine: the shared Mac (Apple silicon, 2 threads per process, at most 2 processes, nice 10), hpkernel build of
2026-11-08 (`/Users/nathan/venv-314`, Python 3.14), not main's multishoot 4.1.0 build. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1083. Branch `wip/mode-horizon-1083` of choptuik-large-d (the
note `notes/MODE_HORIZON.md`, the script `hp/mode_matched.py`). Subagent of the coordinator, 2026-11-24.

States (from this repository): `I1072-dh370/states3/...D3.0444...L0.4_M96_s1.9635.npz` (blob 6a0f83d2) and
`I1072-dh370/states2/...D3.1500...L0.7_M96_s1.8326.npz` (blob 9e683a14). Every plan is `Solver.plan(z, 1e-32, hmax)`,
hmax 0.05 unless the file name says otherwise.

| file | what | written by |
|---|---|---|
| `prof_low.npy`, `prof_hi.npy` | per plan step (segment, x, min over τ of c − x, its τ point), D 3.044375 and D 3.15 | `explore1.py low` / `hi` (with `common.py`) |
| `valley_D3.0444.log`, `valley_D3.15.log` | per segment Σ_j ∫ dx/(c_j − x), its largest term, Σ_j ∫ dx/(x + c_j); the match node | `mode_matched.py valley STATE --threads=2` |
| `explore3_low6_det.log` | D_m (match_node 6) at λ 1 and 3, kernel `mode_det` | `explore3.py low 6 det 1.0 3.0` |
| `pair_D3.0444.jsonl`, `pair_D3.0444.log`, `outer_D3.0444.log` | D_m at the four λ of #1078 comment 7120204793 | `mode_matched.py det OUT STATE λ λ --match=6 --threads=2 --allow_unraw` (twice) |
| `identity_D3.15.jsonl`, `.log` | criterion 4 at D 3.15, λ 4.3 and 4.5: FAIL (4.9e-3 against 1e-6) | `mode_matched.py identity OUT STATE 4.3 4.5 --threads=2 --allow_unraw` |
| `root_m_D3.15.jsonl`, `.log` | D_m's root at D 3.15 (match_node 5): 4.397786345516482 | `mode_matched.py root OUT STATE --lam0=4.397684106690 --xtol=1e-11 --threads=2 --allow_unraw` |
| `explore5.log` | per segment, the λ-change of ln det of the outward and inward blocks against Liouville, D 3.15, hmax 0.05 | `explore5.py STATE 5 8 4.3 4.5` |
| `explore6_h005.log`, `explore6_h001.log` | the same for the outward blocks on the hmax 0.005 and 0.001 plans | `explore6.py STATE HMAX 1e-32 8 4.3 4.5` |
| `blocks_D3.15_h0.05.*`, `blocks_D3.15_h0.001.*` | the same tables from the branch's script | `mode_matched.py blocks OUT STATE 4.3 4.5 --hmax=H --match=valley|out --threads=2 --allow_unraw` |
| `toy.log` | the planted toy (PASS), its shift control (FAIL, exit 1, as it must) and the no-valley case (PASS) | `run_toy.sh`: `mode_matched.py toy`, `--mutate=shift`, `--gap=0.05` |

The `explore*.py` scripts import `hp/mode_matched.py` from the branch (or the scratch `common.py`); the paths in them
are the Mac's scratchpad.
