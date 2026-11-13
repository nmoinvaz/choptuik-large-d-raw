# #641: the chain's own corrector with --kfreeze 9 and 7 at D 80, 100, 150, 200 (hold only 11, 13 / 9-13 on the fit), --steps 1, #603's flags.
# From hp/ of the worktree ~/Source/choptuik-large-d-b640 at main 9839474; RAWDIR is a dedicated worktree of the raw repository (~/Source/choptuik-large-d-raw-641,
# a checkout with RAW_DATA_REPO, up to date: it holds T138-win2 and writes I641-macm3 here, pushed from there).
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
RAWDIR=/Users/nathan/Source/choptuik-large-d-raw-641
FLAGS="--N 24 --eps 1e-14 --h_max 1.0 --D_max 400 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1"
run() {  # K D state threads
  K=$1; D=$2; S=$3; T=$4
  cd /Users/nathan/Source/choptuik-large-d-b640/hp
  caffeinate -is nice -n 10 python3 -u anm_run.py $RAWDIR $RAWDIR/I641-macm3/K${K}_D${D} --state $S --kfreeze $K --held_fit data/held_fit.json --steps 1 $FLAGS --save_base 1 --threads $T > $RAWDIR/I641-macm3/K${K}_D${D}.log 2>&1
  echo "K$K D$D exit $? at $(date -u +%FT%TZ)" >> $RAWDIR/I641-macm3/exits.txt
}
