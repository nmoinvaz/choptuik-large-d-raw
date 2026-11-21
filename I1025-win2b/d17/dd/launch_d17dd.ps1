# launches d17_dd.sh hidden at BelowNormal; children inherit the class
$p = Start-Process 'C:\Program Files\Git\bin\bash.exe' -ArgumentList '-c','"export PATH=/usr/bin:$PATH; cd /d/choptuik-large-d-raw/I1025-win2b/d17/dd && bash d17_dd.sh"' -WindowStyle Hidden -PassThru -RedirectStandardOutput D:\choptuik-large-d-raw\I1025-win2b\d17\dd\launcher.out -RedirectStandardError D:\choptuik-large-d-raw\I1025-win2b\d17\dd\launcher.err
$p.PriorityClass = 'BelowNormal'
"launcher pid $($p.Id) priority $($p.PriorityClass)"
