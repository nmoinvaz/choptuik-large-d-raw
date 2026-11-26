#!/bin/bash
# #1098: dh610's Skylake fastmul6 wheel installed here (site_sky/) with the same commit's hp Python (hp_y/), the four
# checks (relaxed_build_check, recip_check D 300 and D 1000, dmat_check D 300 and D 1000, taylor_mp_check D 300), then,
# only when all six exit 0, the ladder points given (ladder_point2.sh: M 32 to h13, the tail at M 48, kmax 31), each with
# THREADS threads, nice 10, from fastmul6's D 300 and D 1000 states
#
#     install_sky.sh W WHEEL COMMIT PY THREADS "D:KC:KMAX:KSBAR ..."
{
W=$1; WHL=$2; C=$3; PY=$4; TH=$5; PTS=$6
O=$W/out/fastmul6_build
mkdir -p $O $W/hp_y $W/site_sky $W/out/ladder
date -u "+start %Y-%m-%d %H:%M:%S UTC"
T=$(mktemp -d $W/src_XXXX)
curl -sfL https://codeload.github.com/nmoinvaz/choptuik-large-d/tar.gz/$C | tar -xz -C "$T" --strip-components=1 || exit 1
grep -q "floor_dz=1e-12" "$T/hp/form_s.py" || exit 1
cp -r "$T"/hp/. $W/hp_y/
mkdir -p $HOME/.local/share/Trash/files
mv "$T" $HOME/.local/share/Trash/files/src_$(date +%s)
$PY -m zipfile -e "$WHL" $W/site_sky/ || exit 2
cp $W/hp_y/python/hpkernel/__init__.py $W/hp_y/python/hpkernel/driver.py $W/site_sky/hpkernel/
PYTHONPATH=$W/site_sky $PY -c "import hpkernel; from hpkernel._hpkernel import Solver; print(hpkernel.__file__, hasattr(Solver, 'set_dmat_corr'))" || exit 3
cd $W/hp_y
export HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_sky
I=$W/out/ladder/inputs
$PY -u relaxed_build_check.py $I/L2000_step.npz > $O/relaxed.log 2>&1; echo "relaxed_build_check exit=$?" >> $O/exit_codes.txt
$PY -u recip_check.py $I/D300_full_base.npz --threads 4 > $O/recip300.log 2>&1; echo "recip_check D 300 exit=$?" >> $O/exit_codes.txt
$PY -u recip_check.py $I/D1000_base.npz --threads 4 > $O/recip1000.log 2>&1; echo "recip_check D 1000 exit=$?" >> $O/exit_codes.txt
$PY -u dmat_check.py $I/D300_full_base.npz > $O/dmat300.log 2>&1; echo "dmat_check D 300 exit=$?" >> $O/exit_codes.txt
$PY -u dmat_check.py $I/D1000_base.npz > $O/dmat1000.log 2>&1; echo "dmat_check D 1000 exit=$?" >> $O/exit_codes.txt
$PY -u taylor_mp_check.py $I/D300_full_base.npz > $O/taylor300.log 2>&1; echo "taylor_mp_check D 300 exit=$?" >> $O/exit_codes.txt
date -u "+checked %Y-%m-%d %H:%M:%S UTC"
[ "$(grep -c "exit=0" $O/exit_codes.txt)" = "6" ] || exit 4
export HP=$W/hp_y SITE=$W/site_sky PY EXTRA=--allow_unraw
cp $W/ladder_point2.sh $W/resample_m.py $W/out/ladder/
for p in $PTS; do
  IFS=: read -r d kc km kb <<< "$p"
  mkdir -p $W/out/ladder/D$d
  KSBAR=$kb bash $W/out/ladder/ladder_point2.sh $d $kc $TH $W/out/ladder/D$d $I/S300.npz $I/S1000.npz 48 $km &
done
wait
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
