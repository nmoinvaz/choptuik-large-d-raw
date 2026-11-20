#!/bin/bash
{
# #1025: signtests of the 16 delta-table rows at D <= 14.5 (D 4 .. 14.5), which have none yet (coordinator's rule: a row counts only
# with a passing signtest). One row at a time, 2 BLAS threads, nice 10, a per-row timeout; the planted control first.
#
# usage: signtest_lowD_driver.sh WT RAW OUT
#   WT   a choptuik-large-d worktree at wip/ell1-highD 505d839940456a3d04321d75cf66cc3b5bc831c4 (dss_ell and the D 4, D 6 records)
#   RAW  the root of a choptuik-large-d-raw clone holding every file listed in INPUTS below (a sparse clone is fine)
#   OUT  this machine's raw task folder (it must exist with its README.md); the driver writes OUT/signtest_lowD.log and
#        OUT/signtest_lowD.jsonl (and each row's full output in OUT/signtest_lowD_rows/) and refuses if either exists
#   PY   environment variable: the python with numpy and scipy (default python3)
# Per row: signtest.py STATE D kc around=RECORDS:D:0.02 with the record's own --u0/--Ks/--kappa/--rk, from WT/solver/matter.
# signtest.py first checks that these rebuild the record's discrete system (|F| within 1% of the record's or 1e-13, the same step count)
# and exits 3 without signs if not. A row PASSES if both lambda -/+ 0.02 have agree true and opposite signs.
# Stop rules: per-row timeout ROW_TIMEOUT seconds (default 7200); the batch stops after 2 consecutive rows that time out or crash
# (exit not 0 and not 3), and at once if the planted control does not print agree, agree, DISAGREE.
set -u
WT=$1; RAW=$2; OUT=$3; PY=${PY:-python3}; ROW_TIMEOUT=${ROW_TIMEOUT:-7200}
SIGNTEST_BLOB=179ea09681b0a75f7cefdff98984b48051b3f085
WT_COMMIT=505d839940456a3d04321d75cf66cc3b5bc831c4
export OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2
LOG=$OUT/signtest_lowD.log; JS=$OUT/signtest_lowD.jsonl
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*" | tee -a $LOG; }
[ -f $OUT/README.md ] || { echo "refuse: $OUT/README.md missing (make the task folder first)"; exit 2; }
[ -e $LOG ] || [ -e $JS ] && { echo "refuse: $LOG or $JS exists (use a fresh folder)"; exit 2; }
[ "$(git -C $WT rev-parse HEAD)" = "$WT_COMMIT" ] || { echo "refuse: $WT is not at $WT_COMMIT"; exit 2; }
ST=$RAW/I1025-mac/signtest.py
[ "$(git hash-object $ST)" = "$SIGNTEST_BLOB" ] || { echo "refuse: $ST is not blob $SIGNTEST_BLOB"; exit 2; }
# INPUTS: blob, path (raw paths relative to RAW, worktree paths relative to WT)
INPUTS="
53de6a4839b2b7263b86aaeffe1755ad8b58a28e RAW I810-mac/out/l1kc39d5s810.jsonl
be2fb5887dc0ff14ad3c9d2db6e159e9c00bbc87 RAW I810-mac/out/sol_l1kc39d5s810_D5.0000.npy
d96f2c3aac2da6f292bbd936b987341e5eb8e365 RAW I810-mac/out/l1kc39s810.jsonl
2033f3891ccdf71fdf13512f3b0848d3a25c1f5e RAW I810-mac/out/sol_l1kc39s810_D7.0000.npy
a44cc23fb8bd8dde4f49bbcfd3c738dfef062270 RAW I810-mac/out/sol_l1kc39s810_D8.0000.npy
997f082d4f0f85b5a181586c3774eb1450d33289 RAW I810-mac/out/sol_l1kc39s810_D9.0000.npy
c6dac7ca16beeb78c1494db5ed0818b2c8dc8582 RAW I660-mac/out/l1kc39t660.jsonl
737aa11918e7694afd051f0e869af3dbd55af793 RAW I660-mac/out/sol_l1kc39t660_D10.0000.npy
9237f140800926c7fe80709010c549c2a97991bb RAW I1025-mac/out/l1kc47r1025.jsonl
31379cc6dacdecabefb8f43e6dda5f2da07d1073 RAW I1025-mac/out/sol_l1kc47r1025_D10.5000.npy
8a01271a974fc9b1f3e671a98c46e142eaf74884 RAW I1025-mac/out/sol_l1kc47r1025_D11.0000.npy
4090cd96f7ca999ada2af6fe03c60cc1da961421 RAW I1025-mac/out/sol_l1kc47r1025_D11.5000.npy
034efc9eb538e0ed7a3a5ad4b4c07785dc84cb83 RAW I1025-mac/out/sol_l1kc47r1025_D12.0000.npy
38ccf3d081a634cb18d31524964e55648cc44bb9 RAW I1025-mac/out/l1kc39L1025.jsonl
2705a4c394f6c43c1373f07c53182b31b3e995e3 RAW I1025-mac/out/sol_l1kc39L1025_D12.5000.npy
2bb049b132058d9383f8f85a64ec6576de3fecde RAW I1025-mac/out/sol_l1kc39L1025_D13.0000.npy
fd96857d24dae7cde924cd922a1b20dec1652b81 RAW I1025-mac/out/l1kc47L1025.jsonl
f581080e301e5f04fb21d39e3a2dfb98ba35391c RAW I1025-mac/out/sol_l1kc47L1025_D13.5000.npy
56cc0051866b8ffd4f2c407f8ba12fb4b9c82bdc RAW I1025-mac/out/sol_l1kc47L1025_D14.0000.npy
5be40af42cdcf2c1c3751c1b28a03884759fcbd4 RAW I1025-mac/out/l1kc55Fb1025.jsonl
d9238215c3e1cfbcdeb1f990de24c41860c4c46a RAW I1025-mac/out/sol_l1kc55Fb1025_D14.5000.npy
d90f248896a32e11fc3c190776c4946e9775506c WT solver/matter/data/l1_D4_kc47.jsonl
9c6d051ad81ebb3e990ae61bc39d382ebcec6a26 WT solver/matter/data/sol_l1_D4_kc47_D4.0000.npy
6a5d8ea0e64efae75a981d018f65e4f88ec348e9 WT solver/matter/data/l1_kc31r.jsonl
a5befc266306419a0342144bbb2dcfd6e5e946df WT solver/matter/data/sol_l1_kc31r_D6.0000.npy
"
bad=0
while read -r b w p; do
  [ -z "$b" ] && continue
  [ "$w" = RAW ] && f=$RAW/$p || f=$WT/$p
  [ -f $f ] && [ "$(git hash-object $f)" = "$b" ] || { echo "refuse: $f missing or not blob $b"; bad=1; }
done <<< "$INPUTS"
[ $bad = 0 ] || exit 2
say "signtest_lowD_driver.sh: inputs checked; WT $WT_COMMIT, signtest.py $SIGNTEST_BLOB, PY $PY ($($PY -c 'import numpy, scipy; print("numpy", numpy.__version__, "scipy", scipy.__version__)')), 2 BLAS threads, row timeout $ROW_TIMEOUT s"
cd $WT/solver/matter
say "planted control"
$PY -u $ST planted < /dev/null 2>&1 | tee -a $LOG | tee $OUT/.planted.tmp
[ "$(grep -oE 'agree$|DISAGREE$' $OUT/.planted.tmp | tr '\n' ' ')" = "agree agree DISAGREE " ] || { say "STOP: the planted control did not print agree, agree, DISAGREE"; exit 4; }
mv $OUT/.planted.tmp $OUT/signtest_lowD_planted.log
# ROWS: D kc state records u0 Ks kappa rk (state and records as RAW: or WT: paths)
ROWS="
4 47 WT:solver/matter/data/sol_l1_D4_kc47_D4.0000.npy WT:solver/matter/data/l1_D4_kc47.jsonl 0.04 30 0.7 1
5 39 RAW:I810-mac/out/sol_l1kc39d5s810_D5.0000.npy RAW:I810-mac/out/l1kc39d5s810.jsonl 0.01 16 0.5 1
6 31 WT:solver/matter/data/sol_l1_kc31r_D6.0000.npy WT:solver/matter/data/l1_kc31r.jsonl 0.04 30 0.7 1
7 39 RAW:I810-mac/out/sol_l1kc39s810_D7.0000.npy RAW:I810-mac/out/l1kc39s810.jsonl 0.04 30 0.7 1
8 39 RAW:I810-mac/out/sol_l1kc39s810_D8.0000.npy RAW:I810-mac/out/l1kc39s810.jsonl 0.04 30 0.7 1
9 39 RAW:I810-mac/out/sol_l1kc39s810_D9.0000.npy RAW:I810-mac/out/l1kc39s810.jsonl 0.04 30 0.7 1
10 39 RAW:I660-mac/out/sol_l1kc39t660_D10.0000.npy RAW:I660-mac/out/l1kc39t660.jsonl 0.04 30 0.7 1
10.5 47 RAW:I1025-mac/out/sol_l1kc47r1025_D10.5000.npy RAW:I1025-mac/out/l1kc47r1025.jsonl 0.04 30 0.7 1
11 47 RAW:I1025-mac/out/sol_l1kc47r1025_D11.0000.npy RAW:I1025-mac/out/l1kc47r1025.jsonl 0.04 30 0.7 1
11.5 47 RAW:I1025-mac/out/sol_l1kc47r1025_D11.5000.npy RAW:I1025-mac/out/l1kc47r1025.jsonl 0.04 30 0.7 1
12 47 RAW:I1025-mac/out/sol_l1kc47r1025_D12.0000.npy RAW:I1025-mac/out/l1kc47r1025.jsonl 0.04 30 0.7 1
12.5 39 RAW:I1025-mac/out/sol_l1kc39L1025_D12.5000.npy RAW:I1025-mac/out/l1kc39L1025.jsonl 0.04 30 0.7 1
13 39 RAW:I1025-mac/out/sol_l1kc39L1025_D13.0000.npy RAW:I1025-mac/out/l1kc39L1025.jsonl 0.04 30 0.7 1
13.5 47 RAW:I1025-mac/out/sol_l1kc47L1025_D13.5000.npy RAW:I1025-mac/out/l1kc47L1025.jsonl 0.04 30 0.7 1
14 47 RAW:I1025-mac/out/sol_l1kc47L1025_D14.0000.npy RAW:I1025-mac/out/l1kc47L1025.jsonl 0.04 30 0.7 1
14.5 55 RAW:I1025-mac/out/sol_l1kc55Fb1025_D14.5000.npy RAW:I1025-mac/out/l1kc55Fb1025.jsonl 0.04 30 0.7 1
"
mkdir -p $OUT/signtest_lowD_rows
path() { case $1 in RAW:*) echo $RAW/${1#RAW:};; WT:*) echo $WT/${1#WT:};; esac; }
fails=0; summary=""
while read -r D kc st rec u0 Ks kap rk; do
  [ -z "$D" ] && continue
  say "row D $D k_c $kc: signtest.py $(path $st) $D $kc around=$(path $rec):$D:0.02 --u0=$u0 --Ks=$Ks --kappa=$kap --rk=$rk"
  timeout $ROW_TIMEOUT nice -n 10 $PY -u $ST $(path $st) $D $kc around=$(path $rec):$D:0.02 --u0=$u0 --Ks=$Ks --kappa=$kap --rk=$rk \
    < /dev/null > $OUT/signtest_lowD_rows/D$D.log 2>&1
  rc=$?
  grep -vE 'Warning|_umath_linalg|^ *sign, logdet' $OUT/signtest_lowD_rows/D$D.log | tee -a $LOG | grep '^{' >> $JS
  if [ $rc = 0 ]; then
    v=$(grep '"agree"' $OUT/signtest_lowD_rows/D$D.log | $PY -c 'import sys, json; r = [json.loads(l) for l in sys.stdin]
print("PASS" if len(r) == 2 and all(x["agree"] for x in r) and r[0]["signs"][0] != r[1]["signs"][0] else "FAIL")')
    fails=0
  elif [ $rc = 3 ]; then v="SYSTEM MISMATCH"; fails=0
  elif [ $rc = 124 ]; then v="TIMEOUT"; fails=$((fails + 1))
  else v="CRASH (exit $rc)"; fails=$((fails + 1)); fi
  say "row D $D k_c $kc: $v (exit $rc)"
  summary="$summary
D $D k_c $kc: $v"
  [ $fails -ge 2 ] && { say "STOP: two consecutive rows timed out or crashed"; break; }
done <<< "$ROWS"
say "summary:$summary"
say "signtest_lowD_driver.sh done"
exit
}
