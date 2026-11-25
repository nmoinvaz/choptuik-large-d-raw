#!/bin/bash
# #1025 kc111_d21125, the WIDENING ordered by t5's hc (25 Nov, 01:5x UTC): the same state and code as run_scan.sh, four more single-thread processes beside round 2 (lambda 0.875, 0.870 below and 0.905, 0.910 above), lists in stage.conf
# (LAMPW, WINW). Writes scan/scan_D21.125w_p<p>.jsonl and scan/scanw_p<p>.raw (names that the first scan's globs do not match). When the first scan has ended (SCAN_DONE.txt) and these processes have ended it reads the combined window
# (read_lower_wide.txt) and writes SCAN_WIDE_DONE.txt. Memory: alert only, nothing killed on memory. usage: run_scan_wide.sh [dry]. A systemd user unit.
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc111_d21125
MODE=${1:-}
OUT=$ROOT; IN=$OUT/in
WT=/home/nathan/Source/choptuik-large-d-1025k79; WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
[ -f $OUT/stage.conf ] || { echo "no $OUT/stage.conf"; exit 9; }
. $OUT/stage.conf
SCAN=$OUT/scan
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" | tee -a $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1"; }
grep -q '^ACCEPTED' $OUT/VERDICT.txt 2>/dev/null || { step "SCAN STOP: no ACCEPTED verdict"; exit 1; }
while read -r h f; do [ "$(blob $IN/$f)" = "$h" ] || { step "SCAN STOP: in/$f is not blob $h"; exit 1; }; done < $OUT/in_blobs.txt
STATE=$OUT/sol_${TAG}_${DT}.npy; STUB=$OUT/$TAG.jsonl
[ -s $STATE ] && [ -s $STUB ] && [ -s $WTM/data/sol_${TAG}_${DT}.npy ] && [ -s $WTM/data/$TAG.jsonl ] || { step "SCAN STOP: the accepted state or record is missing or empty"; exit 1; }
[ "$(blob $STATE)" = "$(blob $WTM/data/sol_${TAG}_${DT}.npy)" ] && [ "$(blob $STUB)" = "$(blob $WTM/data/$TAG.jsonl)" ] || { step "SCAN STOP: the accepted state or record differs from the worktree's"; exit 1; }
[ -e $OUT/SCAN_WIDE_DONE.txt ] && { step "WIDE STOP: SCAN_WIDE_DONE.txt exists"; exit 1; }
[ -e $SCAN/scanw_p0.raw ] && [ "$MODE" != dry ] && { step "WIDE STOP: the wide scan already started"; exit 1; }
LAMP=("${LAMPW[@]}"); NP=${#LAMP[@]}
[ "$MODE" = dry ] && { n=0; for ((p = 0; p < NP; p++)); do echo "process $p: ${LAMP[$p]}"; n=$((n + $(echo ${LAMP[$p]} | tr ',' '\n' | wc -l))); done; echo "dry run: pins ok, $n evaluations"; exit 0; }
mkdir -p $SCAN
( while sleep 30; do av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); [ "$av" -lt 2048 ] && echo "ALERT $(stamp) UTC MemAvailable $av MiB (alert only, nothing stopped)" >> $OUT/alert.log; done ) &
MEM=$!
( while sleep 60; do echo "$(stamp),$(ps -eo rss=,pcpu=,args= | grep 'd18_hybsign.py' | grep -vE 'grep|time -v' | awk '{r+=$1} END{print r*1024 " bytes rss total, " NR " procs"}'),MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)" >> $SCAN/scan_samples_wide.csv; done ) &
SAMP=$!
step "WIDE scan starts: D $D, $NP evaluations (lambda ${LAMPW[*]}), $NP procs x 1 thread, nice 10; state sol_${TAG}_${DT}.npy $(blob $STATE | cut -c1-8), record $(blob $STUB | cut -c1-8)"
pids=()
for ((p = 0; p < NP; p++)); do
  mine=${LAMP[$p]}
  ( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM \
      /usr/bin/time -v $PY -u $IN/d18_hybsign.py $STUB $STATE $D "$mine" $SCAN/scan_D${D}w_p$p.jsonl > $SCAN/scanw_p$p.raw 2>&1
    rc=$?; echo "$(stamp) UTC WIDE proc $p (lambda $mine) exit $rc" >> $OUT/steps.txt ) &
  pids+=($!)
done
wait "${pids[@]}"
kill $SAMP $MEM 2>/dev/null
grep -h 'the record system\|NOT the record system' $SCAN/scanw_p*.raw | sort | uniq -c >> $OUT/steps.txt
grep -hE 'Elapsed|Maximum resident' $SCAN/scanw_p*.raw | sort | uniq -c >> $OUT/steps.txt
step "waiting for the first scan (SCAN_DONE.txt) before the combined reading"
until [ -e $OUT/SCAN_DONE.txt ]; do sleep 20; done
cat $SCAN/scan_D${D}_p*.jsonl $SCAN/scan_D${D}w_p*.jsonl > $OUT/merged_wide_D${D}.jsonl
cd $IN
{ echo "== combined window: read_lower.py scan $WINW (both scans' points)"; $PY -I read_lower.py $SCAN $WINW; echo "(exit $?)"; } > $OUT/read_lower_wide.txt 2>&1
step "read_lower.py read the combined window (reading in read_lower_wide.txt)"
$PY -I repeat_check.py $OUT/merged_wide_D${D}.jsonl >> $OUT/read_lower_wide.txt 2>&1; step "repeat_check.py exit $?"
echo "SCAN WIDE DONE $(stamp) UTC" > $OUT/SCAN_WIDE_DONE.txt
step "wide scan done"
exit 0
}
