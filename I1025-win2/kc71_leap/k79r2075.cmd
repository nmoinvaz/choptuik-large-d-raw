@echo off
start "" /wait  /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc79_leap && bash regrid79x.sh 20.75 l1kc79win2d2075 fe8503cc 2.1077704855" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\k79r2075.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\k79r2075.stderr
