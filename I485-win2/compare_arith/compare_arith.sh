#!/usr/bin/env bash
# #485: do the double-double sources deleted by 93402cf8 differ from the multidouble crate's (rev 5fb516b, the pin of 93402cf8) beyond formatting?
# usage: bash compare_arith.sh REPO MD_DIR OUT_DIR
#   REPO    a checkout of nmoinvaz/choptuik-large-d (the old sources are read with git show 0a131faf:hp/src/<f>.rs)
#   MD_DIR  a checkout of github.com/nmoinvaz/multidouble at 5fb516b4823679ab397f4fdf7989d18f4cb6789e (on win2: ~/.cargo/git/checkouts/multidouble-2ee9e3c95fe1538e/5fb516b)
#   OUT_DIR where the formatted copies and the diffs go (made if missing)
# Both versions are formatted with rustfmt and the crate's rustfmt.toml (max_width = 120) before the diff, so only code differences remain.
# Control: a planted change of one operator in a copy of dd.rs must show up as a difference (printed as 'control').
set -e
REPO=$1; MD=$2; OUT=$3
mkdir -p $OUT/old $OUT/new
for f in dd dv exact linalg v8 qd qv; do
  git -C $REPO show 0a131faf:hp/src/$f.rs > $OUT/old/$f.rs
  cp $MD/src/$f.rs $OUT/new/$f.rs
done
cp $MD/rustfmt.toml $OUT/rustfmt.toml
(cd $OUT && rustfmt --edition 2021 --config-path rustfmt.toml old/*.rs new/*.rs)
for f in dd dv exact linalg v8 qd qv; do
  diff -u $OUT/old/$f.rs $OUT/new/$f.rs > $OUT/$f.diff || true
  echo "$f.rs: $(grep -c '^[<>+-][^+-]' $OUT/$f.diff) differing lines after rustfmt"
done
# control: the same comparison on a copy of dd.rs whose two_prod is changed must differ
sed 's/a.mul_add(b, -p)/(a * b) - p/' $OUT/old/dd.rs > $OUT/control_dd.rs
if diff -q $OUT/old/dd.rs $OUT/control_dd.rs > /dev/null; then echo "control FAILED: the planted change was not made"; exit 1; else echo "control: the planted two_prod change is a difference, as it must be"; fi
