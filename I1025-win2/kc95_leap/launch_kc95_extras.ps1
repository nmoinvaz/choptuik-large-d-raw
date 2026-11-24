# started by run_kc95.sh after the tag g leap's end and the repeated seed checks (outside the terminal, headless, BelowNormal, through cim_start.ps1): the guard leap_guard.py (--seeds: the previous points are the two seed records, winb's D 21.0
# and dh170's D 21.125; they carry no n_null or cos_t_reg, so the n_null rule starts at the second point) and the alert-only samplers in leapk95/ (ended by kc95_marker.sh at allk95.done).
$k = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$R = 'D:/choptuik-i935-raw/I1025-win2/kc95_leap'
$K = 'D:/choptuik-i935-raw/I1025-win2/kc71_leap'
$PY = 'C:/Users/nathan/Source/venv-md510/Scripts/python.exe'
$DATA = 'D:/choptuik-i1025k79/solver/matter/data'
$d = '/d/choptuik-i935-raw/I1025-win2/kc95_leap'
& "$k\cim_start.ps1" -Name leapk95_guard -Bash "$PY -u $K/leap_guard.py --rec $DATA/l1kc95Lw1025k.jsonl --seeds $R/leapk95_seedA.jsonl $R/leapk95_seedB.jsonl --exits $R/exits_leapk95.txt --rootkey 'leapk95 root pid' --log $R/leapk95.log --out $R/leapk95_points.txt --stop $R/leapk95_STOP.txt --done $R/allk95.done" -Dir $d
& "$k\cim_start.ps1" -Name leapk95_mem_watch -Bash "powershell -NoProfile -File $K/mem_watch.ps1 -Out $R/leapk95" -Dir $d
& "$k\cim_start.ps1" -Name leapk95_commit_watch -Bash "powershell -NoProfile -File $K/commit_watch.ps1 -Out $R/leapk95" -Dir $d
& "$k\cim_start.ps1" -Name leapk95_marker -Bash 'bash kc95_marker.sh' -Dir $d
