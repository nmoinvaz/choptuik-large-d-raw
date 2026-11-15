#!/bin/bash
# #843 on rpi5 (the coordinator): Theorem A(M = 1)'s certificate on aarch64 Linux, the commands of proof/A_certify.md
# sections 8 and 9, each logged with its exit code and wall time, then the cross-load of the stored x86 runs.
SELF=$(realpath "$0")
R=/home/nathan/Source/choptuik-large-d-raw/I843-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
cd /home/nathan/Source/choptuik-large-d/solver/proof || exit 9
mkdir -p $R
log() { echo "843 $1 $(date -u '+%F %T') UTC" >> $R/exits_843.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import flint, numpy, mpmath, scipy, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, 'scipy', scipy.__version__, platform.platform(), platform.machine(), 'python', sys.version.split()[0])"
  cat /proc/device-tree/model 2>/dev/null; echo; nproc; free -g | head -2
} > $R/env.txt 2>&1
run() {  # name, then the command's arguments
  local name=$1; shift
  log "$name start"
  local t=$(date +%s.%N)
  $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s"
}
run certify_M1 certify_M1.py
run certify_M1_pm certify_M1.py --pm
run fixed_point fixed_point.py
run fixed_point_box fixed_point.py --box=1e-3,1e-3
run fixed_point_sector fixed_point.py --sector=0.2
run fixed_point_008 fixed_point.py 0.08
run krawczyk krawczyk.py --xi1=0.3
run vi_point validated_int.py krawczyk 1e-9 --only=point --out=$R/vi_point.json
run vi_box validated_int.py krawczyk 1e-9 --only=box --out=$R/vi_box.json
run vi_test_own validated_int.py krawczyk 1e-9 --point=$R/vi_point.json --box=$R/vi_box.json
run vi_test_stored validated_int.py krawczyk 1e-9 --point=validated_int_krawczyk_1e-9.json --box=validated_int_krawczyk_1e-9.json
log "all done"
