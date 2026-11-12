# sourced by lane_a.sh and lane_b.sh
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I537-win2
J=I461-win2/crawlJ/anm_pin3_D242.3642.npz
MAIN=/d/choptuik-i446g/hp
EQ=/d/choptuik-i505/hp
export PYTHONFAULTHANDLER=1
# step LANE NAME WORKDIR EXPECT(0|1) LOG cmd...   runs cmd, logs start and exit, stops the lane on an unexpected exit code or a Traceback
step() {
  local lane=$1 name=$2 wd=$3 expect=$4 log=$5; shift 5
  cd $wd || { echo "$lane $name: no $wd" >> $R/exits.txt; exit 9; }
  echo "$lane $name start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  "$@" > $R/$log 2>&1
  local rc=$?
  echo "$lane $name exit $rc (expected $expect) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  if grep -q Traceback $R/$log; then echo "$lane $name: Traceback in $log, lane stopped" >> $R/exits.txt; exit 8; fi
  if [ "$expect" = 0 ] && [ $rc -ne 0 ]; then echo "$lane $name: nonzero exit, lane stopped" >> $R/exits.txt; exit 7; fi
  if [ "$expect" = 1 ] && [ $rc -eq 0 ]; then echo "$lane $name: control did not fail, lane stopped" >> $R/exits.txt; exit 6; fi
  return 0
}
[ "$(cd $MAIN && git rev-parse --short=7 HEAD)" = "14dc386" ] || { echo "D:/choptuik-i446g is not at 14dc386" >&2; exit 9; }
[ "$(cd $EQ && git rev-parse --short=7 HEAD)" = "0cce81e" ] || { echo "D:/choptuik-i505 is not at 0cce81e" >&2; exit 9; }
