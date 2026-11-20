#!/bin/bash
# #1025 preparation (coordinator's hc 2026-11-20): new venv-md510, requirements.txt, then multidouble 5.1.0 (8c4360ac) from git with MSVC's link.exe first on PATH. BelowNormal (set by the launching PowerShell).
OUT=/d/choptuik-i935-raw/I1025-win2d
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
EX=$OUT/exits_prep.txt
log() { echo "1025d $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $EX; }
V=/c/Users/nathan/Source/venv-md510
[ -e $V ] && { log "not started: $V exists"; exit 9; }
BASE="/c/Users/nathan/AppData/Local/Programs/Python/Python314/python.exe"
log "start, base python $($BASE --version 2>&1)"
t=$(date +%s)
"$BASE" -m venv $V >> $OUT/venv.log 2>&1 || { log "venv failed"; exit 1; }
log "venv made"
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-md510
export PATH="$V/Scripts:$PATH"
"$V/Scripts/python.exe" -m pip install --no-cache-dir -r $OUT/requirements.txt >> $OUT/pip_requirements.log 2>&1; rc=$?
log "pip install -r requirements.txt exit $rc wall $(( $(date +%s) - t )) s"
[ $rc = 0 ] || exit $rc
MSVC="/c/Program Files/Microsoft Visual Studio/18/Community/VC/Tools/MSVC/14.51.36231/bin/Hostx64/x64"
[ -f "$MSVC/link.exe" ] || { log "MSVC link.exe not found"; exit 1; }
export PATH="$MSVC:$PATH"
log "link.exe first on PATH: $(which link.exe 2>&1)"
t2=$(date +%s)
echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" > $OUT/build.times
"$V/Scripts/python.exe" -m pip install --no-cache-dir "multidouble @ git+https://github.com/nmoinvaz/multidouble@8c4360ac0be804d081faeea524e5c1c6e2fffaaa#subdirectory=python" > $OUT/pip_multidouble.log 2>&1 &
pid=$!
wpid=$(cat /proc/$pid/winpid)
log "pip multidouble root pid $wpid, cap 5400 s"
cap=0
while kill -0 $pid 2>/dev/null; do
  if [ $(( $(date +%s) - t2 )) -ge 5400 ]; then
    cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
    case "$cl" in *pip*) log "cap 5400 s reached, killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; cap=1;; *) log "pid $wpid is not the pip command (${cl:0:80}), nothing killed";; esac
    break
  fi
  sleep 10
done
wait $pid; rc=$?
echo "end $(date -u '+%Y-%m-%d %H:%M:%S UTC') exit $rc capped $cap wall $(( $(date +%s) - t2 )) s" >> $OUT/build.times
log "pip install multidouble exit $rc wall $(( $(date +%s) - t2 )) s capped $cap"
{
  echo "## multidouble direct_url"; cat "$V"/Lib/site-packages/multidouble-*.dist-info/direct_url.json; echo
  echo "## python"; "$V/Scripts/python.exe" --version
  echo "## import"; "$V/Scripts/python.exe" -c "import multidouble as m; print(m.__file__); print(getattr(m,'__version__','(no __version__)')); print('isa', m.isa() if hasattr(m,'isa') else '?'); print('dd_logdet', hasattr(m,'dd_logdet'), 'qd_logdet', hasattr(m,'qd_logdet'))"
  echo "## pip list"; "$V/Scripts/python.exe" -m pip list 2>/dev/null
  echo "## tools"; rustc --version; cargo --version; "$V/Scripts/maturin.exe" --version
} > $OUT/versions.txt 2>&1
touch $OUT/prep.done
exit $rc
