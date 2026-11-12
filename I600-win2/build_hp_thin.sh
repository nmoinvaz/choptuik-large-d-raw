#!/usr/bin/env bash
# #600 hedge: the same hp build as build_hp.sh (main fc697f3a) with thin-style codegen, the release profile's LTO off and 16 codegen units
# (AGENTS.md's recipe for the memory-limited build, CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16), in its own worktree
# D:/choptuik-i600b and its own venv, venv-i600b, so that the fat-LTO build in D:/choptuik-i600 is not disturbed. At most 6 build jobs.
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i600b
export PATH="/c/Users/nathan/Source/venv-i600b/Scripts:$PATH"
export CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=6
cd /d/choptuik-i600b || exit 9
date -u '+build start %Y-%m-%d %H:%M:%S UTC'
bash hp/build.sh
echo "build exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
