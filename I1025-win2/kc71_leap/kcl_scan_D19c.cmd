@echo off
start "" /wait /belownormal /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc71_leap && bash kcl_scan.sh 19 1.40 1.80 1.545995" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\kcl_scan_D19c.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\kcl_scan_D19c.stderr
