#!/bin/bash
# #944: stop a probe run after its first attempt has printed newton_od's "junk directions frozen" line, unless that line
# says more than 0 junk directions (then the run continues). usage: stop_at_junk_line.sh NAME. Prints the line.
NAME=${1:?name}
OUT=$HOME/Source/choptuik-large-d-raw/I944-dh170
while true; do
  L=$(awk '/^step 0: D /{f=1} f && /junk directions frozen/{print; exit}' $OUT/$NAME.log 2>/dev/null)
  [ -n "$L" ] && break
  pgrep -f "^timeout .*anm_run.py .*$OUT/$NAME " > /dev/null || { echo "run $NAME ended before the line"; exit 1; }
  sleep 5
done
echo "$L"
case "$L" in
  *" 0 junk directions frozen"*)
    pkill -TERM -f "^timeout .*anm_run.py .*$OUT/$NAME "
    echo "944 $NAME stopped by me at the first attempt's junk line (0 junk directions, the attempt is the default's) $(date -u '+%F %T') UTC" >> $OUT/exits_944.txt ;;
  *) echo "junk directions above 0: the run continues" ;;
esac
