#!/bin/bash
# #650: the sigmams kernel for this machine (matter/sigma_ms/build.sh, FAST=1: no fat LTO, 16 codegen units; hp found the same bits either way, #600, #604).
# Worktree ~/Source/choptuik-large-d-b650 at origin/main fdcada23; Python 3.14 of venv-macm3-314; the wheel is installed into the worktree's matter/sigma_ms/site.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
cd /Users/nathan/Source/choptuik-large-d-b650/matter/sigma_ms
PY=$(command -v python3) SITE=$PWD/site FAST=1 caffeinate -is ./build.sh > /Users/nathan/Source/choptuik-large-d-raw-641/I650-macm3/build.log 2>&1
echo "build exit $? at $(date -u +%FT%TZ)" >> /Users/nathan/Source/choptuik-large-d-raw-641/I650-macm3/exits.txt
