# common_kc111.sh: variables and helpers of lane_kc111b.sh and its stage scripts (stage_scan.sh, stage_secant.sh); sourced, never run alone.
# The stages are separate files, read when each starts, so that a stage not yet started can be amended while an earlier one runs (the coordinator's ruling of 26 Nov).
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc111_d22875; IN=$F/in; OUT=$F/regrid; S=$F/scan; SEC=$F/secant
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; WTF=/home/nathan/Source/choptuik-large-d-1025f; WF=$WTF/solver/matter; SW=/home/nathan/Source/choptuik-large-d-1025s; SWM=$SW/solver/matter
PY=/home/nathan/Source/venv-i1058/bin/python
SRC=l1kc103win22875; TAG=l1kc111dh610d22875; D=22.875; DS=22.8750; LAM0=2.0996545550; PRED=0.12; BAR=0.02; MEMSTOP=4194304; MEMSTART=8388608; RSS_GUESS=4200000; NP=4
L=$F/exits_kc111.txt; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
export PYTHONDONTWRITEBYTECODE=1
stamp() { date -u '+%F %T'; }
say() { echo "== $(stamp) UTC kc111_d22875: $*" | tee -a $L; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; say "STOP: $*"; exit 1; }
halt() { say "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
