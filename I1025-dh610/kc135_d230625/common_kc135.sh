# common_kc135.sh: variables and helpers of lane_kc135.sh and its stage scripts (stage_scan.sh); sourced, never run alone.
# The stages are separate files, read when each starts, so that a stage not yet started can be amended while an earlier one runs (the coordinator's ruling of 26 Nov).
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc135_d230625; IN=$F/in; OUT=$F/regrid; S=$F/scan
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; WTF=/home/nathan/Source/choptuik-large-d-1025f; WF=$WTF/solver/matter; SW=/home/nathan/Source/choptuik-large-d-1025s; SWM=$SW/solver/matter
PY=/home/nathan/Source/venv-i1058/bin/python
SRC=l1kc127macm3d230625; TAG=l1kc135dh610d230625; D=23.0625; DS=23.0625; LAM0=2.0990016035; PRED=0.008; BAR=0.004; MEMSTOP=4194304; MEMSTART=16777216; RSS_GUESS=6800000; NP=4
L=$F/exits_kc135.txt; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
export PYTHONDONTWRITEBYTECODE=1
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC kc135_d230625: $*" | tee -a $L; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; say "STOP: $*"; exit 1; }
halt() { say "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
