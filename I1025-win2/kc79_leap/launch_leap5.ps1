# launches the k_c 79 leap (step 2 of kc79_leap) OUTSIDE the calling terminal (cim_start.ps1, the headless form; BelowNormal): the driver run_leap5.sh (waits for both regrids' acceptance, then starts the leap),
# the guard leap_guard.py (--seeds: the previous points are the two seed records; waits for the leap's root pid), and the alert-only samplers (mem_watch.ps1, commit_watch.ps1, ended by leap5_marker.sh at all5.done).
$k = 'D:\choptuik-i935-raw\I1025-win2\kc71_leap'
$o = 'D:\choptuik-i935-raw\I1025-win2\kc79_leap'
$R = 'D:/choptuik-i935-raw/I1025-win2/kc79_leap'
$K = 'D:/choptuik-i935-raw/I1025-win2/kc71_leap'
$PY = 'C:/Users/nathan/Source/venv-md510/Scripts/python.exe'
$DATA = 'D:/choptuik-i1025k79/solver/matter/data'
& "$k\cim_start.ps1" -Name run_leap5 -Bash 'bash run_leap5.sh' -Dir /d/choptuik-i935-raw/I1025-win2/kc79_leap
& "$k\cim_start.ps1" -Name leap5_guard -Bash "$PY -u $K/leap_guard.py --rec $DATA/l1kc79Lw1025d.jsonl --seeds $R/rec_k79_D20.5000.jsonl $R/rec_k79_D20.7500.jsonl --exits $R/exits_leap5.txt --rootkey 'leap5 root pid' --log $R/leap5.log --out $R/leap5_points.txt --stop $R/leap5_STOP.txt --done $R/all5.done" -Dir /d/choptuik-i935-raw/I1025-win2/kc79_leap
& "$k\cim_start.ps1" -Name leap5_mem_watch -Bash "powershell -NoProfile -File $K/mem_watch.ps1 -Out $R/leap5" -Dir /d/choptuik-i935-raw/I1025-win2/kc79_leap
& "$k\cim_start.ps1" -Name leap5_commit_watch -Bash "powershell -NoProfile -File $K/commit_watch.ps1 -Out $R/leap5" -Dir /d/choptuik-i935-raw/I1025-win2/kc79_leap
& "$k\cim_start.ps1" -Name leap5_marker -Bash 'bash leap5_marker.sh' -Dir /d/choptuik-i935-raw/I1025-win2/kc79_leap
