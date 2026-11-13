# I712-dh370: the chain's series at three bases past D 255, does track A hold? (the dh370 run of #712)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB. Run at `nice -n 10`, 12 threads, `OPENBLAS_NUM_THREADS=1`, no memory guard.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/712 (recommended by #685, whose series and tables are in I685-dh370/).
Code: choptuik-large-d main at f40deb4a (hp/src, hp/python and the Cargo and pyproject files are unchanged since aedb403b, which ran #685; hp/anm_run.py gained options that are off by default (--reseed_start, --ks, --elim_switch) and hp/jet_singularity.py new planted tests, so the old bases are summarized again here and compared with I685-dh370/jet_685.json), worktree `choptuik-large-d-685`, the venv of `choptuik-large-d-614` (the 3c35f0c build).
Inputs: #603's states `I603-win2/chain_nsr/anm_pin3_D255.0550.npz`, `anm_pin3_D255.3711.npz` and `anm_pin3_D255.7661.npz` and the records `I603-win2/chain_nsr/anm_run.jsonl`, of the raw repository at e8ac541d.
Command: #685's (`anm_run.py --save_jet 2`, N 24, --steps 1) with #603's chain_nsr flags (`I603-win2/run_603_nsr.sh`: --qd_it 20 --od_accept natural --od_strong 4 --reseed_start pred), 12 threads.

## The bars, from the issue, before any series was read

At each new base: (1) the series equals #603's record of the step from that base in all 25 norms and both pivots; (2) the root test of Delta (I685's `root_radius`, the one in table685.txt) within 5% of |255.71 + 4.99i - D0|; (3) the Pade track-A pole of Delta (the stable pole within 0.4 of 255.71 + 4.99i) has Im D* within 0.1 of 4.99. A bar that fails is reported as failed. The other stable poles are tabulated as in #685.
