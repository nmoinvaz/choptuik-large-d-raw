#!/bin/bash
# #896 on rpi5: solver/proof/b8_chain_regen.sh (unedited, from the worktree at origin/main) on aarch64, one process at nice 10
# (the script's own nice). The script writes its 35 outputs into solver/proof/ of the worktree under their stored names, so
# this wrapper checks that solver/proof is clean first, and at the end copies the 35 files to $R/regen/, records git status
# and diff, and runs b8m_lc_liprep.py --compare (stored matrix against this run's). The worktree is never committed.
R=/home/nathan/Source/choptuik-large-d-raw/I896-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-896
cd $WT/solver/proof || exit 9
[ -z "$(git status --porcelain .)" ] || { echo "STOP: the worktree's solver/proof is not clean"; exit 9; }
mkdir -p $R/regen $R/stored
log() { echo "896 $1 $(date -u '+%F %T') UTC" >> $R/exits_896.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)  b8_chain_regen.sh md5 $(md5sum b8_chain_regen.sh | cut -c1-8)"
  $PY -c "import flint, numpy, mpmath, scipy, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, 'scipy', scipy.__version__, platform.platform(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
FILES="b8m_atoms_K4.log b8m_scan_K4_box.out b8m_scan_K4_box.log b8m_h8_K4_L73.89.log b8m_scan_K4_k0.85.log b8m_h8_K4_L104.68_k0.85.log
b8m_scan_K4_fixedZ.log b5_jump.log b5_jump.json b5_threshold.log b8m_scan_K4_d0.log b8m_scan_K4_d0_1e6.log b8m_scan_K4_d0_1e7.log
b8m_h8_K4_L73.89_d0_1e6.log b8m_h8_K4_L73.89_d0_1e7.log b5_jump_d0_1e6.log b5_jump_d0_1e6.json b5_jump_d0_1e7.log b5_jump_d0_1e7.json
b7_ift.log b7_ift.json b7_ift_mutJD.log b7_ift_d0_1e6.log b7_ift_d0_0.log b8m_lc_K4.log b8m_lc_K4.out b8m_lc_lip.json b8m_lc_lipcheck.log
b8m_lc_K4_mut_rho2L.log b8m_lc_K4_mut_rho2L.out b8m_lc_numcheck_n1e3.log b8m_lc_numcheck_mut.log b8m_lcj.log b8m_lcj.json b8m_lcj_mutations.log"
for f in $FILES; do git show HEAD:solver/proof/$f > $R/stored/$f; done
log "regen start"
t=$(date +%s.%N)
bash b8_chain_regen.sh $PY > $R/regen.log 2>&1
rc=$?
log "regen exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s"
git status --porcelain . > $R/status_after.txt
git diff --stat . > $R/diff_against_stored.txt
for f in $FILES; do cp $f $R/regen/$f; done
git status --porcelain . | awk '{print $2}' | sed 's|^solver/proof/||' | while read f; do [ -f "$f" ] && cp -n "$f" $R/regen/ ; done
git show HEAD:solver/proof/b8m_lc_lip.json > $R/stored_b8m_lc_lip.json
log "liprep start"
nice -n 10 $PY b8m_lc_liprep.py --compare=$R/stored_b8m_lc_lip.json,b8m_lc_lip.json > $R/liprep_compare.log 2>&1
log "liprep exit $?"
log "all done"
