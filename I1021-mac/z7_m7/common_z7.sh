# sourced by run_z7.sh (#1021 box 7 at M = 7 on the Mac; common_z16.sh of I1021-dh610/z16_m7 with the Mac's paths)
WT=/Users/nathan/Source/choptuik-large-d-1021nb
PY=/Users/nathan/venv-i1021nb/bin/python
D=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export W1026_WT=$WT W1026_PY=$PY W1027_WT=$WT W1027_PY=$PY
export NUMBA_CACHE_DIR=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/numba_cache_1021nb
export PYTHONDONTWRITEBYTECODE=1
stamp() { date -u '+%F %T'; }
