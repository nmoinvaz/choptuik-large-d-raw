# #848: #812's kf 47 count at D 61.0264, M 48, on a second radial layout: --centre_tol=1e-30 adds inner nodes (kf 47's
# centre tail is 7.1e-26 on #812's layout). From hp/ of the worktree ~/Source/choptuik-large-d-749 at bd7df22f, #812's
# build and venv. R is the live raw worktree ~/Source/choptuik-large-d-raw-749.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-749/I848-macm3
WT=/Users/nathan/Source/choptuik-large-d-749
CT=1e-30
ST=modecount_state_D61.0264_M48_kf47_ct$CT.npz
log() { echo "848 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_848.txt; }
go() {  # name circle threads
  cd $WT/hp || exit 9
  [ "$(git rev-parse --short=8 HEAD)" = "bd7df22f" ] || { log "worktree (#749's) is not at bd7df22f"; exit 9; }
  mkdir -p $R/kf47ct/$1/data
  log "$1 start"
  caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz $2 --M=48 --kf=47 --n0=20 \
    --fmax=1e-15 --tag=D61.0264_M48_kf47_ct --ball=320 --threads=$3 --centre_tol=$CT --data=$R/kf47ct/$1/data \
    > $R/kf47ct/$1/run.log 2>&1
  log "$1 exit $?"
}
