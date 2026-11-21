# I1064 win2 precross helpers (sourced). crun NAME WANT CAP_S REGEX cmd... runs cmd in the background, records its root pid, kills only that pid's tree (taskkill /T /F /PID) when
# CAP_S seconds pass AND its command line matches REGEX; sets RC and CAPPED. No retry. Log lines go to $EX.
OUT=/d/choptuik-i935-raw/I1064-win2/precross
EX=$OUT/exits_1064.txt
SUM=$OUT/summary_1064.txt
log() { echo "1064 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $EX; }
crun() {
  local name=$1 want=$2 cap=$3 rx=$4; shift 4
  local t=$(date +%s)
  "$@" &
  local pid=$! wpid
  wpid=$(cat /proc/$pid/winpid)
  log "$name root pid $wpid, cap $cap s, want exit $want"
  CAPPED=0
  while kill -0 $pid 2>/dev/null; do
    if [ $(( $(date +%s) - t )) -ge $cap ]; then
      local cl
      cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
      case "$cl" in
        *$rx*) log "$name cap $cap s reached, killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; CAPPED=1;;
        *) log "$name pid $wpid does not match '$rx' (command line: ${cl:0:80}), nothing killed";;
      esac
      break
    fi
    sleep 15
  done
  wait $pid; RC=$?
  log "$name exit $RC (want $want) wall $(( $(date +%s) - t )) s capped $CAPPED $([ $RC = $want ] && echo OK || echo MISMATCH)"
}
