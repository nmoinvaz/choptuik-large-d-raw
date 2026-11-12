# I603-win2: the chain_fit chain rerun on main's exact freeze projector from D 225.13

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/603 (queued by the coordinator at 16:29 UTC, 2026-11-12, behind #600; Nathan's decision after #595).
Code and build: worktree `D:\choptuik-i600` at main fc697f3a (hp on multishoot 1.2.1, the exact projector; #523's 1658a4f is in it), the fat-LTO build checked in #600 (`I600-win2/`, hpkernel `_hpkernel.cp314-win_amd64.pyd` sha256 4ede9afec7ffb40e93c321270ddc9614d644473e1b74834e9406a98f7571f90d, AVX2), venv `venv-i600` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1). Not the venv-t126 build that crawlG to crawlJ used.
Start: #595's exact-rows base `I595-mac/polish_c2_s225/base_pin3_D225.1312.npz` (raw 2b818f6f), copied to `base/` (sha256 961d45ac2b3f3516758c1a7d...). Flags: crawlJ's, `run_603.sh`. Output `chain/`, log `chain.log`, starts and exits `exits_603.txt`.

Control (acceptance): at D 235.13125 the chain's Delta equals the table's crawlI row (1.687523233741265 + 2.521580451291125e-17 - 8.824e-34 - 3.869e-50) minus 3.5313e-12, within 1e-14. If it does not, stop and report.
Each accepted step converges to max|F| <= 1e-60. Where the chain stops: the step, its attempts and their first moves, as #461's tables.

Results follow when the chain ends or stops.
