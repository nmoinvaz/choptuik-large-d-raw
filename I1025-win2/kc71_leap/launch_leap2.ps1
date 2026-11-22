# launches run_leap2.sh DA DB H hidden at BelowNormal; the python processes inherit the class. usage: launch_leap2.ps1 DA DB H
param([string]$DA, [string]$DB, [string]$H)
$p = Start-Process 'C:\Program Files\Git\bin\bash.exe' -ArgumentList '-c',"`"export PATH=/usr/bin:`$PATH; cd /d/choptuik-i935-raw/I1025-win2/kc71_leap && bash run_leap2.sh $DA $DB $H`"" -WindowStyle Hidden -PassThru -RedirectStandardOutput D:\choptuik-i935-raw\I1025-win2\kc71_leap\run_leap2.stdout -RedirectStandardError D:\choptuik-i935-raw\I1025-win2\kc71_leap\run_leap2.stderr
$p.PriorityClass = 'BelowNormal'
"launcher pid $($p.Id) priority $($p.PriorityClass)"
