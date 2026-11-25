#!/bin/bash
# fetch_src.sh [DEST]: pins macm3's k_c 87 leg state at D 22.125 (raw I1025-macm3/kc87_leg2/b2/, tag l1kc87Lmacm3b) and its record file from origin/main of the raw repo (the commit that added the state, taken from the push
# worktree after a fetch under the push lock) into DEST (default in/) and writes in_blobs_src.txt (blobs) and source_commit.txt. Exit 1 when the state is not on origin yet, 2 when the record has no row for D 22.125
# with k_c 87 or a blob differs from git's.
D=22.125; F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc95_d22125; DEST=${1:-$F/in}; P=/home/nathan/Source/choptuik-large-d-raw-push; W=I1025-macm3/kc87_leg2/b2; TAG=l1kc87Lmacm3b2
ST=$W/sol_${TAG}_D22.125000.npy
( flock 9; git -C $P fetch -q origin ) 9> /tmp/claude-1000/push_folder.lock
c=$(git -C $P log origin/main --diff-filter=A --format=%h -1 -- $ST)
[ -n "$c" ] || exit 1
mkdir -p $DEST
git -C $P show $c:$ST > $DEST/sol_${TAG}_D22.125000.npy
git -C $P show $c:$W/${TAG}.jsonl > $DEST/${TAG}.jsonl
sb=$(git -C $P rev-parse $c:$ST); rb=$(git -C $P rev-parse $c:$W/${TAG}.jsonl)
[ "$(git hash-object --no-filters $DEST/sol_${TAG}_D22.125000.npy)" = "$sb" ] && [ "$(git hash-object --no-filters $DEST/${TAG}.jsonl)" = "$rb" ] || exit 2
python3 -I -c "
import json, sys
rows = [json.loads(l) for l in open('$DEST/${TAG}.jsonl') if l.strip() and json.loads(l).get('D') == $D]
sys.exit(0 if rows and rows[-1]['kc'] == 87 else 2)" || exit 2
{ echo "$sb sol_${TAG}_D22.125000.npy"; echo "$rb ${TAG}.jsonl"; } > $F/in_blobs_src.txt
echo "$(git -C $P rev-parse origin/main) origin/main at the fetch; commit $c added the state ($(git -C $P log -1 --format='%cI %s' $c))" > $F/source_commit.txt
echo "fetched D $D from commit $c: state $sb record $rb"
