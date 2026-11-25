#!/bin/bash
# keeps b2/, c/ and c2/ delta_reg_rows.txt current (t5, 24 Nov: "keep delta_reg in every tracker row"; the pinned mode_tracker.py does not print it): every 60 s, delta_rows.py on the pushed record copies;
# exits (after a last pass) when b2 has ended and part c has ended or was not started / not needed. The driver's next push carries the files.
L2=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
PY=$HOME/Source/venv-macm3-1058b/bin/python
pass() {
  for d in b2:l1kc87Lmacm3b2 c:l1kc87Lmacm3c c2:l1kc87Lmacm3c2; do
    sub=${d%%:*}; tag=${d##*:}
    [ -e $L2/$sub/$tag.jsonl ] || continue
    python3 $L2/delta_rows.py $L2/$sub/$tag.jsonl > $L2/$sub/delta_reg_rows.txt.new 2>> $L2/delta_rows_loop.err && { cmp -s $L2/$sub/delta_reg_rows.txt.new $L2/$sub/delta_reg_rows.txt && rm -f $L2/$sub/delta_reg_rows.txt.new || mv $L2/$sub/delta_reg_rows.txt.new $L2/$sub/delta_reg_rows.txt; }
  done
}
while :; do
  pass
  if [ -e $L2/b2/LEG_DONE.txt ] && { [ -e $L2/c/LEG_DONE.txt ] || grep -qE 'not needed|NOT started' $L2/start_c2.log; } && { [ -e $L2/c2/LEG_DONE.txt ] || grep -qE 'not needed|NOT started' $L2/start_cont.log 2>/dev/null; }; then sleep 90; pass; echo "$(date -u '+%F %T') UTC delta_rows_loop ends" >> $L2/delta_rows_loop.err; exit 0; fi
  sleep 60
done
