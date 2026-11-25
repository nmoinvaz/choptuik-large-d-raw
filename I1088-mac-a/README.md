# I1088-mac-a: Track A of #1088, the direct solve at a target D (hp/jump.py), development runs on the Mac

Machine: the Mac (Apple M-series, macOS), `/Users/nathan/venv-314` with the hpkernel build of #1043 (main's kernel of
2026-11-20) on `PYTHONPATH`, 2 threads at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1088
Code: branch `wip/large-d-jump` of choptuik-large-d, `hp/jump.py` (a4df1196 and later).

Inputs: chain states of `I903-macm3/chain_k135/` and `I966-dh370/ks_chain3b/` (this repository, origin/main at
c30c2766).

- `g250/`: the guess at D 250 from the 28 states with D 226.13 to 245.56 (`jump.py guess`, its command line in
  `g250/cmd.txt`), its log and the eight-part guess (`guess_D250.npz`, the re-seed failed, so its horizon data are
  the ladder's last rung's).
- `probes/`: one octo-double Newton step of the full system from the chain's state at D 245.5586 (`probe2.py`,
  kfreeze None in `probe2.log`, kfreeze 13 in `probe2_k13.log`), and the ladder and its u0 rung on that state
  (`ladtest*.py`; `run_probes.sh` reran ladtest2 to 4 into their logs).

Files are added as the runs go; each log or script names its command line.
