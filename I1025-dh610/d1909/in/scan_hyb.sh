#!/bin/bash
# #1025 hybrid det-sign scan on the k_c 63 leap state at D $1 over lambda $2 to $3 at 0.01, NP processes of THR threads, nice 10.
# usage: [OUTSUF=_time] bash scan_hyb.sh D LO HI [NP=3] [THR=2]   (D = 19, 19.5 or 20; the window is posted on the issue before the start)
# d18_hybsign.py is xfkappa's, blob e089207a, unmodified; it checks the state against the record line first.
{
D=$1; LO=$2; HI=$3; NP=${4:-3}; THR=${5:-2}
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
SRC=/home/nathan/Source/choptuik-large-d-raw-push960/I1025-mac/d18
WT=/home/nathan/Source/choptuik-large-d-1025
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
TAG=l1kc63dh370
DT=$(printf 'D%.6f' $D)
OUT=$RAW/I1025-dh370/hyb_${DT}${OUTSUF}
STATE=$WT/solver/matter/data/sol_${TAG}_${DT}.npy
STUB=$WT/solver/matter/data/${TAG}.jsonl
mkdir -p $OUT
[ "$(git hash-object $SRC/d18_hybsign.py | cut -c1-8)" = e089207a ] || { echo "d18_hybsign.py is not blob e089207a: stop" >> $OUT/exits.txt; exit 1; }
[ -f $STATE ] || { echo "no state $STATE: stop" >> $OUT/exits.txt; exit 1; }
cp $STATE $STUB $OUT/
mapfile -t LAMS < <(python3 -I -c "
lo, hi = round($LO*100), round($HI*100)
print(*[f'{v/100:.2f}' for v in range(lo, hi + 1)], sep='\n')")
echo "$(date -u '+%F %T') UTC scan D $D lambda $LO..$HI (${#LAMS[@]} values), $NP procs x $THR threads, nice 10" >> $OUT/exits.txt
pids=()
for ((p = 0; p < NP; p++)); do
  mine=""
  for ((i = p; i < ${#LAMS[@]}; i += NP)); do mine="$mine,${LAMS[$i]}"; done
  mine=${mine#,}
  ( cd $WT/solver/matter && nice -n 10 env OMP_NUM_THREADS=$THR OPENBLAS_NUM_THREADS=$THR MKL_NUM_THREADS=$THR \
      P4_WT_MATTER=$WT/solver/matter $PY -u $SRC/d18_hybsign.py $STUB $STATE $D $mine $OUT/scan_${DT}_p$p.jsonl > $OUT/scan_${DT}_p$p.log 2>&1
    echo "$(date -u '+%F %T') UTC proc $p exit $?" >> $OUT/exits.txt ) &
  pids+=($!)
done
wait "${pids[@]}"
cat $OUT/scan_${DT}_p*.jsonl | python3 -I -c "
import sys, json
rows = sorted((json.loads(l) for l in sys.stdin if l.strip()), key=lambda r: r['lam'])
open('$OUT/scan_${DT}_1025.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in rows))
print(len(rows), 'points')" >> $OUT/exits.txt
echo "$(date -u '+%F %T') UTC scan D $D done" >> $OUT/exits.txt
exit 0
}
