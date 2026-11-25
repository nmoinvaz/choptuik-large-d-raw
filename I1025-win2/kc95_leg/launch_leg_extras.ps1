# started by run_kc95leg.sh with the leap (outside the terminal, headless, BelowNormal, through cim_start.ps1): the guard leap_guard.py (--seeds: the previous points are the two seed records, my k_c 95 D 22.875 and D 23.0; they carry no n_null or cos_t_reg,
# so the n_null rule starts at the second point) and the alert-only samplers in leg/ (ended by leg_marker.sh at allleg.done).
$k = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$R = 'D:/choptuik-i935-raw/I1025-win2/kc95_leg'
$K = 'D:/choptuik-i935-raw/I1025-win2/kc71_leap'
$PY = 'C:/Users/nathan/Source/venv-md510/Scripts/python.exe'
$DATA = 'D:/choptuik-i1025k95leg/solver/matter/data'
$d = '/d/choptuik-i935-raw/I1025-win2/kc95_leg'
& "$k\cim_start.ps1" -Name leg95_guard -Bash "$PY -u $K/leap_guard.py --rec $DATA/l1kc95Lw1025m.jsonl --seeds $R/leg_seedA.jsonl $R/leg_seedB.jsonl --exits $R/exits_leg.txt --rootkey 'leg95 root pid' --log $R/leg.log --out $R/leg_points.txt --stop $R/leg_STOP.txt --done $R/leg.finished" -Dir $d
& "$k\cim_start.ps1" -Name leg95_mem_watch -Bash "powershell -NoProfile -File $K/mem_watch.ps1 -Out $R/leg" -Dir $d
& "$k\cim_start.ps1" -Name leg95_commit_watch -Bash "powershell -NoProfile -File $K/commit_watch.ps1 -Out $R/leg" -Dir $d
& "$k\cim_start.ps1" -Name leg95_marker -Bash 'bash leg_marker.sh' -Dir $d
