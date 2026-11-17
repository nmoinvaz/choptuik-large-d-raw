#!/usr/bin/env bash
# #927 part 2 on the Mac: the pilot, criteria in README.md section 3 (fixed before the runs). Step 1 from a stored
# converged state to the first target against lowD_highM.py's own state there (ref48/ or ref/), then the controls from
# the same base: drop2 and kappa (each must exit 1 on check A), dshift with --stop_on_fail 0 (A and B must fail).
# Usage: run_pilot.sh step1|controls|step2
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/raw927/I927-mac
PY=/Users/nathan/venv-314/bin/python
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a611e0854f7930044/hp || exit 9
# default: the amended pilot at M 48, D 3.7 (README section 3, amendment); PAIR=128 the first design at D 3.15
if [ "${PAIR:-48}" = 128 ]; then
    BASE=$R/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz; D1=3.149; D2=3.148; P=pilot; M=128
    REF1=$R/ref/states/lowD927_x0.000625-0.9_D3.1490_M128.npz
    REF2=$R/ref/states/lowD927_x0.000625-0.9_D3.1480_M128.npz
else
    BASE=$R/inputs/lowDv_D3.7000_M48.npz; D1=3.695; D2=3.69; P=pilot48; M=48
    REF1=$R/ref48/states/lowD927_x0.005-0.8_D3.6950_M48.npz
    REF2=$R/ref48/states/lowD927_x0.005-0.8_D3.6900_M48.npz
fi
run() {  # name, then the pilot's arguments
    local name=$1; shift
    nice -n 10 $PY -u anm_lowd_pilot.py $R $R/$P/$name "$@" --N 6 --threads 4 > $R/$P/$name.log 2>&1
    echo "$name exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/$P/exits.txt
}
mkdir -p $R/$P
case "$1" in
    step1) run step1 --state $BASE --target $D1 --ref $REF1 ;;
    controls)
        run drop2 --state $BASE --target $D1 --ref $REF1 --mutate drop2
        run kappa --state $BASE --target $D1 --ref $REF1 --mutate kappa
        run dshift --state $BASE --target $D1 --ref $REF1 --mutate dshift --stop_on_fail 0 ;;
    step2) run step2 --state $R/$P/step1/anm_D${D1}000_M$M.npz --target $D2 --ref $REF2 ;;
esac
