@echo off
start "" /wait /belownormal /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc71_leap/hl_test && while true; do date -u +%%T >> hb_B.txt; sleep 2; done" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\hl_test\B.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\hl_test\B.stderr
