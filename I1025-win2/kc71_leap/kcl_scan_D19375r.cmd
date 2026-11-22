@echo off
start "" /wait /belownormal /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc71_leap && TAGL=l1kc71Lw1025b LEAPFIN=leap2.finished bash kcl_scan2.sh 19.375 1.30 1.60 1.40" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\kcl_scan_D19375r.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\kcl_scan_D19375r.stderr
