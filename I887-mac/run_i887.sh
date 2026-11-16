#!/bin/bash
# The B8 part of Theorem B(1)'s chain, rerun after the scripts state their working precision (#887).
# From solver/proof/ of the checkout (branch wip/sa-887). Usage: run_i887.sh <python> <output directory>.
# The commands are those of proof/B8_constants.md section 13 and proof/B_chain.md section 11. b8m_scan.py and
# b8m_lc.py append to their --log, and b8m_lc.py --lip writes b8m_lc_lip.json, so every output goes to the output
# directory under the stored file's name, and no stored file is touched. exits.txt has each run's exit status.
PY=$1; OUT=$2
: > "$OUT/exits.txt"
run() {   # run <output name> <command...>: stdout and stderr to OUT/<output name>
  local name=$1; shift
  local t0=$(date +%s)
  nice -n 10 "$@" > "$OUT/$name" 2>&1
  echo "$name: exit $?, $(( $(date +%s) - t0 )) s: $*" | sed "s|$PY|python3|; s|$OUT/||g" >> "$OUT/exits.txt"
}
BOX="--rA=2e-6 --rW=2e-6"
run b8m_atoms_K4.log $PY b8m_atoms.py 4 0 0
run b8m_scan_K4_box.out $PY b8m_scan.py 4 73.89,70,66,62 $BOX --log=$OUT/b8m_scan_K4_box.log
run b8m_h8_K4_L73.89.log $PY b8m_h8.py 4 73.89 --log=$OUT/b8m_scan_K4_box.log $BOX
run b8m_scan_K4_d0_1e7.out $PY b8m_scan.py 4 73.89 --d0=1e7 $BOX --log=$OUT/b8m_scan_K4_d0_1e7.log
run b8m_h8_K4_L73.89_d0_1e7.log $PY b8m_h8.py 4 73.89 --log=$OUT/b8m_scan_K4_d0_1e7.log --d0=1e7
run b5_jump_d0_1e7.log $PY b5_jump.py --h8log=$OUT/b8m_h8_K4_L73.89_d0_1e7.log --json=$OUT/b5_jump_d0_1e7.json
run b8m_scan_K4_k0.85.out $PY b8m_scan.py 4 104.68 --kappa1=0.85 $BOX --log=$OUT/b8m_scan_K4_k0.85.log
run b7_ift.log $PY b7_ift.py --adj=b7_adjoint.json --jump=$OUT/b5_jump_d0_1e7.json --json=$OUT/b7_ift.json
run b7_ift_mutJD.log $PY b7_ift.py --adj=b7_adjoint.json --jump=$OUT/b5_jump_d0_1e7.json --mutate=JD
run b8m_lc_K4.out $PY b8m_lc.py 4 73.89 $BOX --lip --log=$OUT/b8m_lc_K4.log --lipout=$OUT/b8m_lc_lip.json
run b8m_lc_lipcheck.log $PY b8m_lc.py --lipcheck=$OUT/b8m_lc_lip.json
run b8m_lc_K4_mut_rho2L.out $PY b8m_lc.py 4 73.89 $BOX --mutate=rho2L --log=$OUT/b8m_lc_K4_mut_rho2L.log
run b8m_lc_numcheck_mut.log $PY b8m_lc_numcheck.py 1000 --log=$OUT/b8m_lc_K4_mut_rho2L.log --mutlc
run b8m_lc_numcheck_n1e3.log $PY b8m_lc_numcheck.py 1000 --log=$OUT/b8m_lc_K4.log
run b8m_lc_numcheck_mut_d0.log $PY b8m_lc_numcheck.py 1000 --log=$OUT/b8m_lc_K4.log --mutate=d0
run b8m_lcj.log $PY b8m_lcj.py --log=$OUT/b8m_lc_K4.log --json=$OUT/b8m_lcj.json
run b8m_lcj_mut_kernel.log $PY b8m_lcj.py --log=$OUT/b8m_lc_K4.log --mutate=kernel
# the two B5 scripts that now work at 192 bits (proof/B_chain.md section 11, proof/B5_inner.md section 10)
run b5_jump.log $PY b5_jump.py --json=$OUT/b5_jump.json
run b5_jump_mut_sum.log $PY b5_jump.py --mutate=sum
run b5_threshold.log $PY b5_threshold.py
cat "$OUT/exits.txt"
