# started by run_leap9.sh after the seeds are accepted (outside the terminal, headless, BelowNormal, through cim_start.ps1): the guard leap_guard.py (--seeds: the previous points are the two seeds' own records, which carry
# n_null and cos_t_reg) and the alert-only samplers in leg9/ (ended by leg9_marker.sh at all9.done).
$k = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$R = 'D:/choptuik-i935-raw/I1025-win2/kc71_leap'
$PY = 'C:/Users/nathan/Source/venv-md510/Scripts/python.exe'
$DATA = 'D:/choptuik-i1025k71/solver/matter/data'
& "$k\cim_start.ps1" -Name leg9_guard -Bash "$PY -u leap_guard.py --rec $DATA/l1kc71Lw1025h.jsonl --seeds $R/leg9_seedA.jsonl $R/leg9_seedB.jsonl --exits $R/exits_kcl9.txt --rootkey 'leap9 root pid' --log $R/leap9.log --out $R/leg9_points.txt --stop $R/leg9_STOP.txt --done $R/all9.done"
& "$k\cim_start.ps1" -Name leg9_mem_watch -Bash "powershell -NoProfile -File $R/mem_watch.ps1 -Out $R/leg9"
& "$k\cim_start.ps1" -Name leg9_commit_watch -Bash "powershell -NoProfile -File $R/commit_watch.ps1 -Out $R/leg9"
& "$k\cim_start.ps1" -Name leg9_marker -Bash 'bash leg9_marker.sh'
