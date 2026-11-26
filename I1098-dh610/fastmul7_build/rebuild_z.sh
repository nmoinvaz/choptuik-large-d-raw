#!/bin/bash
# fastmul7 ($1: its commit; fastmul6 with horizon_mob's B_0 split exact for the matrix applied) on dh610 into hp_z/ and
# site_z/, the low-memory recipe with 4 jobs at nice 19, after the Skylake wheel's build (waits at most 4 h for it); then
# the checks: recip_check D 300 and D 1000, dmat_check D 300 and D 1000, taylor_mp_check D 300, and the split's
# check (horizon_mp_check.py at D 300's u h21 state, Moebius a 8 ks 800 against mpmath: at most 1e-100, the control
# --ctl_mutate 57, the old split, above 1e-80), each log in out/fastmul7_build/
{
W=/home/nathan/Source/choptuik-large-d-1088a
C=$1
O=$W/out/fastmul7_build
mkdir -p $O
n=0
while [ $n -lt 720 ]; do grep -qE "^end |rror" $W/build_sky.log 2>/dev/null && break; sleep 20; n=$((n + 1)); done
set -e
date -u "+start %Y-%m-%d %H:%M:%S UTC"
T=$(mktemp -d $W/src_XXXX)
curl -sfL https://codeload.github.com/nmoinvaz/choptuik-large-d/tar.gz/$C | tar -xz -C "$T" --strip-components=1
grep -c "FS_MUT_SPLIT" "$T/hp/src/form_s.rs"
mkdir -p $W/hp_z
cp -r "$T"/hp/. $W/hp_z/
mkdir -p $HOME/.local/share/Trash/files
mv "$T" $HOME/.local/share/Trash/files/src_$(date +%s)
cd $W/hp_z
export RUSTFLAGS="-C target-cpu=native" CARGO_TARGET_DIR=$W/target_z CARGO_BUILD_JOBS=4 CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
/home/nathan/Source/venv-i1058/bin/maturin build --release -i /home/nathan/Source/venv-i1058/bin/python --out $W/dist_z
cd $W
PY=$(cat $W/python_path)
mkdir -p site_z
WHL=$(ls -t dist_z/hpkernel-*.whl | head -1)
$PY -m zipfile -e "$WHL" site_z/
cp $W/hp_z/python/hpkernel/__init__.py $W/hp_z/python/hpkernel/driver.py site_z/hpkernel/
PYTHONPATH=$W/site_z $PY -c "import hpkernel; print(hpkernel.__file__)"
date -u "+built %Y-%m-%d %H:%M:%S UTC"
set +e
cd $W/hp_z
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
S3=$W/out/budget300_src/D300_full_base.npz
S10=$W/out/fix/D1000_base/release_ls_h13_D1000.0000.npz
$PY -u horizon_mp_check.py $W/out/mpcheck/states/D300u_h21.npz --ks_mp 1100 --ks_mob 800 --bar 1e-100 --ctl_mutate 57 \
  --ctl_bar 1e-80 > $O/split300.log 2>&1; echo "split check D 300 exit=$?" >> $O/exit_codes.txt
$PY -u recip_check.py $S3 --threads 4 > $O/recip300.log 2>&1; echo "recip_check D 300 exit=$?" >> $O/exit_codes.txt
$PY -u recip_check.py $S10 --threads 4 > $O/recip1000.log 2>&1; echo "recip_check D 1000 exit=$?" >> $O/exit_codes.txt
$PY -u dmat_check.py $S3 > $O/dmat300.log 2>&1; echo "dmat_check D 300 exit=$?" >> $O/exit_codes.txt
$PY -u dmat_check.py $S10 > $O/dmat1000.log 2>&1; echo "dmat_check D 1000 exit=$?" >> $O/exit_codes.txt
$PY -u taylor_mp_check.py $S3 > $O/taylor300.log 2>&1; echo "taylor_mp_check D 300 exit=$?" >> $O/exit_codes.txt
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
