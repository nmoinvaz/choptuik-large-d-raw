@echo off
start "" /wait /belownormal /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc71_leap && bash run_leap4.sh 20.6875 20.75 0.03125" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\run_leap4.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\run_leap4.stderr
