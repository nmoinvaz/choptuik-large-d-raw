#!/bin/bash
# #1098 on mm5: D 2828 as a full point on fastmul7 (~/Source/choptuik-fastmul7 at d40a9c62, ~/Source/fastmul7-site),
# chord-free, 6 threads: <ladder>/tools3/ladder_point2.sh (blob 8802fb26; tools3_check.sh first) with kc 250, KSBAR 1e-64
# (the recipe's amendment 1), the jump fitted in 1/n to D 2000's fastmul6 base h13 (<ladder>/inputs, blob b897ba43) and
# D 4000's converged jump state (<ladder>/D4000/jump/jump_s_D4000.0000.npz, sha256 d542ecda), then h5..h11, h13, the M 48
# tail to kmax 23 and the k* stage. Output in <ladder>/D2828; the last act writes "job rc N" to its run.log. After it:
# kmax_rule.py on <ladder>/D2828/tail/release_ls.jsonl (exit 2: the h25 extension of amendment 1)
{
L=$HOME/Source/choptuik-large-d-raw/I1098-mm5/ladder
I=$L/inputs
bash $L/tools3/tools3_check.sh > $L/tools3/check3.log 2>&1 || exit 1
[ "$(git hash-object --no-filters $I/D2000_base6_h13.npz)" = "b897ba43adb46653785b362d2ae6a2f712fdd8db" ] || exit 2
[ "$(shasum -a 256 $L/D4000/jump/jump_s_D4000.0000.npz | cut -c1-8)" = "d542ecda" ] || exit 2
mkdir -p $L/D2828
export HP=$HOME/Source/choptuik-fastmul7/hp SITE=$HOME/Source/fastmul7-site PY=$HOME/venv-314/bin/python
export KSBAR=1e-64 INNER_CHORD=0 EXTRA=
bash $L/tools3/ladder_point2.sh 2828 250 6 $L/D2828 $I/D2000_base6_h13.npz $L/D4000/jump/jump_s_D4000.0000.npz 48 23
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $L/D2828/run.log
exit $rc
}
