#!/bin/bash
# #1025 macm3 kc103_d23/secant (t5's order, hc 25 Nov ~22:55 UTC, step 1): refine the k_c 103 root of lambda_1 at D 23.0 (bracket 0.020-0.030 of my scan kc87_leg_lambda/23.0_kc103) with d18_secant.py of
# origin/wip/ell1-speed 6010e37b (worktree ~/Source/choptuik-large-d-1025s), setup and controls of solver/matter/SPEED_ELL1.md: selftest exit 0, --mutate=half|norobust|nosigncheck exit 1 each (and ell_fastm,
# ell_fastdd selftests with their controls nolam, jround exit 1), one process, --tol=1e-5 --maxev=10, --pin=state blob,stub blob, no --ends (both ends evaluated), default fast float64 matrix and ell_ddm's block 12.
# The venv is venv-macm3-1058b (venv-1025dd is not on this machine; the doc asks for "the venv whose multidouble has dd_logdet": checked here). Memory: waits for 8 GiB available at the start, alert only after.
# Stops (hc to t5): a pin, selftest or control that does not read as written, exit 2 or 3, a traceback. usage: bash secant103.sh [dry]
{
set -u
MODE=${1:-}
F=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc103_d23; IN=$F/in; S=$F/secant; C=$S/checks
WT=$HOME/Source/choptuik-large-d-1025s; WTM=$WT/solver/matter; WT5=$HOME/Source/choptuik-large-d-1025m/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
STATE=sol_l1kc103macm3d23_D23.0000.npy; STUB=l1kc103macm3d23.jsonl; SB=845e92a5; TB=22b366e1
HC=$(command -v hc); LOG=$S/exits_secant.txt
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC kc103_d23/secant: $*" | tee -a $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stop() { tell "macm3 #1025 kc103_d23/secant STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
mkdir -p $C
export PYTHONDONTWRITEBYTECODE=1 RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
say "start (mode ${MODE:-full}; load $(sysctl -n vm.loadavg), $(availgib) GiB available)"
# 1. pins: the code of the worktree and the inputs
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = "6010e37b" ] || stop "worktree $WT is not at 6010e37b"
[ -z "$(git -C $WT status --short)" ] || stop "worktree $WT is not clean"
while read bb f; do case "$bb" in "#"*) continue;; esac
  case "$f" in solver/*) p=$WT/$f;; *) p=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/$f;; esac
  [ -f $p ] && [ "$(blob $p)" = "$bb" ] || stop "$p missing or not blob $bb"; done < $S/in_blobs.txt
for f in dss_ell.py ell_ddm.py ell_dd.py ddnp.py; do [ "$(blob $WTM/$f)" = "$(blob $WT5/$f)" ] || stop "$f differs from the scan worktree's (505d8399)"; done
"$PY" -c "import multidouble, sys; sys.exit(0 if hasattr(multidouble, 'dd_logdet') else 1)" || stop "multidouble of $PY has no dd_logdet"
say "pins checked (in_blobs.txt: d18_secant.py a3d90cd5 ... state $SB stub $TB), worktree 6010e37b clean, dss_ell/ell_ddm/ell_dd/ddnp equal the scan worktree's, dd_logdet present; $($PY -V), multidouble $($PY -c 'import importlib.metadata as m; print(m.version("multidouble"))')"
# 2. selftests and controls (SPEED_ELL1.md): wanted exits 0 1 1 1 | 0 1 | 0 1
cd $WTM || exit 9
ex=""
nice -n 10 $PY d18_secant.py selftest > $C/d18_secant_selftest.txt 2>&1; ex="$?"
for m in half norobust nosigncheck; do nice -n 10 $PY d18_secant.py selftest --mutate=$m > $C/d18_secant_selftest_$m.txt 2>&1; ex="$ex $?"; done
nice -n 10 $PY ell_fastm.py selftest > $C/ell_fastm_selftest.txt 2>&1; ex="$ex $?"
nice -n 10 $PY ell_fastm.py selftest --mutate=nolam > $C/ell_fastm_selftest_nolam.txt 2>&1; ex="$ex $?"
nice -n 10 $PY ell_fastdd.py selftest > $C/ell_fastdd_selftest.txt 2>&1; ex="$ex $?"
nice -n 10 $PY ell_fastdd.py selftest --mutate=jround > $C/ell_fastdd_selftest_jround.txt 2>&1; ex="$ex $?"
[ "$ex" = "0 1 1 1 0 1 0 1" ] || stop "selftest exits '$ex' (wanted '0 1 1 1 0 1 0 1': d18_secant, half, norobust, nosigncheck, ell_fastm, nolam, ell_fastdd, jround)"
say "selftests as wanted: d18_secant exit 0, mutations half norobust nosigncheck exit 1 1 1; ell_fastm exit 0, nolam 1; ell_fastdd exit 0, jround 1"
[ "$MODE" = dry ] && { say "dry run ends here"; exit 0; }
# 3. wait for memory, run
[ -e $S/secant.jsonl ] && stop "$S/secant.jsonl exists (the run appends; move it aside first)"
n=0; until [ "$(echo "$(availgib) >= 8" | bc)" = 1 ]; do n=$((n+1)); [ $n -gt 360 ] && stop "less than 8 GiB available for 3 h"; sleep 30; done
say "secant run starts: d18_secant.py run $STUB $STATE 23.0 0.020 0.030 secant.jsonl --tol=1e-5 --maxev=10 --pin=$SB,$TB (one process, nice 10, cap 18000 s by capped_run.py)"
nice -n 10 $PY -u $IN/capped_run.py 18000 $PY -u $WTM/d18_secant.py run $IN/$STUB $IN/$STATE 23.0 0.020 0.030 $S/secant.jsonl --tol=1e-5 --maxev=10 --pin=$SB,$TB > $S/secant.log 2>&1 &
rp=$!
echo "time_utc,pid,rss_kB,pcpu,avail_GiB,free_mem_pct" > $S/samples.csv
( while kill -0 $rp 2>/dev/null; do
    for p in $(pgrep -f "d18_secant.py run"); do echo "$(stamp),$p,$(ps -o rss= -p $p | tr -d ' '),$(ps -o pcpu= -p $p | tr -d ' '),$(availgib),$(memory_pressure | tail -1 | sed 's/.*: //;s/%//')" >> $S/samples.csv; done
    sleep 60; done ) &
wait $rp; sc=$?
say "secant run exit $sc"
[ $sc = 0 ] || [ $sc = 4 ] || stop "d18_secant.py exit $sc (0 tol reached, 4 maxev or non-robust interior point; 2 refused, 3 pin or record system): see $S/secant.log"
# 4. summary from the files
$PY $S/summarize_secant.py > $S/secant_summary.txt 2>&1; ss=$?
cat $S/secant_summary.txt | tee -a $LOG | tail -30
bash $F/push103.sh "kc103_d23/secant: D 23.0 root refined (d18_secant.py)" > /dev/null 2>&1
tell "macm3 #1025 kc103_d23/secant: $(grep -E '^(root|status|ends|evals)' $S/secant_summary.txt | tr '\n' ';' | cut -c1-1200) (raw kc103_d23/secant/)"
exit 0
}
