#!/bin/bash
# wip/large-d-fastmul6 ($1: its commit; fastmul5 with the d/dtheta matrices' f64 remainders on the quad- and octo-double
# lanes) into hp_y/ (its own copy of hp, so the running jobs' hp/ stays as it is), the release build (low-memory recipe,
# 8 jobs), the wheel unpacked into site_y/; then the checks: recip_check at D 300 and D 1000, dmat_check at D 300 and
# D 1000 (the 2c control inside), taylor_mp_check at D 300, each log in out/fastmul6_build/
{
set -e
W=/home/nathan/Source/choptuik-large-d-1088a
C=$1
O=$W/out/fastmul6_build
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC"
T=$(mktemp -d $W/src_XXXX)
curl -sfL https://codeload.github.com/nmoinvaz/choptuik-large-d/tar.gz/$C | tar -xz -C "$T" --strip-components=1
grep -c "fn dapply_c" "$T/hp/src/model.rs"
grep -c "def dmat_corr" "$T/hp/form_s.py"
mkdir -p $W/hp_y
cp -r "$T"/hp/. $W/hp_y/
mkdir -p $HOME/.local/share/Trash/files
mv "$T" $HOME/.local/share/Trash/files/src_$(date +%s)
cd $W/hp_y
export RUSTFLAGS="-C target-cpu=native" CARGO_TARGET_DIR=$W/target_y CARGO_BUILD_JOBS=8 CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
/home/nathan/Source/venv-i1058/bin/maturin build --release -i /home/nathan/Source/venv-i1058/bin/python --out $W/dist_y
cd $W
PY=$(cat $W/python_path)
mkdir -p site_y
WHL=$(ls -t dist_y/hpkernel-*.whl | head -1)
$PY -m zipfile -e "$WHL" site_y/
cp $W/hp_y/python/hpkernel/__init__.py $W/hp_y/python/hpkernel/driver.py site_y/hpkernel/
PYTHONPATH=$W/site_y $PY -c "import hpkernel; from hpkernel._hpkernel import Solver; print(hpkernel.__file__, hasattr(Solver, 'set_dmat_corr'))"
date -u "+built %Y-%m-%d %H:%M:%S UTC"
set +e
cd $W/hp_y
export HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
S3=$W/out/budget300_src/D300_full_base.npz
S10=$W/out/fix/D1000_base/release_ls_h13_D1000.0000.npz
$PY -u recip_check.py $S3 --threads 4 > $O/recip300.log 2>&1; echo "recip_check D 300 exit=$?" >> $O/exit_codes.txt
$PY -u recip_check.py $S10 --threads 4 > $O/recip1000.log 2>&1; echo "recip_check D 1000 exit=$?" >> $O/exit_codes.txt
$PY -u dmat_check.py $S3 > $O/dmat300.log 2>&1; echo "dmat_check D 300 exit=$?" >> $O/exit_codes.txt
$PY -u dmat_check.py $S10 > $O/dmat1000.log 2>&1; echo "dmat_check D 1000 exit=$?" >> $O/exit_codes.txt
$PY -u taylor_mp_check.py $S3 > $O/taylor300.log 2>&1; echo "taylor_mp_check D 300 exit=$?" >> $O/exit_codes.txt
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
