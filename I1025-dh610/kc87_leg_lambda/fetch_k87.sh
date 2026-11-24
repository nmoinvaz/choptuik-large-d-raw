#!/bin/bash
# fetch_k87.sh D [DEST]: pins dh370's k_c 87 leg state and record for D from origin/main of the raw repo (the commit that added the state, taken from the push worktree after a fetch under the push lock) into DEST
# (default <D>/in, or ${FNAME}/in) and writes DEST/../in_blobs.txt (blobs) and source_commit.txt. Exit 1 when the state is not on origin yet, 2 when the record has no row for D with kc K87_KC (default 87) or a blob differs.
D=$1; F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc87_leg_lambda; DEST=${2:-$F/${FNAME:-$D}/in}; P=/home/nathan/Source/choptuik-large-d-raw-push; W=I1025-dh370/kc87_leg; TAG=l1kc87Ldh370; KC=${K87_KC:-87}
Df=$(printf '%.6f' $D); ST=$W/sol_${TAG}_D$Df.npy
( flock 9; git -C $P fetch -q origin ) 9> /tmp/claude-1000/push_folder.lock
c=$(git -C $P log origin/main --diff-filter=A --format=%h -1 -- $ST)
[ -n "$c" ] || exit 1
mkdir -p $DEST
git -C $P show $c:$ST > $DEST/sol_${TAG}_D$Df.npy
git -C $P show $c:$W/${TAG}.jsonl > $DEST/${TAG}.jsonl
sb=$(git -C $P rev-parse $c:$ST); rb=$(git -C $P rev-parse $c:$W/${TAG}.jsonl)
[ "$(git hash-object --no-filters $DEST/sol_${TAG}_D$Df.npy)" = "$sb" ] && [ "$(git hash-object --no-filters $DEST/${TAG}.jsonl)" = "$rb" ] || exit 2
python3 -I -c "
import json, sys
rows = [json.loads(l) for l in open('$DEST/${TAG}.jsonl') if l.strip() and json.loads(l).get('D') == $D]
sys.exit(0 if rows and rows[-1]['kc'] == $KC else 2)" || exit 2
{ echo "$sb sol_${TAG}_D$Df.npy"; echo "$rb ${TAG}.jsonl"; } > $DEST/../in_blobs.txt
echo "$(git -C $P rev-parse origin/main) origin/main at the fetch; commit $c added the state ($(git -C $P log -1 --format='%cI %s' $c))" > $DEST/../source_commit.txt
echo "fetched D $D from commit $c: state $sb record $rb"
