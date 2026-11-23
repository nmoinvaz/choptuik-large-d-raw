# started by run_leap7.sh after the seeds are accepted (outside the terminal, headless, BelowNormal, through cim_start.ps1): the guard leap_guard.py (--seeds: the previous points are the old leap's two seed records, which carry
# n_null and cos_t_reg) and the alert-only samplers in leap7/ (ended by leap7_marker.sh at all7.done).
$k = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$R = 'D:/choptuik-i935-raw/I1025-win2/kc79_leap'
$K = 'D:/choptuik-i935-raw/I1025-win2/kc71_leap'
$PY = 'C:/Users/nathan/Source/venv-md510/Scripts/python.exe'
$DATA = 'D:/choptuik-i1025k79/solver/matter/data'
$d = '/d/choptuik-i935-raw/I1025-win2/kc79_leap'
& "$k\cim_start.ps1" -Name leap7_guard -Bash "$PY -u $K/leap_guard.py --rec $DATA/l1kc79Lw1025f.jsonl --seeds $R/leap7_seedA.jsonl $R/leap7_seedB.jsonl --exits $R/exits_leap7.txt --rootkey 'leap7 root pid' --log $R/leap7.log --out $R/leap7_points.txt --stop $R/leap7_STOP.txt --done $R/all7.done" -Dir $d
& "$k\cim_start.ps1" -Name leap7_mem_watch -Bash "powershell -NoProfile -File $K/mem_watch.ps1 -Out $R/leap7" -Dir $d
& "$k\cim_start.ps1" -Name leap7_commit_watch -Bash "powershell -NoProfile -File $K/commit_watch.ps1 -Out $R/leap7" -Dir $d
& "$k\cim_start.ps1" -Name leap7_marker -Bash 'bash leap7_marker.sh' -Dir $d
