#!/bin/bash
# stage_secant.sh (kc111_d22875, dh610): d18_secant.py run (wip/ell1-speed 92b9bf53, blob eb1396ad) on the scan's robust bracket nearest PRED 0.12, one process of one thread, nice 10, cap 54000 s, --tol=1e-5 --maxev=10, no --ends, the pins of the
# regrid's state and record. No robust change: no secant. Read when the stage starts. Exits 0 when it has run or has nothing to refine; the tool's own exits 2, 3, 4 are reported as printed.
source /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc111_d22875/common_kc111.sh
BR=$($PY -I -c "
import sys; sys.path.insert(0, '$IN')
import leg_read
ch = leg_read.parse(open('$F/read_lower.txt').read())
if ch:
    b = min(ch, key=lambda c: abs(c['det'] - $PRED)); print('%.3f %.3f %d' % (b['lo'], b['hi'], len(ch)))")
if [ -z "$BR" ]; then say "no robust change: no secant refinement"; exit 0; fi
read -r LO HI NCH <<< "$BR"
SB=$(blob $IN/sol_${TAG}_D${DS}.npy); RB=$(blob $IN/$TAG.jsonl)
export RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1; unset P4_WT_MATTER
CMD2="nice -n 10 timeout 54000 $PY -u d18_secant.py run $IN/$TAG.jsonl $IN/sol_${TAG}_D${DS}.npy $D $LO $HI $SEC/secant.jsonl --tol=1e-5 --maxev=10 --pin=$SB,$RB"
echo "# $(stamp) UTC cmd (cwd $SWM, 1 process, nice 10, cap 54000 s; $NCH robust change(s) in the scan, the one nearest $PRED refined): $CMD2" > $SEC/secant.log
say "secant starts (bracket $LO to $HI of $NCH robust change(s); d18_secant.py blob $(blob $SWM/d18_secant.py | cut -c1-8)): $CMD2"
( while sleep 60; do echo "$(stamp),$(ps -C python -o rss=,pcpu=,nlwp=,args= | grep 'd18_secant.py' | grep -v grep | head -1 | cut -d' ' -f1-4)" >> $SEC/secant_samples.csv; done ) &
SAMP2=$!
t1=$(date +%s)
( cd $SWM && $CMD2 >> $SEC/secant.log 2>&1 ); rc2=$?
kill $SAMP2 2>/dev/null
say "secant exit $rc2 (0 tol reached; 4 maxev or a non-robust interior point; 2 refused; 3 pin or record system; 124 the cap), wall $(( $(date +%s) - t1 )) s"
$PY -I -c "
import json
for l in open('$SEC/secant.jsonl'):
    r = json.loads(l)
    print({k: r[k] for k in r if k not in ('noise_ln',)})" > $SEC/secant_summary.txt 2>&1
say "secant: $(grep -F "'kind': 'root'" $SEC/secant_summary.txt | cut -c1-600)"
bash $PUSH I1025-dh610/kc111_d22875 "I1025-dh610/kc111_d22875: secant refinement of the D 22.875 root" > $F/push_final.txt 2>&1
exit 0
