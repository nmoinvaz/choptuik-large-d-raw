@echo off
start "" /wait /belownormal /b "C:\Program Files\Git\bin\bash.exe" -c "export PATH=/usr/bin:$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc71_leap && GROOT=42624 bash leg1_guard2.sh" 1>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\leg1_guard2.stdout 2>> D:\choptuik-i935-raw\I1025-win2\kc71_leap\leg1_guard2.stderr
