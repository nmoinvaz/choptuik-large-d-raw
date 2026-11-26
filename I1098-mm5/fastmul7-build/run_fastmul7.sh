#!/bin/bash
# fastmul7: the fastmul6 recipe on d40a9c62, then the checks (relaxed_build_check, recip_check x2, dmat_check x2, taylor_mp_check
# with the remainders on and off, horizon_mp_check with its split control)
RAW=$HOME/Source/choptuik-large-d-raw/I1098-mm5/fastmul7-build
RAWS=$HOME/Source/choptuik-large-d-raw/I1098-mm5
source $HOME/.cargo/env
W=$HOME/Source/choptuik-fastmul7; SITE=$HOME/Source/fastmul7-site; PY=$HOME/venv-314/bin/python
D300=$RAWS/kfree300/input/release_ls_h13_D300.0000.npz
D1000=$RAWS/kfree1000/input/release_ls_h13_D1000.0000.npz
D1000DH=$RAWS/fastmul6-build/inputs/D1000_base_h13_dh610.npz
D300U21=$RAWS/ladder/D300u/tail/release_ls_h21_D300.0000.npz
cd $W/hp
echo "start $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > $RAW/times.txt
git log --oneline -1 >> $RAW/times.txt
mkdir -p $SITE $W/dist
( while true; do
    kb=$(ps -axo rss,comm | awk '/rustc|cargo|maturin|\/ld|clang|cc1/ {s+=$1} END {print s+0}')
    sw=$(sysctl -n vm.swapusage | awk '{print $6}')
    echo "$(date -u +%H:%M:%S) build_rss_kb=$kb swap_used=$sw" >> $RAW/mem_samples.log
    sleep 20
  done ) &
SAMP=$!
RUSTFLAGS="-C target-cpu=native" CARGO_PROFILE_RELEASE_STRIP=false CARGO_TARGET_DIR=$W/target \
  /usr/bin/time -l nice -n 10 $HOME/venv-314/bin/maturin build --profile release -i $PY --out $W/dist > $RAW/build.log 2>&1
rc=$?
kill $SAMP 2>/dev/null
echo "maturin build exit=$rc" > $RAW/exit_codes.txt
echo "build end $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> $RAW/times.txt
if [ $rc -eq 0 ]; then
  $PY -m zipfile -e "$(ls -t $W/dist/hpkernel-*.whl | head -1)" $SITE/ >> $RAW/build.log 2>&1
  echo "zipfile exit=$?" >> $RAW/exit_codes.txt
  cp python/hpkernel/__init__.py python/hpkernel/driver.py $SITE/hpkernel/
  echo "cp exit=$?" >> $RAW/exit_codes.txt
  cp $HOME/Source/choptuik-fastmul3/D2000_step.npz $W/D2000_step.npz
  echo "D2000 blob $(git hash-object --no-filters $W/D2000_step.npz)" >> $RAW/exit_codes.txt
  export OPENBLAS_NUM_THREADS=2 HP_EXACT_RECIP=1 HP_EXACT_DMAT=1
  PYTHONPATH=$SITE $PY relaxed_build_check.py $W/D2000_step.npz > $RAW/check.log 2>&1
  echo "relaxed_build_check exit=$?" >> $RAW/exit_codes.txt
  export HP_HORIZON_RELAXED=1 PYTHONPATH=$SITE:$W/hp
  cd $W
  $PY hp/recip_check.py $D300 --threads 4 > $RAW/recip300.log 2>&1;  echo "recip_check D 300 exit=$?" >> $RAW/exit_codes.txt
  $PY hp/recip_check.py $D1000 --threads 4 > $RAW/recip1000.log 2>&1; echo "recip_check D 1000 exit=$?" >> $RAW/exit_codes.txt
  $PY hp/dmat_check.py $D300 > $RAW/dmat300.log 2>&1;  echo "dmat_check D 300 exit=$?" >> $RAW/exit_codes.txt
  $PY hp/dmat_check.py $D1000DH > $RAW/dmat1000.log 2>&1; echo "dmat_check D 1000 exit=$?" >> $RAW/exit_codes.txt
  $PY hp/taylor_mp_check.py $D300 > $RAW/taylor300.log 2>&1; echo "taylor_mp_check D 300 exit=$?" >> $RAW/exit_codes.txt
  HP_EXACT_DMAT=0 $PY hp/taylor_mp_check.py $D300 > $RAW/taylor300_dmat0.log 2>&1; echo "taylor_mp_check D 300 HP_EXACT_DMAT=0 exit=$?" >> $RAW/exit_codes.txt
  $PY hp/horizon_mp_check.py $D300U21 --ks_mp 1100 --ks_mob 800 --bar 1e-100 --ctl_mutate 57 --ctl_bar 1e-80 > $RAW/horizon_mp.log 2>&1; echo "horizon_mp_check exit=$?" >> $RAW/exit_codes.txt
fi
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> $RAW/times.txt
