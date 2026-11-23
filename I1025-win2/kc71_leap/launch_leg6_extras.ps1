# started by run_leap6.sh after the seeds are accepted (outside the terminal, headless, BelowNormal, through cim_start.ps1): the guard leap_guard.py (--seeds: the previous points are leg 4's last two records, which carry n_null and
# cos_t_reg) and the alert-only samplers of leg 4's kind in leg6/ (ended by leg6_marker.sh at all6.done).
$k = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$R = 'D:/choptuik-i935-raw/I1025-win2/kc71_leap'
$PY = 'C:/Users/nathan/Source/venv-md510/Scripts/python.exe'
$DATA = 'D:/choptuik-i1025k71/solver/matter/data'
& "$k\cim_start.ps1" -Name leg6_guard -Bash "$PY -u leap_guard.py --rec $DATA/l1kc71Lw1025e.jsonl --seeds $R/leg6_seedA.jsonl $R/leg6_seedB.jsonl --exits $R/exits_kcl6.txt --rootkey 'leap6 root pid' --log $R/leap6.log --out $R/leg6_points.txt --stop $R/leg6_STOP.txt --done $R/all6.done"
& "$k\cim_start.ps1" -Name leg6_mem_watch -Bash "powershell -NoProfile -File $R/mem_watch.ps1 -Out $R/leg6"
& "$k\cim_start.ps1" -Name leg6_commit_watch -Bash "powershell -NoProfile -File $R/commit_watch.ps1 -Out $R/leg6"
& "$k\cim_start.ps1" -Name leg6_marker -Bash 'bash leg6_marker.sh'
