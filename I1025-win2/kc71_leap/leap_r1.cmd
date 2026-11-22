@echo off
start "" /wait /belownormal /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc71_leap && bash leap_r1.sh" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\leap_r1.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\leap_r1.stderr
