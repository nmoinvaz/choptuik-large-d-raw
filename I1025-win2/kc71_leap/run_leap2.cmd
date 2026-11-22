@echo off
start "" /wait /belownormal /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc71_leap && bash run_leap2.sh 19.25 19.3125 0.0625" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\run_leap2.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\run_leap2.stderr
