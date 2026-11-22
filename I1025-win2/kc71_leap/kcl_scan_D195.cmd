@echo off
start "" /wait /belownormal /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc71_leap && bash kcl_scan.sh 19.5 1.20 1.60 1.397099 /d/choptuik-i935-raw/I1025-win2/kc71_leap/scan_D19.done" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\kcl_scan_D195.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\kcl_scan_D195.stderr
