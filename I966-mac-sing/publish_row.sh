#!/bin/bash
# #966: after newbase.sh D: push the outputs and the README row, then edit comment 7060114909 by id. Usage: publish_row.sh D RAWHASH
set -u
{
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad
W=$S/i966sing; O=$W/out; F=$S/raw1021push/I966-mac-sing; D=$1; RAW=$2; P=/Users/nathan/venv-314/bin/python
gh api repos/nmoinvaz/choptuik-large-d/issues/comments/7060114909 --jq .body > $W/comment_cur.md || exit 1
cp -p $O/exits_new.txt $O/*_D$D.* $O/nextcheck966_D${D}_move.txt $F/
$P -I $W/addrow.py $D $RAW $F/README.md $W/comment_cur.md $W/comment_new.md PENDING "$(date -u '+%Y-%m-%d %H:%M')" || exit 1
cd $S/raw1021push && git add I966-mac-sing && git commit -q -m "I966-mac-sing: base $D" && git fetch -q origin main && git rebase -q origin/main && git push -q origin HEAD:main || exit 1
H=$(git log -1 --format=%h); sed -i '' "s/at PENDING\./at $H./" $W/comment_new.md
gh api -X PATCH repos/nmoinvaz/choptuik-large-d/issues/comments/7060114909 -F body=@$W/comment_new.md --jq .updated_at
echo "raw $H"
exit
}
