#!/bin/bash
# fetch_point.sh D [DEST]: pins win2's k_c 79 far scout state and record for D from origin/main of the raw repo (the commit that added the state, taken from the push worktree after a fetch under the push lock) into DEST
# (default D<D>/in) and writes DEST/../in_blobs.txt (blobs) and source_commit.txt. The state is found by its file name sol_<tag>_D<D:.6f>.npy anywhere under I1025-win2/ (the scout's folder is not fixed in advance); the record
# is <tag>.jsonl beside it. Exit 1 when the state is not on origin yet, 2 when the record is missing, has no row for D with kc NEED_KC (79; the env is for the control), or a blob differs.
# Env for the tests: TAG (default D<D>/tag.txt, else l1kc79Lw1025i), FARDIR (default <here>/D<D>), NEED_KC.
D=$1; FAR=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_far; F=${FARDIR:-$FAR/D$D}; DEST=${2:-$F/in}; P=/home/nathan/Source/choptuik-large-d-raw-push; NEED_KC=${NEED_KC:-79}
TAG=${TAG:-$(cat $F/tag.txt 2>/dev/null || echo l1kc79Lw1025i)}
Df=$(printf '%.6f' $D); NAME=sol_${TAG}_D$Df.npy
( flock 9; git -C $P fetch -q origin ) 9> /tmp/claude-1000/push_folder.lock
c=$(git -C $P log origin/main --diff-filter=A --format=%h -1 -- ":(glob)I1025-win2/**/$NAME")
[ -n "$c" ] || exit 1
ST=$(git -C $P log origin/main --diff-filter=A --name-only --format= -1 -- ":(glob)I1025-win2/**/$NAME" | head -n 1)
W=$(dirname $ST)
mkdir -p $DEST
git -C $P show $c:$ST > $DEST/$NAME
git -C $P show $c:$W/${TAG}.jsonl > $DEST/${TAG}.jsonl || exit 2
sb=$(git -C $P rev-parse $c:$ST); rb=$(git -C $P rev-parse $c:$W/${TAG}.jsonl)
[ "$(git hash-object --no-filters $DEST/$NAME)" = "$sb" ] && [ "$(git hash-object --no-filters $DEST/${TAG}.jsonl)" = "$rb" ] || exit 2
python3 -I -c "
import json, sys
rows = [json.loads(l) for l in open('$DEST/${TAG}.jsonl') if l.strip() and json.loads(l).get('D') == $D]
sys.exit(0 if rows and rows[-1]['kc'] == $NEED_KC else 2)" || exit 2
{ echo "$sb $NAME"; echo "$rb ${TAG}.jsonl"; } > $DEST/../in_blobs.txt
echo "$(git -C $P rev-parse origin/main) origin/main at the fetch; commit $c added the state at $ST ($(git -C $P log -1 --format='%cI %s' $c))" > $DEST/../source_commit.txt
echo "fetched D $D from commit $c ($ST): state $sb record $rb"
