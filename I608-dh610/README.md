# I608-dh610: the d6 and d10 comparison chains on the exact freeze projector from D 225.13 (the fits' error bar for #603)

Machine: dh610 (the former win3), Fedora Linux 45 Workstation (kernel 7.3.3), Intel Core i7-12700 (12 cores, 20
threads, AVX2 and FMA), 62 GB. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/608

Code: choptuik-large-d main at a879ccc3 in a detached worktree (`choptuik-i608`), on the build #606 checked (the venv
of the main checkout; hpkernel avx2, multishoot 1.2.1, so after #523's exact projector). Python 3.14.10, numpy 2.5.4.
Two chains at once, 9 threads each (`--threads 9`), nice 10, one systemd user unit each (`i608-chain_d6`,
`i608-chain_d10`, MemoryMax 16G) wrapped in `systemd-inhibit`, `OPENBLAS_NUM_THREADS=1`.

| chain | start (read, not copied) | held fit |
|---|---|---|
| chain_d6 | I462-win/chain_d6/anm_pin3_D225.1312.npz | hp/data/held_fit_d6.json |
| chain_d10 | I462-win/chain_d10/anm_pin3_D225.1312.npz | hp/data/held_fit_d10.json |

Flags are #462's `d6_long3.cmd` and `d10_long3.cmd` (`run_608.sh`): `--kfreeze 3 --N 24 --eps 1e-14 --h_max 1.0
--steps 400 --D_max 400 --corrector od --tol_od 1e-60 --qd_it 12 --jet_o 1 --reseed 2 --reseed_q 1 --save_pred 1
--od_junk 0 --held_o 1 --reseed_o 3`, with `--threads 9` for #462's 3, the base polish left on (no `--base_polish 0`),
and `--save_base 1` added so that the polished base is saved for the control. `--save_base` only writes the base after
its polish; it changes no step. No wall-clock cap (#462's run_capped.py is not used).

Control, before the first step: each base polish at D 225.13 moves Delta by about #595's measured shift there,
-7.76e-16, within 1e-17 plus the reload offset (`hp/delta_diff.py`, exact eight-part differences).

| file | what |
|---|---|
| run_608.sh | the command of one chain, `run_608.sh d6\|d10 [STATE]` |
| chain_d6.log, chain_d10.log | the chains' logs |
| chain_d6/, chain_d10/ | states (npz), `anm_run.jsonl`, the saved base after its polish |
| exits_608.txt | start and exit of each chain |
| delta_diff_d6.log, delta_diff_d10.log | the control: exact eight-part Delta of each start and polished base |
| report_608.py | reads the two logs and the states: `python3 -I report_608.py <raw clone>` prints each chain's accepted steps, refused attempts (with every Newton iteration) and Delta(d6) - Delta(d10) |
| report_608_HHMM.md, report_608_final.md | its output at that UTC time (the hourly posts); `final` is the stop |

Result: both chains stopped by `systemctl --user stop` at 2026-11-13 09:01:05 UTC (SIGTERM, so the wrapper wrote no exit
line, and `exits_608.txt` has them by hand) after d10 had an accepted step past D 242, as the issue asks. Neither chain
had reached a wall: each a = 1.0 refusal was recovered by the retry at a = 0.5. The step each chain was computing when
stopped (the Taylor series, 22 min each) was not an attempt and left no files.

| chain | accepted steps (a = 1.0, a = 0.5) | last state | refused attempts |
|---|---|---|---|
| chain_d6 | 20 (16, 4) | anm_pin3_D243.1312.npz | 4 |
| chain_d10 | 21 (13, 8) | anm_pin3_D242.1312.npz | 8 |

Restart from a saved state with `run_608.sh d6|d10 I608-dh610/chain_dX/anm_pin3_D<D>.npz`.
