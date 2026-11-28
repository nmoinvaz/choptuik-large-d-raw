# scan_admit.sh (sourced by the drivers of I1101-dh170 and I1104-dh170): memory rule of the dh170 scanners.
# One d18_secant.py scan or run process holds 4.7 to 4.9 GB (peak RSS of the R2 and Test K runs, 4733032 and 4862620 kB), the machine has 31 GiB (MemTotal 32735432 kB) and about
# 4 GiB of other use, and the #1104 re-solve (ell_refine.py) holds up to 2.7 GB: so at most 4 scanner processes run at once while ell_refine.py runs, 5 otherwise, whatever task
# starts them (MAXP overrides, for the dry-run test). bg_admit waits (under one flock, so two drivers cannot both see a free slot) until fewer than the maximum run, starts its
# command in the background, and returns once the new process shows in the count (at most 300 s). It sets ADMIT_PID and ADMIT_WAITED.
maxp() { if [ -n "$MAXP" ]; then echo $MAXP; elif pgrep -f 'ell_refine\.py' > /dev/null; then echo 4; else echo 5; fi; }
SCAN_PAT=${SCAN_PAT:-"^/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python -u .*d18_secant\\.py (scan|run) "}
nscan() { pgrep -fc "$SCAN_PAT"; }
bg_admit() {   # bg_admit CMD...
  local lk n0 i waited=0
  exec {lk}>/tmp/dh170_admit.lock
  flock $lk
  while [ "$(nscan)" -ge "$(maxp)" ]; do sleep ${ADMIT_POLL:-30}; waited=$((waited + ${ADMIT_POLL:-30})); done
  n0=$(nscan)
  "$@" {lk}>&- &            # the child must not inherit the lock
  ADMIT_PID=$!
  for i in $(seq 1 ${ADMIT_SETTLE:-60}); do [ "$(nscan)" -gt "$n0" ] && break; sleep ${ADMIT_TICK:-5}; done
  ADMIT_WAITED=$waited
  exec {lk}>&-
}
