#!/usr/bin/env bash
# ray_identity.sh A.log B.log J same|differ: the BOX lines of ray stops ray1..rayJ in A.log against those in B.log.
# capd_m5 is deterministic (fresh solver per leg, MPFR), so a clean row's ray stops must equal #189's b1_clean.log byte
# for byte (same), and a mutated run's must not (differ, the control of this check). Exit 0 when the expectation holds.
set -u
A=$1
B=$2
J=$3
EXP=$4
tags=""
for i in $(seq 1 "$J"); do tags="${tags:+$tags|}$i"; done
pat="^BOX ray($tags) "
TMP=$(mktemp -d)
grep -E "$pat" "$A" > "$TMP/a"
ra=$?
grep -E "$pat" "$B" > "$TMP/b"
rb=$?
na=$(wc -l < "$TMP/a" | tr -d ' ')
nb=$(wc -l < "$TMP/b" | tr -d ' ')
echo "ray stops 1..$J: $na BOX lines in $(basename "$A"), $nb in $(basename "$B") (expected $((39 * J)) each)"
if [ "$ra" -gt 1 ] || [ "$rb" -gt 1 ] || [ "$na" != $((39 * J)) ] || [ "$nb" != $((39 * J)) ]; then
  echo "VERDICT: FAIL (grep error or missing ray stops)"
  exit 1
fi
nd=$(diff "$TMP/a" "$TMP/b" | grep -c '^<')
if [ "$nd" = 0 ]; then got=same; else got=differ; fi
echo "ray BOX lines: $got ($nd of $na lines differ); expected $EXP"
if [ "$got" = "$EXP" ]; then
  echo "VERDICT: PASS"
  exit 0
fi
echo "VERDICT: FAIL"
exit 1
