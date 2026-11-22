@echo off
start "" /wait /belownormal /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc79_d20 && bash regrid79_d20.sh" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\kc79_regrid.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\kc79_regrid.stderr
