#!/bin/bash
# #1101 macm3 K4 (t5's order, hc 27 Nov 16:3x UTC and #1101 comment 7223316450): the fourth kappa point WITHOUT a re-solve: R1's state and record (tag l1kc127k050m3, kappa 0.5, blobs 0124dbd2 and 944a8179, raw commit 614a47d78)
# scanned with d18_secant.py --kappa_mm=0.25 --b12=rust (worktree choptuik-large-d-kmm at f56f91d2, branch wip/ell1-kappa-mm, d18_secant.py 2f3ee874; ellrs from ~/Source/ellrs-site-1102m3 unchanged) at lambda 0.100, 0.115, 0.130, 0.145,
# then the secant at tol 5e-5 on the robust change. The control first: one point (lambda 0.100) with --kappa_mm=0.5, whose ln|det| must equal the R1 scan's at 0.100 bit for bit. The printed 'kappa_mm 0.25 ... steps' line is checked (about 11700).
# The root is reported against 0.111 (kappa^4), 0.120 (kappa^3) and 0.133 (kappa^2). One process (4 block-12 threads) for the scan: the steps double, and two processes at once would need about twice the memory of R1's scan (3.9 and 4.4 GiB each).
# Stops (hc to t5): a pin or selftest that does not read as wanted, the control not bit-identical, the kappa_mm steps line outside 11400 to 12000, an exception, more than one robust change, a step over 8 h, a secant exit other than 0 or 4. usage: bash lane_kmm.sh [dry]
{
set -u
MODE=${1:-}
F=$HOME/Source/choptuik-large-d-raw-903/I1101-macm3; K=$F/kmm025; IN=$F/in
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
WT=$HOME/Source/choptuik-large-d-kmm; WTM=$WT/solver/matter
WT5=$HOME/Source/choptuik-large-d-1025m; WTM5=$WT5/solver/matter
SITE=$HOME/Source/ellrs-site-1102m3
PY=$HOME/Source/venv-macm3-1058b/bin/python; RAWG=$HOME/Source/choptuik-large-d-raw-1076p
TAG=l1kc127k050m3; D=23.0; DT=D23.0000; STATEFILE=sol_${TAG}_$DT.npy; RAWC=614a47d78
DNC=23.0_r1k050_kmm050ctl; DNM=23.0_r1k050_kmm025; SCANC=$L/$DNC; SCANM=$L/$DNM; SEC=$K/secant
HC=$(command -v hc); LOG=$K/exits_kmm.txt
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC I1101 K4: $*" | tee -a $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stop() { tell "macm3 #1101 K4 STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
mkdir -p $K
export PYTHONDONTWRITEBYTECODE=1
say "start (mode ${MODE:-full}; load $(sysctl -n vm.loadavg), $(availgib) GiB available)"
# 1. pins
while read bb f; do case "$bb" in "#"*) continue;; esac
  p=$F/$f; [ -f $p ] && [ "$(blob $p | cut -c1-8)" = "$bb" ] || stop "$p missing or not blob $bb"; done < $K/in_blobs.txt
[ "$(git -C $WT rev-parse --short=8 HEAD)" = f56f91d2 ] || stop "worktree $WT not at f56f91d2"
[ "$(blob $WTM/d18_secant.py | cut -c1-8)" = 2f3ee874 ] && [ "$(blob $WTM/ell_b12rs.py | cut -c1-8)" = a1fff74f ] || stop "d18_secant.py is not 2f3ee874 or ell_b12rs.py is not a1fff74f in $WT"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(git -C $WT5 rev-parse --short=8 HEAD)" = 505d8399 ] && [ -z "$(git -C $WT5 status --short solver | grep -v 'solver/matter/data/')" ] || stop "the scan worktree $WT5 is not clean at 505d8399"
for f in dss_ell ell_ddm ell_dd ddnp; do [ "$(blob $WTM/$f.py | cut -c1-8)" = "$(blob $WTM5/$f.py | cut -c1-8)" ] || stop "$f.py of the kappa_mm worktree differs from the scan worktree's (505d8399)"; done
[ "$(blob $WTM/dss_ell.py | cut -c1-8)" = 5d28c19e ] && [ "$(blob $WTM/ell_delta.py | cut -c1-8)" = fde699f5 ] || stop "dss_ell.py is not 5d28c19e or ell_delta.py is not fde699f5 in $WT"
[ "$(shasum -a 256 $SITE/ellrs/ellrs.cpython-314-darwin.so | cut -c1-12)" = d2221460d02c ] || stop "the ellrs module in $SITE is not the one gated (sha256 d2221460d02c)"
git -C $RAWG cat-file -e $RAWC:I1101-macm3/in/$TAG.jsonl 2>/dev/null && git -C $RAWG cat-file -e $RAWC:I1101-macm3/in/$STATEFILE 2>/dev/null || stop "the raw commit $RAWC does not hold R1's record and state"
SB=$(blob $IN/$STATEFILE | cut -c1-8); TB=$(blob $IN/$TAG.jsonl | cut -c1-8)
[ "$SB" = 0124dbd2 ] && [ "$TB" = 944a8179 ] || stop "R1's state or record is not blob 0124dbd2 / 944a8179"
say "pins checked (kmm025/in_blobs.txt), worktree $WT f56f91d2 (d18_secant.py 2f3ee874, ell_b12rs.py a1fff74f, dss_ell.py 5d28c19e, ell_delta.py fde699f5; dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399's), only d18_secant.py differs from the scanner worktree d4b6b6ce (git diff: 16 insertions, 1 deletion), ellrs sha256 d2221460d02c in $SITE, R1's state $SB and record $TB (raw $RAWC), $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
# 2. selftests of the scanner of the branch and of ell_b12rs, with their failing mutations; the control of the record system on R1's state
export D18_DIR=$IN OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
C=$K/checks; mkdir -p $C
( cd $WTM && export PYTHONPATH=$SITE RAYON_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  nice -n 10 $PY d18_secant.py selftest > $C/newscan_selftest.txt 2>&1; nx="$?"
  for m in half norobust nosigncheck; do nice -n 10 $PY d18_secant.py selftest --mutate=$m > $C/newscan_selftest_$m.txt 2>&1; nx="$nx $?"; done
  for m in "" nolam harm; do nice -n 10 $PY ell_b12rs.py selftest ${m:+--mutate=$m} > $C/b12rs_selftest${m:+_$m}.txt 2>&1; nx="$nx $?"; done
  echo "$nx" > $C/newscan_exits.txt )
[ "$(cat $C/newscan_exits.txt)" = "0 1 1 1 0 1 1" ] || stop "the scanner's and ell_b12rs's selftest exits '$(cat $C/newscan_exits.txt)' (wanted '0 1 1 1 0 1 1')"
C127="nice -n 10 $PY -I $IN/kc127_syscheck_1025.py $IN/$TAG.jsonl $IN/$STATEFILE $D $WTM"
$C127 > $C/r1_state_syscheck.txt 2>&1; s0=$?; $C127 --mutate=F > $C/r1_state_syscheck_mutF.txt 2>&1; s1=$?; $C127 --mutate=steps > $C/r1_state_syscheck_mutsteps.txt 2>&1; s2=$?
say "scanner d18_secant.py (blob 2f3ee874): selftest exit 0, --mutate=half, norobust, nosigncheck exit 1 each; ell_b12rs.py selftest exit 0, --mutate=nolam, harm exit 1 each; R1's state against its record in the kappa_mm worktree: kc127_syscheck exit $s0 (0 wanted), controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each): $(grep -E '^D ' $C/r1_state_syscheck.txt | cut -c1-300)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] || stop "R1's state does not read as accepted in the kappa_mm worktree (syscheck $s0, controls $s1 $s2)"
cd $F
[ "$MODE" = dry ] && { say "dry run: pins, selftests and R1's state check passed; nothing started"; exit 0; }
# 3. wait for no other scan or regrid, then for memory
while pgrep -f 'd18_hybsign|ell_refine|d18_secant.py (run|scan)' > /dev/null; do sleep 30; done
while python3 -c "import sys; sys.exit(0 if $(availgib) >= 8 else 1)"; [ $? != 0 ]; do sleep 60; done
prep_folder() {   # $1 folder name, $2 kappa_mm, $3 LAMP array text, $4 window
  local DNn=$1 SC=$L/$1
  mkdir -p $SC
  { cat <<PENV
D=$D
TAG=$TAG
RAWC=$RAWC
STATEFILE=$STATEFILE
STATEBLOB=$SB
RECBLOB=$TB
SRC=I1101-macm3/in
KMM=$2
NP=1; GATE=10; NICE=10
LAMP=($3)
WIN="$4"; REP=
PENV
  } > $SC/point.env
  bash $L/prepare87.sh $DNn > $SC/prepare.log 2>&1 || stop "prepare87.sh: a pin mismatch (see $SC/prepare.log)"
  echo "ACCEPTED $(stamp) UTC (R1's state and record, accepted by the lane of I1101 R1 at 15:32:49 UTC and again by kc127_syscheck in the kappa_mm worktree: $C/r1_state_syscheck.txt)" > $SC/VERDICT.txt
  echo "$(stamp) UTC accept (lane_kmm.sh): R1's state $SB and record $TB, kc127_syscheck exit $s0 (0 wanted), controls $s1 $s2 (1 wanted each)" >> $SC/steps.txt
}
# 4. the control: kappa_mm 0.5 at lambda 0.100, bit for bit against the R1 scan
prep_folder $DNC 0.5 '"0.100"' "0.100 0.100"
say "control starts: kappa_mm 0.5 (R1's own kappa) at lambda 0.100, 1 process, 4 Rust threads (pointkmm.sh $DNC scan)"
bash $F/pointkmm.sh $DNC scan >> $SCANC/pipeline.log 2>&1; cs=$?
say "control scan exit $cs"
[ -e $SCANC/SCAN_DONE.txt ] || stop "the control scan did not finish (no SCAN_DONE.txt; see $SCANC/steps.txt)"
$PY $F/control_compare_kmm.py > $K/control_compare.txt 2>&1; cc=$?
$PY $F/control_compare_kmm.py --mutate=ln > $K/control_compare_mut_ln.txt 2>&1; m1=$?; $PY $F/control_compare_kmm.py --mutate=field > $K/control_compare_mut_field.txt 2>&1; m2=$?
say "control read: exit $cc (0 = bit for bit): $(tr '\n' ' ' < $K/control_compare.txt | cut -c1-900); kappa_mm line: $(grep -h '^kappa_mm' $SCANC/scan/scan_p0.log | cut -c1-260); its controls --mutate=ln exit $m1, --mutate=field exit $m2 (1 wanted each)"
[ $m1 = 1 ] && [ $m2 = 1 ] || stop "the control comparison's own mutations did not fail ($m1 $m2)"
[ $cc = 0 ] || stop "the kappa_mm 0.5 control is NOT bit for bit the R1 scan at lambda 0.100: $(tr '\n' ' ' < $K/control_compare.txt | cut -c1-700)"
bash $L/push87.sh "kc87_leg_lambda: D $DNC (I1101 K4 control, kappa_mm 0.5) done" > /dev/null 2>&1
bash $F/push_i1101.sh "I1101-macm3: K4 control read (kappa_mm 0.5, bit for bit)" > /dev/null 2>&1
# 5. the scan at kappa_mm 0.25
prep_folder $DNM 0.25 '"0.100" "0.115" "0.130" "0.145"' "0.100 0.145"
say "scan starts: kappa_mm 0.25 at lambda 0.100 0.115 0.130 0.145, 1 process, 4 Rust threads (pointkmm.sh $DNM scan)"
tell "macm3 #1101 K4 START: the kappa_mm 0.5 control at lambda 0.100 is BIT FOR BIT the R1 scan ($(tr '\n' ' ' < $K/control_compare.txt | cut -c1-420)); the scan with --kappa_mm=0.25 at lambda 0.100, 0.115, 0.130, 0.145 starts now (scanner worktree f56f91d2, d18_secant.py 2f3ee874, 1 process of 4 Rust threads), then the secant at tol 5e-5; the steps line follows"
bash $F/pointkmm.sh $DNM scan >> $SCANM/pipeline.log 2>&1 &
sp=$!
n=0; until grep -q '^kappa_mm' $SCANM/scan/scan_p0.log 2>/dev/null; do n=$((n+1)); [ $n -gt 120 ] && break; kill -0 $sp 2>/dev/null || break; sleep 5; done
KL=$(grep -h '^kappa_mm' $SCANM/scan/scan_p0.log 2>/dev/null | head -1); say "scan's line: $KL"
KS=$(echo "$KL" | sed -E 's/.*, ([0-9]+) steps \(the record.*/\1/')
if ! python3 -c "import sys; sys.exit(0 if 11400 <= int('$KS') <= 12000 else 1)" 2>/dev/null; then pkill -f "d18_secant.py scan.*$DNM" 2>/dev/null; wait $sp; stop "the kappa_mm 0.25 steps line does not read about 11700 (11400 to 12000): '$KL'"; fi
tell "macm3 #1101 K4: the scan's printed line: $KL (steps $KS, about 11700 wanted, 11400 to 12000 accepted)"
wait $sp
say "scan exit $?"
[ -e $SCANM/SCAN_DONE.txt ] || stop "the scan did not finish (no SCAN_DONE.txt; see $SCANM/steps.txt)"
bash $L/push87.sh "kc87_leg_lambda: D $DNM (I1101 K4, kappa_mm 0.25) scan done" > /dev/null 2>&1
nch=$(grep -c 'robust change (' $SCANM/read_lower.txt); nrb=$(grep -o 'robust changes: [0-9]*' $SCANM/read_lower.txt | head -1 | grep -o '[0-9]*')
say "reading: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint|^repeated|^float64' $SCANM/read_lower.txt | tr '\n' ' ' | cut -c1-900)"
tell "macm3 #1101 K4: the kappa_mm 0.25 scan is read: $(grep -E '^hybrid signs|^robust changes|change \(|^endpoint' $SCANM/read_lower.txt | tr '\n' ';' | cut -c1-900) (raw kc87_leg_lambda/$DNM/)"
[ "$nch" = 1 ] && [ "$nrb" = 1 ] || stop "the kappa_mm 0.25 scan reads $nrb robust changes in 0.100-0.145 (one wanted): no secant; reported (no extension was ordered)"
# 6. the secant at kappa_mm 0.25 on the one robust change
BR=$(grep 'robust change (' $SCANM/read_lower.txt | sed -E 's/.*robust change \((-?[0-9.]+), (-?[0-9.]+)\).*/\1 \2/')
LO=${BR% *}; HI=${BR#* }
S_STATE=$SCANM/in/$STATEFILE; S_REC=$SCANM/in/$TAG.jsonl
mkdir -p $SEC; [ -e $SEC/secant.jsonl ] && stop "$SEC/secant.jsonl exists"
say "secant starts: d18_secant.py run $S_REC $S_STATE $D $LO $HI secant.jsonl --tol=5e-5 --maxev=10 --pin=$SB,$TB --b12=rust --b12_threads=4 --kappa_mm=0.25"
echo "time_utc,pid,rss_kB,pcpu,avail_GiB" > $SEC/samples.csv
( cd $WTM && env PYTHONPATH=$SITE OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 10 $PY -u $IN/capped_run.py 18000 $PY -u $WTM/d18_secant.py run $S_REC $S_STATE $D $LO $HI $SEC/secant.jsonl --tol=5e-5 --maxev=10 --pin=$SB,$TB --b12=rust --b12_threads=4 --kappa_mm=0.25 > $SEC/secant.log 2>&1; echo $? > $SEC/exit.txt ) &
sp=$!
( while kill -0 $sp 2>/dev/null; do for p in $(pgrep -f "d18_secant.py run.*I1101-macm3/kmm025/secant"); do echo "$(stamp),$p,$(ps -o rss= -p $p | tr -d ' '),$(ps -o pcpu= -p $p | tr -d ' '),$(availgib)" >> $SEC/samples.csv; done; sleep 60; done ) &
wait $sp; se=$(cat $SEC/exit.txt)
say "secant exit $se"
[ "$se" = 0 ] || [ "$se" = 4 ] || stop "d18_secant.py exit $se (0 tol reached, 4 maxev or non-robust interior point; 2 refused, 3 pin or record system): see $SEC/secant.log"
$PY $F/summarize_point.py $SCANM $SEC > $K/point_summary.txt 2>&1
bash $F/push_i1101.sh "I1101-macm3: K4 scanned at kappa_mm 0.25 and its root refined (secant)" > /dev/null 2>&1
RT=$(grep -o 'det-linear root [0-9.-]*' $K/point_summary.txt | head -1 | awk '{print $3}')
CMPR=$(python3 -c "
r = float('$RT'); h = [('0.111 (kappa^4)', 0.111), ('0.120 (kappa^3)', 0.120), ('0.133 (kappa^2)', 0.133)]
print('root %.8f: minus 0.111 %+.5f, minus 0.120 %+.5f, minus 0.133 %+.5f; nearest %s' % (r, r - 0.111, r - 0.120, r - 0.133, min(h, key=lambda t: abs(r - t[1]))[0]))")
tell "macm3 #1101 K4 done: $CMPR; $(grep -E '^(scan:|secant: status|secant root)' $K/point_summary.txt | tr '\n' ';' | cut -c1-1200) (raw I1101-macm3/kmm025/ and kc87_leg_lambda/$DNM/)"
exit 0
}
