# started by run_leap11.sh after the seeds are accepted (outside the terminal, headless, BelowNormal, through cim_start.ps1): the guard leap_guard.py (--seeds: the previous points are the two seeds' own records, which carry
# n_null and cos_t_reg) and the alert-only samplers in leap11/ (ended by leap11_marker.sh at all11.done).
$k = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$R = 'D:/choptuik-i935-raw/I1025-win2/kc79_leap'
$K = 'D:/choptuik-i935-raw/I1025-win2/kc71_leap'
$PY = 'C:/Users/nathan/Source/venv-md510/Scripts/python.exe'
$DATA = 'D:/choptuik-i1025k79/solver/matter/data'
$d = '/d/choptuik-i935-raw/I1025-win2/kc79_leap'
& "$k\cim_start.ps1" -Name leap11_guard -Bash "$PY -u $K/leap_guard.py --rec $DATA/l1kc79Lw1025j.jsonl --seeds $R/leap11_seedA.jsonl $R/leap11_seedB.jsonl --exits $R/exits_leap11.txt --rootkey 'leap11 root pid' --log $R/leap11.log --out $R/leap11_points.txt --stop $R/leap11_STOP.txt --done $R/all11.done" -Dir $d
& "$k\cim_start.ps1" -Name leap11_mem_watch -Bash "powershell -NoProfile -File $K/mem_watch.ps1 -Out $R/leap11" -Dir $d
& "$k\cim_start.ps1" -Name leap11_commit_watch -Bash "powershell -NoProfile -File $K/commit_watch.ps1 -Out $R/leap11" -Dir $d
& "$k\cim_start.ps1" -Name leap11_marker -Bash 'bash leap11_marker.sh' -Dir $d
