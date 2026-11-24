# started by run_leap8.sh after the seeds are accepted (outside the terminal, headless, BelowNormal, through cim_start.ps1): the guard leap_guard.py (--seeds: the previous points are the two seeds' own records, which carry
# n_null and cos_t_reg) and the alert-only samplers in leap8/ (ended by leap8_marker.sh at all8.done).
$k = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$R = 'D:/choptuik-i935-raw/I1025-win2/kc79_leap'
$K = 'D:/choptuik-i935-raw/I1025-win2/kc71_leap'
$PY = 'C:/Users/nathan/Source/venv-md510/Scripts/python.exe'
$DATA = 'D:/choptuik-i1025k79/solver/matter/data'
$d = '/d/choptuik-i935-raw/I1025-win2/kc79_leap'
& "$k\cim_start.ps1" -Name leap8_guard -Bash "$PY -u $K/leap_guard.py --rec $DATA/l1kc79Lw1025g.jsonl --seeds $R/leap8_seedA.jsonl $R/leap8_seedB.jsonl --exits $R/exits_leap8.txt --rootkey 'leap8 root pid' --log $R/leap8.log --out $R/leap8_points.txt --stop $R/leap8_STOP.txt --done $R/all8.done" -Dir $d
& "$k\cim_start.ps1" -Name leap8_mem_watch -Bash "powershell -NoProfile -File $K/mem_watch.ps1 -Out $R/leap8" -Dir $d
& "$k\cim_start.ps1" -Name leap8_commit_watch -Bash "powershell -NoProfile -File $K/commit_watch.ps1 -Out $R/leap8" -Dir $d
& "$k\cim_start.ps1" -Name leap8_marker -Bash 'bash leap8_marker.sh' -Dir $d
