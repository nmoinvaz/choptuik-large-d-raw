# #789: #749's box at kf 43 and kf 45 (D 61.0264, M 48, --ball=320), #708's commands with only the cut changed.
# From hp/ of the worktree ~/Source/choptuik-large-d-749 at wip/i749 bd7df22f (b5d69cc2, #708's build, with
# modecount_circle.py of 672d01b7: positions up to winding 6). R is the live raw worktree ~/Source/choptuik-large-d-raw-749.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-749/I789-macm3
WT=/Users/nathan/Source/choptuik-large-d-749
go() {  # K name circle threads
  cd $WT/hp || exit 9
  [ "$(git rev-parse --short=8 HEAD)" = "bd7df22f" ] || { echo "789 worktree (#749's) is not at bd7df22f" >> $R/exits_789.txt; exit 9; }
  mkdir -p $R/kf$1/$2/data
  echo "789 kf$1 $2 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_789.txt
  caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz $3 --M=48 --kf=$1 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf$1 --ball=320 --threads=$4 --data=$R/kf$1/$2/data > $R/kf$1/$2/run.log 2>&1
  echo "789 kf$1 $2 exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_789.txt
}
# a circle other than the control waits for its cut's state (saved by the control's setup)
wait_state() {  # K
  while ! grep -q "saved modecount_state_D61.0264_M48_kf$1.npz" $R/kf$1/control/run.log 2>/dev/null; do sleep 15; done
}
