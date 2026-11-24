# started by run_leap10.sh after the seeds are accepted (outside the terminal, headless, BelowNormal, through cim_start.ps1): the guard leap_guard.py (--seeds: the previous points are the two seed records of tag g, which carry
# n_null and cos_t_reg) and the alert-only samplers in leap10/ (ended by leap10_marker.sh at all10.done).
$k = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$R = 'D:/choptuik-i935-raw/I1025-win2/kc79_leap'
$K = 'D:/choptuik-i935-raw/I1025-win2/kc71_leap'
$PY = 'C:/Users/nathan/Source/venv-md510/Scripts/python.exe'
$DATA = 'D:/choptuik-i1025k79/solver/matter/data'
$d = '/d/choptuik-i935-raw/I1025-win2/kc79_leap'
& "$k\cim_start.ps1" -Name leap10_guard -Bash "$PY -u $K/leap_guard.py --rec $DATA/l1kc79Lw1025i.jsonl --seeds $R/leap10_seedA.jsonl $R/leap10_seedB.jsonl --exits $R/exits_leap10.txt --rootkey 'leap10 root pid' --log $R/leap10.log --out $R/leap10_points.txt --stop $R/leap10_STOP.txt --done $R/all10.done" -Dir $d
& "$k\cim_start.ps1" -Name leap10_mem_watch -Bash "powershell -NoProfile -File $K/mem_watch.ps1 -Out $R/leap10" -Dir $d
& "$k\cim_start.ps1" -Name leap10_commit_watch -Bash "powershell -NoProfile -File $K/commit_watch.ps1 -Out $R/leap10" -Dir $d
& "$k\cim_start.ps1" -Name leap10_marker -Bash 'bash leap10_marker.sh' -Dir $d
