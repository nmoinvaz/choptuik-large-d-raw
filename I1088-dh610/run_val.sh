#!/bin/bash
# form S validation on dh610 (#1088): the D 16.76-27.04 checks against form A and delta_all.csv, their controls, the
# planted check, then the conditioning of form A against form S at D 50, 100, 200 and 245.56
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
PY=/home/nathan/Source/venv-i1058/bin/python
export PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2
date -u "+start %Y-%m-%d %H:%M:%S UTC"
$PY -c "import hpkernel; print(hpkernel.__file__)"
$PY -u form_s.py check data/states/up2_D16.7600.npz data/states/up2_D20.0437.npz data/states/up3_D23.0433.npz data/states/up4_D26.0797.npz data/states/up6_D27.0422.npz --threads 8 --out $W/out > $W/out/check.log 2>&1
$PY -u form_s.py check data/states/up2_D20.0437.npz --threads 8 --mutate flux > $W/out/check_flux.log 2>&1
$PY -u form_s.py planted $W/out/s_D20.0437.npz --threads 8 > $W/out/planted.log 2>&1
$PY -u form_s.py planted $W/out/s_D20.0437.npz --threads 8 --mutate step > $W/out/planted_step.log 2>&1
date -u "+check done %Y-%m-%d %H:%M:%S UTC"
$PY -u form_s.py cond data/states/up8_D50.0075.npz $W/states/anm_pin3_D100.0000.npz $W/states/anm_pin3_D200.0000.npz $W/states/anm_pin3_D245.5586.npz --threads 8 --kfreeze 13 > $W/out/cond.log 2>&1
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
