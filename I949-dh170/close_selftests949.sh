#!/bin/bash
# #949 close-out: every selftest must exit 0 and every --mutate must exit 1 (a control that does not fail is itself a failure).
cd /home/nathan/Source/choptuik-large-d-raw/I949-dh170 || exit 9
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
bad=0
run() { want=$1; shift; out=$(OPENBLAS_NUM_THREADS=1 timeout 1200 nice -n 10 $PY -I "$@" 2>&1); rc=$?; if [ "$rc" = "$want" ]; then v=ok; else v=WRONG; bad=1; fi
  echo "$* -> exit $rc (want $want): $v"; echo "$out" | tail -n 1 | cut -c1-160; }
for f in track949.py pairfold949.py fold949.py twomode949.py stopcheck949.py; do
  run 0 $f --selftest
  run 1 $f --selftest --mutate
done
run 0 relay_dh370_949.py --selftest
run 1 relay_dh370_949.py --selftest --mutate
run 1 relay_dh370_949.py --selftest --mutate=sign
echo "close selftests: $([ $bad = 0 ] && echo all ok || echo SOME WRONG)"
exit $bad
