@echo off
start "" /wait  /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc79_leap && bash regrid79x.sh 20.5 l1kc79win2d205 63399965 2.1088217835" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\k79r205.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\k79r205.stderr
