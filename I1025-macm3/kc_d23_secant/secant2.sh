#!/bin/bash
# #1025 macm3 kc_d23_secant (t5's order, hc 25 Nov ~23:50 UTC): refine lambda_1 at D 23.0 at k_c 87 (my part c2 state, bracket -0.040 to -0.020) and at k_c 95 (win2's accepted state, bracket 0.000 to 0.020) with d18_secant.py
# of origin/wip/ell1-speed 6010e37b (worktree ~/Source/choptuik-large-d-1025s; the setup and controls of SPEED_ELL1.md, as kc103_d23/secant/secant103.sh), --tol=1e-5 --maxev=10, pinned by blob (--pin=state blob,record blob),
# one process each, nice 10, cap 18000 s by capped_run.py; the two cases run side by side. Venv: venv-macm3-1058b (t5 accepted it for venv-1025dd).
# Stops (hc to t5): a pin, selftest or control that does not read as written, exit 2 or 3, a traceback. usage: bash secant2.sh kc87|kc95 [dry]
{
set -u
NAME=${1:?kc87 or kc95}; MODE=${2:-}
K=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc_d23_secant; IN=$K/in; S=$K/$NAME/secant; C=$K/$NAME/checks
WT=$HOME/Source/choptuik-large-d-1025s; WTM=$WT/solver/matter; WT5=$HOME/Source/choptuik-large-d-1025m/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
D=23.0
case $NAME in
  kc87) STUB=l1kc87Lmacm3c2.jsonl; STATE=sol_l1kc87Lmacm3c2_D23.000000.npy; PIN=bb32ff05,2dda16f7; LO=-0.040; HI=-0.020;;
  kc95) STUB=l1kc95win2d23.jsonl; STATE=sol_l1kc95win2d23_D23.0000.npy; PIN=096f1cc0,e3fff23f; LO=0.000; HI=0.020;;
  kc87b) STUB=l1kc87Lmacm3c2_asof_D22.9375.jsonl; STATE=sol_l1kc87Lmacm3c2_D22.937500.npy; PIN=5d759685,e854c38e; LO=0.040; HI=0.060; D=22.9375;;
  kc111dh) STUB=l1kc111dh170j.jsonl; STATE=sol_l1kc111dh170j_D23.0000.npy; PIN=c0edd3c1,74d49790; LO=0.020; HI=0.040; D=23.0;;
  kc95L) STUB=l1kc95Lw1025m.jsonl; STATE=sol_l1kc95Lw1025m_D23.062500.npy; PIN=696bd814,a54f6896; LO=-0.060; HI=-0.040; D=23.0625;;
  *) echo "kc87, kc95, kc95L, kc87b or kc111dh"; exit 9;;
esac
HC=$(command -v hc); LOG=$K/exits_$NAME.txt
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC kc_d23_secant/$NAME: $*" | tee -a $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stop() { tell "macm3 #1025 kc_d23_secant/$NAME STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
mkdir -p $S $C
export PYTHONDONTWRITEBYTECODE=1 RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
say "start (mode ${MODE:-full}; load $(sysctl -n vm.loadavg), $(availgib) GiB available)"
while read bb f; do case "$bb" in "#"*) continue;; esac
  [ -f $K/$f ] && [ "$(blob $K/$f)" = "$bb" ] || stop "$K/$f missing or not blob $bb"; done < $K/in_blobs.txt
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = "6010e37b" ] && [ -z "$(git -C $WT status --short)" ] || stop "worktree $WT is not clean at 6010e37b"
for p in "d18_secant.py a3d90cd5" "ell_fastm.py 93f963f6" "ell_fastdd.py 237ebfdd"; do set -- $p; [ "$(blob $WTM/$1)" = "$2" ] || stop "$1 is not blob $2"; done
for f in dss_ell.py ell_ddm.py ell_dd.py ddnp.py; do [ "$(blob $WTM/$f)" = "$(blob $WT5/$f)" ] || stop "$f differs from the scan worktree's (505d8399)"; done
"$PY" -c "import multidouble, sys; sys.exit(0 if hasattr(multidouble, 'dd_logdet') else 1)" || stop "multidouble of $PY has no dd_logdet"
say "pins checked (in_blobs.txt; state and record ${PIN}), worktree 6010e37b clean, code blobs as pinned, dd_logdet present; $($PY -V), multidouble $($PY -c 'import importlib.metadata as m; print(m.version("multidouble"))')"
cd $WTM || exit 9
ex="$(nice -n 10 $PY d18_secant.py selftest > $C/d18_secant_selftest.txt 2>&1; echo $?)"
for m in half norobust nosigncheck; do nice -n 10 $PY d18_secant.py selftest --mutate=$m > $C/d18_secant_selftest_$m.txt 2>&1; ex="$ex $?"; done
[ "$ex" = "0 1 1 1" ] || stop "d18_secant selftest exits '$ex' (wanted '0 1 1 1': selftest, half, norobust, nosigncheck)"
say "selftest as wanted: d18_secant exit 0, mutations half norobust nosigncheck exit 1 1 1 (ell_fastm and ell_fastdd selftests and controls: kc103_d23/secant/checks, same blobs)"
case $NAME in kc95L) POS=kc95; NEGS="kc87 kc103";; kc87b) POS=kc87; NEGS="kc95 kc103";; kc111dh) POS=kc111; NEGS="kc103 kc95";; *) POS="";; esac
if [ -n "$POS" ]; then   # a state taken from another run (win2's leg state; my part c2 state at D 22.9375): the $POS check accepts it (controls 1 1), the other two checks refuse it
  A="nice -n 10 $PY -I $IN/${POS}_syscheck_1025.py $IN/$STUB $IN/$STATE $D $WTM"
  $A > $C/accept_$POS.txt 2>&1; a0=$?; $A --mutate=F > $C/accept_${POS}_mutF.txt 2>&1; a1=$?; $A --mutate=steps > $C/accept_${POS}_mutsteps.txt 2>&1; a2=$?
  set -- $NEGS; N1=$1; N2=$2
  nice -n 10 $PY -I $IN/${N1}_syscheck_1025.py $IN/$STUB $IN/$STATE $D $WTM > $C/accept_${N1}_refuses.txt 2>&1; a3=$?
  nice -n 10 $PY -I $IN/${N2}_syscheck_1025.py $IN/$STUB $IN/$STATE $D $WTM > $C/accept_${N2}_refuses.txt 2>&1; a4=$?
  say "acceptance of the state: ${POS}_syscheck exit $a0 (0 wanted), controls --mutate=F $a1 and --mutate=steps $a2 (1 wanted each), ${N1}_syscheck $a3 and ${N2}_syscheck $a4 on it (1 wanted each): $(grep -E '^D ' $C/accept_$POS.txt | cut -c1-260)"
  [ "$a0 $a1 $a2 $a3 $a4" = "0 1 1 1 1" ] || stop "the state is not accepted as written (exits $a0 $a1 $a2 $a3 $a4; wanted 0 1 1 1 1)"
fi
[ "$MODE" = dry ] && { say "dry run ends here"; exit 0; }
[ -e $S/secant.jsonl ] && stop "$S/secant.jsonl exists"
say "secant run starts: d18_secant.py run $STUB $STATE $D $LO $HI secant.jsonl --tol=1e-5 --maxev=10 --pin=$PIN (one process, nice 10, cap 18000 s)"
nice -n 10 $PY -u $IN/capped_run.py 18000 $PY -u $WTM/d18_secant.py run $IN/$STUB $IN/$STATE $D $LO $HI $S/secant.jsonl --tol=1e-5 --maxev=10 --pin=$PIN > $S/secant.log 2>&1 &
rp=$!
echo "time_utc,pid,rss_kB,pcpu,avail_GiB" > $S/samples.csv
( while kill -0 $rp 2>/dev/null; do for p in $(pgrep -f "d18_secant.py run.*kc_d23_secant/$NAME/secant"); do echo "$(stamp),$p,$(ps -o rss= -p $p | tr -d ' '),$(ps -o pcpu= -p $p | tr -d ' '),$(availgib)" >> $S/samples.csv; done; sleep 60; done ) &
wait $rp; sc=$?
say "secant run exit $sc"
[ $sc = 0 ] || [ $sc = 4 ] || stop "d18_secant.py exit $sc (0 tol reached, 4 maxev or non-robust interior point; 2 refused, 3 pin or record system): see $S/secant.log"
$PY $K/summarize_point.py $K/$NAME $S > $K/$NAME/secant_summary.txt 2>&1
bash $K/push_kc_d23_secant.sh "kc_d23_secant/$NAME: D 23.0 root refined (d18_secant.py)" > /dev/null 2>&1
tell "macm3 #1025 kc_d23_secant/$NAME: $(grep -E '^(scan:|secant: status|secant root)' $K/$NAME/secant_summary.txt | tr '\n' ';' | cut -c1-1300) (raw kc_d23_secant/$NAME/)"
exit 0
}
