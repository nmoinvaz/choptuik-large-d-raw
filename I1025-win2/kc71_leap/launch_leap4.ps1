# launches leg 4 OUTSIDE the calling terminal (cim_start.ps1, the headless form: conhost.exe --headless cmd.exe /c; BelowNormal): the driver run_leap4.sh, the guard leg4_guard.py (the stop rule and the point table),
# and the alert-only samplers of leg 3's kind (mem_watch.ps1, commit_watch.ps1, ended by leg4_marker.sh at all4.done). usage: launch_leap4.ps1 DA DB H
param([string]$DA, [string]$DB, [string]$H)
$S = "$PSScriptRoot\cim_start.ps1"
$R = 'D:/choptuik-i935-raw/I1025-win2/kc71_leap'
$PY = 'C:/Users/nathan/Source/venv-md510/Scripts/python.exe'
& $S -Name run_leap4 -Bash "bash run_leap4.sh $DA $DB $H"
& $S -Name leg4_guard -Bash "$PY -u leg4_guard.py --rec D:/choptuik-i1025k71/solver/matter/data/l1kc71Lw1025c.jsonl --n0 12 --exits $R/exits_kcl4.txt --log $R/leap4.log --out $R/leg4_points.txt --stop $R/leg4_STOP.txt --done $R/all4.done"
& $S -Name leg4_mem_watch -Bash "powershell -NoProfile -File $R/mem_watch.ps1 -Out $R/leg4"
& $S -Name leg4_commit_watch -Bash "powershell -NoProfile -File $R/commit_watch.ps1 -Out $R/leg4"
& $S -Name leg4_marker -Bash "bash leg4_marker.sh"
