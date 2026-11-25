# I1089-dss-mac: logs of the DSS-construction literature slice (momentum-constraint slaving of a, checks and controls)

Machine: the Mac (coordinator's machine), one process at nice 10. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1089,
slice 3. The note is `notes/LIT_GAPS_DSS.md` on branch `wip/lit-gaps-dss` of the main repository; the scripts are in its
`solver/lit_gaps_dss/` (commit 4e684981).

- `mc_check.txt`, `mc_check_mutate_flux.txt`: `python3 solver/lit_gaps_dss/mc_check.py [--mutate=flux]` (sympy). In our
  form (A) the momentum-constraint residual obeys x E_x = -(n-1) a^2 E; in the slaved form (S) the Hamiltonian residual
  obeys H_tau = (n-1) a^2 H. The control flips the flux term of S and must fail.
- `mc_states*.txt`: `python3 solver/lit_gaps_dss/mc_states.py STATES... [--mutate=flux|n1]` on four stored states,
  `git archive`d at 073640009 of this repository: T73/t73/pin5_D68.0835.npz, T139-macm3/chain/anm_pin3_D100.0000.npz,
  I903-macm3/chain_k135/anm_pin3_D226.1312.npz, I966-dh370/ks_chain3b/leg15_D263.4862_ks293/anm_pin3_D263.5987.npz.
  The scratch prefix of the paths is removed. No state was changed and no solve was run.
- `pole_mc.txt` (table), `pole_mc.jsonl` (records), `pole_mc_warnings.txt` (numpy's overflow warning from
  `hp/pole_test.py`'s ratio test, whose non-finite terms it drops): `python3 solver/lit_gaps_dss/pole_mc.py STATES...`
  (commit f33a83e5) on the same four states, with the venv-314 hpkernel (the path is printed in the log). The horizon
  series is recomputed for horizon data moved three ways: a_h scaled (A), m_h scaled with a_h re-slaved by the
  momentum constraint (S), and m_h scaled with a_h held (S0). Each row gives the ratio-test radius and the data's
  momentum residual at the SSH.

Python 3.14 (the Mac's venv-314), numpy and sympy as pinned in the main repository's requirements.txt.
