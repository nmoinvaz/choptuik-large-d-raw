# #708: #551's box on the exact determinant at kf 35 and kf 37 (D 61.0264, M 48, --ball=320), the commands of #657/#656 (I551-win2/run_551.sh) with only the cut changed.
# From hp/ of the worktree ~/Source/choptuik-large-d-b596 at main b5d69cc2; R is the raw worktree ~/Source/choptuik-large-d-raw-641 (pushed from there).
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I708-macm3
go() {  # K name circle threads
  cd /Users/nathan/Source/choptuik-large-d-b596/hp
  mkdir -p $R/kf$1/$2/data
  echo "708 kf$1 $2 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_708.txt
  caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz $3 --M=48 --kf=$1 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf$1 --ball=320 --threads=$4 --data=$R/kf$1/$2/data > $R/kf$1/$2/run.log 2>&1
  echo "708 kf$1 $2 exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_708.txt
}
# a circle other than the control waits for its cut's state (saved by the control's setup)
wait_state() {  # K
  while ! grep -q "saved modecount_state_D61.0264_M48_kf$1.npz" $R/kf$1/control/run.log 2>/dev/null; do sleep 15; done
}
