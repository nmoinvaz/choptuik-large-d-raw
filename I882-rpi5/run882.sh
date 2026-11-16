#!/bin/bash
# #882 on rpi5 (the coordinator): Theorem B(1)'s certified constants reproduced on aarch64 Linux. Every command of
# proof/B8_constants.md 13, proof/B5_inner.md 10 and proof/B_chain.md 11, as written, from solver/proof/ of a worktree
# at main, one process at a time at nice 10. Each command's output goes to $R/<name>.log. Files the commands write
# overwrite the worktree's stored ones; at the end git status and diff are recorded and every changed or new file of
# solver/proof/ is copied to $R/changed/. The worktree is never committed.
R=/home/nathan/Source/choptuik-large-d-raw/I882-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-882
cd $WT/solver/proof || exit 9
[ -z "$(git status --porcelain .)" ] || { echo "STOP: the worktree's solver/proof is not clean"; exit 9; }
mkdir -p $R
log() { echo "882 $1 $(date -u '+%F %T') UTC" >> $R/exits_882.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import flint, numpy, mpmath, scipy, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, 'scipy', scipy.__version__, platform.platform(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
run() {  # kind (run|ctrl|scan), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s.%N)
  nice -n 10 $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s ($kind)"
}
# --- B8_constants.md 13
run run  b8m_model            b8m_model.py
run run  b8m_formal           b8m_formal.py 1 4 --check
run run  b8m_atoms            b8m_atoms.py 4 0 0
run run  b8m_identities       b8m_identities.py
run ctrl b8m_identities_rho2old b8m_identities.py --mutate=rho2old
run ctrl b8m_identities_q     b8m_identities.py --mutate=q
run run  b8m_scan_box         b8m_scan.py 4 73.89,70,66,62 --rA=2e-6 --rW=2e-6 --log=b8m_scan_K4_box.log
run run  b8m_h8               b8m_h8.py 4 73.89 --log=b8m_scan_K4_box.log --rA=2e-6 --rW=2e-6
run run  b8m_numcheck         b8m_numcheck.py 1000 4 --log=b8m_scan_K4_box.log
run ctrl b8m_numcheck_weight  b8m_numcheck.py 1000 4 --log=b8m_scan_K4_box.log --load=b8m_numcheck_n1000.npz --mutate=weight
run ctrl b8m_numcheck_kernel  b8m_numcheck.py 1000 4 --log=b8m_scan_K4_box.log --load=b8m_numcheck_n1000.npz --mutate=kernel
run ctrl b8m_numcheck_tau     b8m_numcheck.py 1000 4 --mutate=tau
# --- B5_inner.md 10
run run  b5_system            b5_system.py
run ctrl b5_system_epsCB      b5_system.py --mutate=epsCB
run ctrl b5_system_theta      b5_system.py --mutate=theta
run ctrl b5_system_t5         b5_system.py --mutate=t5
run run  b5_formulas          b5_formulas.py
run ctrl b5_formulas_res      b5_formulas.py --mutate=res
run run  b5_numeric_residual  b5_numeric.py residual
run ctrl b5_numeric_offsol    b5_numeric.py residual --mutate=offsol
run run  b5_numeric_lip       b5_numeric.py lip --Z=0.0085 --kappa=0.3
run run  b5_bounds            b5_bounds.py --kappa=0.3 --Z=0.0085 --json=b5_bounds_k0.3_Z0.0085.json
run scan b5_bounds_scan       b5_bounds.py --kappa=0.3 --Z=0.0085,0.009,0.0091
run scan b5_bounds_rp         b5_bounds.py --kappa=0.3 --Z=0.0085 --rp=0.15
run run  b5_bounds_check      b5_bounds.py check
run ctrl b5_bounds_check_res  b5_bounds.py check --mutate=res
run ctrl b5_bounds_check_jacP b5_bounds.py check --mutate=jacP
run ctrl b5_bounds_jac        b5_bounds.py --kappa=0.3 --Z=0.0085 --mutate=jac
run ctrl b5_bounds_series     b5_bounds.py --kappa=0.3 --Z=0.0085 --mutate=series
run run  b5_data              b5_data.py
run ctrl b5_data_gauge        b5_data.py --mutate=gauge
run run  b5_threshold         b5_threshold.py
run ctrl b5_threshold_sum     b5_threshold.py --mutate=sum
run run  b5_path              b5_path.py --n=1e8
run ctrl b5_path_stokes       b5_path.py --n=1e8 --mutate=stokes
# --- B_chain.md 11
run run  b5_label             b5_label.py --json=b5_label.json
run run  b5_label_check       b5_label.py check
run ctrl b5_label_Ct2         b5_label.py check --mutate=Ct2
run ctrl b5_label_scale       b5_label.py check --mutate=scale
run run  b5_jump              b5_jump.py --json=b5_jump.json
run ctrl b5_jump_sum          b5_jump.py --mutate=sum
run run  b8m_scan_d0          b8m_scan.py 4 73.89 --d0=1e7 --rA=2e-6 --rW=2e-6 --log=b8m_scan_K4_d0_1e7.log
run run  b8m_h8_d0            b8m_h8.py 4 73.89 --log=b8m_scan_K4_d0_1e7.log --d0=1e7
cp $R/b8m_h8_d0.log b8m_h8_K4_L73.89_d0_1e7.log      # B_chain.md redirects this run's stdout to that file
run run  b5_jump_d0           b5_jump.py --h8log=b8m_h8_K4_L73.89_d0_1e7.log --json=b5_jump_d0_1e7.json
run run  b8m_scan_k085        b8m_scan.py 4 104.68 --kappa1=0.85 --rA=2e-6 --rW=2e-6 --log=b8m_scan_K4_k0.85.log
run run  b7_box               b7_adjoint.py box --hr=1.1e-8 --hi=1e-8 --out=b7_box.json
run run  b7_adjoint           b7_adjoint.py adjoint --box=b7_box.json --out=b7_adjoint.json
run run  b7_point             b7_adjoint.py point --out=b7_box_point.json
run run  b7_adjoint_point     b7_adjoint.py adjoint --box=b7_box_point.json --out=b7_adjoint_point.json
run run  b7_check             b7_adjoint.py check --adj=b7_adjoint_point.json --start=b7_box_point.json
run run  b7_adjoint_mutT      b7_adjoint.py adjoint --box=b7_box_point.json --out=b7_adjoint_point_mutT.json --mutate=transpose
run ctrl b7_check_mutT        b7_adjoint.py check --adj=b7_adjoint_point_mutT.json --start=b7_box_point.json --mutate=transpose
run run  b7_ift               b7_ift.py --adj=b7_adjoint.json --jump=b5_jump_d0_1e7.json --json=b7_ift.json
run ctrl b7_ift_JD            b7_ift.py --adj=b7_adjoint.json --jump=b5_jump_d0_1e7.json --mutate=JD
run run  b8m_lc               b8m_lc.py 4 73.89 --rA=2e-6 --rW=2e-6 --lip --log=b8m_lc_K4.log
run run  b8m_lc_lipcheck      b8m_lc.py --lipcheck=b8m_lc_lip.json
run run  b8m_lc_mut_rho2L     b8m_lc.py 4 73.89 --rA=2e-6 --rW=2e-6 --mutate=rho2L --log=b8m_lc_K4_mut_rho2L.log
run ctrl b8m_lc_numcheck_mut  b8m_lc_numcheck.py 1000 --log=b8m_lc_K4_mut_rho2L.log --mutlc
run run  b8m_lc_numcheck      b8m_lc_numcheck.py 1000 --log=b8m_lc_K4.log
run ctrl b8m_lc_numcheck_d0   b8m_lc_numcheck.py 1000 --log=b8m_lc_K4.log --mutate=d0
run ctrl b8m_lc_numcheck_weight b8m_lc_numcheck.py 1000 --log=b8m_lc_K4.log --mutate=weight
run run  b8m_lcj              b8m_lcj.py --log=b8m_lc_K4.log --json=b8m_lcj.json
run ctrl b8m_lcj_kernel       b8m_lcj.py --log=b8m_lc_K4.log --mutate=kernel
run ctrl b8m_lcj_Om           b8m_lcj.py --log=b8m_lc_K4.log --mutate=Om
# --- what changed in the worktree
git -C $WT status --porcelain -- solver/proof > $R/status_after.txt 2>&1
git -C $WT diff --stat -- solver/proof > $R/diff_against_stored.txt 2>&1
mkdir -p $R/changed
# porcelain paths are relative to the repository root
git -C $WT status --porcelain -- solver/proof | cut -c4- | while read -r f; do [ -f "$WT/$f" ] && cp "$WT/$f" $R/changed/; done
log "all done"
