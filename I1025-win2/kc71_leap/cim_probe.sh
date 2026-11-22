#!/bin/bash
# probe of the environment of a Win32_Process.Create tree: tools the scripts need, the priority and the parent chain, to cim_probe.out
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
{
  echo "bash pid $$ winpid $(cat /proc/$$/winpid)"; date -u '+%F %T UTC'; echo "HOME=$HOME USER=$USERNAME"
  for t in git gh python tasklist taskkill powershell date cmp sed grep sleep tail mapfile; do printf '%s: ' $t; command -v $t || echo MISSING; done
  git -C /d/choptuik-i1025k71 rev-parse --short HEAD
  powershell -NoProfile -Command "(Get-Process -Id $(cat /proc/$$/winpid)).PriorityClass; (Get-Process -Id $PPID -ErrorAction SilentlyContinue).Id" 
  C:/Users/nathan/Source/venv-md510/Scripts/python.exe -c "import numpy, scipy; print('python ok', numpy.__version__)"
  powershell -NoProfile -File D:/choptuik-i935-raw/I1025-win2/kc71_leap/chain.ps1 $(cat /proc/$$/winpid)
} > /d/choptuik-i935-raw/I1025-win2/kc71_leap/cim_probe.out 2>&1
