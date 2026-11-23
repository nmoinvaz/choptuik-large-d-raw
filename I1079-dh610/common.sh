# #1079 dh610 common settings of the Linux rerun of the excited-zero certificates (sourced by chain.sh, h2.sh, incl.sh, xload.sh)
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1079-dh610; IN=$F/in/macm3
W=/home/nathan/Source/choptuik-large-d-1079a; BR=c40fbc77d8505d8838c2c0ecc51d3feaa5d7a340
PY=/home/nathan/Source/venv-i1058/bin/python
H=$F/steps.txt
export CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
N=${1:?N}
case $N in
  1) T=x1E2; H_=1e-12; W_=1e-13 ;;
  2) T=x2E2; H_=1e-12; W_=1e-12 ;;
  *) echo "unknown zero $N" >&2; exit 1 ;;
esac
BOX=M3${T}_h${H_}_w${W_}
stamp() { date -u '+%F %T'; }
note() { echo "$STAGE exc$N $(stamp) $*" >> $H; }
stopmsg() { echo "$(stamp) STOP: $STAGE exc$N: $*" >> $H; }
pin_check() { [ "$(git -C $W rev-parse HEAD)" = "$BR" ] && [ -z "$(git -C $W status --porcelain --untracked-files=no)" ] || { stopmsg "the worktree $W is not at $BR or has tracked changes"; exit 1; }; }
run() {   # run NAME CMD...: output to logs/NAME.log in the worktree's solver/proof, returns the exit code, records command, seconds and last line
  local name=$1; shift
  note "$name command: cd $W/solver/proof && nice -n 15 env CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 $PY $* > logs/$name.log 2>&1"
  local t0=$(date +%s)
  nice -n 15 $PY "$@" >> logs/$name.log 2>&1; local rc=$?
  note "$name end exit $rc, $(( $(date +%s) - t0 )) s: $(tail -1 logs/$name.log | cut -c1-220)"
  return $rc
}
