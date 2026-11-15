#!/bin/bash
# #860 on winb (a runner's launcher; the issue's commands as given): Theorem A's certificates at M = 1, 3 and 5 on Windows
# x86-64, each logged with its exit code and wall time in exits.txt. Run in the worktree choptuik-i860 (data/ and logs/ of
# the m1 rerun are overwritten there and copied into the raw folder). box5 starts first in the background and the M = 1 and
# M = 3 parts and the rest of M = 5 run beside it, one process at a time. "ctrl" is a control that must fail by its verdict.
# The chain stops at the first unexpected result (a run that exits nonzero, a ctrl that exits 0 or whose log has a Traceback).
RAW=C:/Users/nathan/Source/choptuik-large-d-raw-754
O=$RAW/I860-winb
OB=/c/Users/nathan/Source/choptuik-large-d-raw-754/I860-winb
PY=/c/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe
WT=/c/Users/nathan/Source/choptuik-i860
export PYTHONUTF8=1
cd $WT/solver/proof || exit 9
mkdir -p $OB
EX=$OB/exits.txt
log() { echo "860 $1 $(date -u '+%F %T') UTC" >> $EX; }
{
  echo "commit $(git rev-parse --short=8 HEAD) ($(git rev-parse HEAD))"
  $PY -c "import flint, numpy, mpmath, scipy, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, 'scipy', scipy.__version__); print(platform.platform(), platform.machine(), 'python', sys.version.split()[0], 'uv-made venv venv-choptuik-314'); print('PYTHONUTF8=1 (logs are UTF-8 as on the Pi)')"
  powershell.exe -NoProfile -File C:/Users/nathan/AppData/Local/Temp/claude/bb1153300f5e1654/458d2fcb-c4f2-4c70-bd54-8689899a03bd/scratchpad/cpuinfo.ps1
} > $OB/env.txt 2>&1
run() {  # kind (run|ctrl), name, then the command's arguments; returns 1 on an unexpected result
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s.%N)
  $PY -u "$@" > $OB/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(awk "BEGIN{printf \"%.3f\", $(date +%s.%N) - $t}") s ($kind)"
  if [ $kind = run ] && [ $rc -ne 0 ]; then log "$name UNEXPECTED: a run exited $rc"; return 1; fi
  if [ $kind = ctrl ] && [ $rc -eq 0 ]; then log "$name UNEXPECTED: a control exited 0"; return 1; fi
  if [ $kind = ctrl ] && grep -q Traceback $OB/$name.log; then log "$name UNEXPECTED: a control crashed"; return 1; fi
  return 0
}
must() { run "$@" || { log "stopped after $2"; exit 1; }; }
B1=$O/A_M2_box_M1_1e-6.json; B3A=$O/A_M_box_M3_1e-10.json; B3=$O/A_M2_box_M3_1e-8.json; B5=$O/A_M2_box_M5_1e-10.json
# box5 first, in the background (two processes at most)
run run box5 certify_M2.py box 5 --chart=data/A_M2_chart_M5.json --h=1e-10 --w=1e-18,1e-19 --out=$B5 --log=$O/A_M2_box_M5_1e-10.log &
# ---- A(M = 1)
must run certify_M1          certify_M1.py
must run certify_M1_pm       certify_M1.py --pm
must run residual_poly       residual_poly.py 0.08
must run fixed_point         fixed_point.py
must run fixed_point_box     fixed_point.py --box=1e-3,1e-3
must run fixed_point_sector  fixed_point.py --sector=0.2
must run fixed_point_008     fixed_point.py 0.08
must run krawczyk            krawczyk.py --xi1=0.3
must run vi_point            validated_int.py krawczyk 1e-9 --only=point --out=$O/vi_point.json
must run vi_box              validated_int.py krawczyk 1e-9 --only=box --out=$O/vi_box.json
must run vi_test_own         validated_int.py krawczyk 1e-9 --point=$O/vi_point.json --box=$O/vi_box.json
must run vi_test_stored      validated_int.py krawczyk 1e-9 --point=validated_int_krawczyk_1e-9.json --box=validated_int_krawczyk_1e-9.json
must run vi_test_pi          validated_int.py krawczyk 1e-9 --point=$RAW/I843-rpi5/vi_point.json --box=$RAW/I843-rpi5/vi_box.json
log "part M1 done"
# ---- A(M = 3)
must run  sys_selftest       certify_M_sys.py selftest
must ctrl sys_selftest_mut   certify_M_sys.py selftest --mutate=coupling
must run  m1_rerun           certify_M.py m1 --rerun
must ctrl m1_mut             certify_M.py m1 --mutate=m1ref
must run  startcheck3        certify_M.py startcheck 3
must ctrl startcheck3_mut    certify_M.py startcheck 3 --mutate
must run  crosscheck3        certify_M.py crosscheck 3
must ctrl crosscheck3_mut    certify_M.py crosscheck 3 --mutate
must run  box3               certify_M.py box 3 --centre=data/A_M_refine_M3_c.json --use_out --h=1e-10 --w=4e-16 --out=$B3A --log=$O/A_M_box_M3_1e-10.log
must run  krawczyk3          certify_M.py krawczyk --box=$B3A --hier
must run  controls3          certify_M.py controls --box=$B3A
must ctrl krawczyk3_mut      certify_M.py krawczyk --box=$B3A --hier --mutate=hier
must run  recheck3           certify_M_recheck.py $B3A
must ctrl recheck3_mut       certify_M_recheck.py $B3A --mutate
must run  krawczyk3_stored   certify_M.py krawczyk --box=data/A_M_box_M3_1e-10.json --hier
must run  krawczyk3_pi       certify_M.py krawczyk --box=$RAW/I844-rpi5/A_M_box_M3_1e-10.json --hier
must run  usys_M             lemma6_usys_M.py
must run  fpm_check_m1       fixed_point_M.py --check-m1
must run  fpm_M3             fixed_point_M.py --M=3
cp data/A_M_point_M1.json data/A_M_box_M1_1e-9.json logs/A_M_m1.log $OB/ 2>> $EX
log "part M3 done"
# ---- A(M = 5), without box5
must run  lohner_selftest     certify_M2_lohner.py selftest
must ctrl lohner_selftest_mut certify_M2_lohner.py selftest --mutate=lin2
must run  box1                certify_M2.py box 1 --chart=data/A_M2_chart_M1.json --h=1e-6 --w=0 --out=$B1 --log=$O/A_M2_box_M1_1e-6.log
must run  krawczyk1           certify_M2.py krawczyk --box=$B1 --shrink --reference=thmA1
must ctrl krawczyk1_mut       certify_M2.py krawczyk --box=$B1 --shrink --reference=thmA1 --mutate=ref
must run  controls1           certify_M2.py controls --box=$B1
must run  recheck1            certify_M_recheck.py $B1
must ctrl recheck1_mut        certify_M_recheck.py $B1 --mutate
must run  box3m2              certify_M2.py box 3 --chart=data/A_M2_chart_M3.json --h=1e-8 --w=1e-13 --out=$B3 --log=$O/A_M2_box_M3_1e-8.log
must run  krawczyk3m2         certify_M2.py krawczyk --box=$B3 --shrink --reference=AM3
must run  controls3m2         certify_M2.py controls --box=$B3
must run  d2check3            certify_M2.py d2check --box=$B3 --fd=data/A_M2_fd_M3.json
must run  recheck3m2          certify_M_recheck.py $B3
must ctrl recheck3m2_mut      certify_M_recheck.py $B3 --mutate
must run  krawczyk5_stored    certify_M2.py krawczyk --box=data/A_M2_box_M5_1e-10.json --shrink --hier
must run  krawczyk5_pi        certify_M2.py krawczyk --box=$RAW/I847-rpi5/A_M2_box_M5_1e-10.json --shrink --hier
log "waiting for box5"
wait
grep -q "box5 exit 0 " $EX || { log "stopped: box5 did not exit 0"; exit 1; }
if grep -q "box5 UNEXPECTED" $EX; then log "stopped: box5 unexpected"; exit 1; fi
must run  krawczyk5           certify_M2.py krawczyk --box=$B5 --shrink --hier
must ctrl krawczyk5_mut       certify_M2.py krawczyk --box=$B5 --hier --mutate=hier
must run  controls5           certify_M2.py controls --box=$B5
must run  d2check5            certify_M2.py d2check --box=$B5 --fd=data/A_M2_fd_M5.json
log "part M5 done"
log "all done"
